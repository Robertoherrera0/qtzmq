from .subscriber import QtSubscriber
from .publisher import QtPublisher
from .requester import QtRequester
from .replier import QtReplier


_streams = {}


def _ensure(name):
    if name not in _streams:
        _streams[name] = {}
    return _streams[name]


def subscribe(name, address, topic=""):
    entry = _ensure(name)

    if "sub" in entry:
        return entry["sub"]

    sub = QtSubscriber(address, topic)
    sub.start()

    entry["sub"] = sub

    # bridge existing requester (if already created)
    if "req" in entry:
        entry["req"].response.connect(lambda resp: sub.message.emit(resp))

    return sub


def publish(name, address):
    entry = _ensure(name)

    if "pub" in entry:
        return entry["pub"]

    pub = QtPublisher(address)
    entry["pub"] = pub
    return pub


def request(name, address):
    entry = _ensure(name)

    if "req" in entry:
        return entry["req"]

    req = QtRequester(address)
    entry["req"] = req

    # bridge into subscriber if exists
    if "sub" in entry:
        sub = entry["sub"]
        req.response.connect(lambda resp: sub.message.emit(resp))

    return req


def reply(name, address):
    entry = _ensure(name)

    if "rep" in entry:
        return entry["rep"]

    rep = QtReplier(address)
    rep.start()

    entry["rep"] = rep
    return rep


def stream(name):
    if name not in _streams or "sub" not in _streams[name]:
        raise KeyError(
            f"Stream '{name}' has no subscriber. "
            "Call subscribe(name, ...) first."
        )

    return _streams[name]["sub"]


def requester(name):
    if name not in _streams or "req" not in _streams[name]:
        raise KeyError(
            f"Stream '{name}' has no requester. "
            "Call request(name, ...) first."
        )

    return _streams[name]["req"]


def streams():
    return dict(_streams)


def stop(name):
    if name in _streams:
        entry = _streams[name]

        for obj in entry.values():
            if hasattr(obj, "stop"):
                obj.stop()

        del _streams[name]


def stop_all():
    for entry in list(_streams.values()):
        for obj in entry.values():
            if hasattr(obj, "stop"):
                obj.stop()

    _streams.clear()