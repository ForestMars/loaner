# Overview

Loaner is a complete, secure and scalable microservice example written in Python (and compiled to executable C code) to provide up to date and historical account information for loan payments. 

The application includes 2 implementations for containerized deployments. The supplied Docker compose file will bring up all service containers (app server, database server and caching server) running locally. Not included here is an additional configuration file for individually specifying targets to run each of the different services on. Rather, it’s expected that a distributed service mesh will be orchestrated using Kubernetes, presumably with Helm for deployment and service discovery.

Alternately, a custom “Docker factory” is included that will build a complete Docker image from the supplied Dockerfile, and deploy it to a remote server using credentials sourced from your environment settings, and automatically run it. This is pre-configured for AWS/debian but can be easily adapted for any Posix compatible endpoint.  Not included here is an option to deploy with [Terraform](https://github.com/ForestMars/terraform-station), or finished Helm charts.

The service is written in Python and then compiled to C byte code. However this version includes the source files as a fallback. so it can be run without compiling *make build-arch* (or *docker-compose up*).

To keep things simple for this demo, neither Docker nor compilation is required. All that's needed for a fully working instance is to:

1. `pip install -r requirements.txt`,
1. source the .env & .auth files, and
1. start the service either by simply invoking `python3 run.py` for the CLI demo, or `python loaner.app` for the REST API.

This (obviously) assumes you have python3 available in your execution context.


# Table of contents

  * [Overview](#overview)
  * [Build](#build)
  * [Install](#install)
  * [Run](#run)  
  * [Deploy](#deploy)
    * [Docker Compose](#docker-compose)
    * [Docker Factory](#docker-factory)
  * [API](#api)
  * [Security](#security)
    * [Client Access](#token-based-secure-access)
    * [Secrets Management](#vault-secrets-management)
    * [TLS](#tls)
  * [Known Issues](#knownissues)
  * [License](#license)
  * [Contact](#Contact)


### BUILD

While not required for this demo, building for your architecture is as simple as running:

```
make build
```

This is an alias for `build-arch` which compiles from the source files (found in `lib/c`) to executable objects in `lib/ext`.

The included Makefile also supports options for `build-source` which creates the C source code used by build-arch, and `build-local` which, intended for developers, skips the intermediate step and directly compiles the binaries for your local architecture.

This demo version includes fallback to the original source files, so you do not need to compile for your architecture to run.

## INSTALL

### Bare Installation

Demo does not presume Docker is present, or Conda, (or Poetry, yadayada) so we can just install with pip.

To install, run pip install on the supplied reqirements file:

* ``pip install -r requirements.txt``


## RUN

After you have installed the requirements with pip, a command line demo can be started with:

* `` source .env``
* ``source .auth``
* ``python3 run.py``

This will start an interactive CLI based demo of the service.

To start the web API, invoke the app file:

``python3 loaner.app``

This should bring up the [API](api) on port 5555, accepting requests for outstanding balance by loan id and date using a GET request formatted as:

https://{HOST}:5555/loan_id/date

## DEPLOY

To run containerized or deploy to remote servers.

### Docker Compose

Standard Docker deployment builds and runs 3 containers:
* App-server
* Database-server
* Cache-server

All 3 containers can be run on a single server, or deployed to different endpoints.

### Docker Factory

The supplied Docker factory automatically creates a completely build Docker image, copies it to a remote server and starts it up on the specified port.

### Kubernetes

Helm chart is WIP.

## API

The REST API is self-documenting, thus once the service is running, the complete API specification (which for our demo only fetches outstanding loan balance by date) can be viewed at: https://locallost:5555/api/v1. This view let's you try out any API requests and methods interactively. Any new service routes added will automatically be added to the OAS (Openapi Specification) endpoint for their supported methods, which will be available via the web UI to try out. (And using Swagger Editor we can edit any information accessible at the interactive documentation endpoint.)  

![Self-documenting API is fully interactive](API_screencap.png?raw=true "interactive API")

To view any outstanding balance submit an API request formatted as: ```https://localhost:5555/api/v1/loan/<id>/<date>```, where id is an integer from 1-10 and date is a valid date after Jan. 1, 2020 formatted as year-month-day, for example:

``https://localhost:5555/api/v1/loan/1/2021-02-15``

The loan info endpoint is written to be secure (see [security](#token-based-secure-access) section) but for this demo, that endpoint is available without authentication.

However the service also provides a health check endpoint at /status, which is access protected in the demo. To check if the service is up and running, issue the following command, after sourcing the included ``.auth`` file (to set the included access token as an environmental variable.)

* ``curl -X GET https://localhost:5555/status -H 'Authorization: Bearer ${JWT}'``

## Security

### Token Based Secure Access

The loan service runs on a secure server, with an access token required for clients to use the API. This token can be generated via the /token endpoint, and a valid working token can also be found in the `.env` file; however, the demo has token access turned off for the loan info endpoint for ease of use. (`/status` demonstrates a fully secured endpoint.) To re-activate the secure API for the loan info path, simply uncomment the JWT token decorator on the /loan route.

### Secured with Vault

With client side access secured by access tokens, the back end is protected by Hashicorp Vault. When the service is started, it contacts a Vault server running on AWS to request read-only credentials to access the Postgres database running on RDS. These credentials are set with a TTL of one hour.

The secrets management service can be turned on/off; the demo is configured to use Vault as the default. If for some reason the vault server is not desired or is not reachable (Vault is intended to run on a cluster, for this demo version it's only a single instance) just set ``USE_VAULT = False`` in ``config/postgres.py`` and the demo will fall back to a standard PSQL user.

### TLS

When running this app without a reverse proxy, (ie. nginx) TLS will not be enabled (see [WSGI issues](#wsgi-issues)) thus any URLs with `https` should be treated as `http.`  

## KNOWN ISSUES

### Protobuf Issues

The synchronize_to_protobuf library has a missing DESCRIPTOR for proto_cls and as a result that particular caching layer is currently disabled in the demo.

### WSGI Issues

Waitress, used here as the WSGI server, [does not natively support TLS](https://github.com/Pylons/waitress/blob/36240c88b1c292d293de25fecaae1f1d0ad9cc22/docs/reverse-proxy.rst). When running app without nginx, the https url scheme will not be available, but only http.

### Github issue queue

Feel free to [report any problems here](https://github.com/ForestMars/loandemo/issues).

### ⚖ LICENSE

All original code here with is copyright 2021 Forest Mars / Continuum Software.

### CONTACT

[via email](mailto:themarsgroup@gmail.com)
