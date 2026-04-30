# 🛠️ Project: Data Processing Pipeline

## 📌 Topic Name
Project: Event-Driven ETL: S3, Lambda, SQS, and Glue

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: When a file is uploaded to S3, automatically clean it and save it to a database.
*   **Expert**: This project implements a **Serverless Data Lake Pipeline**. It uses **S3 Event Notifications** to trigger a decoupled processing chain. It handles **Backpressure** using **SQS**, data transformation using **AWS Glue**, and final storage in a queryable format (**Parquet/Athena**). The goal is to build a system that can process millions of files without managing any servers.

## 🏗️ Architecture Overview
- **Ingestion**: **S3 Bucket** receives raw CSV files.
- **Trigger**: S3 triggers an **SQS Queue** (to decouple and ensure no files are missed).
- **Processing**: **Lambda** polls SQS, reads the CSV, validates it, and writes it to a "Clean" S3 bucket.
- **Cataloging**: **AWS Glue Crawler** scans the clean bucket and creates a table in the **Glue Data Catalog**.
- **Analysis**: **Amazon Athena** is used to query the data using standard SQL.

## 📐 Architecture Diagram
```text
[ RAW S3 ] --(Event)--> [ SQS ]
                            |
                     [ LAMBDA (Worker) ]
                            |
[ ATHENA ] <--- [ GLUE CATALOG ] <--- [ CLEAN S3 ]
```

## 🔍 Implementation Steps (Terraform)
1.  **Storage**: Create `raw-data-bucket` and `clean-data-bucket`.
2.  **Messaging**: Create an SQS queue with a policy that allows S3 to `SendMessage`.
3.  **Compute**: Create a Lambda function with permissions to read from S3/SQS and write to S3.
4.  **ETL**: Create an AWS Glue Crawler pointing to the `clean-data-bucket`.
5.  **Analytics**: Configure Athena to use the Glue Catalog.

## 🔍 Code Snippet (Glue Crawler Definition)
```hcl
resource "aws_glue_crawler" "clean_data" {
  database_name = aws_glue_catalog_database.main.name
  name          = "clean-data-crawler"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.clean.bucket}/data/"
  }
}
```

## 💥 Production Considerations
1.  **Batching**: Configure the SQS-Lambda trigger to process 10 messages at a time (batching) to save costs and improve throughput.
2.  **Concurrency**: If 10,000 files are uploaded at once, Lambda will try to scale to 1,000 instances. Use **Reserved Concurrency** to prevent the pipeline from overwhelming downstream resources.
3.  **Partitioning**: Ensure the "Clean S3" bucket stores data in a partitioned format (e.g., `s3://clean/year=2023/month=01/...`) to make Athena queries faster and cheaper.

## 💼 Interview Walkthrough
- **Q**: Why use SQS between S3 and Lambda? Why not trigger Lambda directly?
- **A**: **Reliability and Throttling**. If I trigger Lambda directly and the Lambda service is throttled or down, the event is lost. By using **SQS**, the message stays in the queue for up to 14 days until a Lambda is available to process it. It also allows me to control the "Rate" of processing by setting the `MaximumConcurrency` on the SQS trigger.

## 🧩 Practice Problems
1.  Add an **SNS Topic** at the end of the pipeline to notify an administrator if a file fails to process after 3 retries.
2.  Convert the CSV data to **Parquet** format in the Lambda function and compare the Athena query cost.

---
Prev: [02_Highly_Available_SQL_Cluster.md](../Projects/02_Highly_Available_SQL_Cluster.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [04_Multi_Region_DR_Setup.md](../Projects/04_Multi_Region_DR_Setup.md)
---
