# File Uploads

## What You Will Learn
* How file uploads are transmitted over HTTP using `multipart/form-data` encoding.
* Security risks: Denial of Service (DoS) and Remote Code Execution (RCE) vulnerabilities.
* Parsing file uploads in Express using the Multer middleware.
* Validating file sizes, extensions, and MIME types.
* Streaming file uploads directly to Cloud Object Storage (like AWS S3).

## Why This Matters
Handling file uploads incorrectly is a major security risk. If you allow clients to upload files of any size without validation, they can exhaust your server's disk space, causing a Denial of Service (DoS). If you allow them to upload executable scripts (like `.js` or `.php`) to a folder served by your web server, they can execute code on your server (Remote Code Execution - RCE). Proper file upload validation and storage are critical for security.

## Theory

### Multipart/form-data Encoding
Standard JSON APIs transmit payload data using `application/json` format. However, JSON is text-based and inefficient for transmitting binary files.
* **`multipart/form-data`**: Encodes the request body as a series of parts separated by a unique boundary string. Each part can contain text fields or binary file payloads, allowing you to upload files alongside metadata in a single request.

### Security Vulnerabilities
1. **Denial of Service (DoS)**: Attackers upload massive files (e.g. 50GB) to fill up the server's disk space, crashing the operating system.
2. **Remote Code Execution (RCE)**: Attackers upload malicious scripts (e.g. `exploit.js` or `exploit.php`) to a public directory on your server. If your web server is configured to execute scripts in that directory, the attacker can trigger the script to gain control of your server.

## Deep Dive

### Streaming to Cloud Storage (AWS S3)
A common mistake is saving uploaded files to a temporary folder on the local server's disk before uploading them to cloud storage (like AWS S3).
* **Local Buffer Risk**: If you run your application in ephemeral containers (like Docker under Kubernetes), writing to local disk is slow and can exhaust container memory or disk space if many users upload files concurrently.
* **Stream Approach**: Use memory storage engines or custom stream wrappers to stream the incoming file upload directly to S3 as the bytes arrive from the network card, keeping memory usage low and eliminating local disk writes.

## Visual Explanation

### Streaming Upload Pipeline: Local Disk vs. Direct to Cloud (S3)
```text
Insecure/Slow (Local Temp Disk write):
[ Client Upload ] ── TCP Sockets ──> [ Write Temp File to local disk ] ──> [ Upload to S3 ] ──> [ Delete Temp File ]
                                          │
                                          └── Danger: If disk fills up, server crashes!

Secure/Fast (Direct Streaming):
[ Client Upload ] ── TCP Sockets ──> [ Express Router ] ── Memory Stream Pipe ──> [ AWS S3 Bucket ]
  - Bytes are written directly to S3 as they arrive in chunks. RAM usage remains flat (~64KB).
```

## Real-World Example
Consider an application that allows users to upload profile pictures. You configure the upload middleware to restrict files to image MIME types only (`image/jpeg`, `image/png`), set a maximum file size limit of 2MB, and generate random filenames using UUIDs. You stream the files directly to an AWS S3 bucket, ensuring the uploads are secure and efficient.

## Code Examples

### Local Storage Parsing with Validation and Streaming to AWS S3

```javascript
// middleware/upload.js
// Dependencies required: npm install express multer @aws-sdk/client-s3 multer-s3
const multer = require('multer');
const path = require('path');
const AppError = require('../utils/AppError');

// 1. Local Storage Engine configuration with filename sanitization
const localStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/'); // Saves files to a local 'uploads/' folder
  },
  filename: (req, file, cb) => {
    // Generate a unique filename using timestamp and random number
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    // Sanitize extension
    const ext = path.extname(file.originalname).toLowerCase();
    cb(null, file.fieldname + '-' + uniqueSuffix + ext);
  }
});

// 2. Strict File Filter (Accept images only)
const imageFileFilter = (req, file, cb) => {
  const allowedMimeTypes = ['image/jpeg', 'image/png', 'image/webp'];
  
  if (allowedMimeTypes.includes(file.mimetype)) {
    cb(null, true); // Accept file
  } else {
    // Reject file with a clear validation error
    cb(new AppError('Bad Request: Only JPEG, PNG, and WebP images are allowed.', 400), false);
  }
};

// 3. Configure local upload middleware
const uploadImageLocal = multer({
  storage: localStorage,
  fileFilter: imageFileFilter,
  limits: {
    fileSize: 2 * 1024 * 1024 // Set maximum file size limit to 2MB
  }
});

module.exports = { uploadImageLocal };
```

