# WebInject-Server Roadmap

## Proof of concept
* (GET) Kick off an existing test case file in the WebInject project using existing config
* Result message states overall pass or fail
* Link is provided to test results
* Test run is synchronous - i.e. http request does not return until test case file has been run and results are available
* Possible for two or more requests to run at the same time

## MVP
* (POST) test case file can be provided in post request
* config can be provided in post request
* test target can be a previously unknown host - e.g. developer desktop

## Nice to have
* (POST) can post resources the test might need, e.g MyCv.docx, JobFeed.xml



