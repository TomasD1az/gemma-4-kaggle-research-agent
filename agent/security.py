from __future__ import annotations

import socket
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Iterator


@dataclass
class NetworkMonitor:
    attempts: int = 0


_network_monitor_lock = threading.Lock()


@contextmanager
def monitor_external_calls() -> Iterator[NetworkMonitor]:
    monitor = NetworkMonitor()
    original_create_connection: Callable[..., object]

    _network_monitor_lock.acquire()
    original_create_connection = socket.create_connection

    try:
        def tracked_create_connection(*args, **kwargs):
            monitor.attempts += 1
            return original_create_connection(*args, **kwargs)

        socket.create_connection = tracked_create_connection
        yield monitor
    finally:
        socket.create_connection = original_create_connection
        _network_monitor_lock.release()
