# Examples

This directory contains small examples demonstrating how to use **qtzmq** with Qt applications.

## Publisher / Subscriber

### publisher_test.py

Simple ZeroMQ publisher that sends JSON messages.

Run:

python examples/publisher_test.py

### subscriber_test.py

Qt application that subscribes to the publisher and displays messages.

Run in another terminal:

python examples/subscriber_test.py

## Multi-Widget Example

### multi_widget_publisher.py

Publishes two message types:

- metadata
- status

Run:

python examples/multi_widget_publisher.py

### multi_widget_subscriber.py

Qt GUI with two widgets consuming the same stream.

MetadataWidget displays metadata messages.

StatusWidget logs status updates.

Run:

python examples/multi_widget_subscriber.py

This example demonstrates the core idea of qtzmq:

One ZMQ stream → multiple Qt widgets.


## Request / Reply

### replier_test.py

Simple service that receives requests and sends replies.

Run:

python examples/replier_test.py

### request_test.py

Qt GUI that sends a request and displays the reply.

Run:

python examples/request_test.py


## Running the Examples

Some examples require two terminals.

Example workflow:

Terminal 1:

python examples/multi_widget_publisher.py

Terminal 2:

python examples/multi_widget_subscriber.py


## Requirements

pip install pyzmq PySide6

## Notes
These examples are intentionally minimal and are meant to demonstrate how qtzmq integrates ZeroMQ messaging with the Qt event loop.