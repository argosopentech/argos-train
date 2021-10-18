#### Building container
```
sudo docker build -t argosopentech/argostrain .

```

#### Create `argosopentech/argostrain` container from `argosopentech/argostrain` image
```
sudo docker create --name argostrain argosopentech/argostrain


```

#### Start container
```
sudo docker start argostrain

```

#### Exec shell in container
```
sudo docker exec -it argostrain /bin/bash

```

#### Push to Docker Hub
```
sudo docker login
sudo docker push argosopentech/argostrain

```

#### Reset
```
sudo docker container stop argosopentech/argostrain && sudo docker container rm argosopentech/argostrain && sudo docker image rm argosopentech/argostrain

```

#### Debug run
```
sudo docker build -t argosopentech/argostrain . && sudo docker create --name argosopentech/argostrain argosopentech/argostrain && sudo docker start argosopentech/argostrain && sudo docker exec -it argosopentech/argostrain /bin/bash

```

