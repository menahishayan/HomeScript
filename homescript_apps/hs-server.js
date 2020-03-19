var http = require('http');
var url = require('url');
var moment = require('moment');

const execSync = require('child_process').execSync;
const hsappPath = '/home/shares/public/scripts/HomeScript/homescript_apps'

let eventLog = {}
let idleTesterActive = false

let idleTester = async(n, app) => {
    if(!idleTesterActive) {
        idleTesterActive = true
        setInterval(() => {
            let diff = moment().diff(eventLog[n], 'seconds')
            if (diff >= 100)
                execSync(`python3 ${hsappPath}/hs-${app}/hs-${app}.py ${n} -x`, { encoding: 'utf-8' });
        }, 100000);
    }
}

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write("OK");
  var q = url.parse(req.url, true);
  let app = q.pathname.substr(1);
  let n = q.query.n;

  if(!eventLog[n]) {
      eventLog[n] = moment()
      execSync(`python3 ${hsappPath}/hs-${app}/hs-${app}.py ${n}`, { encoding: 'utf-8' });
  }
  else {
      let diff = moment().diff(eventLog[n], 'seconds')
      eventLog[n] = moment()
      if (diff > 30)
          execSync(`python3 ${hsappPath}/hs-${app}/hs-${app}.py ${n}`, { encoding: 'utf-8' });
  }
  // execSync(`python3 ${hsappPath}/hs-${app}/hs-${app}.py ${n}`, { encoding: 'utf-8' });
  res.end();
  idleTester(n, app);
}).listen(35946);
