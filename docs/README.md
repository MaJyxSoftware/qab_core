# QAB Core Documentation

Welcome to the documentation for QAB Core, the core component for building secure and fast APIs. QAB Core is based on the Bottle framework and uses Gunicorn as the server. This documentation provides an overview, configuration details, and links to in-depth guides for each major component.

## Table of Contents

- [QAB Core Documentation](#qab-core-documentation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Getting Started](#getting-started)
  - [Configuration](#configuration)
    - [Parameters](#parameters)
    - [Files location](#files-location)
    - [Sample](#sample)
    - [Custom](#custom)
  - [Project Structure](#project-structure)
  - [Components Guides](#components-guides)
    - [Server](#server)
    - [Console](#console)
    - [Controller](#controller)
    - [Scheduler](#scheduler)
  - [Usage Example](#usage-example)

## Overview

QAB Core is designed for rapid development of secure, production-ready APIs. It provides:
- Automatic route registration based on controller methods
- Configurable server and scheduler
- Pluggable logging and error handling
- Easy integration with Bottle and Gunicorn

## Getting Started

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Set up configuration:**
   - Use the provided sample config or environment variables.
3. **Run your API server:**
   ```sh
   python qab_core/server.py
   ```

## Configuration

By design, all configuration variables have a default value allowing quick testing.

### Parameters

If you want to customize those configuration, you have 2 ways to do it:

1) using configuration files
2) using environment variables

| Variable | Environment | Description | Default |
| - | - | - | - |
| server.port | LISTEN_PORT | Set listen server listen port | `8443` |
| server.address | LISTEN_ADDRESS | Set listen server address | `0.0.0.0` |
| server.cors_enabled | CORS_ENABLED | Enable CORS header | `False` |
| server.cors_domains | CORS_DOMAINS | Allowed domains for CORS usage | `*` (shouldn't be used in production)|
| server.certificate | CERTIFICATE | Path to SSL publique certificate | `certs/fullchain.pem` |
| server.private_key | PRIVKEY | Path to SSL private key | `certs/privkey.pem` |
| server.generate_ssl | GENERATE_SSL | Enable auto generation of a self-signed certificate | `False` |
| server.workers | WORKERS | Define the number of Gunicorn workers | Core count - 1 |
| server.threads | THREADS | Define the number of threads per Gunicorn workers | Core count - 1 |
| console.quiet | QUIET | Set state of output in the console | `False` |
| console.nolog | NOLOG | Set state of fie logging | `False` |
| console.debug | DEBUG | Set loggin level to debug | `False` |
| console.log_dir | LOG_DIR | Set directory for logs files | `logs/` |
| scheduler.max_workers | SCHEDULER_MAX_WORKERS | Set max number of paralelle tasks in the scheduler | `10` |

### Files location

Configuration files are loaded in the following order (highest priority last):
1. `/etc/qab/app.json`
2. `~/.qab.json`
3. `./config.json`

### Sample

```json
{
    "server": {
        "port": "8443",
        "address": "0.0.0.0",
        "cors_enabled": true,
        "cors_domains": [
            "www.company.ltd",
            "intranet.company.ltd"
        ],
        "certificate": "/etc/letsencrypt/live/api.company.ltd/fullchain.pem",
        "private_key": "/etc/letsencrypt/live/api.company.ltd/privkey.pem",
        "generate_ssl": true,
        "workers": 7,
        "threads": 1,
    },
    "console": {
        "quiet": false,
        "nolog": false,
        "debug": false,
        "log_dir": "/var/logs/qab"
    },
    "scheduler": {
        "max_workers": 6
    }
}
```

### Custom

You can add custom configuration for your controllers, for exemple:

```json
{
  "my_controller": {
    "key": "value",
    "dict": {
      "key": "value"
    }
  }
}
```

## Project Structure

```
```

## Components Guides

### Server

See [server.md](./server.md)

### Console

See [console.md](./console.md)

### Controller

See [controller.md](./controller.md)

### Scheduler

See [scheduler.md](./scheduler.md)

## Usage Example

See [samples folder](/samples)
