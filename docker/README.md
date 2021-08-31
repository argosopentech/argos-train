#### Building container
```
sudo docker build -t argosopentech/argos-train .

```

#### Create `argosopentech/argos-train` container from `argosopentech/argos-train` image
```
sudo docker create --name argosopentech/argos-train argosopentech/argos-train


```

#### Start container
```
sudo docker start argosopentech/argos-train

```

#### Exec shell in container
```
sudo docker exec -it argosopentech/argos-train /bin/bash

```

#### Push to Docker Hub
```
sudo docker login
sudo docker push argosopentech/argos-train

```

#### Reset
```
sudo docker container stop argosopentech/argos-train && sudo docker container rm argosopentech/argos-train && sudo docker image rm argosopentech/argos-train

```

#### Debug run
```
sudo docker build -t argosopentech/argos-train . && sudo docker create --name argosopentech/argos-train argosopentech/argos-train && sudo docker start argosopentech/argos-train && sudo docker exec -it argosopentech/argos-train /bin/bash

```

