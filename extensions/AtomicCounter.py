"""An atomic, thread-safe incrementing counter."""

import threading


class AtomicCounter:
    """An atomic, thread-safe incrementing counter.
    >>> counter = AtomicCounter()
    >>> counter.increment()
    1
    >>> counter.increment(4)
    5
    >>> counter = AtomicCounter(42)
    >>> counter.value
    42
    >>> counter.increment(1)
    43
    >>> counter.decrement(1)
    42
    >>> counter.compare(42)
    True
    >>> counter.compare(43)
    False
    >>> counter = AtomicCounter()
    >>> def incrementor():
    ...     for i in range(100000):
    ...         counter.increment()
    >>> threads = []
    >>> for i in range(4):
    ...     thread = threading.Thread(target=incrementor)
    ...     thread.start()
    ...     threads.append(thread)
    >>> for thread in threads:
    ...     thread.join()
    >>> counter.value
    400000
    """

    def __init__(self, initial=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self.value = initial
        self._lock = threading.Lock()

    def increment(self, num=1) -> int:
        """Atomically increment the counter by num (default 1) and return the
        new value.
        """
        with self._lock:
            self.value += num
            return self.value

    def decrement(self, num=1) -> int:
        """Atomically decrements the counter by num (default 1) and return the
        new value.
        """
        with self._lock:
            self.value -= num
            return self.value

    def compare(self, num) -> bool:
        """
        Atomically compares value with given num.
        """
        with self._lock:
            return self.value == num
