# 📈 Predictive Scaling

## 📌 Topic Name
Machine Learning Driven Elasticity: AWS Predictive Scaling

## 🧠 Concept Explanation (Basic → Expert)
*   **Basic**: ASG looks at the past 14 days of traffic and "guesses" how many servers you'll need tomorrow.
*   **Expert**: Predictive Scaling uses **Machine Learning (ML)** to analyze historical load patterns and proactively provision EC2 capacity before it's needed. It solves the "Warm-up Time" problem where standard scaling (reactive) is too slow to handle sharp, predictable spikes (like a daily 9 AM login surge). It creates a "Forecast" and schedules scaling actions to match the expected load.

## 🏗️ Mental Model
Think of Predictive Scaling as a **Weather Forecast for Traffic**.
- **Standard Scaling**: You see it start raining, so you go outside to open your umbrella (takes time, you get wet).
- **Predictive Scaling**: The forecast says "100% chance of rain at 2 PM," so you open your umbrella at 1:55 PM (you stay dry).

## ⚡ Actual Behavior
- **Minimum Data**: Needs at least 24 hours of data to start, but works best with 14 days.
- **Forecast only vs. Forecast and Scale**: You can run it in "Forecast Only" mode to see how well it predicts your traffic before trusting it with your servers.
- **Buffer**: You can add a "Capacity Buffer" (e.g., 10%) on top of the prediction for extra safety.

## 🔬 Internal Mechanics
1.  **Data Ingestion**: CloudWatch sends historical metrics (CPU or Request Count) to the Predictive Scaling engine.
2.  **Pattern Recognition**: The engine identifies daily and weekly seasonality.
3.  **Scaling Plan**: The engine generates a 48-hour forecast and creates a schedule.
4.  **Scheduled Action**: 15-30 minutes before a predicted spike, the ASG begins launching instances so they are `InService` exactly when the spike hits.

## 🔁 Execution Flow (Predictive Cycle)
1.  **Analyze**: ML model scans the last 14 days of `RequestCount`.
2.  **Predict**: Predicts 50,000 requests/sec at 9:00 AM tomorrow.
3.  **Plan**: Calculates that 20 instances are needed to handle 50k RPS.
4.  **Execute**: At 8:40 AM, ASG changes `MinSize` to 20.
5.  **Reactive Layer**: If the spike is actually 70k RPS (higher than predicted), standard **Target Tracking** kicks in to add more instances.

## 🧠 Resource Behavior
- **Scaling Modes**:
    - `ForecastAndScale`: Proactively changes the ASG size.
    - `ForecastOnly`: Just shows you the graph in the console.
- **Recalculation**: The forecast is updated every 24 hours.

## 📐 ASCII Diagrams
```text
[ TRAFFIC ] ^
            |          /--\ (Predicted Spike)
            |    /----/    \
            |---/           \----
            +---------------------> [ TIME ]
              ^
[ PREDICTIVE ]| (ASG Scales up HERE, before the spike)
```

## 🔍 Code / IaC (Predictive Scaling Policy)
```hcl
resource "aws_autoscaling_policy" "predictive" {
  name                   = "predictive-scaling-policy"
  autoscaling_group_name = aws_autoscaling_group.app_asg.name
  policy_type            = "PredictiveScaling"

  predictive_scaling_configuration {
    metric_specification {
      target_value = 50.0 # Target 50% CPU
      predefined_metric_pair_specification {
        predefined_metric_type = "ASGCPUUtilization"
      }
    }
    mode                     = "ForecastAndScale"
    scheduling_buffer_time   = 300 # 5 minutes
  }
}
```

## 💥 Production Failures
1.  **The "Flash Sale" Outage**: Predictive scaling is great for *seasonal* patterns, but it can't predict a random "Flash Sale" or a "Viral Tweet." Relying *only* on predictive scaling without a reactive backup is dangerous.
2.  **Over-provisioning Cost**: A holiday causes a massive traffic spike. Predictive scaling assumes this will happen *every week* at the same time and over-provisions servers for the next month. **Solution**: Use "Forecast Only" during high-anomaly periods.
3.  **Low Traffic Noise**: If your traffic is extremely erratic and has no pattern, the ML model will produce a "Flat" forecast, making it useless.

## 🧪 Real-time Q&A
*   **Q**: Does it cost extra?
*   **A**: No. Predictive Scaling is a free feature of ASG (you only pay for the instances).
*   **Q**: Can I use it with Spot Instances?
*   **A**: Yes, but remember that Spot instances can be reclaimed.

## ⚠️ Edge Cases
*   **Metric Choice**: `ASGCPUUtilization` is common, but `ALBRequestCountPerTarget` is often a better "leading indicator" for web apps.
*   **Max Capacity Limit**: Predictive scaling will never scale beyond the `MaxSize` of your ASG.

## 🏢 Best Practices
1.  **Always use it with Target Tracking** (Reactive). They work together: Predictive handles the "Knowns," Target Tracking handles the "Unknowns."
2.  **Start with "Forecast Only"** for a few days to verify the accuracy.
3.  **Set a reasonable Buffer** to handle slight variations in the forecast.

## ⚖️ Trade-offs
*   **Predictive**: Eliminates "Warm-up" lag and improves user experience, but can lead to higher costs if the forecast is wrong.

## 💼 Interview Q&A
*   **Q**: How would you handle a traffic spike that happens every Monday morning at 8:00 AM sharp?
*   **A**: I would use **Predictive Scaling**. Standard scaling would wait for the CPU to spike at 8:00 AM, and by the time the new instances are "InService" at 8:05 AM, the users would have already experienced slowness. Predictive scaling would identify the Monday morning pattern and start launching instances at 7:45 AM, ensuring full capacity is ready at 8:00 AM.

## 🧩 Practice Problems
1.  Enable "Forecast Only" on an existing ASG and observe the graph after 24 hours.
2.  Compare the "Predefined Metric Pairs" available for predictive scaling (CPU vs. Load Balancer requests).
