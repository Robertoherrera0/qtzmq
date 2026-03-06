"""
Global stream registry for qtzmq.

Allows applications to create a named ZeroMQ stream once
and access it anywhere in the Qt application.
"""

from .subscriber import QtSubscriber
from .publisher import QtPublisher
from .requester import QtRequester
from .replier import QtReplier


_streams = {}

def subscribe(name, address, topic=""):
    """
    Create and start a named QtSubscriber stream.
    """

    if name in _streams:
        return _streams[name]

    sub = QtSubscriber(address, topic)
    sub.start()

    _streams[name] = sub
    return sub


def publish(name, address):
    """
    Create and start a named QtPublisher stream.
    """

    if name in _streams:
        return _streams[name]

    pub = QtPublisher(address)
    pub.start()

    _streams[name] = pub
    return pub


def request(name, address):
    """
    Create and start a named QtRequester stream.
    """
    if name in _streams:
        return _streams[name]

    req = QtRequester(address)

    _streams[name] = req
    return req


def reply(name, address):
    """
    Create and start a named QtReplier stream.
    """

    if name in _streams:
        return _streams[name]

    rep = QtReplier(address)
    rep.start()

    _streams[name] = rep
    return rep


def stream(name):
    """
    Retrieve an existing stream.
    """

    if name not in _streams:
        raise KeyError(
            f"Stream '{name}' does not exist. "
            "Create it first with subscribe(), publish(), request(), or reply()."
        )

    return _streams[name]


def streams():
    """
    Return a dictionary of all active streams.
    """

    return dict(_streams)


def stop(name):
    """
    Stop and remove a stream.
    """

    if name in _streams:
        _streams[name].stop()
        del _streams[name]


def stop_all():
    """
    Stop all active streams.
    """

    for s in list(_streams.values()):
        s.stop()

    _streams.clear()