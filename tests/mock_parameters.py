from typing import Any


class MockParameters:
    def __init__(self, **attributes: dict[str, Any]) -> None:
        for field_name, field_value in attributes.items():
            setattr(self, field_name, field_value)
