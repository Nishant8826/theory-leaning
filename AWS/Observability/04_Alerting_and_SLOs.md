# 📊 Alerting and SLOs

## 📌 Topic Name
Actionable Observability: Alarms, Service Level Objectives (SLOs), and Error Budgets

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: Send a Slack message when CPU is above 90%.
*   **Expert**: Alerting is the **Quantification of User Pain**. Instead of alerting on "Technical Debt" (High CPU, Low Memory), a Staff engineer alerts on **Symptoms** (High Latency, High Error Rate). This is managed through **Service Level Indicators (SLIs)** and **Service Level Objectives (SLOs)**. The "Error Budget" determines how much unreliability the business can tolerate before engineers must stop feature work and focus on stability.

## 🏗️ Mental Model
Think of Alerting as a **Cockpit in an Airplane**.
- **SLI (Indicator)**: The Altimeter (Current height).
- **SLO (Objective)**: The goal to stay above 10,000 feet 99.9% of the time.
- **Error Budget**: How many feet we can drop during turbulence before the pilot gets in trouble.
- **Alert**: The loud "PULL UP" siren when the altimeter shows we are at 500 feet and falling fast.

## ⚡ Actual Behavior
- **SLI**: A metric like "Availability" or "Latency."
- **SLO**: A target for that SLI (e.g., "99.9% of requests must return 2xx in < 200ms").
- **Error Budget**: 100% - SLO. For 99.9%, the error budget is 0.1% (about 43 minutes per month).

## 🔬 Internal Mechanics
1.  **Threshold-based Alarms**: The simplest form. "If X > Y, Fire."
2.  **Anomaly Detection**: CloudWatch uses machine learning to learn the "normal" pattern of a metric (e.g., traffic is higher on Mondays) and only alerts if the metric goes outside the predicted band.
3.  **Composite Alarms**: Combining multiple conditions (e.g., "Latency is high AND throughput is high").
4.  **Suppression**: Preventing downstream alarms from firing if a root-cause alarm (like "Database Down") is already active.

## 🔁 Execution Flow (The Alert Path)
1.  **Metric**: Application reports `Latency: 250ms`.
2.  **SLI Calculation**: CloudWatch calculates the `p90` latency over 5 minutes.
3.  **SLO Check**: Is `p90 < 200ms`? No.
4.  **Error Budget Consumption**: The budget begins to burn.
5.  **Burn Rate Alert**: A specialized alarm fires if the budget is burning so fast that it will be gone in < 24 hours.
6.  **Notification**: SNS sends a message to PagerDuty/OpsGenie.
7.  **Incident Response**: Engineer investigates.

## 🧠 Resource Behavior
- **Evaluation Periods**: How many times the condition must be met before firing. "3 out of 5 periods" helps ignore transient spikes.
- **Missing Data Treatment**: You can choose to treat missing data as `breaching`, `notBreaching`, `ignore`, or `missing`. For security alarms, always use `breaching`.

## 📐 ASCII Diagrams
```text
[ METRIC ] --(SLI)--> [ SLO TARGET ]
                          |
            +-------------+-------------+
            |                           |
    [ ERROR BUDGET ]            [ BURN RATE ALARM ]
    (The "Gas Tank")            (The "Warning Light")
            |                           |
    [ BUDGET EXHAUSTED ] ----> [ STOP FEATURE WORK ]
```

## 🔍 Code / IaC (Anomaly Detection Alarm)
```hcl
resource "aws_cloudwatch_metric_alarm" "anomaly_alarm" {
  alarm_name          = "latency-anomaly-detection"
  comparison_operator = "GreaterThanUpperThreshold"
  evaluation_periods  = "2"
  threshold_metric_id = "ad1"
  
  # The actual metric we are monitoring
  metric_query {
    id = "m1"
    metric {
      metric_name = "Duration"
      namespace   = "AWS/Lambda"
      period      = "60"
      stat        = "Average"
      unit        = "Milliseconds"
    }
  }

  # The anomaly detection model
  metric_query {
    id          = "ad1"
    expression  = "ANOMALY_DETECTION_BAND(m1, 2)" # 2 standard deviations
    label       = "Latency (Expected)"
    return_data = true
  }
}
```

## 💥 Production Failures
1.  **The "Alert Storm"**: A core router fails, triggering 500 separate alarms for every single microservice. The on-call engineer receives 500 pages and can't find the root cause. **Solution**: Use **Composite Alarms**.
2.  **Alerting on the Wrong Metric**: Alerting on "High CPU" for a cluster that is designed to run at 100% CPU (e.g., Video Transcoding). The alarm is constantly on, leading to "Alarm Fatigue."
3.  **Ignoring the Error Budget**: Continuing to deploy new features even though the budget for the month is gone. A major outage occurs because stability was ignored.

## 🧪 Real-time Q&A
*   **Q**: What is the "Golden Signals" of SRE?
*   **A**: 1. Latency. 2. Traffic. 3. Errors. 4. Saturation.
*   **Q**: When should I use Anomaly Detection?
*   **A**: For metrics that have a strong cyclical pattern (like daily traffic) where a fixed threshold would be too high at night and too low during the day.

## ⚠️ Edge Cases
*   **Heartbeat Alarms**: An alarm that fires if a metric *stops* being reported (indicating the agent or service has crashed).
*   **Suppression**: Using CloudWatch Alarm Suppression to silence alerts during a scheduled maintenance window.

## 🏢 Best Practices
1.  **Alert on Symptoms, not Causes**: Users care about "Site is slow," not "Instance i-123 has high CPU."
2.  **Every Alert must be Actionable**: If an engineer gets a page and says "I can't do anything about this," the alert should be removed or changed.
3.  **Use P99 for Latency**: Never alert on "Average" latency; it hides the pain of your unluckiest users.

## ⚖️ Trade-offs
*   **Low Threshold**: Fast detection of issues, but high risk of false positives (noise).
*   **High Threshold**: Zero noise, but users will suffer for longer before you are notified.

## 💼 Interview Q&A
*   **Q**: How do you decide what to alert on for a new microservice?
*   **A**: I start with the **Golden Signals**: 1. **Errors** (5xx rate). 2. **Latency** (p99 response time). 3. **Traffic** (RPS). I would then define **SLOs** based on business requirements (e.g., "99.9% of orders must be processed in < 1 second"). I would only alert the on-call engineer if the **Error Budget** is burning fast enough to threaten that SLO.

## 🧩 Practice Problems
1.  Define an SLO for a "Checkout" service and create the corresponding CloudWatch Alarms.
2.  Configure a "Composite Alarm" that only fires if both an ALB 5xx alarm and a Lambda error alarm are active.

---
Prev: [03_Logging_Strategies.md](../Observability/03_Logging_Strategies.md) | Index: [Docker/00_Index.md](../00_Index.md) | Next: [01_CI_CD_Pipelines.md](../DevOps/01_CI_CD_Pipelines.md)
---
