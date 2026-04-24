# 🏗️ Case Study: WhatsApp (Messaging System)

## 📋 Requirements

**Functional:**
- 1:1 real-time messaging
- Group chats (up to 1,024 members)
- Message delivery status (sent ✓, delivered ✓✓, read ✓✓ in blue)
- Media sharing (photos, videos, documents, voice notes)
- End-to-end encryption
- Message history (even after offline)
- Online/last seen status

**Non-Functional:**
- 2 billion users, 100 million DAU
- 65 billion messages per day
- Message delivered in < 100ms (when online)
- 99.999% availability
- End-to-end encrypted
- Offline messages stored and delivered when user comes back online

---

## 📊 Capacity Estimation

```
Messages/day: 65B
Messages/sec: 750,000
Active connections: 100M simultaneous WebSocket connections!

Message size: 100 bytes (text avg)
65B × 100 bytes = 6.5TB message data per day

Media: ~30% messages have media
20B media messages × 1MB avg = 20PB/day media → Store in S3!

Storage: 
  Last 1 year: 6.5TB × 365 = ~2.4PB messages
  + 20PB/day × 365 days media (huge!)
  WhatsApp: Doesn't store messages server-side after delivery (E2E encrypted)
```

---

## 🏗️ High Level Architecture

```
[Client A: React Native / Web]
          |
          | WebSocket (persistent connection)
          |
[AWS API Gateway WebSocket / Node.js + Socket.IO]
          |
     [Message Broker] ← Redis Pub/Sub OR Kafka
          |
[AWS API Gateway WebSocket / Node.js + Socket.IO]
          |
[Client B: React Native / Web]

For offline delivery:
  Message → Queue (SQS) → Delivered when B reconnects

Storage:
  MongoDB (messages) + Redis (presence) + S3 (media)
```

---

## 💬 Core Messaging Implementation

