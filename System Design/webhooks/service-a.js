const express = require("express");
const axios = require("axios");
const app = express();

app.use(express.json());

app.get("/trigger-event", async (req, res) => {
  const eventData = {
    event: "order_created",
    orderId: 12345,
    amount: 500
  };

  try {
    await axios.post("http://localhost:4000/webhook", eventData);
    res.send("Event triggered and webhook sent");
  } catch (error) {
    console.error("Error sending webhook:", error.message);
    res.status(500).send("Webhook failed");
  }
});

app.listen(3000, () => {
  console.log("Service A running on port 3000");
});
