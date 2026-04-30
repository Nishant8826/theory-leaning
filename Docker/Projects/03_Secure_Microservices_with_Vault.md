# 📌 Project: Secure Microservices with HashiCorp Vault

## 🏗️ Project Overview
Hardcoding passwords or even using `.env` files is a major security risk. In this project, we implement a **Zero-Trust Secret Management** system. Our Node.js microservices will have **No Secrets** in their code or environment variables. Instead, they will authenticate with **HashiCorp Vault** using their Docker identity and fetch temporary, short-lived credentials at runtime.

## 📐 Architecture Diagram

```text
       [ CLUSTER ]
            |
    +-------+-------+
    |               |
[ API 1 ]       [ API 2 ]
    |               |
    +--( Auth )-----+
            |
    [ VAULT SERVER ] <---( Sealed Storage )
    ( Transit Engine )
```

## 🛠️ Step 1: Configuring Vault
We use the **AppRole** authentication method, designed for automated machine-to-machine security.
```bash
# 1. Enable AppRole auth
vault auth enable approle

# 2. Create a policy for the API
vault policy write api-policy - <<EOF
path "secret/data/db-creds" {
  capabilities = ["read"]
}
EOF

# 3. Create the Role
vault write auth/approle/role/my-api \
    secret_id_ttl=10m \
    token_num_uses=10 \
    token_ttl=20m \
    policies="api-policy"
```

## ⛓️ Step 2: The Secure API (Node.js)
The app uses the Vault SDK to log in and fetch the DB password.
```javascript
const vault = require("node-vault")({ endpoint: "http://vault:8200" });

async function getSecrets() {
  // Login using RoleID and SecretID (provided via Docker Secrets or Env)
  const result = await vault.approleLogin({
    role_id: process.env.ROLE_ID,
    secret_id: process.env.SECRET_ID
  });
  
  vault.token = result.auth.client_token;
  
  // Fetch the actual secrets
  const { data } = await vault.read("secret/data/db-creds");
  return data.data; // { password: "..." }
}

getSecrets().then(creds => {
  // Connect to DB only after getting the secret
  connectToDB(creds.password);
});
```

## 🔬 Internal Mechanics (The Dynamic Secret)
1. **Request**: API starts up and asks Vault for a token.
2. **Identity**: Vault verifies that the API is who it says it is (via AppRole).
3. **Lease**: Vault issues a token that expires in 20 minutes.
4. **Retrieval**: API uses the token to get the DB password.
5. **Renewal**: API must "Renew" its token periodically. If the API is hacked and killed, the token dies with it, and the "Blast Radius" is limited to 20 minutes.

## 💥 Production Failures & Fixes
- **Failure**: Vault is "Sealed" (locked) after a restart. The API cannot fetch secrets and crashes.
  *Fix*: Use **Auto-Unseal** with AWS KMS or Google Cloud KMS so Vault can unlock itself securely.
- **Failure**: SecretID leak. Someone finds the `SECRET_ID` in the logs.
  *Fix*: Use Vault's **Response Wrapping**. The SecretID is sent as a one-time-use token. If anyone else tries to use it, the original API will fail, alerting you to the breach.

## 💼 Interview Q&A
**Q: Why is using a Secret Manager like Vault better than using Docker Secrets or Environment Variables?**
**A**: Environment variables are easily leaked through logs, `/proc` filesystem, or CI/CD dashboards. Docker Secrets are better but they are "Static"—once set, they rarely change. **Vault** provides **Dynamic Secrets**. It can generate a *new* database user and password for every container instance and delete them when the container stops. This ensures that even if a database password is leaked, it is only valid for one specific container for a very short period, providing the highest level of security.

## 🧪 Lab Exercise
1. Run a local Vault container in `-dev` mode.
2. Create a secret using the `vault kv put` command.
3. Write a small script to fetch that secret using the Vault API.
4. "Revoke" the token manually in Vault and observe how the script fails on its next request.

---
Prev: [02_RealTime_SocketIO_Cluster.md](./02_RealTime_SocketIO_Cluster.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_CI_CD_with_Jenkins_and_ECR.md](./04_CI_CD_with_Jenkins_and_ECR.md)
---
