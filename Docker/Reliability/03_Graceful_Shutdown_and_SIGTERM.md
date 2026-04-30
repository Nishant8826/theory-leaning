# 📌 Topic: Graceful Shutdown and SIGTERM

## 🧠 Concept Explanation (Basic → Expert)
**Basic**: Graceful Shutdown means giving your app a few seconds to "clean up" before it's killed. It's like closing your files and saving your game before turning off the computer.
**Expert**: This is the implementation of **Process Lifecycle Management**. When Docker wants to stop a container, it sends a **SIGTERM** (Signal 15) to PID 1. The app must catch this signal, stop accepting new connections, finish processing existing ones, close database handles, and exit voluntarily. If the app doesn't exit within a "Grace Period" (default 10s), Docker sends a **SIGKILL** (Signal 9), which kills the process instantly, potentially causing data corruption or broken transactions. Staff-level engineering requires mastering the **Init Process (tini)** and ensuring that signals are correctly propagated from Docker to the application code.

## 🏗️ Mental Model
- **SIGTERM**: A polite "Closing in 10 minutes" announcement at a store. Customers finish their shopping and leave.
- **SIGKILL**: Turning off the lights and locking the doors while people are still inside.

## ⚡ Actual Behavior
- **Zero-Downtime Updates**: During a rolling update, the old container is sent a SIGTERM. It finishes the last few requests while the NEW container starts taking over. If shutdown isn't graceful, the last few users will see "Connection Reset" errors.
- **Database Integrity**: Graceful shutdown ensures that a database container flushes its memory to disk before stopping, preventing a corrupted database file.

## 🔬 Internal Mechanics (The PID 1 Problem)
1. **The Signal**: Docker sends `SIGTERM` to the process with ID 1 inside the container.
2. **The Shell Trap**: If your `CMD` is `CMD npm start`, Docker runs `/bin/sh -c npm start`. The shell is PID 1. Shells do NOT pass signals to their children by default. Your app (npm) never sees the SIGTERM and is eventually killed by SIGKILL.
3. **The Fix (Exec Form)**: Use `CMD ["npm", "start"]`. This runs the app directly as PID 1, allowing it to receive the signal.

## 🔁 Execution Flow
1. Orchestrator: `docker stop my-app`.
2. Kernel: Sends `SIGTERM` to PID 1 in the container.
3. App: Receives signal via `process.on('SIGTERM')` or `signal.Notify`.
4. App: Tells Load Balancer "I am no longer healthy" (Readiness probe failure).
5. App: Waits for active requests to finish (e.g., 5 seconds).
6. App: Closes Redis, Postgres, and File handles.
7. App: Exits with code 0.
8. Docker: Container status becomes `Exited (0)`.

## 🧠 Resource Behavior
- **Connections**: During shutdown, the number of active connections should drop to zero.
- **Time**: The "Shutdown Window" should be shorter than the orchestrator's "Termination Grace Period."

## 📐 ASCII Diagrams (REQUIRED)

```text
       GRACEFUL SHUTDOWN TIMELINE
       
[ Docker Stop ] -> [ SIGTERM Received ] -> [ Finish Requests ] -> [ Exit ]
      |                   |                     |                  |
( 0s )             ( 0.1s )              ( 5s )             ( 5.5s )
      |                                                            |
      +-------------------( GRACE PERIOD: 10s )--------------------+
```

## 🔍 Code (Node.js Graceful Shutdown)
```javascript
const server = app.listen(3000);

process.on('SIGTERM', () => {
  console.info('SIGTERM signal received. Shutting down gracefully...');
  
  // 1. Stop accepting new connections
  server.close(() => {
    console.log('Http server closed.');
    
    // 2. Close DB connections
    db.close().then(() => {
      console.log('Database connection closed.');
      
      // 3. Exit process
      process.exit(0);
    });
  });
});
```

## 💥 Production Failures
- **The "Dangling Transaction"**: A user is halfway through a 30-second checkout process. You deploy a new version. The old container is killed instantly (SIGKILL). The user's payment is taken, but the order is never recorded in the DB.
  *Fix*: Implement SIGTERM handling and increase the grace period.
- **The "Zombie Container"**: Your app has a bug where it catches SIGTERM but enters an infinite loop and never exits. Docker waits 10 seconds and then kills it. Your deployments feel "Slow" because every container takes 10 seconds to stop.

## 🧪 Real-time Q&A
**Q: How do I handle PID 1 issues if I can't use 'Exec Form'?**
**A**: Use **tini**. It's a tiny init process designed for containers. You set it as your `ENTRYPOINT`. Tini becomes PID 1, spawns your app as a child, and correctly forwards all signals to it. It also "reaps" zombie processes.

## ⚠️ Edge Cases
- **Long-Running Jobs**: If your container is running a 1-hour video encoding job, a 10-second grace period is useless. You must either use a much longer grace period or design the job to be "Resumable" from a checkpoint.

## 🏢 Best Practices
- **Always use `Exec Form`**: `["executable", "param1"]`.
- **Set a timeout in your app**: If your cleanup takes more than 8 seconds, just force exit so you don't hit the 10-second SIGKILL limit.
- **Dumb-init / Tini**: Use them for any complex container setup.

## ⚖️ Trade-offs
| Feature | SIGTERM (Term) | SIGKILL (Kill) |
| :--- | :--- | :--- |
| **Speed** | Slow (Cleanup) | **Instant** |
| **Safety** | **Highest** | Low (Corrupt) |
| **User Impact** | None | **High (Broken Req)** |

## 💼 Interview Q&A
**Q: Why is it important for a Dockerized application to handle SIGTERM signals?**
**A**: In a dynamic container environment, containers are frequently stopped and moved (during updates, scaling, or host maintenance). When Docker stops a container, it sends a SIGTERM. If the application doesn't handle this signal, it will be forcefully killed by SIGKILL after a timeout. This leads to interrupted user requests, orphaned database transactions, and potential data corruption. By handling SIGTERM, the application can perform a "Graceful Shutdown"—finishing in-flight requests and closing connections properly—ensuring high availability and data integrity.

## 🧩 Practice Problems
1. Start an Nginx container and run `time docker stop <id>`. Notice it takes almost 0 seconds.
2. Start a custom app that *ignores* SIGTERM and run `time docker stop <id>`. Notice it takes exactly 10 seconds.
3. Add `tini` to a Dockerfile and verify that your app now receives signals even if run via a shell script.

---
Prev: [02_Circuit_Breakers_and_Retries.md](./02_Circuit_Breakers_and_Retries.md) | Index: [00_Index.md](../00_Index.md) | Next: [04_Chaos_Engineering_Basics.md](./04_Chaos_Engineering_Basics.md)
---
