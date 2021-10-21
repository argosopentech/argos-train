#### Building container
```
sudo docker build -t argosopentech/argostrain .

```

#### Run `argostrain` container from `argosopentech/argostrain` image
```
sudo docker run -it --name argostrain argosopentech/argostrain /bin/bash


```

#### Push to Docker Hub
```
sudo docker login
sudo docker push argosopentech/argostrain

```

#### Reset
```
sudo docker container stop argostrain && sudo docker container rm argostrain && sudo docker image rm -f argosopentech/argostrain

```

