const { createServer } = require("http")

console.log('\nStarting webserver ...\n')

createServer((req, res) => {
  if (req.method === "GET") {
    res.statusCode = 200
    return res.end("webserver is responding!")
  }
  else if (req.method === "POST") {
    try {
    console.log(`New code has been deployed – pull and install`)
    console.log(`Reset any changes that have been made locally`)
    console.log(execSync(`git -C ${process.cwd()} reset --hard`))
    console.log(`Ditch any files that have been added locally too`)
    console.log(execSync(`git -C ${process.cwd()} clean -df`))
    console.log(`Pull down the latest`)
    console.log(execSync(`git -C ${process.cwd()} pull -f`))
    console.log(`Install requirements`)
    console.log(execSync(`pip3 install -r requirements.txt`))
    console.log(`All good`)
    res.statusCode = 200
    return res.end("Code was pulled repo")
    } catch (error) {
      console.log(`Could not pull from repo, failed with exception:`)
      console.log(error)
      res.statusCode = 500
      return res.end(error)
    }
  }
}).listen(8080, () => console.log(`  Running on port 8080`))