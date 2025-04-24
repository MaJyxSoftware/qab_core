# Console

[[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/console.py#L28)]

- [Console](#console)
  - [Description](#description)
  - [Methods](#methods)
    - [log(text, log_type)](#logtext-log_type)
    - [Error](#error)
    - [Debug](#debug)

## Description

The `Console` is used to log the application and alos manage it's own lifecycle (log rotation and compression).

It's binded to the application and therefor accessible to any controller.

It has few methods to allow you to quickly trace your application.

## Methods

### log(text, log_type)

[[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/console.py#L44)]

The `log` method is the main method to use to log. It takes a first arguement as `text` and an optional argument as `log_type` (`"INFO"` by default).

Usage from your controller:

```python
class DemoController(Controller):
  ...

  def index(self):
    self.app.console.log("Hello from index of my controller")

    try:
      ...
    except:
      self.app.console.log("Error handled as expected", log_type="WARN")
```

### Error

[[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/console.py#L69)]



### Debug

[[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/console.py#L44)]