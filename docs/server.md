# Server

[← Back to Main Documentation](./README.md)

[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/server.py#L131)

- [Server](#server)
  - [Description](#description)
    - [Initialization](#initialization)
    - [Routes management](#routes-management)
    - [Starting and Stopping the Server](#starting-and-stopping-the-server)
    - [SSL and CORS](#ssl-and-cors)
    - [Error Handling](#error-handling)
  - [Methods](#methods)
    - [Start - *start()*](#start---start)

## Description

The `Server` class is responsible for initializing and running the API server. It manages route registration, SSL configuration, CORS settings, and worker management. The server can be started and stopped programmatically.

### Initialization

To initialize a server, create an instance of the `Server` class. You can pass configuration directly or rely on config files/environment variables.

**Example:**
```python
from qab_core.server import Server
app = Server()
```

During init, it will fetch the different configuration source files and load them. Then, it will load the [Console](#console) and the [Scheduler](#scheduler)

### Routes management

Routes are generated automatically by introspecting the controller(s) you register with the server. For each public method of your controller, both GET and POST routes are registered. The system generates all possible combinations of required and optional parameters, resulting in flexible and RESTful endpoints.

By default, the route prefix is the name of the controller class (with `Controller` removed). For example, a class `TestController` will have routes prefixed with `/test`.

**Example log output:**
```log
[INFO] Registering route /test/ => controllers.test.index
[INFO] Registering route /test/hello/<firstname> => controllers.test.hello
[INFO] Registering route /test/hello/<firstname>/lastname/<lastname> => controllers.test.hello
[INFO] Registering route /test/hello/<firstname>/lastname/<lastname>/ => controllers.test.hello
[INFO] Registering route /test/index => controllers.test.index
```

The `index` method of your controller class, if present, is used as the base endpoint. If you need custom routes, you can use the same decorators and patterns as with Bottle.

See also: [Controller documentation](./controller.md)

### Starting and Stopping the Server

To start the server, call the `start()` method. This method will block until the server is stopped (e.g., via keyboard interrupt or programmatically).

**Example:**
```python
app.start()
```

Before starting, the server performs several checks:
- Validates SSL certificates (and generates them if enabled)
- Starts the scheduler for background tasks
- Ensures all required configuration is loaded

To stop the server, you can call `app.stop()` (if supported by your entrypoint logic).

### SSL and CORS

- **SSL:**
  - The server supports SSL/TLS. Provide certificate and key paths in your configuration, or enable auto-generation of a self-signed certificate for development.
  - Example config:
    ```json
    {
      "server": {
        "certificate": "/etc/letsencrypt/live/api.company.ltd/fullchain.pem",
        "private_key": "/etc/letsencrypt/live/api.company.ltd/privkey.pem",
        "generate_ssl": true
      }
    }
    ```
- **CORS:**
  - Cross-Origin Resource Sharing (CORS) can be enabled and configured via the `cors_enabled` and `cors_domains` settings.
  - Example:
    ```json
    {
      "server": {
        "cors_enabled": true,
        "cors_domains": ["www.company.ltd", "intranet.company.ltd"]
      }
    }
    ```
  - **Warning:** Avoid using wildcards (`*`) in production for security reasons.

### Error Handling

All server errors, startup issues, and runtime exceptions are logged via the [Console](./console.md). The server will attempt to provide clear error messages and will not start if critical configuration or SSL issues are detected.

---

## Methods

### start()

[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/server.py#L294)

Starts the server and blocks until exit. Performs pre-flight checks, including SSL certificate validation/generation and scheduler startup.

**Example:**
```python
app.start()
```

---

For more on controllers and scheduled tasks, see:
- [Controller Documentation](./controller.md)
- [Scheduler Documentation](./scheduler.md)
- [Console Documentation](./console.md)