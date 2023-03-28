# TCP Socket Client

The TCP Socket Client is responsible for fetching products and updating products from TCP Socket Server

## Table of Contents

- [Message Format](#message-format)
- [Configuration File](#configuration-file)
- [Response Format](#response-format)
- [Running the Project with Docker](#running-the-project-with-docker)

## Message Format

The client send to the server messages in the following format:

```
HTTP VERB + ENDPOINT TYPE + PATH VARIABLES + QUERY PARAMS
```

Based on this format, the server determines which Django API service to call.

When the Socket Client get some response, this has the following format

```
DATA TYPE (LIST | JSON) + ENDPOINT TYPE + DATA
```

## Configuration File

The configuration file is in YAML format and contains the following constants:

```yaml
server: # Server configuration
  address: 127.0.0.1
  port: 5000
```

## Response Format

The server returns the following string format to the socket client:

```
DATA TYPE(LIST | JSON) + ENDPOINT_TYPE + DATA
```

## Running the Client

You have 2 commands:
```
get-products
get-product --code <some product code>
```

Just execute cli.py file and you will se this commands:

```
python cli.py
```