```javascript
// s3-upload.js (Cloud upload configuration using streams)
const express = require('express');
const multer = require('multer');
const { S3Client } = require('@aws-sdk/client-s3');
const multerS3 = require('multer-s3');
const { uploadImageLocal } = require('./middleware/upload');

const app = express();

// Initialize AWS S3 Client
const s3 = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID || 'mock',
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || 'mock'
  }
});

// Configure Multer-S3 to stream uploads directly to S3
const uploadImageToS3 = multer({
  storage: multerS3({
    s3: s3,
    bucket: process.env.AWS_S3_BUCKET || 'my-app-assets',
    acl: 'public-read',
    metadata: (req, file, cb) => {
      cb(null, { fieldName: file.fieldname });
    },
    key: (req, file, cb) => {
      const uniqueName = Date.now() + '-' + file.originalname;
      cb(null, `profile-pictures/${uniqueName}`);
    }
  }),
  limits: { fileSize: 5 * 1024 * 1024 } // 5MB limit
});

// --- API ROUTE ENDPOINTS ---

// Route 1: Local storage file upload
app.post('/api/profile/avatar-local', uploadImageLocal.single('avatar'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });
  }
  
  res.json({
    message: 'File uploaded locally successfully.',
    fileInfo: {
      filename: req.file.filename,
      size: req.file.size,
      path: req.file.path
    }
  });
});

// Route 2: Direct S3 stream upload
app.post('/api/profile/avatar-s3', uploadImageToS3.single('avatar'), (req, res) => {
  res.json({
    message: 'File streamed to S3 successfully.',
    url: req.file.location // Public URL returned by S3
  });
});

// Error boundary middleware
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    // Handle Multer-specific errors (like file size limit exceeded)
    return res.status(400).json({ error: `Upload error: ${err.message}` });
  }
  res.status(err.statusCode || 500).json({ error: err.message });
});

app.listen(3000, () => console.log('File upload server running on port 3000'));
```

## Best Practices
* **Set File Size Limits**: Always define strict file size limits (e.g. 2MB for images) in your upload configurations to prevent disk space exhaustion.
* **Validate MIME Types and Extensions**: Validate both the file extension and the MIME type. Do not rely on client-provided filenames alone; check the header and verify it.
* **Upload to Cloud Object Storage**: Stream uploaded files directly to Cloud Object Storage (like AWS S3) rather than storing them on the local application disk in production.
* **Sanitize Filenames**: Always rename uploaded files to random strings (like UUIDs) to prevent Directory Traversal attacks and avoid duplicate filename collisions.

## Interview Questions

### Beginner
* **What HTTP encoding format is used to upload files, and why is it preferred over JSON?**
  *Answer*: File uploads use the `multipart/form-data` encoding format. It is preferred over JSON because JSON is a text-based format that cannot transmit raw binary data efficiently. `multipart/form-data` encodes the request body in multiple parts using boundary strings, allowing binary files and text fields to be transmitted efficiently in a single request.

### Intermediate
* **What is a Remote Code Execution (RCE) vulnerability in file uploads, and how do you prevent it?**
  *Answer*: An RCE vulnerability occurs when an attacker uploads an executable script (such as a `.js` or `.php` file) to a public folder on your server. If the web server is configured to serve and execute files in that folder, the attacker can execute code on your server. 
  To prevent it, rename all uploaded files to random strings, validate that only safe file extensions and MIME types are allowed, and configure your web server (e.g. Nginx) to disable execution permissions in the upload directory.

### Advanced
* **Why should you stream file uploads directly to AWS S3 instead of writing them to a local temporary folder first?**
  *Answer*: Storing files locally first creates performance and security issues:
  1. Writing to a local disk is a slow, blocking I/O operation.
  2. If multiple users upload files concurrently, it can fill up the local disk space, causing a Denial of Service (DoS) crash.
  3. In ephemeral container environments (like Kubernetes pods), local storage is temporary and lost when the container restarts.
  Streaming files directly to S3 as the data bytes arrive in chunks keeps memory and disk utilization low, improving scalability.

### Senior Architect
* **How would you build a highly secure file upload scanning pipeline that scans uploaded files for malware and viruses before making them publicly available in an S3 bucket?**
  *Answer*: To build a secure file upload scanning pipeline:
  1. Set up an S3 bucket with two main directories: `/quarantine` (private) and `/public` (publicly accessible).
  2. Configure the Node.js application to stream uploads directly to the `/quarantine` folder in S3, making the file private by default.
  3. Configure an S3 event trigger that executes an AWS Lambda function whenever a new file is uploaded to the `/quarantine` folder.
  4. The Lambda function runs an antivirus engine (like ClamAV) to scan the file's binary content.
  5. If the scan passes, the Lambda function moves the file from `/quarantine` to the `/public` folder, making it available to clients. If the scan fails, the Lambda function deletes the file and alerts security systems, protecting users from malware.

---
Previous : [43_Rate_Limiting.md] | Index : [00_index.md] | Next : [45_Email_Services.md]
