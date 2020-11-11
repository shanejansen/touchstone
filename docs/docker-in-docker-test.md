```commandline
docker run -it -v /var/run/docker.sock:/var/run/docker.sock docker
apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
python3 -m ensurepip
pip3 install --no-cache --upgrade pip setuptools
pip3 install pipenv
docker commit CONTAINER_NAME did-test
docker run -it --network="host" -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/toushtone did-test /bin/sh
cd touchstone
pip install .
```
