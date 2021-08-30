#### Building container
```
sudo docker build -t argos_train .

```

#### Create `argos_train` container from `argos_train` image
```
sudo docker create --name argos_train argos_train


```

#### Start container
```
sudo docker start argos_train

```

#### Exec shell in container
```
sudo docker exec -it argos_train /bin/bash

```

#### Reset
```
sudo docker container stop argos_train && sudo docker container rm argos_train && sudo docker image rm argos_train

```

