# 📌 Topic: Dockerfile Basics and Instructions

🟢 **Simple Explanation (Beginner)**
-----------------------------------
A **Dockerfile** is a **Recipe Card**. 
Instead of telling a cook "Do this, then do that" over the phone, you write it down. Docker reads this recipe and builds the image automatically.

**The main ingredients (instructions):**
1. **FROM**: What is my base? (e.g., "Start with a clean kitchen" / Node.js).
2. **WORKDIR**: Where am I working? (e.g., "Go to the counter" / `/app`).
3. **COPY**: Bring in the food (e.g., "Bring my source code into the kitchen").
4. **RUN**: Do some cooking (e.g., "Install dependencies" / `npm install`).
5. **CMD**: How to serve it? (e.g., "Start the app" / `npm start`).

🟡 **Practical Usage**
-----------------------------------
**A Real-World Node.js Dockerfile:**
```dockerfile
# 1. Base Image
FROM node:18-alpine

# 2. Set the working directory
WORKDIR /usr/src/app

# 3. Copy package files first (for better caching!)
COPY package*.json ./

# 4. Install dependencies
RUN npm install

# 5. Copy the rest of the code
COPY . .

# 6. Set the command to run the app
CMD ["node", "index.js"]
```

**Build Command:**
```powershell
# Build the image and name it "my-node-app"
docker build -t my-node-app .
```

🔵 **Intermediate Understanding**
-----------------------------------
### CMD vs ENTRYPOINT
- **CMD**: The default command. It can be easily overridden when running the container (`docker run my-app echo "hello"` will run echo instead of CMD).
- **ENTRYPOINT**: The command that *must* run. It's harder to override. You usually use it to turn your container into an executable tool.

### ENV vs ARG
- **ARG**: Variables used only during the **Build** process (e.g., version numbers). They disappear after the image is built.
- **ENV**: Variables that persist in the **Running Container** (e.g., DB credentials, PORT).

🔴 **Internals (Advanced)**
-----------------------------------
### Shell Form vs. Exec Form
Docker instructions can be written in two ways:
1. **Shell Form**: `CMD node index.js` (Executes as `/bin/sh -c "node index.js"`).
2. **Exec Form**: `CMD ["node", "index.js"]` (Executes directly).

**Staff Warning**: **Always use Exec Form.** 
Why? Because Shell Form starts a sub-shell (`sh`). If you send a "Stop" signal to the container, it goes to `sh`, which doesn't always pass it to your Node.js app. Your app becomes a "zombie" and Docker has to kill it forcefully after 10 seconds.

### The Build Context
When you run `docker build .`, the `.` is the **Context**. 
Docker zips up everything in that folder and sends it to the Docker Daemon. 
**Staff Insight**: If you have a 1GB database file in your folder, your build will be slow even if you don't use it in the Dockerfile. Use `.dockerignore`!

⚫ **Staff-Level Insights**
-----------------------------------
### The Principle of Least Privilege
Never run your app as `root` inside the container. 
**Best Practice**:
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install
# Use the built-in 'node' user instead of root
USER node
CMD ["node", "index.js"]
```

### Reproducible Builds
Always use specific versions. 
- **Bad**: `FROM node:latest` (Your build might break tomorrow when Node 22 comes out).
- **Good**: `FROM node:18.16.0-alpine` (Locks the version).

🏗️ **Mental Model**
A Dockerfile is an **Automated Installation Script** that produces a snapshot.

⚡ **Actual Behavior**
Each instruction creates a temporary container, runs the command, commits the result to a new layer, and deletes the temporary container.

🧠 **Resource Behavior**
- **Layer Limits**: Linux has a limit on the number of layers (usually 127). Combining `RUN` commands helps avoid this.

💥 **Production Failures**
- **Build failing due to cache**: You updated your `apt` packages in the Dockerfile, but Docker used the cached version from 3 months ago, missing a critical security patch.
  - **Fix**: `docker build --no-cache ...`

🏢 **Best Practices**
- Order: `FROM` -> `ENV` -> `WORKDIR` -> `COPY package.json` -> `RUN npm install` -> `COPY source` -> `CMD`.
- Use `alpine` or `slim` images to keep the surface area small for hackers.

🧪 **Debugging**
```bash
# Debug a failing build: Run the last successful layer
docker run -it <last_successful_layer_id> /bin/sh
```

💼 **Interview Q&A**
- **Q**: Why should we copy `package.json` before the source code?
- **A**: To leverage layer caching. If the source code changes but dependencies don't, Docker skips `npm install` and saves minutes.
- **Q**: Difference between `COPY` and `ADD`?
- **A**: `COPY` is simple and preferred. `ADD` can also download files from URLs and extract `.tar.gz` files automatically (can be dangerous).

---
Prev: [05_The_Anatomy_of_an_Image.md](05_The_Anatomy_of_an_Image.md) | Index: [00_Index.md](../00_Index.md) | Next: [07_Layer_Caching_and_Optimization.md](07_Layer_Caching_and_Optimization.md)
---
