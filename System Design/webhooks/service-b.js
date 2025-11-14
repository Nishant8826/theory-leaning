const express = require("express");
const app = express();

app.use(express.json());

app.post("/webhook", (req, res) => {
  console.log("Webhook received:");
  console.log(req.body);

  res.status(200).send("Webhook received successfully");
});

app.listen(4000, () => {
  console.log("Service B running on port 4000");
});
