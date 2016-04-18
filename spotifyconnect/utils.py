from __future__ import unicode_literals

import collections
import sys

from spotifyconnect import ffi, lib, serialized


PY2 = sys.version_info[0] == 2

if PY2:  # pragma: no branch
    string_types = (basestring,)  # noqa
    text_type = unicode  # noqa
    binary_type = str
else:
    string_types = (str,)
    text_type = str
    binary_type = bytes


class EventEmitter(object):

    """Mixin for adding event emitter functionality to a class."""

    def __init__(self):
        self._listeners = collections.defaultdict(list)

    @serialized
    def on(self, event, listener, *user_args):
        """Register a ``listener`` to be called on ``event``.

        The listener will be called with any extra arguments passed to
        :meth:`emit` first, and then the extra arguments passed to :meth:`on`
        last.

        If the listener function returns :class:`False`, it is removed and will
        not be called the next time the ``event`` is emitted.
        """
        self._listeners[event].append(
            _Listener(callback=listener, user_args=user_args))

    @serialized
    def off(self, event=None, listener=None):
        """Remove a ``listener`` that was to be called on ``event``.

        If ``listener`` is :class:`None`, all listeners for the given ``event``
        will be removed.

        If ``event`` is :class:`None`, all listeners for all events on this
        object will be removed.
        """
        if event is None:
            events = self._listeners.keys()
        else:
            events = [event]
        for event in events:
            if listener is None:
                self._listeners[event] = []
            else:
                self._listeners[event] = [
                    l for l in self._listeners[event]
                    if l.callback != listener]

    def emit(self, event, *event_args):
        """Call the registered listeners for ``event``.

        The listeners will be called with any extra arguments passed to
        :meth:`emit` first, and then the extra arguments passed to :meth:`on`
        """
        listeners = self._listeners[event][:]
        for listener in listeners:
            args = list(event_args) + list(listener.user_args)
            result = listener.callback(*args)
            if result is False:
                self.off(event, listener.callback)

    def num_listeners(self, event=None):
        """Return the number of listeners for ``event``.

        Return the total number of listeners for all events on this object if
        ``event`` is :class:`None`.
        """
        if event is not None:
            return len(self._listeners[event])
        else:
            return sum(len(l) for l in self._listeners.values())

    def call(self, event, *event_args):
        """Call the single registered listener for ``event``.

        The listener will be called with any extra arguments passed to
        :meth:`call` first, and then the extra arguments passed to :meth:`on`

        Raises :exc:`AssertionError` if there is none or multiple listeners for
        ``event``. Returns the listener's return value on success.
        """
        # XXX It would be a lot better for debugging if this error was raised
        # when registering the second listener instead of when the event is
        # emitted.
        assert self.num_listeners(event) == 1, (
            'Expected exactly 1 event listener, found %d listeners' %
            self.num_listeners(event))
        listener = self._listeners[event][0]
        args = list(event_args) + list(listener.user_args)
        return listener.callback(*args)


class _Listener(collections.namedtuple(
        'Listener', ['callback', 'user_args'])):

    """An listener of events from an :class:`EventEmitter`"""


class IntEnum(int):

    """An enum type for values mapping to integers.

    Tries to stay as close as possible to the enum type specified in
    :pep:`435` and introduced in Python 3.4.
    """

    def __new__(cls, value):
        if not hasattr(cls, '_values'):
            cls._values = {}
        if value not in cls._values:
            cls._values[value] = int.__new__(cls, value)
        return cls._values[value]

    def __repr__(self):
        if hasattr(self, '_name'):
            return '<%s.%s: %d>' % (self.__class__.__name__, self._name, self)
        else:
            return '<Unknown %s: %d>' % (self.__class__.__name__, self)

    @classmethod
    def add(cls, name, value):
        """Add a name-value pair to the enumeration."""
        attr = cls(value)
        attr._name = name
        setattr(cls, name, attr)


def make_enum(lib_prefix, enum_prefix=''):
    """Class decorator for automatically adding enum values.

    The values are read directly from the :attr:`spotify.lib` CFFI wrapper
    around libspotify. All values starting with ``lib_prefix`` are added. The
    ``lib_prefix`` is stripped from the name. Optionally, ``enum_prefix`` can
    be specified to add a prefix to all the names.
    """

    def wrapper(cls):
        for attr in dir(lib):
            if attr.startswith(lib_prefix):
                name = attr.replace(lib_prefix, enum_prefix)
                cls.add(name, getattr(lib, attr))
        return cls
    return wrapper


def to_bytes(value):
    """Converts bytes, unicode, and C char arrays to bytes.

    Unicode strings are encoded to UTF-8.
    """
    if isinstance(value, text_type):
        return value.encode('utf-8')
    elif isinstance(value, ffi.CData):
        return ffi.string(value)
    elif isinstance(value, binary_type):
        return value
    else:
        raise ValueError('Value must be text, bytes, or char[]')


def to_bytes_or_none(value):
    """Converts C char arrays to bytes and C NULL values to None."""
    if value == ffi.NULL:
        return None
    elif isinstance(value, ffi.CData):
        return ffi.string(value)
    else:
        raise ValueError('Value must be char[] or NULL')


def to_char(value):
    """Converts bytes, unicode, and C char arrays to C char arrays.  """
    return ffi.new('char[]', to_bytes(value))


def to_char_or_null(value):
    """Converts bytes, unicode, and C char arrays to C char arrays, and
    :class:`None` to C NULL values.
    """
    if value is None:
        return ffi.NULL
    else:
        return to_char(value)


def to_unicode(value):
    """Converts bytes, unicode, and C char arrays to unicode strings.

    Bytes and C char arrays are decoded from UTF-8.
    """
    if isinstance(value, ffi.CData):
        return ffi.string(value).decode('utf-8')
    elif isinstance(value, binary_type):
        return value.decode('utf-8')
    elif isinstance(value, text_type):
        return value
    else:
        raise ValueError('Value must be text, bytes, or char[]')


def to_unicode_or_none(value):
    """Converts C char arrays to unicode and C NULL values to None.

    C char arrays are decoded from UTF-8.
    """
    if value == ffi.NULL:
        return None
    elif isinstance(value, ffi.CData):
        return ffi.string(value).decode('utf-8')
    else:
        raise ValueError('Value must be char[] or NULL')
