# Welcome to Quick API Builder Core

![Version](https://img.shields.io/pypi/v/qab-core?style=flat&logo=pypi)
![Coverage](https://sonar.lab.majyx.net/api/project_badges/measure?project=qab_core&metric=coverage)
![Status](https://sonar.lab.majyx.net/api/project_badges/measure?project=qab_core&metric=alert_status)
![Maintainability](https://sonar.lab.majyx.net/api/project_badges/measure?project=qab_core&metric=sqale_rating)
[![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=flat)](https://github.com/MaJyxSoftware/qab_core/blob/main/docs)
![Workflow](https://img.shields.io/github/workflow/status/MaJyxSoftware/qab_core/Test/main?style=flat&logo=github)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://github.com/MaJyxSoftware/qab_core/blob/main/LICENSE)
[![Twitter: MaJyxWorld](https://img.shields.io/twitter/follow/MaJyxWorld.svg?style=flat&logo=twitter)](https://twitter.com/MaJyxWorld)

 Quickly build secured and fast API

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

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/MaJyxSoftware/qab_core/issues). You can also take a look at the [contributing guide](https://github.com/MaJyxSoftware/qab_core/blob/main/CONTRIBUTE.md).

## Show your support

Give a like if this project helped you!

[![Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/heavensleep)

## License

Copyright © 2021 [MaJyx](https://www.majyx.net).

This project is [MIT](https://github.com/MaJyxSoftware/qab_core/blob/main/LICENSE) licensed.
