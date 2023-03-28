# TCP Socket Server

The TCP Socket Server is responsible for handling requests from the socket client and communicating with the Django HTTP server to obtain either a list of products or the details of a specific product.

## Table of Contents

- [Message Format](#message-format)
- [Configuration File](#configuration-file)
- [Response Format](#response-format)
- [Running the Project with Docker](#running-the-project-with-docker)

## Message Format

The server receives messages in the following format:

\`\`\`
HTTP VERB + ENDPOINT TYPE + PATH VARIABLES + QUERY PARAMS
\`\`\`

Based on this format, the server determines which Django API service to call.

## Configuration File

The configuration file is in YAML format and contains the following constants:

\```yaml
server: # Server configuration (used even within a Docker container)
  address: 0.0.0.0
  port: 5000

s3_server: # Django server connection information
  schema: http
  address: 192.168.0.92
  port: 8000

handler_options: # Product detail query interval options
  interval: 60
\```

## Response Format

After processing the data, the server returns the following string format to the socket client:

\`\`\`
DATA TYPE(LIST | JSON) + ENDPOINT_TYPE + DATA
\`\`\`

## Running the Project with Docker

To run the project with Docker, you need to build the Docker image and then run it, mapping the appropriate ports:

\```bash
docker build . -t server_tcp
docker run -p <map_port>:<expose_port> server_tcp
\```

---
