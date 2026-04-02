# Storage and Databases in GCP

---

### 2. What
Data comes in different shapes, and Google offers specific services for each:
- **Cloud Storage:** An "Object Store". It holds files (Images, PDFs, Videos). You drop files in "Buckets".
- **Persistent Disk:** Raw SSD hard drives that you physically attach to your Compute Engine VMs.
- **Cloud SQL:** Managed Relational Databases (MySQL, PostgreSQL). Perfect for highly structured tabular data (Users, Orders).
- **Firestore:** A Serverless NoSQL Document database. Extremely fast, scales automatically, excellent for unstructured mobile/web data.
- **BigQuery:** A massive Data Warehouse. You can run heavy AI analytics on petabytes of data in seconds.

✅ **Simple Analogy:**
- *Cloud Storage:* Dropbox or Google Drive. Used strictly for files.
- *Cloud SQL:* An Excel Spreadsheet. Columns, rows, strictly structured.
- *Firestore:* A giant folder of JSON files. Flexible, fast, nested data.

---

### 3. Why
Saving an image directly onto an active server's hard drive is disastrous. If your Cloud Run app scales to 5 servers, Server B cannot see the image uploaded to Server A!
**The Golden Rule of Cloud:** Your servers must be *stateless*. Any permanent file must be sent to Cloud Storage. Any user state must be saved to a Database (SQL/Firestore).

---

### 4. How
When building a Node.js backend, you utilize the official `@google-cloud/` npm packages to hook into these extremely secure pipelines.

---

### 5. Implementation

**Practical Example: Uploading to Cloud Storage in Node.js**

```javascript
// 1. Install via: npm install @google-cloud/storage
const { Storage } = require('@google-cloud/storage');

// Initialize client (Google magically authenticates if running on Cloud Run!)
const storage = new Storage();
const bucketName = 'my-app-profile-pictures';

async function uploadImageToGCP(filePath, destinationFileName) {
  try {
    console.log(`Starting upload to ${bucketName}...`);
    
    // Uploads target file strictly into our GCP bucket
    await storage.bucket(bucketName).upload(filePath, {
      destination: destinationFileName,
    });

    console.log(`Successfully uploaded ${destinationFileName} to Google Cloud Storage!`);
    
    // We can then generate a public URL to save to our Database!
    return `https://storage.googleapis.com/${bucketName}/${destinationFileName}`;

  } catch (error) {
    console.error('ERROR uploading:', error);
  }
}

// uploadImageToGCP('./local-images/nishant.png', 'users/nishant.png');
```

---

### 6. Steps (Database Strategy)
1. Are you storing Profile Avatars or User PDFs? $\rightarrow$ **Cloud Storage**.
2. Does your data have extremely complex table relationships with exact schemas required? $\rightarrow$ **Cloud SQL (PostgreSQL)**.
3. Are you building a fast, scalable web/mobile app relying on rapid JSON document structures? $\rightarrow$ **Firestore**.

⚠️ **Common Mistake:** Beginners use Firestore for everything because it's NoSQL and easy to setup. However, executing deeply complex mathematical queries summing thousands of fields is extremely expensive in Firestore. That is what BigQuery/SQL is designed for.

---

### 7. Integration

🧠 **Think Like This:** 
* **React/Next.js:** A user selects an image using `<input type="file" />`. React sends this image directly to a Node.js API format.
* **Node.js (Backend):** The Node endpoint intercepts the file stream and routes it directly using the `@google-cloud/storage` SDK strictly into the Cloud Storage bucket. It receives a Public URL back.
* **Firestore:** Node.js then saves `{ username: "Nishant", avatarUrl: "https://gcp-storage..." }` neatly into Firestore.

---

### 8. Impact
📌 **Real-World Scenario:** Twitter cannot store 500 million images on one server. They use massive Object Storage systems (like Cloud Storage) to hold the raw binary images safely globally, and use extremely fast databases to point to those image URLs.

---

### 9. Interview Questions
1. **Why should you never store user-uploaded files locally on a Cloud Run or App Engine container instance?**
   *Answer: Because Serverless containers are strictly stateless and ephemeral. The container can scale down and be destroyed at any moment, permanently erasing any locally stored files. Artifacts must be handled by Cloud Storage.*
2. **What is the fundamental distinction between Cloud Storage and a Persistent Disk?**
   *Answer: Cloud Storage is an Object store accessed entirely via HTTP REST APIs, perfect for global unstructured file blobs. A Persistent Disk is a raw Block Storage drive attached physically directly to a singular VM's operating system natively.*
3. **Explain when to use Cloud SQL versus Firestore.**
   *Answer: Assess structural demands. If relying inherently on completely structured schemas utilizing complex ACID transactional joins historically universally, utilize Cloud SQL. If requiring infinitely scalable schema-less JSON document trees natively updating rapidly directly over WebSockets, use Firestore.*

---

### 10. Summary
* Store Files/Images structurally in Cloud Storage (Buckets).
* Store complex structured Relational data exactly in Cloud SQL.
* Store flexible rapid Web/Mobile JSON natively within Firestore.
* Keep your compute server completely *Stateless*.

---
Prev : [03_gcp_compute_services.md](./03_gcp_compute_services.md) | Next : [05_gcp_networking_and_security.md](./05_gcp_networking_and_security.md)