```javascript
// server.js — Socket.IO based real-time messaging

const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const Redis = require('ioredis');

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: process.env.FRONTEND_URL },
  transports: ['websocket', 'polling']
});

// Redis Pub/Sub adapter — enables multiple Node.js servers!
const pubClient = new Redis(process.env.REDIS_URL);
const subClient = pubClient.duplicate();
io.adapter(createAdapter(pubClient, subClient));

// MongoDB for message persistence
const Message = mongoose.model('Message', new mongoose.Schema({
  _id: { type: String, default: () => uuidv4() },
  conversationId: { type: String, index: true },
  senderId: { type: String, required: true },
  type: { type: String, enum: ['text', 'image', 'video', 'audio', 'document'], default: 'text' },
  content: String,
  mediaUrl: String,
  status: { type: String, enum: ['sent', 'delivered', 'read'], default: 'sent' },
  replyTo: String,
  deletedFor: [String],
  createdAt: { type: Date, default: Date.now }
}));

// Connection handling
io.use(async (socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = user.userId;
    next();
  } catch (e) {
    next(new Error('Authentication failed'));
  }
});

io.on('connection', async (socket) => {
  const userId = socket.userId;
  
  console.log(`User ${userId} connected`);
  
  // 1. Join all user's conversation rooms
  const conversations = await getUserConversations(userId);
  conversations.forEach(conv => socket.join(`conv:${conv._id}`));
  
  // 2. Map userId to socket (for presence)
  await redis.hset('user:sockets', userId, socket.id);
  await redis.setex(`presence:${userId}`, 300, JSON.stringify({ status: 'online', lastSeen: new Date() }));
  
  // 3. Deliver queued offline messages
  await deliverOfflineMessages(userId, socket);
  
  // 4. Notify contacts user is online
  const contacts = await getContacts(userId);
  contacts.forEach(contactId => {
    io.to(`user:${contactId}`).emit('presence_update', { userId, status: 'online' });
  });
  
  // --- Message Events ---
  
  socket.on('send_message', async (data, callback) => {
    const { conversationId, content, type = 'text', mediaUrl, replyTo } = data;
    
    try {
      // Verify user is part of this conversation
      const conversation = await getConversation(conversationId);
      if (!conversation.participants.includes(userId)) {
        return callback({ error: 'Not authorized' });
      }
      
      // Create message
      const message = new Message({
        conversationId,
        senderId: userId,
        type,
        content,
        mediaUrl,
        replyTo,
        status: 'sent'
      });
      
      await message.save();
      
      // Update conversation last message
      await updateConversation(conversationId, {
        lastMessage: { content: type === 'text' ? content : `[${type}]`, senderId: userId, at: new Date() },
        lastActivity: new Date()
      });
      
      // Acknowledge to sender
      callback({ success: true, messageId: message._id, timestamp: message.createdAt });
      
      // Broadcast to conversation room
      socket.to(`conv:${conversationId}`).emit('new_message', {
        message: message.toObject(),
        conversationId
      });
      
      // Check who is online in conversation and update delivery status
      const otherParticipants = conversation.participants.filter(p => p !== userId);
      const onlineParticipants = [];
      
      for (const participantId of otherParticipants) {
        const socketId = await redis.hget('user:sockets', participantId);
        if (socketId) {
          onlineParticipants.push(participantId);
        } else {
          // Offline: Queue message for later delivery
          await queueOfflineMessage(participantId, message._id, conversationId);
        }
      }
      
      // Mark as delivered to online participants
      if (onlineParticipants.length > 0) {
        await message.updateOne({ status: 'delivered' });
        socket.emit('message_delivered', { messageId: message._id, deliveredTo: onlineParticipants });
      }
      
    } catch (error) {
      callback({ error: 'Message send failed' });
    }
  });
  
  // Message read receipt
  socket.on('messages_read', async ({ conversationId, upToMessageId }) => {
    await Message.updateMany(
      {
        conversationId,
        senderId: { $ne: userId }, // Not my messages
        status: { $ne: 'read' },
        _id: { $lte: upToMessageId }
      },
      { $set: { status: 'read' } }
    );
    
    // Notify message senders
    socket.to(`conv:${conversationId}`).emit('messages_read', {
      readBy: userId,
      conversationId,
      upToMessageId
    });
  });
  
  // Typing indicator
  socket.on('typing', ({ conversationId, isTyping }) => {
    socket.to(`conv:${conversationId}`).emit('typing_indicator', {
      userId,
      conversationId,
      isTyping
    });
  });
  
  // Disconnection
  socket.on('disconnect', async () => {
    await redis.hdel('user:sockets', userId);
    
    const lastSeen = new Date();
    await redis.setex(`presence:${userId}`, 7 * 24 * 60 * 60, JSON.stringify({ status: 'offline', lastSeen }));
    
    // Notify contacts
    const contacts = await getContacts(userId);
    contacts.forEach(contactId => {
      io.to(`user:${contactId}`).emit('presence_update', { userId, status: 'offline', lastSeen });
    });
    
    console.log(`User ${userId} disconnected`);
  });
});
```

### Offline Message Delivery

```javascript
// Queue offline messages
async function queueOfflineMessage(userId, messageId, conversationId) {
  await redis.lpush(
    `offline:messages:${userId}`,
    JSON.stringify({ messageId, conversationId, queuedAt: new Date() })
  );
}

// Deliver queued messages when user reconnects
async function deliverOfflineMessages(userId, socket) {
  const queueKey = `offline:messages:${userId}`;
  const queuedMessages = await redis.lrange(queueKey, 0, -1);
  
  if (queuedMessages.length === 0) return;
  
  // Fetch actual messages
  const messageIds = queuedMessages.map(m => JSON.parse(m).messageId);
  const messages = await Message.find({ _id: { $in: messageIds } });
  
  // Send them
  socket.emit('offline_messages', messages);
  
  // Mark as delivered
  await Message.updateMany(
    { _id: { $in: messageIds }, status: 'sent' },
    { $set: { status: 'delivered' } }
  );
  
  // Clear queue
  await redis.del(queueKey);
  
  // Also check SQS queue for any that Redis missed
}
```

---

## 📸 Media Sharing

