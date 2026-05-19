# Helm

## Why This Exists
Writing Kubernetes YAML files by hand is extremely repetitive. If you want to deploy your app to Dev, Staging, and Production, you often have to copy-paste the same YAML files and manually change the image tags or replica counts. Helm is a "Package Manager" for Kubernetes (like `apt` or `npm`) that templates these files so you can reuse them easily.

## Real World Analogy
Think of buying furniture. Writing raw Kubernetes YAML is like buying **raw wood and a box of screws**—you have to measure and cut everything yourself.
Using Helm is like buying from **IKEA**. You get a pre-packaged box (a Chart) with instructions. You just fill out a quick form (the `values.yaml` file) choosing the color and size, and Helm builds the furniture for you.

## Core Concepts
*   **Chart:** A bundle of templated Kubernetes YAML files (the IKEA box).
*   **Values.yaml:** A file where you define your custom settings, like `replicaCount: 3` or `image: myapp:v2`.
*   **Release:** A specific instance of a chart running in your cluster. (You can install the same chart 5 times to get 5 releases).
*   **Repository:** An online server where people share their Helm charts (like Docker Hub, but for Helm).

## Architecture / Flow
1. Developer runs `helm install my-database bitnami/mysql`.
2. Helm downloads the `mysql` Chart from the Bitnami repository.
3. Helm reads your custom `values.yaml` file.
4. Helm injects your values into the blank spaces of the templates.
5. Helm generates the final, raw Kubernetes YAML and sends it to the K8s API.

## Practical Commands
*   `helm search repo nginx` - Search for an existing package.
*   `helm install my-release <chart-name>` - Install a chart.
*   `helm upgrade my-release <chart-name> -f values.yaml` - Apply changes.
*   `helm list` - See all installed apps.
*   `helm rollback my-release 1` - Instantly go back to a previous version if an upgrade breaks!

## Hands-On Exercise
Install the official Nginx chart using Helm. Then, upgrade it by passing a `--set replicaCount=3` flag in your command to scale it up, without ever touching a YAML file.

## Mini Project
**"My First Chart"**
Run `helm create my-webapp`. Look at the folder structure it generates. Delete all the boiler-plate code and replace it with a simple Deployment and Service. Replace hardcoded values with `{{ .Values.replicaCount }}`. Deploy it to your cluster.

## Real Production Usage
Almost every popular open-source tool (Prometheus, Grafana, Redis, MongoDB) is installed in production using Helm. Furthermore, companies build their own internal Helm charts to standardize how their developers deploy microservices.

## Common Mistakes
*   **Editing the Templates instead of Values:** If you find yourself hardcoding a specific environment name directly into the `deployment.yaml` template of your Helm chart, you are using Helm wrong. That should be a variable in `values.yaml`.

## Debugging Guide
*   **Syntax Error in Template?** Use `helm template my-release ./my-chart --debug`. This command will process the templates and print the generated YAML to your screen *without* sending it to Kubernetes. It's the best way to spot indentation errors.

## Best Practices
*   **Version Everything:** Both your Docker Image and your Helm Chart should have version numbers. 
*   **Keep it Simple:** Don't overuse complex `if/else` logic in your templates. If a chart becomes too complicated to read, it's too complicated to maintain.

## Interview Questions
*   **Q: What is the difference between a Helm Chart and a Helm Release?**
    *   *A: A Chart is the blueprint (the package of code). A Release is the actual running instance of that chart deployed in a Kubernetes cluster.*
*   **Q: How do you manage different environments (Dev vs Prod) with Helm?**
    *   *A: You use one single Chart, but you maintain separate value files: `values-dev.yaml` and `values-prod.yaml`.*

## Summary
Helm bridges the gap between writing infrastructure code and actually managing it. It allows teams to share, version, and deploy complex Kubernetes applications with a single command.

---
Prev: [Index](../00_index.md) | Index: [Index](../00_index.md) | Next: [02_statefulsets.md](./02_statefulsets.md)
