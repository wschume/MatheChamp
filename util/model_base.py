from dataclasses import dataclass, field
from typing import Any, Callable

from util.signal import ValueChangedSignal, Blocker


class ValueChangedEmitter:
    def __init__(self):
        self.value_changed = ValueChangedSignal(self)

    def _setattr(
        self, key: str, value: Any, setter: Callable[[Any], None] | None = None
    ):
        private_key = f"_{key}"
        if getattr(self, private_key) == value:
            return

        with Blocker.from_signal(self.value_changed):
            if setter is None:
                setattr(self, private_key, value)
            else:
                setter(value)

        self.value_changed.emit(self, key)

    async def _setattr_async(
        self, key: str, value: Any, setter: Callable[[Any], None] | None = None
    ):
        private_key = f"_{key}"

        if getattr(self, private_key) == value:
            return

        with Blocker.from_signal(self.value_changed):
            if setter is None:
                setattr(self, private_key, value)
            else:
                setter(value)

        await self.value_changed.emit_async(self, key)
