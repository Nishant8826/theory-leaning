# Kubernetes ConfigMaps

## Why This Exists
You should never hardcode configuration details (like API URLs, database names, or feature flags) inside your application code or container images. Why? Because if the API URL changes, you would have to rebuild the entire Docker image, push it to Docker Hub, and redeploy.

**ConfigMaps** allow you to separate your configuration from your image content. You store your configuration keys and values in a ConfigMap object in Kubernetes, and then inject them into your Pods as environment variables or as configuration files. This makes your application portable and easy to configure across different environments (Dev, QA, Prod).

## Real World Analogy
Think of a ConfigMap like the **Settings Menu in a Video Game**.
- The game disk (Docker Image) is the same for everyone.
- However, you can change the difficulty, graphics settings, and audio volume (ConfigMap) without changing the game files on the disk.
- If you want to play on a different TV (Environment), you just adjust the settings menu, you don't buy a new game disk.

## Core Concepts
- **ConfigMap**: A dictionary of key-value pairs that store non-sensitive data.
- **Environment Variables**: Injecting ConfigMap values directly into the container's environment.
- **Volume Mount**: Mounting the ConfigMap as a physical file inside the container directory.

## Architecture / Flow

```text
[ ConfigMap ] (Key: VALUE)
       │
       ├─► Injected as Env Var ──► [ Pod / Container ] ($KEY = VALUE)
       │
       └─► Mounted as File ──────► [ Pod / Container ] (/config/app.properties)
```

## Practical Commands

```bash
# Create a configmap from literal values
kubectl create configmap my-config --from-literal=APP_COLOR=blue --from-literal=APP_MODE=prod

# Create a configmap from a file
kubectl create configmap app-config --from-file=config.properties

# View configmaps
kubectl get cm

# See the values inside a configmap
kubectl describe cm my-config
```

## Hands-On Exercise
Let's create a ConfigMap and use it as an environment variable in a Pod.

1. Create a file named `configmap.yaml`:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: app-settings
   data:
     DATABASE_URL: "jdbc:mysql://db.example.com:3306/mydb"
     LOG_LEVEL: "INFO"
   ```
2. Apply it:
   ```bash
   kubectl apply -f configmap.yaml
   ```
3. Create a Pod that uses this ConfigMap (`pod.yaml`):
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-app
   spec:
     containers:
     - name: my-app-container
       image: alpine
       command: ["sh", "-c", "echo The DB URL is $DB_URL && sleep 3600"]
       env:
       - name: DB_URL
         valueFrom:
           configMapKeyRef:
             name: app-settings
             key: DATABASE_URL
   ```
4. Apply and check logs: `kubectl logs my-app`. It should print the database URL.

## Mini Project
**Task**: Mount a ConfigMap as a file inside a container.

This is very useful for custom application configuration files (like `nginx.conf`).

1. Create a ConfigMap from a file or literal:
   ```yaml
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: special-config
   data:
     special.json: |
       {
         "theme": "dark",
         "language": "en"
       }
   ```
2. Mount it in a Pod:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: file-pod
   spec:
     containers:
     - name: file-container
       image: alpine
       command: ["sh", "-c", "cat /etc/config/special.json && sleep 3600"]
       volumeMounts:
       - name: config-volume
         mountPath: /etc/config
     volumes:
     - name: config-volume
       configMap:
         name: special-config
   ```
3. The file `special.json` will now exist at `/etc/config/special.json` inside the container!

## Real Production Usage
- **Environment Parity**: You create one `ConfigMap` named `app-config` in your Dev namespace and a different `ConfigMap` with the same name but different values in your Prod namespace. Your Deployment YAML remains exactly the same!

## Common Mistakes
- **Storing Secrets**: Putting passwords, API tokens, or private keys in a ConfigMap. ConfigMaps are **not encrypted** and anyone with cluster access can read them. **Always use Secrets for sensitive data.**
- **Assuming live updates**: If you mount a ConfigMap as environment variables, updating the ConfigMap **does not** update the env vars in the running Pod. You must restart the Pod. (If mounted as a file, it *does* update eventually, but takes time).

## Debugging Guide
- **Env var is empty**: Ensure the `key` name in `configMapKeyRef` matches the key in the ConfigMap exactly (it is case-sensitive).

## Best Practices
- **Immutable ConfigMaps**: In newer Kubernetes versions, you can set `immutable: true` to prevent accidental changes that could break your app.

## Interview Questions
1. **What is a ConfigMap used for?**
   *Answer*: It is used to store non-sensitive configuration data as key-value pairs or files, allowing you to separate configuration from image content.
2. **What happens to a Pod's environment variables if you update the referenced ConfigMap?**
   *Answer*: The environment variables in the running container will not update. You need to recreate the Pod (or trigger a rollout of the Deployment) to apply the changes.

## Summary
ConfigMaps are essential for creating flexible, environment-independent applications. By separating configuration from code, you make your deployments cleaner and safer.

---
Prev: [04_ingress.md](./04_ingress.md) | Index: [Index](../00_index.md) | Next: [06_secrets.md](./06_secrets.md)
