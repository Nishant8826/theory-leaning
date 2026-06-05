# 53 – Kafka on Kubernetes using Strimzi Operator

---

## Table of Contents

1. [What is Apache Kafka?](#1-what-is-apache-kafka)
2. [Kafka Core Components](#2-kafka-core-components)
3. [Kafka vs RabbitMQ](#3-kafka-vs-rabbitmq)
4. [Why Run Kafka on Kubernetes?](#4-why-run-kafka-on-kubernetes)
5. [What is the Strimzi Operator?](#5-what-is-the-strimzi-operator)
6. [KRaft Mode (ZooKeeper-less Kafka)](#6-kraft-mode-zookeeper-less-kafka)
7. [Architecture Diagram](#7-architecture-diagram)
8. [Hands-On: Full Deployment Steps](#8-hands-on-full-deployment-steps)
9. [Tech Stack Mapping](#9-tech-stack-mapping)
10. [Scenario-Based Q&A](#10-scenario-based-qa)
11. [Interview Q&A](#11-interview-qa)

---

## 1. What is Apache Kafka?

### What
Apache Kafka is a **distributed event streaming platform** — think of it as a high-speed, fault-tolerant pipe that lets applications send and receive millions (or trillions) of messages in real time.

### Why
Modern applications (e-commerce, ride-hailing, banking) generate massive amounts of data every second. Traditional message queues like RabbitMQ can handle ~50,000 messages/day. Kafka can handle **trillions of messages**, making it the go-to tool for large-scale, real-time data pipelines.

### How
1. A **Producer** application publishes a message (e.g., "Order placed") to a named **Topic**.
2. The topic is stored on a **Broker** (a Kafka server) and split into **Partitions** for parallelism.
3. One or more **Consumer** applications subscribe to the topic and read those messages.
4. Kafka retains the messages for a configurable period, so consumers can replay them.

### Impact

| With Kafka | Without Kafka |
|---|---|
| Services are decoupled — they don't call each other directly | Services become tightly coupled, causing cascading failures |
| Handle millions of events per second | Bottleneck at high load |
| Messages are retained and replayable | Lost if consumer was offline |
| Multiple consumers can read the same event independently | Each message consumed only once |

### Real-World Analogy
Imagine Zomato's order system. The moment you place an order, that event (message) is published to Kafka. Multiple services — the restaurant dashboard, the delivery partner app, the analytics team — all independently consume that same event from Kafka. Nobody calls anybody directly. It's like a **centralized notice board** that everyone subscribes to.

---

## 2. Kafka Core Components

### Broker
A **Kafka Broker** is a single Kafka server. It receives messages from producers, stores them on disk, and serves them to consumers. A Kafka **cluster** is made of multiple brokers for fault tolerance.

```
Cluster
├── Broker 1  (Leader for Partition 0)
├── Broker 2  (Leader for Partition 1)
└── Broker 3  (Replica for Partition 0 & 1)
```

### Topic
A **Topic** is a named category/stream of messages — like a folder name. For example: `order-events`, `payment-events`.

### Partition
Topics are split into **Partitions** stored across brokers. Partitions allow Kafka to:
- Scale horizontally (more partitions = more parallelism)
- Guarantee ordering *within* a partition

### Producer
An application that **writes/sends** messages to a topic.

### Consumer
An application that **reads/receives** messages from a topic. Consumers can be grouped into **Consumer Groups** — each partition is assigned to exactly one consumer in a group, enabling parallel processing.

### ZooKeeper (Legacy)
Previously used to manage broker metadata, leader election, and cluster coordination. Now replaced by **KRaft**.

### KRaft (New)
Kafka's own built-in **consensus mechanism** (Raft protocol) that replaces ZooKeeper. Introduced in Kafka 2.8+, production-ready from 3.x onwards.

---

## 3. Kafka vs RabbitMQ

| Feature | Kafka | RabbitMQ |
|---|---|---|
| Throughput | Trillions of messages | ~50,000/day (approx. practical limit) |
| Message Retention | Configurable (days/weeks) | Deleted after consumption |
| Use Case | Event streaming, log aggregation | Task queues, RPC |
| Message Replay | ✅ Yes | ❌ No |
| Consumer Model | Pull-based | Push-based |
| Ordering | Within partition | Within queue |
| Protocol | Custom TCP (binary) | AMQP |
| Best For | High-volume, real-time analytics | Simple job queues |

**When to choose Kafka:** You need replay, high throughput, multiple consumers reading the same event, or real-time analytics pipelines.

**When to choose RabbitMQ:** Simple task distribution, low-volume, or you need request/reply patterns.

---

## 4. Why Run Kafka on Kubernetes?

### What
Running Kafka on Kubernetes (K8s) means deploying Kafka brokers as Kubernetes Pods/StatefulSets instead of on bare VMs.

### Why
- **Auto-scaling:** K8s can automatically add/remove Kafka broker pods based on load.
- **Self-healing:** If a broker pod crashes, K8s restarts it automatically.
- **Containerization:** Kafka packaged in Docker images — consistent across dev, staging, prod.
- **High Availability:** Spread pods across nodes/zones for fault tolerance.
- **Cloud-native:** Leverage K8s features like persistent volumes, secrets, config maps.
- **Cost Efficiency:** Share cluster resources with other workloads.

### How
You don't deploy Kafka manually on K8s — you use an **Operator** (Strimzi) that understands Kafka's lifecycle and manages it like a native K8s resource.

---

## 5. What is the Strimzi Operator?

### What
Strimzi is a **Kubernetes Operator** specifically built to run Apache Kafka on Kubernetes and OpenShift. It was donated to the **CNCF (Cloud Native Computing Foundation)** and is production-ready.

### Why
Without Strimzi, deploying Kafka on K8s requires complex manual configuration of StatefulSets, Services, PersistentVolumeClaims, ConfigMaps, etc. Strimzi wraps all of this into simple **Custom Resource Definitions (CRDs)** like `Kafka`, `KafkaTopic`, `KafkaUser`.

### How Strimzi Works

```
kubectl apply -f kafka.yaml
        |
        v
Strimzi Operator (Controller)
        |
        v
Creates K8s Resources automatically:
  - StatefulSet (Broker Pods)
  - Services (bootstrap, per-broker)
  - PersistentVolumeClaims (storage)
  - ConfigMaps (config)
  - ServiceAccounts, RBAC
```

### Strimzi Custom Resources (CRDs)

| CRD | Purpose |
|---|---|
| `Kafka` | Defines the entire Kafka cluster |
| `KafkaNodePool` | Defines a pool of broker/controller nodes |
| `KafkaTopic` | Creates/manages topics declaratively |
| `KafkaUser` | Creates/manages Kafka users with ACLs |

### Impact
- Without Strimzi: Days of manual YAML + operational complexity
- With Strimzi: Kafka cluster in minutes, managed declaratively via `kubectl`

---

## 6. KRaft Mode (ZooKeeper-less Kafka)

### What
**KRaft** (Kafka Raft Metadata mode) is Kafka's built-in replacement for ZooKeeper. Brokers now manage their own metadata using the Raft consensus algorithm.

### Why
- Reduces operational overhead (no separate ZooKeeper cluster to manage)
- Faster controller failover
- Simpler architecture
- Required for Kafka 4.x (ZooKeeper support removed)

### How (with KafkaNodePool)
In the demo, nodes have **dual roles** — each node is both a **controller** (manages metadata) and a **broker** (handles messages):

```yaml
spec:
  roles:
    - controller   # Raft consensus / metadata
    - broker       # Actual message storage
```

In large production setups, you'd separate these roles into different node pools for better isolation.

---

## 7. Architecture Diagram

### High-Level Kafka on Kubernetes Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster                       │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                  kafka Namespace                       │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │            Strimzi Operator                      │  │  │
│  │  │     ← watches Kafka CRDs                         │  │  │
│  │  └──────────────────────┬───────────────────────────┘  │  │
│  │                         │                              │  │
│  │                         ▼                              │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │             my-cluster (Kafka)                   │  │  │
│  │  │                                                  │  │  │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │  │  │
│  │  │  │ Broker Pod 0 │  │ Broker Pod 1 │  │ Broker  │ │  │  │
│  │  │  │ (ctrl+brk)   │  │ (ctrl+brk)   │  │ Pod 2   │ │  │  │
│  │  │  └──────┬───────┘  └──────┬───────┘  └────┬────┘ │  │  │
│  │  │         │                 │                │     │  │  │
│  │  │         ▼                 ▼                ▼     │  │  │
│  │  │  ┌─────────────────────────────────────────────┐ │  │  │
│  │  │  │ my-cluster-kafka-bootstrap Service (9092)   │ │  │  │
│  │  │  └─────────────────────────────────────────────┘ │  │  │
│  │  │                                                  │  │  │
│  │  │  Topics: my-topic (3 partitions, RF=3)           │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │                                                        │  │
│  │  Producer Pod  ─────────────► Consumer Pod             │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### Message Flow

```
Producer App
    │
    │  publish("Hello Kafka") → topic: my-topic
    ▼
Bootstrap Service (my-cluster-kafka-bootstrap:9092)
    │
    │  routes to leader broker for partition
    ▼
Broker Pod (e.g., dual-role-0)
    │
    │  writes to Partition 0 on disk (PVC)
    │  replicates to Broker 1, Broker 2
    ▼
Consumer App
    │  subscribe(topic: my-topic, from-beginning)
    ▼
reads messages: "Hello Kafka", "Kafka on Kubernetes", ...
```

### Topic Partition Layout

```
Topic: my-topic (partitions=3, replicas=3)

Partition 0: Leader=Pod0, Replicas=Pod1,Pod2
Partition 1: Leader=Pod1, Replicas=Pod0,Pod2
Partition 2: Leader=Pod2, Replicas=Pod0,Pod1
```

---

## 8. Hands-On: Full Deployment Steps

### Prerequisites
- Kubernetes cluster (GCP Standard mode, 3 nodes, 30GB disk recommended)
- `kubectl` configured to point to the cluster

---

### Step 1 – Create Kafka Namespace

```bash
kubectl create namespace kafka
```

**Why?** Isolates all Kafka resources in a dedicated namespace. Keeps things clean and makes RBAC easier.

---

### Step 2 – Install Strimzi Operator

```bash
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
```

**What happens:**
- Downloads Strimzi CRD definitions (Kafka, KafkaTopic, KafkaUser, etc.)
- Creates the Strimzi cluster operator Deployment
- Sets up RBAC (ClusterRoles, ServiceAccounts)

**Verify:**

```bash
kubectl get pods -n kafka
# Expected:
# strimzi-cluster-operator-xxxxx   1/1 Running
```

---

### Step 3 – Deploy Kafka Cluster (KRaft Mode)

```bash
cat <<EOF | kubectl apply -f -
apiVersion: kafka.strimzi.io/v1
kind: KafkaNodePool
metadata:
  name: dual-role
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  replicas: 3
  roles:
    - controller
    - broker
  storage:
    type: jbod
    volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: true
---
apiVersion: kafka.strimzi.io/v1
kind: Kafka
metadata:
  name: my-cluster
  namespace: kafka
  annotations:
    strimzi.io/node-pools: enabled
    strimzi.io/kraft: enabled
spec:
  kafka:
    version: 4.2.0
    metadataVersion: 4.2-IV0
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF
```

**Key config explained:**

| Config | Value | Meaning |
|---|---|---|
| `replicas` | 3 | 3 Kafka broker pods |
| `roles` | controller + broker | Each pod handles both metadata and messages (KRaft dual-role) |
| `storage.size` | 10Gi | 10GB persistent disk per pod |
| `deleteClaim: true` | true | PVC deleted when Kafka cluster is deleted |
| `offsets.topic.replication.factor` | 3 | Consumer offset data replicated 3x |
| `min.insync.replicas` | 2 | At least 2 replicas must acknowledge a write |
| `tls: false` | false | Plain text listener (demo only; use TLS in prod) |

**Watch pods come up:**

```bash
kubectl get pods -n kafka -w
# Pods progress through: Pending → Init → Running
```

**Check cluster status:**

```bash
kubectl get kafka -n kafka
# NAME         READY
# my-cluster   True
```

---

### Step 4 – Create a Kafka Topic

```bash
cat <<EOF | kubectl apply -f -
apiVersion: kafka.strimzi.io/v1
kind: KafkaTopic
metadata:
  name: my-topic
  namespace: kafka
  labels:
    strimzi.io/cluster: my-cluster
spec:
  partitions: 3
  replicas: 3
EOF
```

**Verify:**

```bash
kubectl get kafkatopic -n kafka
# NAME       CLUSTER      PARTITIONS  REPLICATION FACTOR  READY
# my-topic   my-cluster   3           3                   True
```

---

### Step 5 – Run a Producer

```bash
kubectl -n kafka run kafka-producer \
  -ti --image=quay.io/strimzi/kafka:latest-kafka-4.2.0 \
  --rm=true --restart=Never \
  -- bin/kafka-console-producer.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --topic my-topic
```

Send messages (type and press Enter):

```
Hello Kafka
Kafka on Kubernetes
Strimzi Demo
```

---

### Step 6 – Run a Consumer (new terminal)

```bash
kubectl -n kafka run kafka-consumer \
  -ti --image=quay.io/strimzi/kafka:latest-kafka-4.2.0 \
  --rm=true --restart=Never \
  -- bin/kafka-console-consumer.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --topic my-topic \
  --from-beginning
```

You'll see all previously sent messages appear instantly.

---

### Step 7 – List All Topics

```bash
kubectl -n kafka run kafka-client \
  -ti --image=quay.io/strimzi/kafka:latest-kafka-4.2.0 \
  --rm=true --restart=Never \
  -- bin/kafka-topics.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --list
```

---

### Step 8 – Describe a Topic

```bash
kubectl -n kafka run kafka-client \
  -ti --image=quay.io/strimzi/kafka:latest-kafka-4.2.0 \
  --rm=true --restart=Never \
  -- bin/kafka-topics.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --describe \
  --topic my-topic
```

Output shows: Leader broker, ISR (in-sync replicas) per partition.

---

### Cleanup

```bash
kubectl delete kafka my-cluster -n kafka
kubectl delete namespace kafka
```

---

## 9. Tech Stack Mapping

### How Kafka Fits Into Your Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                      Production Architecture                     │
│                                                                 │
│  Node.js API ──► Kafka Topic ──► Node.js Consumer ──► MongoDB  │
│  (Producer)        (orders)       (order-service)    (persist) │
│                        │                                        │
│                        └──────────────────────────────►         │
│                                             Analytics Service   │
│                                             (reads same topic)  │
└─────────────────────────────────────────────────────────────────┘
```

### Node.js Producer Example (KafkaJS)

```javascript
// npm install kafkajs
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: ['my-cluster-kafka-bootstrap:9092'], // K8s service DNS
});

const producer = kafka.producer();

async function publishOrder(order) {
  await producer.connect();
  await producer.send({
    topic: 'order-events',
    messages: [
      { key: order.id, value: JSON.stringify(order) }
    ],
  });
  await producer.disconnect();
}

publishOrder({ id: 'ORD-001', item: 'Pizza', status: 'placed' });
```

### Node.js Consumer Example

```javascript
const consumer = kafka.consumer({ groupId: 'notification-group' });

async function startConsumer() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'order-events', fromBeginning: false });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const order = JSON.parse(message.value.toString());
      console.log(`New order received: ${order.id}`);
      // Send email/push notification
    },
  });
}

startConsumer();
```

### Next.js App → Kafka Flow

```
User places order on Next.js frontend
        │
        ▼
Next.js API Route (/api/orders)
        │
        ▼
Publishes to Kafka: topic=order-events
        │
        ├──► Consumer 1: Restaurant Dashboard (WebSocket push)
        ├──► Consumer 2: Delivery Partner App
        ├──► Consumer 3: Analytics / BigQuery
        └──► Consumer 4: Email Notification Service
```

### AWS Integration Pattern

```
AWS EKS Cluster
  └── Kafka (Strimzi)
        └── Topics
              ├── Consumed by Lambda (via MSK/event bridge)
              ├── Stored to S3 (via Kafka Connect S3 Sink)
              └── Streamed to RDS (via Debezium CDC connector)
```

### Cross-Cloud Kafka (AWS ↔ GCP)

```
GCP Kubernetes (Kafka Cluster)
        │
        │  MirrorMaker2 (Kafka-native replication)
        ▼
AWS MSK (Managed Kafka)
        │
        ▼
AWS Lambda / EC2 consumers
```

### Jenkins Pipeline for Kafka Deployment

```groovy
pipeline {
  agent any
  stages {
    stage('Deploy Strimzi Operator') {
      steps {
        sh 'kubectl apply -f https://strimzi.io/install/latest?namespace=kafka -n kafka'
        sh 'kubectl wait --for=condition=available deployment/strimzi-cluster-operator -n kafka --timeout=120s'
      }
    }
    stage('Deploy Kafka Cluster') {
      steps {
        sh 'kubectl apply -f k8s/kafka-cluster.yaml'
        sh 'kubectl wait kafka/my-cluster --for=condition=Ready --timeout=300s -n kafka'
      }
    }
    stage('Create Topics') {
      steps {
        sh 'kubectl apply -f k8s/kafka-topics/'
      }
    }
    stage('Verify') {
      steps {
        sh 'kubectl get kafkatopic -n kafka'
        sh 'kubectl get kafka -n kafka'
      }
    }
  }
}
```

### Socket.IO + Kafka for Real-Time Updates

```javascript
// server.js — Kafka consumer pushes to WebSocket clients
const { Server } = require('socket.io');
const io = new Server(httpServer);

consumer.run({
  eachMessage: async ({ message }) => {
    const event = JSON.parse(message.value.toString());
    // Broadcast to all connected browser clients
    io.emit('order-update', event);
  }
});
```

---

## 10. Scenario-Based Q&A

---

🔍 **Scenario 1:** Your Node.js order service is directly calling your notification service via HTTP. On peak sale days, the notification service crashes and orders are lost.

✅ **Answer:** Decouple using Kafka. The order service publishes to `order-events` topic. The notification service consumes from it. If notification service crashes, messages wait in Kafka. When it restarts, it picks up from where it left off — no orders lost.

---

🔍 **Scenario 2:** Your team wants real-time analytics on every user action (clicks, purchases) on your Next.js app. Millions of events per day.

✅ **Answer:** Instrument the Next.js API routes to publish events to a Kafka topic (e.g., `user-actions`). An analytics consumer reads from Kafka and writes to a data warehouse (BigQuery, Redshift). Kafka handles millions of events per second easily.

---

🔍 **Scenario 3:** A Kafka broker pod crashes on your Kubernetes cluster at 2 AM.

✅ **Answer:** Kubernetes self-healing automatically restarts the crashed pod. With `replicas: 3` and `min.insync.replicas: 2`, the cluster stays operational. The restarted pod syncs its partition replicas from the remaining brokers before rejoining as a leader.

---

🔍 **Scenario 4:** Your manager asks "Why not just use Redis Pub/Sub instead of Kafka?"

✅ **Answer:** Redis Pub/Sub is fire-and-forget — if a subscriber is offline, messages are lost. Kafka persists messages to disk for a configurable retention period (days/weeks). Late consumers can replay all messages from the beginning. For high-volume, reliable event streaming, Kafka is far superior.

---

🔍 **Scenario 5:** You need to connect Kafka running on GCP to consumers on AWS.

✅ **Answer:** Use **Kafka MirrorMaker 2** (MM2) to replicate topics from the GCP Kafka cluster to AWS MSK or another Kafka cluster on AWS. MM2 is Kafka-native and handles offset sync, so consumers on AWS can pick up messages reliably.

---

🔍 **Scenario 6:** A new team member asks, "As a DevOps engineer, what Kafka work is mine vs the developer's?"

✅ **Answer:** DevOps owns: cluster deployment (Strimzi), topic creation/management, monitoring (Prometheus/Grafana), scaling, backup, upgrades, CI/CD pipelines for Kafka configs. Developers own: producer/consumer code, schema design, message format, consumer group management.

---

## 11. Interview Q&A

---

**Q1. What is Apache Kafka and what problem does it solve?**

**A:** Kafka is a distributed event streaming platform that allows applications to publish and subscribe to streams of records (messages) in real time. It solves the problem of **tight coupling** between services — instead of Service A calling Service B directly (synchronous, fragile), A publishes an event to Kafka and B consumes it independently. It also handles **massive throughput** (trillions of messages) that traditional message queues cannot.

---

**Q2. What are Kafka's core components?**

**A:**
- **Broker** – A Kafka server that stores and serves messages.
- **Topic** – A named stream of messages (like a folder).
- **Partition** – A topic is split into partitions across brokers for parallelism and scalability.
- **Producer** – Application that writes messages to a topic.
- **Consumer** – Application that reads messages from a topic.
- **Consumer Group** – Multiple consumers sharing work; each partition assigned to one consumer in the group.
- **KRaft** – Kafka's built-in consensus mechanism (replaced ZooKeeper in Kafka 4.x).

---

**Q3. What is the difference between Kafka and RabbitMQ?**

**A:** Kafka is designed for **high-throughput event streaming** with message retention and replay capability. RabbitMQ is designed for **task queues** with push-based delivery. Key differences: Kafka retains messages after consumption (consumers can replay), whereas RabbitMQ deletes messages once consumed. Kafka can handle trillions of messages vs RabbitMQ's more limited throughput. Choose Kafka for event sourcing, analytics pipelines, and microservices communication at scale; choose RabbitMQ for simple job queues.

---

**Q4. What is the Strimzi Operator and why do we use it?**

**A:** Strimzi is a **Kubernetes Operator** for Apache Kafka. It extends Kubernetes with Custom Resource Definitions (CRDs) like `Kafka`, `KafkaTopic`, `KafkaUser`. Instead of manually managing StatefulSets, Services, PVCs for Kafka, you declare the desired state in YAML and Strimzi's operator reconciles it. It handles day-2 operations like rolling upgrades, scaling, and TLS certificate management automatically. It's CNCF-adopted and production-ready.

---

**Q5. What is KRaft mode in Kafka?**

**A:** KRaft (Kafka Raft Metadata) is Kafka's built-in metadata management system that **replaces ZooKeeper**. Previously, Kafka required a separate ZooKeeper cluster for leader election and metadata storage. KRaft embeds this functionality directly into Kafka brokers using the Raft consensus algorithm. Benefits: simpler architecture (no ZooKeeper to maintain), faster failover, and it's mandatory in Kafka 4.x+. In Strimzi, you enable it with `strimzi.io/kraft: enabled` annotation.

---

**Q6. What is `min.insync.replicas` in Kafka?**

**A:** `min.insync.replicas` (ISR) defines the **minimum number of replicas that must acknowledge a write** before the producer considers it successful (when using `acks=all`). For example, with 3 brokers and `min.insync.replicas: 2`, at least 2 brokers must confirm they've written the message. This provides durability — you won't lose data even if one broker fails. Setting it too low risks data loss; setting it equal to total replicas means any broker failure blocks writes.

---

**Q7. How would you deploy Kafka on Kubernetes in a CI/CD pipeline?**

**A:** The flow would be:
1. Store Kafka manifests (Strimzi CRDs, Kafka cluster YAML, KafkaTopic YAMLs) in a Git repository.
2. Jenkins/GitHub Actions pipeline detects changes.
3. Pipeline applies Strimzi operator via `kubectl apply`.
4. Pipeline waits for operator to be ready (`kubectl wait --for=condition=available`).
5. Pipeline applies Kafka cluster manifest and waits for `Ready` status.
6. Pipeline applies topic manifests.
7. Pipeline runs smoke tests (produce/consume a test message).
This is GitOps-style Kafka lifecycle management.

---

**Q8. How does Kafka handle fault tolerance in a 3-broker cluster?**

**A:** Each topic partition has a **leader** and **replicas** on different brokers. With `replication.factor: 3`, each partition exists on all 3 brokers. If one broker goes down: Kafka's controller (via KRaft) detects the failure and **elects a new leader** from the in-sync replicas. Producers and consumers automatically reconnect to the new leader via the bootstrap service. The cluster continues to function as long as enough brokers are up (governed by `min.insync.replicas`). Kubernetes' self-healing also restarts the crashed pod.

---

**Q9. What is a KafkaNodePool in Strimzi?**

**A:** `KafkaNodePool` is a Strimzi CRD that defines a group (pool) of Kafka nodes with a specific role and storage configuration. In KRaft mode, a node can have the role of `controller` (manages metadata/Raft quorum), `broker` (handles messages), or both (`dual-role`). Using node pools allows you to scale controllers and brokers independently in large production setups. For smaller setups, dual-role nodes handle both responsibilities.

---

**Q10. As a DevOps engineer, what Kafka experience can you put on your resume?**

**A:** You can claim:
- Deployed Apache Kafka on Kubernetes using Strimzi Operator (KRaft mode)
- Managed Kafka clusters: topic creation, partition configuration, replication factor tuning
- Integrated Kafka deployment into CI/CD pipelines (Jenkins/GitHub Actions)
- Configured Kafka monitoring using Prometheus and Grafana
- Managed Kafka on GCP GKE / AWS EKS
- Cross-cloud Kafka replication using MirrorMaker2

Note: Full Kafka application development (producer/consumer code, stream processing with Kafka Streams/Flink) is typically owned by **Data Engineers**. DevOps engineers focus on cluster lifecycle, observability, and platform reliability.

---

## Quick Reference: Essential Commands

```bash
# Namespace
kubectl create namespace kafka

# Install operator
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Check operator
kubectl get pods -n kafka

# Check Kafka cluster status
kubectl get kafka -n kafka

# List topics
kubectl get kafkatopic -n kafka

# Produce messages (interactive)
kubectl -n kafka run kafka-producer -ti \
  --image=quay.io/strimzi/kafka:latest-kafka-4.2.0 --rm=true --restart=Never \
  -- bin/kafka-console-producer.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 --topic my-topic

# Consume messages
kubectl -n kafka run kafka-consumer -ti \
  --image=quay.io/strimzi/kafka:latest-kafka-4.2.0 --rm=true --restart=Never \
  -- bin/kafka-console-consumer.sh \
  --bootstrap-server my-cluster-kafka-bootstrap:9092 \
  --topic my-topic --from-beginning

# Cleanup
kubectl delete kafka my-cluster -n kafka
kubectl delete namespace kafka
```

---

## Navigation Footer

← Previous: [`52_Splunk_(Log_Analytics)_&_Docker_Compose.md`](52_Splunk_(Log_Analytics)_&_Docker_Compose.md) | Next: [`54_Kafka_on_Kubernetes_using_Strimzi_Operator.md`](54_Kafka_on_Kubernetes_using_Strimzi_Operator.md) →