```javascript
// Media Service for WhatsApp-style sharing

app.post('/api/media/upload', authenticate, upload.single('media'), async (req, res) => {
  const { conversationId } = req.body;
  
  // Validate file
  const allowedTypes = {
    'image/jpeg': { maxSize: 16 * 1024 * 1024 },  // 16MB
    'image/png': { maxSize: 16 * 1024 * 1024 },
    'video/mp4': { maxSize: 100 * 1024 * 1024 },   // 100MB
    'audio/ogg': { maxSize: 16 * 1024 * 1024 },    // Voice notes
    'application/pdf': { maxSize: 100 * 1024 * 1024 }
  };
  
  const fileType = allowedTypes[req.file.mimetype];
  if (!fileType) return res.status(400).json({ error: 'File type not allowed' });
  if (req.file.size > fileType.maxSize) return res.status(400).json({ error: 'File too large' });
  
  const mediaId = uuidv4();
  const key = `whatsapp/media/${conversationId}/${mediaId}`;
  
  // Upload to S3 (private — only accessible via signed URL or CDN)
  await s3.putObject({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    Body: req.file.buffer,
    ContentType: req.file.mimetype,
    ServerSideEncryption: 'aws:kms', // Encrypt with KMS key
    Metadata: {
      'conversation-id': conversationId,
      'uploader-id': req.user.id
    }
  }).promise();
  
  // For images: Generate thumbnail
  let thumbnailUrl = null;
  if (req.file.mimetype.startsWith('image/')) {
    const thumbnail = await sharp(req.file.buffer).resize(200, 200, { fit: 'cover' }).jpeg({ quality: 60 }).toBuffer();
    const thumbKey = `whatsapp/thumbs/${mediaId}.jpg`;
    await s3.putObject({ Bucket: process.env.S3_BUCKET, Key: thumbKey, Body: thumbnail }).promise();
    thumbnailUrl = `${process.env.CDN_URL}/${thumbKey}`;
  }
  
  // Return signed URL (7 day expiry)
  const mediaUrl = s3.getSignedUrl('getObject', { Bucket: process.env.S3_BUCKET, Key: key, Expires: 604800 });
  
  res.json({ mediaId, mediaUrl, thumbnailUrl, type: req.file.mimetype });
});
```

---

## 👁️ Presence System

```javascript
// Online/Last Seen with Redis TTL

// Update presence (called every 30 seconds while connected)
async function updatePresence(userId, status = 'online') {
  await redis.setex(
    `presence:${userId}`,
    60, // Expires in 60 seconds (heartbeat every 30s)
    JSON.stringify({ status, lastSeen: new Date().toISOString() })
  );
}

// Get presence
async function getPresence(userId) {
  const data = await redis.get(`presence:${userId}`);
  if (!data) return { status: 'offline', lastSeen: null };
  return JSON.parse(data);
}

// Get presence for multiple users
async function getBatchPresence(userIds) {
  const pipeline = redis.pipeline();
  userIds.forEach(id => pipeline.get(`presence:${id}`));
  const results = await pipeline.exec();
  
  return userIds.reduce((acc, id, i) => {
    acc[id] = results[i][1] ? JSON.parse(results[i][1]) : { status: 'offline' };
    return acc;
  }, {});
}

// API
app.get('/api/presence/:userId', authenticate, async (req, res) => {
  // Check if user allows last seen
  const targetUser = await db.getUser(req.params.userId);
  if (!targetUser.showLastSeen && !isContact(req.user.id, targetUser.id)) {
    return res.json({ status: 'unknown' });
  }
  res.json(await getPresence(req.params.userId));
});
```

---

## 🔐 End-to-End Encryption

```javascript
// WhatsApp uses Signal Protocol. Here's a simplified version:
// In a real implementation, E2E encryption happens on the CLIENT side

// Client-side encryption (browser/React Native):
const sodium = require('libsodium-wrappers');
await sodium.ready;

class E2EEncryption {
  // Generate key pair for a user (done once, stored locally)
  static generateKeyPair() {
    const keyPair = sodium.crypto_box_keypair();
    return {
      publicKey: sodium.to_hex(keyPair.publicKey),
      privateKey: sodium.to_hex(keyPair.privateKey)  // NEVER send to server!
    };
  }
  
  // Upload public key to server (so others can encrypt messages to you)
  static async uploadPublicKey(publicKey) {
    await fetch('/api/keys', {
      method: 'POST',
      body: JSON.stringify({ publicKey })
    });
  }
  
  // Encrypt message for recipient (using their public key)
  static encryptMessage(message, recipientPublicKey, senderPrivateKey) {
    const nonce = sodium.randombytes_buf(sodium.crypto_box_NONCEBYTES);
    const messageBytes = sodium.from_string(message);
    const recipientPKBytes = sodium.from_hex(recipientPublicKey);
    const senderSKBytes = sodium.from_hex(senderPrivateKey);
    
    const ciphertext = sodium.crypto_box_easy(messageBytes, nonce, recipientPKBytes, senderSKBytes);
    
    return {
      ciphertext: sodium.to_hex(ciphertext),
      nonce: sodium.to_hex(nonce)
    };
  }
  
  // Decrypt message (using own private key)
  static decryptMessage(encryptedData, senderPublicKey, recipientPrivateKey) {
    const ciphertext = sodium.from_hex(encryptedData.ciphertext);
    const nonce = sodium.from_hex(encryptedData.nonce);
    const senderPKBytes = sodium.from_hex(senderPublicKey);
    const recipientSKBytes = sodium.from_hex(recipientPrivateKey);
    
    const decrypted = sodium.crypto_box_open_easy(ciphertext, nonce, senderPKBytes, recipientSKBytes);
    return sodium.to_string(decrypted);
  }
}

// Server stores only encrypted messages — can't read content!
// Server stores public keys but NEVER private keys
```

