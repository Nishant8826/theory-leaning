# 🛡️ Chaos Engineering on AWS

## 📌 Topic Name
Chaos Engineering: Resilience Testing with AWS FIS and Game Days

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Purposefully break things to see if your system can handle it.
*   **Expert**: Chaos Engineering is the **Discipline of Experimenting on a System** to build confidence in its capability to withstand turbulent conditions in production. It involves injecting controlled failures (e.g., killing an EC2 instance, spiking CPU, introducing network latency) and observing if the system's "Steady State" remains stable. A Staff engineer uses **AWS Fault Injection Simulator (FIS)** to automate these experiments and validates that HA and DR mechanisms actually work.

## 🏗️ Mental Model
Think of Chaos Engineering as a **Fire Drill**.
- **The Building**: Your AWS environment.
- **The Fire Drill**: A planned event where you pull the alarm and see if everyone knows the exits and if the sprinklers work.
- **The Goal**: Not to cause a fire, but to ensure that if a REAL fire happens, the damage is minimized and people are safe.

## ⚡ Actual Behavior
- **Controlled Experiments**: You define exactly what to break, for how long, and in which environment.
- **Stop Conditions**: If the system's health drops below a certain threshold (e.g., Error rate > 5%), FIS automatically stops the experiment and rolls back the changes.
- **Steady State**: The baseline metric you monitor (e.g., "99.9% success rate on Login").

## 🔬 Internal Mechanics
1.  **AWS Fault Injection Simulator (FIS)**: A managed service that allows you to run "Experiments." It uses IAM roles to perform actions (like `StopInstances`) on your behalf.
2.  **Fault Types**:
    - **Resource-based**: Stop instances, reboot DBs, terminate nodes.
    - **Network-based**: Inject latency, packet loss, or block traffic to a specific AZ.
    - **State-based**: Stress CPU or Memory on an instance.
3.  **Experiment Template**: Defines the **Actions** (what to do) and the **Targets** (on which resources).

## 🔁 Execution Flow (A Chaos Experiment)
1.  **Hypothesis**: "If one EC2 instance in the ASG is terminated, the ELB will detect it and the user won't notice."
2.  **Define Steady State**: Monitor the "Target Group 2xx Count" and "ALB Latency."
3.  **Run Experiment**: FIS terminates one random EC2 instance in the ASG.
4.  **Observe**: ASG launches a replacement. ELB health check removes the dead node.
5.  **Verify**: Did the 2xx count drop? No. Did latency spike? No.
6.  **Conclusion**: Hypothesis confirmed. Resilience verified.

## 🧠 Resource Behavior
- **SSM Agent**: For some "In-guest" faults (like CPU stress or disk full), FIS uses the Systems Manager (SSM) agent to run scripts inside the EC2 instance.
- **Guardrails**: You can define "Safety Levers" in CloudWatch. If a high-priority alarm fires, the chaos experiment is immediately aborted.

## 📐 ASCII Diagrams
```text
[ STEADY STATE ] ----(Normal Traffic)----> [ SYSTEM OK ]
      |
[ CHAOS EXPERIMENT ] --(Inject Fault: Kill DB)--> [ SYSTEM ]
      |                                              |
[ MONITORING ] <-------(Automatic Failover?)---------+
      |
[ HYPOTHESIS VALIDATED? ]
```

## 🔍 Code / IaC (FIS Experiment Template)
```hcl
resource "aws_fis_experiment_template" "stop_instances" {
  description = "Stop 10% of instances in the web ASG"
  role_arn    = aws_iam_role.fis_role.arn

  stop_condition {
    source = "none" # In prod, this would be a CloudWatch Alarm
  }

  action {
    action_id = "aws:ec2:stop-instances"
    name      = "stop-web-instances"
    parameter {
      key   = "startInstancesAfterDuration"
      value = "PT5M" # Restart after 5 mins
    }
    target {
      key   = "Instances"
      value = "web-tier-target"
    }
  }

  target {
    name           = "web-tier-target"
    resource_type  = "aws:ec2:instance"
    selection_mode = "PERCENT(10)"
    resource_tag {
      key   = "Role"
      value = "Web"
    }
  }
}
```

## 💥 Production Failures
1.  **Chaos in Production (Uncontrolled)**: Running an experiment without proper "Stop Conditions." A small test escalates into a total site outage because the system wasn't as resilient as you thought.
2.  **Testing the Wrong Thing**: Spiking CPU on a server that isn't CPU-bound. You learn nothing about the system's actual failure modes.
3.  **Ignoring the Results**: Finding a bug during a "Game Day" but never putting it in the backlog to be fixed. The same bug then causes a real outage 3 months later.

## 🧪 Real-time Q&A
*   **Q**: Is Chaos Engineering only for Netflix-scale companies?
*   **A**: No. Even a small startup can benefit from knowing "What happens if our single database reboots?".
*   **Q**: Should I run chaos experiments in production?
*   **A**: Start in **Staging**. Once you have confidence and robust monitoring/automated rollbacks, you can move to Production (the only place where you find "real" chaos).

## ⚠️ Edge Cases
*   **Cascading Failures**: An experiment in Service A causes an unexpected failure in Service B, which then takes down the Shared Database. This reveals a "Hidden Dependency."
*   **Blast Radius**: Ensuring the experiment targets are isolated (e.g., using specific tags) so you don't accidentally reboot the CEO's demo server.

## 🏢 Best Practices
1.  **Define a Steady State** before you start.
2.  **Start Small**: Terminate one instance before you terminate an AZ.
3.  **Always have a Stop Condition** (CloudWatch Alarm).
4.  **Communicate**: Tell the whole team (and leadership) when a chaos experiment is running so they don't panic when they see alarms.

## ⚖️ Trade-offs
*   **Chaos Engineering**: Massive increase in confidence and system knowledge, but requires significant time and carries a risk of accidental downtime.

## 💼 Interview Q&A
*   **Q**: What is a "Game Day"?
*   **A**: A Game Day is a scheduled event where the engineering team simulates a failure (e.g., a regional outage or a database corruption) and practices their response. It’s not just about testing the *system*, it’s about testing the *people* and the *processes* (e.g., "Do we know where the logs are? Is the on-call rotation working?").

## 🧩 Practice Problems
1.  Use AWS FIS to simulate a 500ms network latency to a specific RDS instance and observe the application's response.
2.  Design a "Game Day" scenario for a team that manages a serverless API.
