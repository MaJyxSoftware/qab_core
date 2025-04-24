# Scheduler

[Source](https://github.com/MaJyxSoftware/qab_core/blob/main/qab_core/scheduler.py#L11)

[← Back to Main Documentation](./README.md)

## About This Document

This file documents the `Scheduler` class, its methods, and how to use it for background and periodic tasks. For API endpoints, see [controller.md](./controller.md). For server setup, see [server.md](./server.md).

- [Scheduler](#scheduler)
  - [Description](#description)
  - [Methods](#methods)
    - [start() -> None](#start---none)
    - [stop() -> None](#stop---none)
    - [add(recurrence, func, *args, **kwargs) -> None](#addrecurrence-func-args-kwargs---none)

## Description

The `Scheduler` class manages background and periodic tasks for the application. It uses thread pools to execute scheduled jobs concurrently and supports cron-style recurrence for flexible scheduling. Tasks can be started, stopped, and added dynamically.

## Methods

### start() -> None

Starts the scheduler, enabling execution of all registered tasks according to their recurrence schedule.

**Signature:**
```python
def start(self) -> None:
```
**Example:**
```python
app.scheduler.start()
```

### stop() -> None

Stops the scheduler and waits for all running tasks to finish. This is typically called during application shutdown.

**Signature:**
```python
def stop(self) -> None:
```
**Example:**
```python
app.scheduler.stop()
```

### add(recurrence, func, *args, **kwargs) -> None

Adds a new scheduled task. The `recurrence` parameter uses cron syntax (e.g., "0 0 * * *" for daily). The `func` is the function to execute, with optional positional and keyword arguments.

**Signature:**
```python
def add(self, recurrence, func, *args, **kwargs) -> None:
```
- `recurrence`: Cron-style string defining when the task should run.
- `func`: Callable to execute.
- `*args`, `**kwargs`: Arguments passed to the callable.

**Example:**
```python
def backup():
    print("Performing backup...")

app.scheduler.add("0 3 * * *", backup)
```

**Exceptions:**
- Raises `SchedulerInvalidTaskError` if the recurrence string is invalid.

---

[← Back to Main Documentation](./README.md)