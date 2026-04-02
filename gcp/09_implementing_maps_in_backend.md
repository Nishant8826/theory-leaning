# Implementing Google Maps in the Backend (Node.js)

---

### 2. What
While maps are visually rendered on the Frontend (React), the heavy mathematical calculations (like calculating the distance between 50 delivery drivers and a restaurant) must be done on the **Backend (Node.js)**. We use the `@googlemaps/google-maps-services-js` package to securely query Google Maps from our server.

---

### 3. Why
If you calculate shipping costs based on distance on the Frontend, a hacker can easily manipulate the Javascript to trick your app into thinking the delivery is 0 miles away, avoiding the $15 delivery fee. **Rule of thumb: Never trust the client.** Always calculate pricing and distances securely on your Node.js backend.

---

### 4. How
1. Install the official Node.js SDK for Google Maps.
2. Initialize the client securely using your API Key stored in an Environment Variable (`.env`).
3. Call specific APIs (like Geocoding or Distance Matrix) using `async/await`.

---

### 5. Implementation

**Backend Example: Calculating Distance for Delivery Fees**

```javascript
// 1. Install via: npm install @googlemaps/google-maps-services-js
const { Client } = require("@googlemaps/google-maps-services-js");

// Initialize the Google Maps Node Client
const client = new Client({});

async function calculateDeliveryFee(restaurantAddress, userAddress) {
  try {
    const response = await client.distancematrix({
      params: {
        origins: [restaurantAddress],
        destinations: [userAddress],
        key: process.env.GOOGLE_MAPS_SERVER_API_KEY, // MUST SECURE THIS IN .ENV
      },
    });

    // The API returns complex nested JSON. We extract the distance in meters.
    const distanceInMeters = response.data.rows[0].elements[0].distance.value;
    const distanceInMiles = distanceInMeters * 0.000621371;

    // Calculate cost: $5 base fee + $1.50 per mile
    const fee = 5 + (distanceInMiles * 1.5);
    
    return `$${fee.toFixed(2)}`;
  } catch (error) {
    console.error("Error calculating distance:", error.message);
  }
}

// simulate: calculateDeliveryFee("Times Square, NY", "Brooklyn Bridge, NY")
```

---

### 6. Steps
1. Navigate to GCP Console $\rightarrow$ APIs & Services $\rightarrow$ Credentials.
2. Generate a **brand new API Key**. Do not reuse your React API Key!
3. Add **API Restrictions**: Restrict this key to ONLY the "Distance Matrix API" to prevent abuse.
4. Add **Application Restrictions**: Restrict this key strictly by IP Address (the exact static IP of your Cloud Run server).
5. Load the key into your Node.js `.env` file successfully.

---

### 7. Integration

🧠 **Think Like This:**
* **Full-Stack App Workflow:**
  1. User selects their location in the browser (React/Next.js) using the Places Autocomplete UI.
  2. React sends the selected String ("123 Apple St") to your Node.js API via POST request.
  3. Node.js calls the Maps Backend SDK to verify the address and calculate the exact distance to the store.
  4. Node.js saves the distance to Cloud SQL and returns the finalized secure price to React.

---

### 8. Impact
📌 **Real-World Scenario:** UberEats relies entirely on backend Maps processing. Before you even see the restaurant menu, their backend uses the Distance Matrix API to calculate the exact drive time from the restaurant to your specific GPS coordinates, dynamically adjusting the "Delivery Fee" display securely.

---

### 9. Interview Questions
1. **Why should you use two separate Google Maps API Keys for a Full-Stack application?**
   *Answer: Because client-side keys are publicly visible in the browser and must be restricted by Website URLs (HTTP Referrers). Backend keys are kept completely secret and should be rigorously restricted by Server IP addresses. Mixing them voids your security.*
2. **If a user modifies the distance payload on the frontend to cheat a delivery fee, how does the backend pattern prevent this?**
   *Answer: The backend never blindly accepts distance values submitted by the client. It only accepts the physical address/coordinates and recalculates the definitive distance internally using the server-side Maps SDK.*
3. **What is the `google-maps-services-js` package used for?**
   *Answer: It is the official Node.js client library that provides strongly-typed, promise-based wrappers for making HTTP requests to Google Maps web services like Geocoding and Directions.*

---

### 10. Summary
* Backend calculation ensures zero client-side manipulation.
* Use the official `@googlemaps/google-maps-services-js` library on Node.
* Secure server API keys exclusively via IP Address restrictions.
* Perfect for calculating secure pricing, delivery routes, and batch geo-locating.

---
Prev : [08_implementing_maps_in_react.md](./08_implementing_maps_in_react.md) | Next : [10_gcp_console_and_cli.md](./10_gcp_console_and_cli.md)
