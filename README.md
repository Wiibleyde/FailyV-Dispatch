# FailyV-Dispatch

**NOT AN OFFICIAL FAILYV PROJECT**

This is a simple dispatch system for the web designed for FailyV the LSMS, and adapted for the LSPD (and could be adapted for any other service).

## Features

- [x] Units
- [x] Service
- [x] Rooms
- [x] Interventions
- [x] Indisponibilities

## Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/) (Included in Docker)

## Installation

1. Clone the repository

```bash
git clone https://github.com/Wiibleyde/FailyV-Dispatch.git
```

2. Create the container

```bash
docker-compose up -d
```

3. Open the website

```bash
http://localhost:9123
```

## Flags

| Flag | Description |
| --- | --- |
| -p | Port to listen on (default: 9123) |
| -d | Debug mode (default: false) |
| -h | Help message |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
