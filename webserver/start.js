const { createServer } = require("http");
const { existsSync, readdirSync } = require("fs");
const { spawn } = require("child_process");

console.log("\nStarting webserver ...\n");

createServer((req, res) => {
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
    res.statusCode = 404;
    res.write("The following commands are available:");
    readdirSync("./commands")
      .filter((file) => !/langoon.py|__init__.py|__pycache__/.test(file))
      .forEach((file) => {
        res.write("\n - " + file.replace(".py", ""));
      });
    res.end();
  } else {
    /**
     * Otherwise spawn the command
     */
    if (req.method === "OPTIONS") {
      params.unshift(["help"]);
    }
    const childProcess = spawn("python3", [
      ...[`.${commandPath}.py`],
      ...params,
    ]);
    childProcess.stdout.on("data", (data) => {
      res.write(data);
    });
    childProcess.stderr.on("data", (data) => {
      res.write(data);
    });
    childProcess.on("close", (code) => {
      if (code) {
        res.statusCode = 500;
        res.end();
      } else {
        res.statusCode = 200;
        res.end();
      }
    });
  }
}).listen(8080, () => console.log(`  Running on port 8080`));
