# 🔐 KMS Internals

## 📌 Topic Name
AWS Key Management Service: The Foundation of Data Encryption

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: KMS manages the keys used to encrypt your data in S3, EBS, and RDS.
*   **Expert**: KMS is a **Secure, Multi-Tenant, FIPS 140-2 Level 3 Hardware Security Module (HSM) Service**. It uses **Envelope Encryption** to scale. Instead of sending all your data to KMS for encryption (which is slow and limited by payload size), KMS provides you with a **Data Key**. You encrypt your data with the Data Key locally, and KMS only manages the **Root Key (CMK)** that encrypts the Data Key.

## 🏗️ Mental Model
Think of KMS as a **Master Key Holder in a Vault**.
- **The CMK (Customer Master Key)**: The master key that never leaves the vault (HSM).
- **The Data Key**: A small disposable key the master key holder gives you.
- **Envelope Encryption**: You put your secret in a box, lock it with the data key, and then tape the "encrypted" data key to the top of the box. Only the master key holder can unlock that tape to give you back the data key.

## ⚡ Actual Behavior
- **Regional**: KMS keys are specific to a region (except for Multi-Region Keys).
- **Rotation**: AWS-managed keys rotate every 3 years; Customer-managed keys can rotate every 1 year.
- **Grant vs. Policy**: You can control access to keys using **Key Policies** (like bucket policies) or **Grants** (temporary, programmatic delegations).

## 🔬 Internal Mechanics
1.  **HSM Security**: KMS keys are generated and used inside FIPS-certified hardware. The plaintext of a CMK is NEVER visible to AWS employees or recorded in logs.
2.  **GenerateDataKey API**:
    - You request a data key for a specific CMK.
    - KMS returns two things: **Plaintext Data Key** and **Encrypted Data Key**.
    - You use the plaintext to encrypt your data, then immediately discard it from memory.
    - You store the encrypted data key alongside your data.
3.  **Key Hierarchy**: 
    *   **AWS Managed**: `aws/s3`, `aws/ebs`. Free to use, but limited policy control.
    *   **Customer Managed**: You have full control over the policy and rotation.

## 🔁 Execution Flow (Envelope Encryption)
1.  **Client**: `kms:GenerateDataKey(KeyId='my-cmk')`.
2.  **KMS**: Returns `{ Plaintext: 'abc', Ciphertext: 'xyz' }`.
3.  **Client**: `EncryptedData = Encrypt(Data, 'abc')`.
4.  **Storage**: Save `EncryptedData` + `xyz` (the encrypted key).
5.  **Client**: Discard `'abc'`.

## 🧠 Resource Behavior
- **Symmetric vs Asymmetric**: Symmetric (AES-256) is for data encryption. Asymmetric (RSA/ECC) is for digital signatures or small data encryption outside of AWS.
- **Encryption Context**: A set of key-value pairs used as "additional authenticated data" (AAD). If you don't provide the same context during decryption, it fails. Use this to prevent "Key Substitution" attacks.

## 📐 ASCII Diagrams
```text
[ KMS HSM ]
|  [ CMK (Root) ]  |
+---------|--------+
          |
    (GenerateDataKey)
          |
          V
[ Plaintext Key ] ----> [ APP ] <--- [ DATA ]
[ Encrypted Key ] --+      |
                    |      V
                    +--> [ ENCRYPTED DATA ]
                         [ + ENCRYPTED KEY ]
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_kms_key" "my_key" {
  description             = "KMS key for app secrets"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = { "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root" }
        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_kms_alias" "my_key_alias" {
  name          = "alias/app-key"
  target_key_id = aws_kms_key.my_key.key_id
}
```

## 💥 Production Failures
1.  **Key Deletion**: You delete a KMS key. All data encrypted with that key (EBS volumes, S3 objects, RDS snapshots) becomes PERMANENTLY unreadable. There is no "undelete" after the 7-30 day waiting period.
2.  **KMS Throttling**: Every `Decrypt` or `GenerateDataKey` call is an API request. If you have a high-traffic app decrypting a key for every request, you will hit KMS RPS limits. **Solution**: Use **Data Key Caching**.
3.  **Key Policy Lockout**: You update a key policy and remove your own ability to manage it. You must use the Root user or contact AWS Support.

## 🧪 Real-time Q&A
*   **Q**: Does KMS store my data?
*   **A**: No. It only stores the keys.
*   **Q**: Is KMS expensive?
*   **A**: $1 per key per month + $0.03 per 10,000 requests. It can become expensive if mismanaged.

## ⚠️ Edge Cases
*   **Multi-Region Keys**: Allow you to replicate a key's metadata and key material to another region. Useful for Global DynamoDB tables or cross-region DR.
*   **Imported Key Material**: You generate the key on-prem and upload it to KMS. You are responsible for the durability of that key material.

## 🏢 Best Practices
1.  **Use Aliases**: Refer to keys by alias (`alias/my-app`) so you can swap the underlying key without updating code.
2.  **Enable Rotation**: Always enable automatic annual rotation.
3.  **Encryption Context**: Always use an encryption context (e.g., `AppName: MyService`) for extra security.

## ⚖️ Trade-offs
*   **AWS Managed**: Easy, free, but you can't control who uses them via key policies.
*   **Customer Managed**: Full control, granular auditing, but costs $1/month.

## 💼 Interview Q&A
*   **Q**: Why do we use "Envelope Encryption" instead of just sending data to KMS?
*   **A**: 1. **Performance**: Encrypting data locally is much faster than a network round-trip. 2. **Payload Size**: KMS API limits requests to 4KB. You can't send a 1GB file to KMS. 3. **Scale**: It allows us to manage one root key while encrypting billions of individual objects.

## 🧩 Practice Problems
1.  Encrypt a string using the AWS CLI and then decrypt it.
2.  Create a KMS key that can only be used by a specific IAM Role for `kms:Decrypt` if the request comes from a specific VPC.
