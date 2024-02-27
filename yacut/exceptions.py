from typing import Optional


class InvalidAPIUsageError(Exception):
    status_code = 400

    def __init__(
        self, message: str, status_code: Optional[int] = None
    ) -> None:
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict[str, str]:
        return dict(message=self.message)