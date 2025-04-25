# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- Changes since v0.0.5:

## [v0.0.5] - 2025-04-25

### 🚀 Major Changes

- **Revamp Documentation & Structure:**
  - Complete overhaul of documentation for all core components (server, controller, scheduler, console, main README).
  - Improved navigation, usage examples, and cross-references.
  - Refactored core components, updated plugins structure, and improved error handling.
  - Reset file permissions to 644 for all files.
- **Compatibility:**
  - Updated support for Python 3.9–3.13 (tox, pyenv, CI, requirements).

### 🧪 Testing & CI

- Improved and expanded test coverage, added new test fixtures.
- Better test cleanup and route generation.
- Improved CORS and security tests.
- Upgraded GitHub Actions workflows:
  - Switched to official SonarQube scan step.
  - Updated to trusted PyPI publishing (OIDC).
  - Upgraded to latest GitHub Actions for checkout and setup-python.

### 🐛 Bug Fixes & Improvements

- Fixed security issue on tar open.
- Fixed infinite loop on auto log rotate.
- Fixed CORS tests to emulate AJAX requests.
- Fixed typo and ensured SSL generation is disabled in tests.
- Only add CORS headers if request is AJAX.
- Check at start if access log needs to be rotated.
- Removed unnecessary code and improved codebase cleanliness.

## [v0.0.4] - 2021-01-22

- Initial version up to tag v0.0.4 (see previous git history for details).
