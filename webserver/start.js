const { createServer } = require("https");
const { existsSync, readdirSync } = require("fs");
const { spawn } = require("child_process");

const options = {
  key: process.env.SSL_KEY,
  cert: process.env.SSL_CERT,
};

const server = createServer(options, (req, res) => {
  if (req.method !== "POST")
    res
      .writeHead(405, "Method Not Allowed", { "Content-Type": "text/plain" })
      .end(`Only POST requests a re allowed. You used ${req.method}`);

  if (
    process.env.DEVICE_TOKEN &&
    req.headers.authorization !== `Bearer ${process.env.DEVICE_TOKEN}`
  ) {
    return res
      .writeHead(403, "Forbidden", { "Content-Type": "text/plain" })
      .end(
        "Could not sign in with the provided authorization token. Make sure it is correctly provided: Authorization: Bearer <token>"
      );
  }

  const [commandPath, queryString] = req.url.split("?", 2);
  const params = queryString
    ? queryString.split("&").map((param) => {
        const [key, value] = param.split("=");
        return [`-${key}`, value];
      })
    : [];

  /**
   * Return 404 Not Found if the URL does not start with '/command' or if
   * there is no command matching the requested resource
   */
  if (
    req.url === "/commands" ||
    !req.url.startsWith(`/commands`) ||
    !existsSync(`.${commandPath}.py`) ||
    req.url === "/commands/langoon"
  ) {
    const commands = readdirSync("./commands")
      .filter((file) => !/langoon.py|__init__.py|__pycache__/.test(file))
      .map((file) => "\n - " + file.replace(".py", ""))
      .join(", ");
    return res
      .writeHead(404, "Not Found", { "Content-Type": "text/plain" })
      .end(
        `Could not find the command. The following commands are available: ${commands}`
      );
  } else {
    let message = "";
    let error = "";
    const childProcess = spawn("python3", [
      ...[`.${commandPath}.py`],
      ...params,
    ]);
    childProcess.stdout.on("data", (data) => {
      message += data.toString();
    });
    childProcess.stderr.on("data", (data) => {
      error += data.toString();
    });
    childProcess.on("exit", (code) => {
      if (code) {
        res
          .writeHead(500, "Internal Server Error", {
            "Content-Type": "text/plain",
          })
          .end(error);
      } else {
        return res
          .writeHead(200, { "Content-Type": "application/json" })
          .end(message);
      }
    });
  }
}).listen(443, () => {
  console.log(`Webserver is running on port 443 ...`);
  if (process.env.SMOKETEST === "true") {
    console.log("\nClosing webserver ...\n");
    server.close(() => {
      console.log("Webserver has closed\n");
    });
  }
});
