# 🏗️ Case Study: Uber (Ride Sharing Platform)

## 📋 Requirements

**Functional:**
- Riders can request rides with pickup and dropoff location
- System matches rider with nearest available driver
- Driver can accept/reject ride
- Real-time location tracking during ride
- Fare calculation (surge pricing)
- Payment processing
- Ratings after ride

**Non-Functional:**
- 100M rides per day globally
- Driver location updates every 3-5 seconds (highest volume!)
- Match rider to driver in < 5 seconds
- Location data must be real-time (< 1 second staleness)
- 99.99% availability

---

## 📊 Capacity Estimation

```
Active drivers: 5M at any time
Location updates: 5M drivers × 1 update/5sec = 1M location writes/sec!
Active riders: 10M looking for rides

Location queries: A rider sees nearby drivers → geospatial query
  5M location updates/sec × 100 bytes = 500MB/sec writes!

Rides: 100M/day = ~1,157 rides/sec

Critical insight:
→ Location Service is the HARDEST part (1M writes/sec)
→ Everything else is relatively standard
```

---

## 🏗️ High Level Architecture

```
[Rider App] ←→ [Driver App]
     ↓               ↓
[AWS API Gateway + Load Balancer]
     ↓
┌─────────────────────────────────────────────────────────────┐
│                     MICROSERVICES                            │
│                                                             │
│  [Location Service]  ← CORE: handles 1M loc updates/sec    │
│  [Matching Service]  ← Finds nearest driver for rider       │
│  [Ride Service]      ← Manages ride lifecycle               │
│  [Auth Service]      ← JWT + Driver/Rider accounts          │
│  [Payment Service]   ← Stripe integration + surge pricing   │
│  [Notification Svc]  ← Push notifications + WebSocket       │
│  [Rating Service]    ← Post-ride ratings                    │
└─────────────────────────────────────────────────────────────┘
     ↓
[Redis Geospatial]  ← Driver locations (most critical!)
[PostgreSQL]        ← Rides, users, payments
[MongoDB]           ← Ride history, analytics
[Kafka]             ← Location event stream
[S3]                ← Analytics data warehouse
```

---

## 📍 Location Service (Most Critical)

```javascript
// Driver App → sends location every 3-5 seconds
// Location Service must handle 1M writes/sec!

const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

// Location Service
class LocationService {
  // Driver updates location (called every 3-5 seconds from driver app)
  async updateDriverLocation(driverId, latitude, longitude, heading, speed) {
    const key = 'active_drivers';
    
    // Redis GEOADD — O(log N) operation, extremely fast!
    await redis.geoadd(key, longitude, latitude, driverId);
    
    // Also store additional metadata (heading, speed, availability)
    await redis.hset(`driver:${driverId}:meta`, {
      lat: latitude,
      lng: longitude,
      heading,
      speed,
      updatedAt: Date.now(),
      isAvailable: 1
    });
    
    // Set TTL — remove driver from map if offline
    await redis.expire(`driver:${driverId}:meta`, 30); // 30 seconds timeout
    
    // Publish to Kafka for analytics and downstream services
    await kafkaProducer.send({
      topic: 'driver-locations',
      messages: [{
        key: driverId,
        value: JSON.stringify({ driverId, latitude, longitude, heading, speed, timestamp: Date.now() })
      }]
    });
  }
  
  // Find nearby drivers within radius
  async getNearbyDrivers(latitude, longitude, radiusKm = 5, limit = 20) {
    // GEORADIUS — spatial search in O(N+log M) where N = matches
    const nearbyDrivers = await redis.georadius(
      'active_drivers',
      longitude, latitude,
      radiusKm, 'km',
      'WITHCOORD',      // Include coordinates
      'WITHDIST',       // Include distance
      'COUNT', limit,   // Max results
      'ASC'             // Nearest first
    );
    
    if (!nearbyDrivers || nearbyDrivers.length === 0) return [];
    
    // Get availability metadata for each driver
    const driverIds = nearbyDrivers.map(d => d[0]);
    const metaKeys = driverIds.map(id => `driver:${id}:meta`);
    
    const pipeline = redis.pipeline();
    metaKeys.forEach(key => pipeline.hgetall(key));
    const metaResults = await pipeline.exec();
    
    return nearbyDrivers
      .map((driver, i) => {
        const [id, distance, coords] = driver;
        const meta = metaResults[i][1] || {};
        return {
          driverId: id,
          distance: parseFloat(distance),
          coordinates: { lng: parseFloat(coords[0]), lat: parseFloat(coords[1]) },
          heading: parseFloat(meta.heading),
          speed: parseFloat(meta.speed),
          isAvailable: meta.isAvailable === '1',
          lastUpdate: parseInt(meta.updatedAt)
        };
      })
      .filter(d => d.isAvailable); // Only available drivers
  }
  
  // Get specific driver location
  async getDriverLocation(driverId) {
    const pos = await redis.geopos('active_drivers', driverId);
    if (!pos || !pos[0]) return null;
    
    const meta = await redis.hgetall(`driver:${driverId}:meta`);
    
    return {
      driverId,
      latitude: parseFloat(pos[0][1]),
      longitude: parseFloat(pos[0][0]),
      ...meta
    };
  }
}

// API Endpoints
const locationService = new LocationService();

// Driver sends location update
app.post('/api/driver/location', authenticate, async (req, res) => {
  const { latitude, longitude, heading = 0, speed = 0 } = req.body;
  
  await locationService.updateDriverLocation(
    req.user.id, latitude, longitude, heading, speed
  );
  
  res.status(204).send();
});

// Get nearby drivers (for rider UI — shows cars on map)
app.get('/api/nearby-drivers', authenticate, async (req, res) => {
  const { latitude, longitude, radius = 5 } = req.query;
  
  const drivers = await locationService.getNearbyDrivers(
    parseFloat(latitude), parseFloat(longitude), parseFloat(radius)
  );
  
  res.json({ drivers });
});
```

