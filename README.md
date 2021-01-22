<h1 align="center">Welcome to Quick API Builder Core</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.0.2-blue.svg?cacheSeconds=2592000" />
  <img alt="Coverage" src="https://sonar.majyx.net/api/project_badges/measure?project=qab_core&metric=coverage">
  <img alt="Status" src="https://sonar.majyx.net/api/project_badges/measure?project=qab_core&metric=alert_status">
  <img alt="Maintainability" src="https://sonar.majyx.net/api/project_badges/measure?project=qab_core&metric=sqale_rating">
  <a href="https://github.com/MaJyxSoftware/qab_core/blob/main/docs" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <img alt="Workflow" src="https://img.shields.io/github/workflow/status/MaJyxSoftware/qab_core/Test/main" />
  <a href="https://github.com/MaJyxSoftware/qab_core/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/MaJyxWorld" target="_blank">
    <img alt="Twitter: MaJyxWorld" src="https://img.shields.io/twitter/follow/MaJyxWorld.svg?style=social" />
  </a>
</p>

> Quickly build secured and fast API

### [Homepage](https://github.com/MaJyxSoftware/qab_core)

## Install

```sh
pip install qab_core
```

## Usage

Make your controllers such as:

```python
from qab_core.controller import Controller

class TestController(Controller):
    
    def index(self):
        return "Hello world!"

    def hello(self, firstname, lastname=""):
        return f"Hello {firstname} {lastname}"
```

Then create the startup file, and run it as you wish:

```python
from qab_core.server import Server

from controllers.testcontrollers import TestController


def start():
    app = Server()
    
    TestController(app).register()

    app.start()

if __name__ == "__main__":
    start()
```

If you want more information, please, refer to the [documentation](https://github.com/MaJyxSoftware/qab_core/blob/main/docs)

## Run tests

### PyTest

```sh
pytest --cov=qab_core --cov-report=xml --cov-report=html
```

### TOX

```sh
tox
```

### SonarQube

```sh
sonar-scanner
```

## Author

**Benjamin Schwald**

* Website: https://www.majyx.net/
* Twitter: [@MaJyxWorld](https://twitter.com/MaJyxWorld)
* Github: [@HeavenSleep](https://github.com/HeavenSleep)
* LinkedIn: [@Benjamin SCHWALD](https://www.linkedin.com/in/benjamin-schwald-765ab0bb/)

## Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/MaJyxSoftware/qab_core/issues). You can also take a look at the [contributing guide](https://github.com/MaJyxSoftware/qab_core/blob/main/CONTRIBUTE.md).

## Show your support

Give a ⭐️ if this project helped you!

<a href="https://www.patreon.com/heavensleep">
  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## License

Copyright © 2021 [MaJyx](https://www.majyx.net).<br />
This project is [MIT](https://github.com/MaJyxSoftware/qab_core/blob/main/LICENSE) licensed.

***
