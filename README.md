# FailyV-Dispatch 

![GitHub license](https://img.shields.io/github/license/Wiibleyde/FailyV-Dispatch) ![GitHub issues](https://img.shields.io/github/issues/Wiibleyde/FailyV-Dispatch) ![GitHub pull requests](https://img.shields.io/github/issues-pr/Wiibleyde/FailyV-Dispatch) ![GitHub last commit](https://img.shields.io/github/last-commit/Wiibleyde/FailyV-Dispatch) ![GitHub repo size](https://img.shields.io/github/repo-size/Wiibleyde/FailyV-Dispatch) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Wiibleyde/FailyV-Dispatch) ![GitHub language count](https://img.shields.io/github/languages/count/Wiibleyde/FailyV-Dispatch) ![GitHub top language](https://img.shields.io/github/languages/top/Wiibleyde/FailyV-Dispatch)

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

| Flag | Description | Alias | Usage |
| --- | --- | --- | --- |
| -p | Port to listen on (default: 9123) | --port | ```-p 9123``` |
| -d | Debug mode (default: false) | --debug | ```-d``` |
| -ho | Host to listen on (default:0.0.0.0) | --host | ```-ho x.x.x.x``` |
| -h | Help message | --help | ```-h``` |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