---

## 🗄️ Database Schema

```javascript
// MongoDB Schemas (flexible document store for messages)

const conversationSchema = new mongoose.Schema({
  _id: String,
  type: { type: String, enum: ['direct', 'group'] },
  participants: [String],  // User IDs
  
  // Group only fields
  name: String,
  description: String,
  groupAvatarUrl: String,
  admins: [String],
  
  lastMessage: {
    content: String,
    senderId: String,
    at: Date
  },
  
  createdAt: { type: Date, default: Date.now },
  lastActivity: { type: Date, default: Date.now }
});

conversationSchema.index({ participants: 1, lastActivity: -1 });

const messageSchema = new mongoose.Schema({
  _id: String,
  conversationId: { type: String, index: true },
  senderId: String,
  type: { type: String, enum: ['text', 'image', 'video', 'audio', 'document'] },
  content: String,      // Encrypted on client, opaque blob to server
  mediaUrl: String,
  status: { type: String, enum: ['sent', 'delivered', 'read'] },
  readBy: [{ userId: String, at: Date }],
  replyTo: String,
  reactions: [{ userId: String, emoji: String }],
  deletedFor: [String],
  createdAt: { type: Date, default: Date.now }
});

messageSchema.index({ conversationId: 1, createdAt: -1 });
```

---

## 🎯 Interview Discussion Points

### Key Design Decisions

1. **WebSocket Architecture:** Socket.IO with Redis adapter allows scaling across multiple Node.js servers. Each server can receive/send messages for users connected to OTHER servers via Redis pub/sub.

2. **Message Storage:** MongoDB for flexibility (messages have varying schemas). Partition by conversationId for efficient queries.

3. **Offline Delivery:** Redis queue for recent offline messages. SQS for guaranteed delivery (if Redis dies, messages safe in SQS).

4. **Presence System:** Redis with TTL (60 seconds). Client sends heartbeat every 30 seconds. No heartbeat → key expires → user appears offline. Much cheaper than maintaining persistent connections.

5. **E2E Encryption:** Server never sees message content. Public keys stored on server. Private keys ONLY on client device. Server is a "dumb" relay.

6. **Media:** Upload to S3 directly (bypass your servers for large files). Generate signed URLs for access. CDN for fast delivery globally.

### Scaling Challenges

```
100M Concurrent Connections:
  Each WebSocket needs ~10KB memory
  100M × 10KB = 1TB RAM needed!
  
  Solution: Use AWS API Gateway WebSocket (fully managed, infinite scale)
  Or: Many Node.js servers, each handles ~50K connections
  
Message Fanout for Large Groups:
  Group has 1,024 members
  1 message → 1,024 deliveries
  10,000 active groups → 10.24M deliveries/message
  
  Solution: Kafka for group message fanout
  Each server subscribes to Kafka topics for conversations
  Message → Kafka → All servers → Each delivers to their connected clients
  
Global Scale:
  Users in India and USA in same group → high latency!
  Solution: Regional deployments (AWS Mumbai + US-East)
  Route users to nearest region
  Cross-region message relay via Kafka/SNS
```

---

### Navigation
**Prev:** [02_Design_Instagram.md](02_Design_Instagram.md) | **Index:** [00_Index.md](00_Index.md) | **Next:** [04_Design_Uber.md](04_Design_Uber.md)
