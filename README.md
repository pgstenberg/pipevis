#Pipevis

**Deployment pipeline visualization aid for agile teams, which can act as a information radiator.**

This application was developed in association with [Per-Gustaf Stenberg](http://stenberg.stonepath.se) Master's Thesis around the subject **Container-based Continuous Delivery for Clusters**. The report will be downloadable as soon as it is finished.

##Dependencies
Pipevis uses [Flask](http://flask.pocoo.org/) for the backend; and for the frontend [AngularJS](https://angularjs.org/) and [Bootstrap](http://getbootstrap.com/). For the CLI it uses [Click](http://click.pocoo.org/)

[Docker](http://docker.io/) is recommended to administrate and maintain the server and integration with your CI server.


##Starting the server
The pipevis-server can easily be started using docker hub with this command.
```
docker run -p 5000:5000 pgstenberg/pipevis-server
```
You need to expose port 5000, which are the default Flask port.

##Using the CLI
To ease the integration pain with Pipevis and your CI server, a CLI is provided in order to communicate with the backend service. For instance: if your using Jenkins you can execute a shell script running the CLI container with the command of your choosing.

###Initialize a new pipeline
To initialize a new pipeline you need to describe your pipeline steps using a simple json file.

_Here is an example of how your json init file can look like:_

```json
{
"stages":[
{"title":"Integration","order":0, "tasks":
[
  {"title":"Compile source","order":0},
  {"title":"Unit testing","order":1},
  {"title":"Package War","order":2},
  {"title":"Prepare DockerImage","order":3}
]
},
{"title":"Development","order":1, "tasks":
[
  {"title":"Prepare DockerImage","order":0},
  {"title":"Prepare Deployment","order":1},
  {"title":"Perform Deployment","order":2}
]
},
{"title":"Quality Assurance","order":2, "tasks":
[
  {"title":"Prepare DockerImage","order":0},
  {"title":"Prepare Deployment","order":1},
  {"title":"Perform Deployment","order":2},
  {"title":"Quality Testing","order":3},
  {"title":"Analyse Quality","order":4}
]
}
]
}
```

_To ask the backend to initialize the pipeline with the init file:_

```
docker run -t --rm -v /path/to/pipevis/init/file:/var/pipeline-data:ro pgstenberg/pipevis-cli -f /var/pipeline-data/pipeline.json -t 'Build #10' -d 'This is your description' init http://pipevis-backend:5000"
```

###Progress your pipeline
```
docker run -t --rm pgstenberg/pipevis-cli progress http://pipevis-backend:5000
```

###Notifying your pipeline
As soon as your CI-server have archived some artifact, notifies for failures or have some plain information you can notify the pipevis.

####Linking to an artifact
```
docker run -t --rm pgstenberg/pipevis-cli -t 'Artifact' -m 'Link to the artifact can be found {{ result }}.' --type 'ARTIFACT' --link result here http://linktoarticaft.com notify http://pipevis-backend:5000
```

####Simple information message
```
docker run -t --rm pgstenberg/pipevis-cli -t 'Information' -m 'This is just some information.' notify http://pipevis-backend:5000
```

####Warnings or failures
```
docker run -t --rm pgstenberg/pipevis-cli -t 'Failure!' -m '${all.message}' --type 'WARNING' notify http://pipevis-backend:5000
```

###CLI Help
All the commands can be seen by using the *--help* flag:
```
docker run -t --rm pgstenberg/pipevis-cli --help
```

##Integration with Giphy
Pipevis is dynamically generating gifs depending on the success fo the pipeline using the [Giphy API](https://github.com/giphy/GiphyAPI). As mentioned in section 5 A of the terms of service for the API an "Powered By Giphy" logo need to be visual at all time.

![Powerd by Giphy](images/logo_giphy.png)

By default it uses Giphys *public beta key*, but can be changed in the backend code if so is desired.

##License
Feel free to use it as you like.
