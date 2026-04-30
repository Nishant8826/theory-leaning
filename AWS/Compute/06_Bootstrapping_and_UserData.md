# 🛠️ Bootstrapping and UserData

## 📌 Topic Name
EC2 Bootstrapping: From Raw Image to Production Server

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: You provide a script (UserData) that runs when the instance starts for the first time.
*   **Expert**: Bootstrapping is the **Bridge between Immutable Infrastructure and Dynamic Configuration**. It leverages the `cloud-init` industry standard to execute shell scripts, cloud-config directives, or metadata lookups during the initial boot sequence. A Staff engineer uses bootstrapping to "hydrate" an instance with secrets, join a cluster, or configure environment-specific tuning.

## 🏗️ Mental Model
Think of Bootstrapping as **Setting up a New Laptop**.
- **The AMI**: The factory-installed OS (Windows/macOS).
- **The UserData**: The script you run once to install Chrome, Slack, and your dev tools.
- **IMDS**: The "Info" sticker on the bottom of the laptop that tells you the serial number and model.

## ⚡ Actual Behavior
UserData is passed as a Base64-encoded string in the `RunInstances` API call.
1.  The instance boots.
2.  The `cloud-init` service starts.
3.  `cloud-init` fetches the UserData from the Metadata Service at `http://169.254.169.254/latest/user-data`.
4.  It executes the script as the `root` user.
5.  By default, it runs **only once** on the very first boot of the instance.

## 🔬 Internal Mechanics
1.  **Cloud-init Modules**: UserData can be more than just shell scripts. It can be a `#cloud-config` YAML file that manages users, writes files, or mounts disks.
2.  **Logs**: All output from UserData is logged to `/var/log/cloud-init-output.log`. This is the first place a Staff engineer looks when an instance doesn't join the cluster.
3.  **Execution Order**: UserData runs late in the boot cycle, after networking is up but before some system services might be ready.

## 🔁 Execution Flow
1.  **Launch**: `aws ec2 run-instances --user-data file://myscript.sh`.
2.  **Provisioning**: AWS stores the script in the instance metadata.
3.  **OS Boot**: Kernel starts, systemd starts `cloud-init`.
4.  **Fetch**: `cloud-init` curls the metadata service.
5.  **Run**: Script is executed.
6.  **Completion**: Signal (optional) is sent to ASG Lifecycle Hook or CloudFormation Wait Condition.

## 🧠 Resource Behavior
- **Security**: UserData is NOT encrypted. Never put plaintext passwords or private keys in UserData. Use IAM roles and Secrets Manager instead.
- **Updates**: If you change the UserData on a *running* instance, it won't execute until you use a special `cloud-init` override.

## 📐 ASCII Diagrams
```text
[ EC2 API ] --(Base64 UserData)--> [ Instance Metadata Service ]
                                              |
[ OS Boot ] --> [ cloud-init ] --(HTTP GET)---+
                     |
            +--------V--------+
            |  RUN SCRIPT     |
            |  (Install App)  |
            |  (Apply Config) |
            +-----------------+
```

## 🔍 Code / IaC (Terraform)
```hcl
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  user_data     = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              # Pulling a secret from Secrets Manager using IAM role
              DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id prod/db --query SecretString --output text)
              echo "Database Password fetched safely"
              EOF

  iam_instance_profile = aws_iam_instance_profile.app_profile.name
}
```

## 💥 Production Failures
1.  **Script Error = Silent Death**: If a command in UserData fails (e.g., `yum install` times out), the script stops, but the instance stays "Running." Your app never starts, and health checks fail.
2.  **No Internet for Yum**: An instance in a private subnet with no NAT Gateway tries to `yum update`. The script hangs indefinitely.
3.  **Base64 Limit**: UserData has a hard limit of **16KB**. If your script is too large, it will be truncated. (Solution: Download a larger script from S3 in UserData).

## 🧪 Real-time Q&A
*   **Q**: Can I run UserData every time the instance reboots?
*   **A**: Yes, by adding `<script>` tags or using a `cloud-config` directive to change the frequency, but this is usually not recommended.
*   **Q**: How do I debug a failed UserData?
*   **A**: `tail -f /var/log/cloud-init-output.log` on the instance.

## ⚠️ Edge Cases
*   **Windows**: Uses `EC2Launch` or `EC2Config` instead of `cloud-init`. Scripts are usually PowerShell.
*   **MIME Multi-part**: You can send both a shell script and a `#cloud-config` file by using MIME multi-part formatting.

## 🏢 Best Practices
1.  **Minimalist UserData**: Only do what is absolutely necessary (e.g., install an agent and pull the rest from S3/Ansible).
2.  **Signal Success**: Use `cfn-signal` or ASG Lifecycle hooks to tell the control plane that bootstrapping finished successfully.
3.  **Use AMIs**: If bootstrapping takes more than 2-3 minutes, bake your software into a **Custom AMI** (using Packer) to speed up scaling.

## ⚖️ Trade-offs
*   **UserData (Dynamic)**: Very flexible but slow and prone to runtime errors.
*   **Custom AMI (Baking)**: Fast and reliable but requires a build pipeline for every change.

## 💼 Interview Q&A
*   **Q**: How do you pass secrets to an EC2 instance during bootstrapping?
*   **A**: I attach an IAM Role to the instance. In the UserData script, I use the AWS CLI to fetch the secret from Secrets Manager. I never put the secret itself in the UserData because it is visible to anyone with `ec2:DescribeInstanceAttribute` permissions.

## 🧩 Practice Problems
1.  Write a UserData script that mounts an EFS volume and starts a Docker container.
2.  Use a CloudFormation WaitCondition to ensure an ASG doesn't mark an instance as "InService" until the UserData finishes.

---
Prev: [05_Fargate_Deep_Dive.md](../Compute/05_Fargate_Deep_Dive.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [07_Instance_Types_and_Performance.md](../Compute/07_Instance_Types_and_Performance.md)
---
