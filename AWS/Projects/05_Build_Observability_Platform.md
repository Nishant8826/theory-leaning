# 🛠️ Project: Build an Observability Platform

## 📌 Topic Name
Project: Centralized Logging and Metrics with CloudWatch, Kinesis, and OpenSearch

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Send all your logs to one place so you can search them easily.
*   **Expert**: This project implements a **Distributed Observability Pipeline**. It goes beyond simple log storage by creating a real-time stream of telemetry data. It uses **Kinesis Data Firehose** to ingest logs from multiple accounts, **Lambda** for real-time transformation and enrichment, and **Amazon OpenSearch Service** (formerly Elasticsearch) for sub-second searching and visualization. The goal is to provide **Actionable Insights** across a massive fleet of services.

## 🏗️ Architecture Overview
- **Sources**: **CloudWatch Logs** from EC2, Lambda, and Containers.
- **Ingestion**: **Kinesis Data Firehose** subscribed to CloudWatch Log groups.
- **Transformation**: **Lambda** (Firehose Transformation) to parse JSON, anonymize PII, and add Geo-IP data.
- **Storage/Search**: **Amazon OpenSearch Service** for indexing and querying.
- **Visualization**: **OpenSearch Dashboards** (Kibana) for real-time dashboards.
- **Alerting**: **CloudWatch Metric Filters** to trigger SNS notifications on error spikes.

## 📐 Architecture Diagram
```text
[ SERVICES ] ----> [ CLOUDWATCH LOGS ]
                          |
                  [ KINESIS FIREHOSE ]
                          |
                  [ LAMBDA (Enrich) ]
                          |
                  [ OPENSEARCH SERVICE ] <---- [ DASHBOARDS ]
                          |
                  [ S3 (Archive/Backup) ]
```

## 🔍 Implementation Steps (Terraform)
1.  **Search**: Deploy an Amazon OpenSearch domain with a dedicated master node.
2.  **Stream**: Create a Kinesis Data Firehose delivery stream with the OpenSearch domain as the destination.
3.  **Transformation**: Create a Lambda function that receives Firehose records and returns them in a format OpenSearch understands.
4.  **Integration**: Create a CloudWatch Logs "Subscription Filter" that sends log events to the Firehose stream.
5.  **Security**: Set up IAM roles and OpenSearch access policies to allow Firehose to write data.

## 🔍 Code Snippet (Lambda Transformation Logic)
```javascript
exports.handler = async (event) => {
    const output = event.records.map((record) => {
        // Decode the incoming data
        const payload = Buffer.from(record.data, 'base64').toString('utf8');
        const logData = JSON.parse(payload);

        // Enrich the log (e.g., add environment tag)
        logData.environment = "production";
        logData.timestamp = new Date().toISOString();

        // Re-encode for Firehose
        return {
            recordId: record.recordId,
            result: 'Ok',
            data: Buffer.from(JSON.stringify(logData)).toString('base64'),
        };
    });
    return { records: output };
};
```

## 💥 Production Considerations
1.  **Index Management**: Use **Index State Management (ISM)** in OpenSearch to automatically delete or move old logs to "Cold" storage (S3) after 7 days to save costs.
2.  **Backpressure**: Firehose automatically buffers data and retries. If OpenSearch is overwhelmed, Firehose will back up the data to S3.
3.  **Cost**: OpenSearch is expensive. For many workloads, **CloudWatch Logs Insights** or **Athena on S3** might be a more cost-effective alternative for searching logs.

## 💼 Interview Walkthrough
- **Q**: Why use OpenSearch instead of just searching CloudWatch Logs?
- **A**: **Speed and Complexity**. CloudWatch Logs Insights is great for ad-hoc queries, but **OpenSearch** allows for full-text search, complex aggregations, and real-time visualization in Kibana. It also allows us to correlate logs from multiple different accounts and regions in a single dashboard, which is essential for a large-scale microservice architecture.

## 🧩 Practice Problems
1.  Set up an OpenSearch dashboard that shows the "Top 5 Error Messages" across your entire environment.
2.  Implement "Log Sampling" in your Firehose Lambda to only send 10% of "Debug" logs to OpenSearch while keeping 100% of "Error" logs.

---
Prev: [04_Multi_Region_DR_Setup.md](../Projects/04_Multi_Region_DR_Setup.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: None
---
