# 🚀 Quick API Builder Core (QAB Core)

[![PyPI Version](https://img.shields.io/pypi/v/qab-core?style=flat&logo=pypi)](https://pypi.org/project/qab-core/)
[![Coverage](https://sonar.majyx.net/api/project_badges/measure?project=qab_core&metric=coverage)](https://sonar.majyx.net/dashboard?id=qab_core)
[![Quality Gate](https://sonar.majyx.net/api/project_badges/measure?project=qab_core&metric=alert_status)](https://sonar.majyx.net/dashboard?id=qab_core)
[![Maintainability](https://sonar.majyx.net/api/project_badges/measure?project=qab_core&metric=sqale_rating)](https://sonar.majyx.net/dashboard?id=qab_core)
[![Documentation](https://img.shields.io/badge/documentation-yes-brightgreen.svg?style=flat)](https://github.com/MaJyxSoftware/qab_core/blob/main/docs)
[![Build Status](https://img.shields.io/github/actions/workflow/status/MaJyxSoftware/qab_core/Test/main?style=flat&logo=github)](https://github.com/MaJyxSoftware/qab_core/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://github.com/MaJyxSoftware/qab_core/blob/main/LICENSE)
[![Twitter: MaJyxWorld](https://img.shields.io/twitter/follow/MaJyxWorld.svg?style=flat&logo=twitter)](https://twitter.com/MaJyxWorld)

> **Quickly build secure and blazing-fast APIs with Python.**  
> QAB Core is built on top of [Bottle](https://bottlepy.org/) and uses [Gunicorn](https://gunicorn.org/) for production performance.

---

## ✨ Features

- ⚡ **Ultra-fast API creation** with minimal boilerplate
- 🔒 **Secure by default** (SSL, best practices)
- 🧩 **Pluggable architecture** for controllers and extensions
- 🧪 **Easy testing** with Pytest & Tox
- 📈 **Built-in code coverage & SonarQube support**
- 📝 **Comprehensive documentation**

---

## 📦 Installation

```sh
pip install qab_core
```

---

## 🚀 Quick Start

### 1. Create a Controller

```python
from qab_core.controller import Controller

class TestController(Controller):
    def index(self):
        return "Hello world!"

    def hello(self, firstname, lastname=""):
        return f"Hello {firstname} {lastname}"
```

### 2. Create a Startup File

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

---

## 🧪 Running Tests

**With Pytest:**

```sh
pytest --cov=qab_core --cov-report=xml --cov-report=html
```

**With Tox:**

```sh
tox
```

**With SonarQube:**

```sh
sonar-scanner
```

---

## 📚 Documentation

Full documentation is available [here](https://github.com/MaJyxSoftware/qab_core/blob/main/docs).

---

## 👤 Author

> **Benjamin Schwald**

- 🌐 [majyx.net](https://www.majyx.net/)
- 🐦 [@MaJyxWorld](https://twitter.com/MaJyxWorld)
- 💼 [LinkedIn](https://www.linkedin.com/in/benjamin-schwald-765ab0bb/)
- 💻 [GitHub](https://github.com/HeavenSleep)

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome!  
Check the [issues page](https://github.com/MaJyxSoftware/qab_core/issues) or see the [contributing guide](https://github.com/MaJyxSoftware/qab_core/blob/main/CONTRIBUTE.md).

---

## 💖 Show your support

If you find this project useful, please give it a ⭐️ or consider supporting:

[![Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/heavensleep)

---

## 📝 License

Copyright © 2021-2025 [MaJyx](https://www.majyx.net).

This project is [MIT](https://github.com/MaJyxSoftware/qab_core/blob/main/LICENSE) licensed.
