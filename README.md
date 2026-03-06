# qtzmq

Qt-friendly ZeroMQ bindings for Python.

`qtzmq` provides lightweight wrappers around ZeroMQ sockets that expose incoming messages as Qt signals.  
It is designed for PySide6 and PyQt applications that need to consume streaming data without blocking the GUI thread.

The library handles:

- ZeroMQ socket setup
- background worker threads
- safe interaction with the Qt event loop
- clean message dispatch through Qt signals

## Why qtzmq?

When building Qt applications that use ZeroMQ, developers usually need to write the same boilerplate:

- create a ZeroMQ socket
- run a background thread
- receive messages
- emit Qt signals
- manage shutdown safely

`qtzmq` provides a small reusable layer that removes this boilerplate and exposes a simple API.

## API Overview

`qtzmq` manages ZeroMQ connections through a global registry.

An endpoint is created once and can then be accessed anywhere in the Qt application.

### Create an endpoint

subscribe(name, address)

publish(name, address)

request(name, address)

reply(name, address)

Each call creates a named endpoint and registers it internally.

### Access an endpoint

stream(name)

This returns the previously created endpoint.

Widgets and other components can then attach handlers or send messages through it.

Multiple Qt widgets can consume the same endpoint without managing sockets or threads directly.

See the `examples/` directory for complete usage examples.

## Installation

pip install qtzmq