---

## 🤝 Ride Matching Service

```javascript
class RideMatchingService {
  constructor(locationService, rideService, notificationService) {
    this.locationService = locationService;
    this.rideService = rideService;
    this.notificationService = notificationService;
  }
  
  async matchRider(rideRequestId) {
    const rideRequest = await this.rideService.getRideRequest(rideRequestId);
    const { pickup, riderId, rideType } = rideRequest;
    
    // Find nearby available drivers
    let nearbyDrivers = await this.locationService.getNearbyDrivers(
      pickup.latitude, pickup.longitude, 
      radius = 5  // 5km search radius
    );
    
    // Filter by ride type (UberX, UberXL, Black, etc.)
    nearbyDrivers = nearbyDrivers.filter(d => d.vehicleType === rideType);
    
    if (nearbyDrivers.length === 0) {
      // Expand search radius
      nearbyDrivers = await this.locationService.getNearbyDrivers(pickup.latitude, pickup.longitude, radius = 10);
      if (nearbyDrivers.length === 0) {
        await this.rideService.updateStatus(rideRequestId, 'no_drivers_available');
        return null;
      }
    }
    
    // Rank drivers by ETA (not just distance)
    const rankedDrivers = await this.rankByETA(nearbyDrivers, pickup);
    
    // Try drivers in order
    for (const driver of rankedDrivers.slice(0, 5)) { // Try top 5
      const accepted = await this.offerRideToDriver(driver.driverId, rideRequestId);
      if (accepted) {
        await this.rideService.assignDriver(rideRequestId, driver.driverId);
        return driver;
      }
    }
    
    await this.rideService.updateStatus(rideRequestId, 'no_drivers_accepted');
    return null;
  }
  
  async offerRideToDriver(driverId, rideRequestId) {
    // Send push notification to driver
    await this.notificationService.sendRideRequest(driverId, rideRequestId);
    
    // Wait for driver response (15 seconds timeout)
    const responseKey = `ride_offer:${driverId}:${rideRequestId}`;
    
    for (let i = 0; i < 15; i++) {
      await new Promise(r => setTimeout(r, 1000));
      const response = await redis.get(responseKey);
      
      if (response === 'accepted') {
        await redis.del(responseKey);
        return true;
      }
      
      if (response === 'rejected') {
        await redis.del(responseKey);
        return false;
      }
    }
    
    // Timeout — treat as rejection
    return false;
  }
  
  async rankByETA(drivers, pickup) {
    // For production: use a routing engine (OSRM, Google Maps API)
    // Simplified: rank by straight-line distance
    return drivers.sort((a, b) => a.distance - b.distance);
  }
}

// Rider requests a ride
app.post('/api/rides/request', authenticate, async (req, res) => {
  const { pickupLat, pickupLng, dropoffLat, dropoffLng, rideType = 'standard' } = req.body;
  
  // Calculate estimated fare
  const distance = calculateDistance(pickupLat, pickupLng, dropoffLat, dropoffLng);
  const surgeMultiplier = await getSurgeMultiplier(pickupLat, pickupLng);
  const fare = calculateFare(distance, rideType, surgeMultiplier);
  
  // Create ride request
  const rideRequest = await db.query(
    'INSERT INTO ride_requests (rider_id, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng, ride_type, estimated_fare, surge_multiplier) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *',
    [req.user.id, pickupLat, pickupLng, dropoffLat, dropoffLng, rideType, fare, surgeMultiplier]
  );
  
  res.status(202).json({
    rideRequestId: rideRequest.rows[0].id,
    estimatedFare: fare,
    surgeMultiplier,
    message: 'Looking for drivers...'
  });
  
  // Start matching process asynchronously
  matchingService.matchRider(rideRequest.rows[0].id).catch(console.error);
});

// Driver accepts/rejects ride
app.post('/api/driver/ride-offer/:rideId/respond', authenticate, async (req, res) => {
  const { accepted } = req.body;
  const { rideId } = req.params;
  const driverId = req.user.id;
  
  const responseKey = `ride_offer:${driverId}:${rideId}`;
  await redis.setex(responseKey, 20, accepted ? 'accepted' : 'rejected');
  
  if (accepted) {
    await redis.hset(`driver:${driverId}:meta`, 'isAvailable', 0); // Mark as busy
  }
  
  res.json({ success: true });
});
```

