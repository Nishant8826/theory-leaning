# Core Google Maps APIs

---

### 2. What
The Google Maps platform is divided into individual purpose-built APIs. You only enable the ones you specifically need.
- **Maps JavaScript API:** Displays the actual interactive visual map UI inside a web browser.
- **Geocoding API:** Converts text into coordinates. (Converts "1600 Amphitheatre Parkway" into Latitude 37.422, Longitude -122.084).
- **Places API:** A search database for locations. (Searches for "Coffee Shops" or predicts user typing during autocomplete).
- **Directions API:** Calculates the exact driving/walking route and turn-by-turn navigation between two points.
- **Distance Matrix API:** Calculates travel time and distance for a matrix of multiple origins and destinations.

---

### 3. Why
Bundling all mapping logic into one API would be bloated and excessively expensive. By splitting them, you only pay for what you use. If you just need to calculate the distance between two stores on the backend, you simply use the Distance Matrix API without loading any visual Javascript packages at all.

---

### 4. How
1. Use the GCP Console to search for and enable "Geocoding API" and "Places API".
2. Use the frontend Maps JavaScript API to visualize data.
3. Use backend HTTP requests to ping the Geocoding and Matrix APIs directly to generate numbers.

---

### 5. Implementation

**Mini Exercise: Conceptualizing the Flow**

Imagine a User buys shoes on your website.
1. The user types "123 Main St" into the checkout form. 
2. The **Places Autocomplete API** helps correct their typos as they type.
3. Upon pressing Submit, your Node server receives "123 Main St".
4. The Node server uses the **Geocoding API** to turn that address into coordinates (Lat/Lng).
5. The Node server then uses the **Distance Matrix API** to calculate how far those coordinates are from your warehouse.
6. The shipping fee is updated, and a visual map pin confirms the location using the **Maps JavaScript API**.

---

### 6. Steps (Enabling Multiple APIs)
1. A common mistake is enabling the Maps JavaScript API and assuming you have access to everything. You do not.
2. In the GCP Console, you must manually go to the library and click "Enable" for the Places API, Geocoding API, and Distance Matrix API individually.
3. Your single API key can access all of them once enabled.

---

### 7. Integration

🧠 **Think Like This:**
* The **Visual APIs** go on the Frontend (React).
* The **Calculation APIs** go on the Backend (Node.js).

---

### 8. Impact
📌 **Real-World Scenario:** Lyft heavily relies on the Distance Matrix API. They do not just route one car to one person. They calculate the distance matrix of 50 available cars near you, determining in milliseconds which specific driver has the fastest route to your specific pick-up pin.

---

### 9. Interview Questions
1. **Explain the functional difference between the Geocoding API and the Places API.**
   *Answer: Geocoding is responsible for specifically converting human-readable string addresses into exact latitude and longitude coordinates. The Places API acts as a semantic search engine matching vague user queries (e.g. "nearby sushi") to registered business entities and points of interest.*
2. **What is Reverse Geocoding?**
   *Answer: It is the process of providing raw latitude and longitude numeric coordinates to the Geocoding API, and having it return the human-readable street address associated with that precise physical point.*
3. **Why would a logistics company use the Distance Matrix API instead of the Directions API?**
   *Answer: The Directions API is optimized for returning complex turn-by-turn navigation paths for a single route. The Distance Matrix API computes duration and distance purely numerically across dozens of varied origins and destinations simultaneously, which is required for fleet dispatching algorithms.*

---

### 10. Summary
* Maps JS API renders the visual canvas.
* Geocoding transforms text to coordinates.
* Places API handles location searches and autocomplete.
* Distance Matrix handles complex fleet math and travel times.

---
Prev : [06_google_maps_platform_intro.md](./06_google_maps_platform_intro.md) | Next : [08_implementing_maps_in_react.md](./08_implementing_maps_in_react.md)
