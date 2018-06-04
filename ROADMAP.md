# WebInject-Server Roadmap

## Proof of concept

### ToDo

### Done
* (GET) Kick off an existing test case file in the WebInject project using existing config
* Test run is synchronous - i.e. http request does not return until test case file has been run and results are available
* Result message states overall pass or fail `Test Cases Failed: 0`
* Link is provided to test results
* Possible for two or more requests to run at the same time

## MVP

### ToDo
* (POST) test case file can be provided in post request
* test target can be a previously unknown host - e.g. developer desktop

### Done

## Future

### ToDo
* (POST) can post resources the test might need, e.g MyCv.docx, JobFeed.xml
* View the resolved config for DEV
* No need to provide opening and closing xml file tags
* No need to provide case tags - separate by a blank line instead
* No need to provide id numbers


### Done

