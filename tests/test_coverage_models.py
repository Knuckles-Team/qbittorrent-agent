import inspect
from typing import Any

from pydantic import BaseModel


def test_qbittorrent_models_coverage():
    """Verify deserialization of all declarative Pydantic schemas in qbittorrent_models.

    CONCEPT:AU-OS.governance.reactive-multi-axis-budget — Guardrail Engine / Session Concurrency
    """
    from qbittorrent_agent import qbittorrent_models

    for name, obj in inspect.getmembers(qbittorrent_models, inspect.isclass):
        if issubclass(obj, BaseModel) and obj is not BaseModel:
            kwargs = _synthesize_model_kwargs(obj)
            try:
                inst = obj(**kwargs)
                assert isinstance(inst, obj)
            except Exception as e:
                print(f"Operation failed: {type(e).__name__}")
                raise e


def _default_value_for_field(field: Any) -> Any:
    """Synthesize a plausible value for a required pydantic field, by annotation text."""
    anno_str = str(field.annotation)
    if "list" in anno_str or "List" in anno_str:
        return []
    if "dict" in anno_str or "Dict" in anno_str:
        return {}
    if "int" in anno_str:
        return 1
    if "float" in anno_str:
        return 1.0
    if "bool" in anno_str:
        return True
    return "test"


def _synthesize_model_kwargs(obj: type[BaseModel]) -> dict[str, Any]:
    """Build kwargs covering every required field of a pydantic BaseModel subclass."""
    kwargs: dict[str, Any] = {}
    for field_name, field in obj.model_fields.items():
        if field.is_required():
            kwargs[field_name] = _default_value_for_field(field)
    return kwargs
