"""This type stub file was generated by pyright.
"""

from typing import Any

from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1

def create_model(
    model_name: str,
    *,
    field_definitions: dict[str, Any] | None = ...,
    root: Any | None = ...,
) -> BaseModel | BaseModelV1:
    """Create a pydantic model with the given field definitions.

    Args:
        model_name: The name of the model.
        field_definitions: The field definitions for the model.
        root: Type for a root model (RootModel)
    """
