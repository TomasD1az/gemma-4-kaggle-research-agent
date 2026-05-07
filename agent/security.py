from __future__ import annotations

import socket
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Callable, Iterator


@dataclass
class NetworkMonitor:
    attempts: int = 0


@contextmanager
def monitor_external_calls() -> Iterator[NetworkMonitor]:
    monitor = NetworkMonitor()
    original_create_connection: Callable[..., object] = socket.create_connection

    def tracked_create_connection(*args, **kwargs):
        monitor.attempts += 1
        return original_create_connection(*args, **kwargs)

    socket.create_connection = tracked_create_connection
    try:
        yield monitor
    finally:
        socket.create_connection = original_create_connection
