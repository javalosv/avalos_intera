## Watson IoT Platform getting started guides
This sample application is included as a component in a set of Getting Started guides that step through the basics of developing a ready-for-production, end-to-end IoT prototype system with Watson IoT Platform.

Developers who are new to working with Watson IoT Platform can use the step-by-step processes in the Getting Started guides to develop and deploy a solution that demonstrates one or more Watson IoT Platform features.

For more information about the getting started guides, see the [Watson IoT Platform documentation](https://console.bluemix.net/docs/services/IoT/getting_started/getting-started-iot-overview.html).

UI using widget library
###  Install dependencies

#### Step 1: Clone this repository

```
git clone https://github.com/ibm-watson-iot/iot-guide-conveyor-ui-html.git

```
#### Step 2: Install dependencies

```
cd iot-guide-conveyor-ui-html
npm install
```

#### Step 3: Building UI

#### Widget signature
Each widget uses the following JavaScript parameters:
```
WIoTPWidget.Create<widgetType>(html_id,eventName,deviceType,deviceId,param(s),[, .. widget specific config])
```

| Name | Meaning | example|
| ------ | ------ |----|
| html_id | Represents the element id to which the widget will be rendered | "rpmgauge"|
|eventName |Name of the event that the device is emitting this will the sets of sensor values in generally| "sensorData"|
|deviceType | your device type | "iot-conveyor-belt"|
|deviceId |  your device Id to which you want to update the value of the widget as per the real time data|"belt1"|
| param | A event may contain multiple values like temperature ,humidity etc this specifies which sensor reading that you want to show | "rpm" |
| params | A set of sensor data that you want to plot simultaneously | ["rpm", "ay"] |


##### Adding gauge for r.p.m
* Open the public/index.html template
* Find the place holder for rpm gauge in the line no:17
* Added dev element with an unique id as given below

```html
<div id="rpmgauge" ></div>
```  
* Update the javascript to create the widget

```javascript

WIoTPWidget.CreateGauge("rpmgauge","sensorData", "iot-conveyor-belt", "belt1", "rpm" ,{
           label: {
               format: function(value, ratio) {
                   return value;
               },
               show: true // to turn off the min/max labels.
           },
        min: 0.0, // 0 is default, can handle negative min e.g. vacuum / voltage / current flow / rate of change
        max: 5.0, // 100 is default
        units: 'rpm'
      },['#FF0000', '#F97600', '#F6C600', '#60B044']);

```

##### Adding gauge for Accelerometer
* Find the place holder for accelerometer gauge in the line no:26
* Added dev element with an unique id as given below

```html
<div id="aygauge" ></div>
```  
* Update the javascript to creat the widget

```javascript

WIoTPWidget.CreateGauge("aygauge","sensorData", "iot-conveyor-belt", "belt1", "ay" ,{
     label: {
         format: function(value, ratio) {
             return value;
         },
         show: true // to turn off the min/max labels.
     },
  min: -1.0, // 0 is default,can handle negative min e.g. vacuum / voltage / current flow / rate of change
  max: 1.0, // 100 is default
  units: 'g'//,
},['#FF0000', '#F97600', '#F6C600', '#60B044']);
```

##### Adding gauge for motor speed chart
* Find the place holder for motor speed chart in the line no: 35
* Added dev element with an unique id as given below

```html
<div id="speedchart" ></div>
```  
* Update the javascript to creat the widget

```javascript

WIoTPWidget.CreateChart("speedchart","sensorData", "iot-conveyor-belt", "belt1",
["rpm", "ay"], [["line","rpm"],["line","ay"]],['#2ca02c','#d62728']);

```
#### Step 4: Deploying it to bluemix


* Update the Watson IoT platform service name that you have created in the previous lesson in the manifest.yml

```
declared-services:
  <your iot platform service name >:
    label: iotf-service
    plan: iotf-service-free
applications:
- path: .
  memory: 128M
  instances: 1
  domain: mybluemix.net
  disk_quota: 1024M
  services:
  - <your iot platform service name >
```


* Run the following command to push the application into bluemix

```
cf push <appname>

```

##### To run locally

* Add application credentials under config folder with the following json

``` javascript
config/default.json

{
  "api-key" : "Your app key",
  "auth-token" : "your auth-token"
}

```
* start the application
 `npm run start`

### Reference

To know more about the widget library please refer the [github]("https://github.com/ibm-watson-iot/iot-widgets")

# Privacy notice

This web application includes code to track deployments to [IBM Bluemix](https://www.bluemix.net/) and other Cloud Foundry platforms. The following information is sent to a [Deployment Tracker](https://github.com/cloudant-labs/deployment-tracker) service on each deployment:

* Application Name (`application_name`)
* Space ID (`space_id`)
* Application Version (`application_version`)
* Application URIs (`application_uris)``

This data is collected from the `VCAP_APPLICATION` environment variable in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix to measure the usefulness of our examples, so that we can continuously improve the content we offer to you. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

## Disabling deployment tracking

Deployment tracking can be disabled by removing the require("cf-deployment-tracker-client").track(); line from the end of the 'app.js' file.

## Useful links
[Install Node.js]: https://nodejs.org/en/download/
[bluemix_dashboard_url]: https://console.ng.bluemix.net/dashboard/
[bluemix_signup_url]: https://console.ng.bluemix.net/registration/
[cloud_foundry_url]: https://github.com/cloudfoundry/cli

[IBM Bluemix](https://bluemix.net/)  
[IBM Bluemix Documentation](https://www.ng.bluemix.net/docs/)  
[IBM Bluemix Developers Community](http://developer.ibm.com/bluemix)  
[IBM Watson Internet of Things](http://www.ibm.com/internet-of-things/)  
[IBM Watson IoT Platform](http://www.ibm.com/internet-of-things/iot-solutions/watson-iot-platform/)   
[IBM Watson IoT Platform Developers Community](https://developer.ibm.com/iotplatform/)
