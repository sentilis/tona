from typing import Any

class TonaException(Exception):

    def __init__(self, code: int, detail: Any = None) -> None:
        self.code = code
        self.detail = detail
        super().__init__(*[code, detail])
