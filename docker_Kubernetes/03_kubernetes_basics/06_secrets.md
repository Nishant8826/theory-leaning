# Kubernetes Secrets

## Why This Exists
While **ConfigMaps** are great for storing general configuration details (like API URLs), you should **never** use them to store sensitive data like passwords, API keys, database credentials, or SSL certificates.

**Secrets** are specifically designed to hold sensitive information. They are similar to ConfigMaps but are handled with extra care by Kubernetes:
1.  They are usually stored in a different way in the cluster's database (`etcd`).
2.  They are only sent to nodes that have Pods that actually need them.
3.  They are stored in memory on the nodes, not on the disk.

## Real World Analogy
Think of a Secret like a **Hotel Room Safe**.
- The room layout, TV channels, and AC temperature are like **ConfigMaps** (everyone can see them).
- But your passport, jewelry, and cash go into the **Safe** (Secret). Only you and the manager with the key can access it.

## Core Concepts
- **Secret**: An object that contains a small amount of sensitive data such as a password, a token, or a key.
- **Base64 Encoding**: Secrets are stored in a Base64 encoded format. **Warning**: Base64 is **not** encryption. It just makes the data hard to read at a glance. It can be easily decoded!
- **Types of Secrets**:
    - `Opaque`: Arbitrary user-defined data (most common).
    - `kubernetes.io/tls`: For SSL/TLS certificates.
    - `kubernetes.io/dockerconfigjson`: For Docker registry credentials.

## Architecture / Flow

```text
[ Secret ] (Base64 Encoded)
       │
       ├─► Decoded & Injected as Env Var ──► [ Pod / Container ] ($PASS = secret)
       │
       └─► Decoded & Mounted as File ──────► [ Pod / Container ] (/var/run/secrets/pass)
```

## Practical Commands

```bash
# Create an opaque secret from literal values
kubectl create secret generic my-db-pass --from-literal=password=supersecret

# View secrets
kubectl get secrets

# See details (values will be hidden/masked)
kubectl describe secret my-db-pass

# To see the actual value, you must decode it
kubectl get secret my-db-pass -o jsonpath="{.data.password}" | base64 --decode
```

## Hands-On Exercise
Let's create a Secret and use it as an environment variable.

1. Create a file named `secret.yaml`. Notice that the values **must** be Base64 encoded!
   *   To encode string `admin` in Linux/Mac: `echo -n "admin" | base64` -> `YWRtaW4=`
   *   To encode string `secret123`: `echo -n "secret123" | base64` -> `c2VjcmV0MTIz`

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: db-credentials
   type: Opaque
   data:
     username: YWRtaW4=        # "admin" encoded
     password: c2VjcmV0MTIz    # "secret123" encoded
   ```
2. Apply it:
   ```bash
   kubectl apply -f secret.yaml
   ```
3. Use it in a Pod:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: secure-app
   spec:
     containers:
     - name: app-container
       image: alpine
       command: ["sh", "-c", "echo The password is $DB_PASS && sleep 3600"]
       env:
       - name: DB_PASS
         valueFrom:
           secretKeyRef:
             name: db-credentials
             key: password
   ```

## Mini Project
**Task**: Use a Secret to authenticate with a database.

1. Create a Secret for a MySQL password.
2. Run a MySQL Pod and use that Secret to set the `MYSQL_ROOT_PASSWORD` environment variable.

## Real Production Usage
- **External Secret Managers**: In real production, companies rarely write base64 strings in YAML files because anyone who sees the file can steal the password. Instead, they use tools like **HashiCorp Vault**, **AWS Secrets Manager**, or **Sealed Secrets** which encrypt the data and inject it automatically.

## Common Mistakes
- **Treating Base64 as Encryption**: Thinking that because the password looks like `YWRtaW4=`, it is safe. Anyone can decode it instantly.
- **Committing Secrets to Git**: Pushing `secret.yaml` files with real passwords to public GitHub repositories. **Never do this.**

## Debugging Guide
- **Container fails with Env Var missing**: Ensure the key in `secretKeyRef` matches the key in the Secret file exactly.

## Best Practices
- **Restrict Access**: Use Kubernetes RBAC (Role-Based Access Control) to prevent regular users from viewing Secrets.
- **Encrypt at Rest**: Enable encryption for `etcd` in your cluster so that secrets are encrypted when stored in the database.

## Interview Questions
1. **Is a Kubernetes Secret encrypted by default?**
   *Answer*: No. By default, it is only Base64 encoded. To make it secure at rest, you must enable `etcd` encryption in the cluster configuration.
2. **How do you use a Secret in a Pod?**
   *Answer*: You can either inject specific keys as environment variables using `valueFrom.secretKeyRef` or mount the whole secret as a volume so files appear inside the container.

## Summary
Secrets are vital for securing your application's sensitive data. While they are not fully secure out of the box (due to Base64), they provide the necessary structure to implement high-level security patterns in production.

---
Prev: [05_configmaps.md](./05_configmaps.md) | Index: [Index](../00_index.md) | Next: [07_volumes.md](./07_volumes.md)