---

## 💰 Surge Pricing

```javascript
// Dynamic pricing based on supply/demand

async function getSurgeMultiplier(latitude, longitude) {
  // Define city grid cells (e.g., 1km × 1km squares)
  const gridKey = `${Math.floor(latitude * 100) / 100}:${Math.floor(longitude * 100) / 100}`;
  
  // Get supply (available drivers) and demand (pending ride requests) in this cell
  const [availableDrivers, pendingRequests] = await Promise.all([
    locationService.getNearbyDrivers(latitude, longitude, 1), // 1km radius
    redis.get(`pending_requests:${gridKey}`)
  ]);
  
  const supply = availableDrivers.length;
  const demand = parseInt(pendingRequests || 0);
  
  if (supply === 0) return 3.0; // No drivers → maximum surge
  
  const ratio = demand / supply;
  
  if (ratio < 1) return 1.0;      // Normal pricing
  if (ratio < 2) return 1.5;      // 1.5x surge
  if (ratio < 3) return 2.0;      // 2x surge
  if (ratio < 5) return 2.5;      // 2.5x surge
  return 3.0;                     // Maximum 3x surge
}

function calculateFare(distanceKm, rideType, surgeMultiplier = 1.0) {
  const rates = {
    standard: { base: 2.00, perKm: 1.50, perMin: 0.25, minimum: 5.00 },
    xl: { base: 3.00, perKm: 2.25, perMin: 0.38, minimum: 7.00 },
    black: { base: 5.00, perKm: 4.00, perMin: 0.55, minimum: 15.00 }
  };
  
  const rate = rates[rideType] || rates.standard;
  const estimatedMinutes = (distanceKm / 30) * 60; // Assume 30km/h average speed
  
  const fare = rate.base + (distanceKm * rate.perKm) + (estimatedMinutes * rate.perMin);
  const surgedFare = fare * surgeMultiplier;
  
  return Math.max(surgedFare, rate.minimum);
}
```

---

## 🗄️ Database Schema

