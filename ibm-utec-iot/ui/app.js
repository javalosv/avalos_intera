var http = require('http');
var express = require("express");
var bodyParser = require('body-parser');
var logger = require('morgan');
var cfenv = require('cfenv');

//Track Deployment
require("cf-deployment-tracker-client").track();

var IoTWidgets = require("wiotpwidgets");

// Create an Express app
var app = express();

//Add required middleware’s
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));


// Add a simple route for static content served from 'public'
app.use("/",express.static("public"));

// Create a server
var server = http.createServer(app);

// Initialise the IoTWidgets with a server
IoTWidgets.init(server);

// Serve the UI components
app.use(express.static(IoTWidgets.uiPath));

// Serve the http api for the connection

app.use(IoTWidgets.path, IoTWidgets.api);

//server.listen(3000);
// get the app environment from Cloud Foundry
var appEnv = cfenv.getAppEnv();

// start server on the specified port and binding host
server.listen(appEnv.port, '0.0.0.0', function() {
	// print a message when the server starts listening
  console.log("server starting on " + appEnv.url);
});
