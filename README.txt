_______________________________________________________________________
# Auto Refresh Tool

A python based scripting framework to automate refresh steps for a
Salesforce sandbox. The needed tools are brought together and
example starting methods are written. A script specific to the org
will need to be written. There is an accompanying user interface to
make launching the scripts easy.

_______________________________________________________________________
## Getting Started

++ These instructions will get you a copy of the project up and running on
++ your local machine for development and testing purposes. See deployment
++ for notes on how to deploy the project on a live system.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### Dependencies

Apache ANT
(http://ant.apache.org/)

Salesforce Migration Tool
(https://developer.salesforce.com/docs/atlas.en-us.daas.meta/daas/forcemigrationtool_install.htm)

Python 3.6.x
(https://www.python.org/)
- SimpleSalesforce library (Custom version including Tooling API access)
- wxPython
    (https://www.wxpython.org/)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### Installing

++ A step by step series of examples that tell you have to get a
++ development env running

++ Say what the step will be

```
++ Give the example
```

++ And repeat

```
++ until finished
```

++ End with an example of getting some data out of the system or using it
++ for a little demo

_______________________________________________________________________

## Running the tests

++ Explain how to run the automated tests for this system

### Break down into end to end tests

++ Explain what these tests test and why

```
++ Give an example
```

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### And coding style tests

++ Explain what these tests test and why

```
++ Give an example
```

_______________________________________________________________________
## Deployment

++ Add additional notes about how to deploy this on a live system

_______________________________________________________________________
## Contributing

++ Please read [CONTRIBUTING.md]
++ (https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details
++ on our code of conduct, and the process for submitting pull requests
++ to us.

_______________________________________________________________________
## Versioning

++ We use [SemVer](http://semver.org/) for versioning. For the versions
++ available, see the [tags on this repository]
++ (https://github.com/your/project/tags). 

_______________________________________________________________________
## Future State

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### Add check to queue_apex_batch that allows will allow to check if the
    batch is completed. This will allow sequentially dependent apex
    scripts to finish before moving on to the next step.

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### Migrate change sets to bring org up to date

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### Custom link updates may need to have the encoding done during the
    string write

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
### Possibly replace simple_salesforce with ForceFlow or the BigAssForce
macro for anonymous apex

_______________________________________________________________________
## Authors

* **Jackson Sims** - *Initial work* - Acumen Solutions

_______________________________________________________________________
## License

++ This project is licensed under the MIT License - see the [LICENSE.md]
++ (LICENSE.md) file for details

