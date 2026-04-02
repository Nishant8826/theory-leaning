# Deploying a Node.js Backend & Database

---

### 2. What
Your backend acts as the bridge between your Frontend (React) and your Database (Cloud SQL/Firestore). Deploying it means securely spinning up a Node.js server on **Cloud Run**, creating a database instance, and securely passing connection strings between them so they can communicate.

---

### 3. Why
If you try to run your Node.js API and your Database inside the exact same server instance, the server becomes bloated. If the server crashes, your database is destroyed. By deploying them separately—using Cloud Run for the API and Cloud SQL for the database—you ensure high availability and data permanence.

---

### 4. How
1. Use **Cloud SQL** to generate a managed PostgreSQL or MySQL database.
2. The database will give you a Private IP and a connection string.
3. Deploy your Node.js application to **Cloud Run**.
4. Attach the database connection string explicitly to the backend via Environment Variables.

---

### 5. Implementation

**A. Create the Database (Terminal)**

```bash
# Generate a tiny Postgres Database for our backend
gcloud sql instances create my-app-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1

# Set the password for the default "postgres" user
gcloud sql users set-password postgres \
    --instance=my-app-db \
    --password="SuperSecretPassword123"
```

**B. Deploy Node.js and Connect to DB**

```bash
# Deploy to Cloud Run, securely passing the DB Password and Google Maps Key!
gcloud run deploy backend-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --update-env-vars DB_PASS=SuperSecretPassword123,MAPS_KEY=AIza... \
  --add-cloudsql-instances my-project:us-central1:my-app-db
```

---

### 6. Steps
1. Write your Node.js code utilizing `process.env.DB_PASS` to connect to Postgres.
2. Spin up the Cloud SQL instance in the exact same region as your eventual Cloud Run service (`us-central1`).
3. Deploy Cloud Run, ensuring you use the `--add-cloudsql-instances` flag. This flag magically authorizes the serverless container to tunnel into the locked-down database automatically!

---

### 7. Integration

🧠 **Think Like This:**
* **React + Node + Maps:** React sends an address to Node.js. Node.js uses `process.env.MAPS_KEY` to query Google Maps for coordinates. Node.js takes those coordinates and uses `process.env.DB_PASS` to save them into Postgres. Node.js then returns the saved ID back to React.

---

### 8. Impact
📌 **Real-World Scenario:** By isolating the API (Cloud Run) from the Database (Cloud SQL), your app can withstand viral traffic. The API can aggressively scale to 100 duplicate containers, all funneling securely into one dedicated, powerful SQL Database, preventing server overload.

---

### 9. Interview Questions
1. **Why must you use the `--add-cloudsql-instances` flag when deploying Cloud Run?**
   *Answer: Because Cloud SQL instances are strictly secured behind GCP's private network. This flag provisions a specialized Unix socket acting as a secure tunnel uniquely granting the container access to the database.*
2. **Where is the safest place to store the database password in GCP?**
   *Answer: Passwords should never be hardcoded or passed raw in the CLI if avoidable. They should be securely stored in Google Secret Manager, and injected into Cloud Run at runtime as Environment Variables.*

---

### 10. Summary
* Deploy databases utilizing Cloud SQL (Relational) or Firestore (NoSQL).
* Deploy Backends using Cloud Run.
* Formally connect them using Environment Variables and specific GCP network tunneling flags.

---
Prev : [11_deploying_react_and_nextjs.md](./11_deploying_react_and_nextjs.md) | Next : [13_cloud_build_and_docker.md](./13_cloud_build_and_docker.md)
