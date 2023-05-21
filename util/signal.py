from typing import Any, Callable, TypeVar


class Signal:
    def __init__(self, obj: Any):
        self._object = obj
        self._slots: list[Callable] = []
        self._blocked = False

    def connect(self, slot: Callable | "Signal"):
        self._slots.append(slot)

    def disconnect(self, slot: Callable):
        self._slots.remove(slot)

    @property
    def object(self) -> Any:
        return self._object

    @property
    def blocked(self) -> bool:
        return self._blocked

    @blocked.setter
    def blocked(self, value: bool):
        self._blocked = value

    def emit(self, *args, **kwargs):
        if self._blocked:
            return

        for slot in self._slots:
            if isinstance(slot, Signal):
                slot.emit(*args, **kwargs)
            else:
                slot(*args, **kwargs)

    async def emit_async(self, *args, **kwargs):
        if self._blocked:
            return

        for slot in self._slots:
            if isinstance(slot, Signal):
                slot.emit(*args, **kwargs)
            else:
                await slot(*args, **kwargs)


T = TypeVar("T")


class ValueChangedSignal(Signal):
    def emit(self, value: T, key: str):
        super().emit(value, key)

    async def emit_async(self, value: T, key: str):
        await super().emit_async(value, key)


class Blocker:
    _block_status: list[bool]

    def __init__(self, signals: list[Signal]):
        self._signals = signals

    @classmethod
    def from_signal(cls, signal: Signal) -> "Blocker":
        return cls([signal])

    def __enter__(self) -> "Blocker":
        self._block_status = [signal.blocked for signal in self._signals]

        for signal in self._signals:
            signal.blocked = True

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        for signal, status in zip(self._signals, self._block_status):
            signal.blocked = status
