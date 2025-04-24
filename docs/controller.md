# Controler

[[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/controller.py#L5)]

- [Controler](#controler)
  - [About This Document](#about-this-document)
  - [Description](#description)
  - [Methods](#methods)
    - [Register](#register)
    - [Render](#render)
    - [Abort](#abort)


[← Back to Main Documentation](./README.md)

## About This Document

This file documents the `Controller` class, its main methods, and how to use it to handle API routes and responses. For route registration, see also [server.md](./server.md). For background/scheduled tasks, see [scheduler.md](./scheduler.md).

## Description

The `Controller` class is the base class for all controllers in the QAB Core framework. It provides essential methods for registering controllers, rendering responses, and handling errors. Each controller is associated with an application instance and can define its own content type for responses.

## Methods

### Register

Registers the current controller with the application. This enables the automatic route registration for all public methods in the controller.

**Signature:**
```python
def register(self):
```
**Example:**
```python
class MyController(Controller):
    ...

my_controller = MyController(app)
my_controller.register()
```

### Render

Renders a response to the client. Supports both JSON and non-JSON (e.g., HTML) responses. For JSON, it wraps the data in a standard structure; for other types, it sets the appropriate content type and headers.

**Signature:**
```python
def render(self, msg, data=None, status="success", code=200):
```
- `msg`: Message string to include in the response.
- `data`: Data to return (dict/str/other). If a string, returned as-is with the controller's content type.
- `status`: Status string (default: "success").
- `code`: HTTP status code (default: 200).

**Example:**
```python
def index(self):
    return self.render("Welcome!", {"hello": "world"})
```

### Abort

Sends an error response to the client with a given HTTP status code and error message. Uses the `render` method internally.

**Signature:**
```python
def abort(self, code=404, text="Not found"):
```
- `code`: HTTP status code (default: 404).
- `text`: Error message (default: "Not found").

**Example:**
```python
def get_user(self, user_id):
    user = find_user(user_id)
    if not user:
        return self.abort(404, "User not found")
    ...
```

---

[← Back to Main Documentation](./README.md)
