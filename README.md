# Swagger generated server

## Overview
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.  This
is an example of building a swagger-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.5.2+


## Running with Docker

The certificate of the emulab user must be downloaded first and put under local directory such as .bssw similar to geni-lib documentation.

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run --rm -it \
    --env-file .env \
    -p 127.0.0.1:8888:8080 \
    -v /var/log/:/var/log/ \
    -v ~/.bssw/ssh/id_emulab_rsa:/root/.ssh/id_rsa:ro \
    -v ~/.bssw/ssh/config:/root/.ssh/config:ro \
    -v ~/.bssw/geni-emulab:/root/.bssw/geni/ \
    -d \
    swagger_server

```

and open your browser to here:

```
http://127.0.0.1:8888/aerpawgateway/1.0.0/ui/
```

Your Swagger definition lives here:

```
http://127.0.0.1:8888/aerpawgateway/1.0.0/swagger.json
```

logging file:
/var/log/aerpaw-gateway.log


## Usage without docker
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
pip3 install werkzeug==0.16.1
cd geni-lib
python3 setup.py install
cd ..
# cp perl/* <somewhere> and make sure .env points to here
source .env
python3 -m swagger_server
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```