```sql
-- Drivers
CREATE TABLE drivers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  vehicle_make VARCHAR(50),
  vehicle_model VARCHAR(50),
  vehicle_year INT,
  vehicle_plate VARCHAR(20) UNIQUE,
  vehicle_type VARCHAR(20) DEFAULT 'standard',
  license_number VARCHAR(50),
  rating DECIMAL(3,2) DEFAULT 5.0,
  total_rides INT DEFAULT 0,
  is_active BOOLEAN DEFAULT false,
  is_verified BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Rides (main lifecycle table)
CREATE TABLE rides (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rider_id UUID REFERENCES users(id),
  driver_id UUID REFERENCES drivers(id),
  status VARCHAR(30) NOT NULL DEFAULT 'requested',
  pickup_lat DECIMAL(10, 8),
  pickup_lng DECIMAL(11, 8),
  dropoff_lat DECIMAL(10, 8),
  dropoff_lng DECIMAL(11, 8),
  pickup_address TEXT,
  dropoff_address TEXT,
  distance_km DECIMAL(8,2),
  duration_minutes INT,
  ride_type VARCHAR(20) DEFAULT 'standard',
  estimated_fare DECIMAL(8,2),
  final_fare DECIMAL(8,2),
  surge_multiplier DECIMAL(4,2) DEFAULT 1.0,
  driver_earnings DECIMAL(8,2),
  rating_by_rider DECIMAL(3,2),
  rating_by_driver DECIMAL(3,2),
  requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  accepted_at TIMESTAMP WITH TIME ZONE,
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_rides_rider_id ON rides(rider_id, requested_at DESC);
CREATE INDEX idx_rides_driver_id ON rides(driver_id, requested_at DESC);
CREATE INDEX idx_rides_status ON rides(status) WHERE status NOT IN ('completed', 'cancelled');

-- Location history (keep recent in Redis, archive to DB for analytics)
CREATE TABLE driver_location_history (
  driver_id UUID,
  ride_id UUID REFERENCES rides(id),
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  heading SMALLINT,
  speed SMALLINT,
  recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
) PARTITION BY RANGE (recorded_at);
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **Location Storage — Redis GEOSPATIAL:** 
   - Redis `GEOADD` stores driver locations as sorted sets with geographic encoding
   - `GEORADIUS` queries nearest N drivers in O(N+log M)
   - 5M drivers × 30 bytes/entry = 150MB in Redis → affordable and fast!

2. **1M Location Writes/sec:**
   - Single Redis instance can handle ~100K writes/sec
   - Solution: Shard by geographic region (US West, US East, Europe, Asia)
   - Each region has its own Redis cluster
   - Drivers/riders only need their regional data

3. **Driver Matching Algorithm:**
   - Simple: Nearest driver first
   - Advanced: ETA-based (accounts for traffic), score includes driver rating, acceptance rate
   - Very advanced: LP (Linear Programming) optimization — optimal global matching

4. **Surge Pricing:**
   - Grid-based: Divide city into cells
   - Calculate supply/demand per cell
   - Smooth boundary transitions between cells

5. **WebSocket for Real-time:**
   - Driver and rider connected via WebSocket
   - Location updates streamed to rider during trip
   - Socket.IO with Redis adapter for multi-server support

### Scaling the Location Service

```
Problem: 5M drivers × 1 update/5 sec = 1M writes/sec

Solution 1: Geographic sharding
  US West Redis cluster
  US East Redis cluster
  Europe Redis cluster
  Asia Redis cluster
  Each handles subset of drivers

Solution 2: Write batching
  Buffer driver updates in memory
  Write to Redis every 1 second (not every location event)
  Smooth out write spikes

Solution 3: Kafka as buffer
  Driver → Kafka (very fast, async)
  Kafka → Location Service → Redis (controlled rate)
  Decouples producer (drivers) from consumer (Redis writes)

Problem: Finding nearest driver across region boundaries
  Use 1km overlap between shards
  Driver near boundary appears in multiple shards
```

---

### Navigation
**Prev:** [03_Design_WhatsApp.md](03_Design_WhatsApp.md) | **Index:** [00_Index.md](00_Index.md) | **Next:** [05_Design_Netflix.md](05_Design_Netflix.md)
