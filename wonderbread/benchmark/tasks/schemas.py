"""
Pydantic models for structured JSON output across all benchmark tasks.
These schemas ensure reliable parsing of model responses.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


# ============================================================================
# Demo Segmentation Schemas
# ============================================================================

class SegmentationUUIDResponse(BaseModel):
    """Schema for UUID-based workflow segmentation.

    Maps each UUID to a workflow classification letter (A, B, C, etc.).
    Example: {"UUID_0": "A", "UUID_1": "A", "UUID_2": "B"}
    """
    class Config:
        extra = "allow"  # Allow dynamic UUID keys

    def model_dump(self, **kwargs):
        """Override to return the raw dict for UUID mappings."""
        return super().model_dump(**kwargs)


class WorkflowRange(BaseModel):
    """Start and end UUID range for a workflow."""
    start: int = Field(description="Starting UUID for this workflow")
    end: int = Field(description="Ending UUID for this workflow")


class SegmentationStartEndResponse(BaseModel):
    """Schema for start/end-based workflow segmentation.

    Maps each workflow letter to its start and end UUIDs.
    Example: {"A": {"start": 0, "end": 5}, "B": {"start": 6, "end": 10}}
    """
    class Config:
        extra = "allow"  # Allow dynamic workflow letter keys (A, B, C, etc.)

    def model_dump(self, **kwargs):
        """Override to return the raw dict for workflow mappings."""
        return super().model_dump(**kwargs)


# ============================================================================
# Demo Validation Schemas
# ============================================================================

class DemoCompletionResponse(BaseModel):
    """Schema for validating if a workflow was successfully completed."""
    thinking: str = Field(description="Step-by-step reasoning about completion status")
    was_completed: bool = Field(description="Whether the workflow was successfully completed")


class DemoAccuracyResponse(BaseModel):
    """Schema for validating if a workflow accurately followed the SOP."""
    thinking: str = Field(description="Step-by-step reasoning about accuracy")
    inaccurate_steps: Optional[List[str]] = Field(
        default=None,
        description="List of steps that were performed inaccurately or out of order"
    )
    was_accurate: bool = Field(description="Whether the SOP was accurately followed")


# ============================================================================
# SOP Ranking Schema
# ============================================================================

class SOPRankingResponse(BaseModel):
    """Schema for ranking SOPs by quality."""
    thinking: str = Field(description="Step-by-step reasoning about the ranking")
    pred_ranking: List[int] = Field(
        description="List of SOP IDs ranked from best to worst. First ID is best, last is worst."
    )


def get_json_schema(model_class: type[BaseModel], schema_name: str, strict: bool = False) -> Dict:
    """
    Convert a Pydantic model to OpenRouter-compatible JSON schema format.

    Args:
        model_class: The Pydantic model class
        schema_name: Name for the schema
        strict: Whether to use strict mode. Default False because strict mode doesn't support
                dynamic keys (additionalProperties), which some schemas need.

    Returns:
        Dict formatted for OpenRouter's json_schema response_format
    """
    schema = model_class.model_json_schema()

    # Remove title if it exists (some APIs don't like it)
    schema.pop('title', None)

    return {
        "type": "json_schema",
        "json_schema": {
            "name": schema_name,
            "strict": strict,
            "schema": schema
        }
    }
