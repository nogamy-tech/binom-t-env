# libraries
from pathlib import Path
from typing import Union
from pydantic import BaseModel, ValidationError
import json
import base64


#  PYDANTIC class
class LLMResponse(BaseModel):
    chain_of_thought: str
    final_answer: bool
    confidence: int


# -----------------
# UTILITY FUNCTIONS
def base64_to_context(base64_str: str, model: str) -> Union[bytes, str]:
    """
    Decodes from base 64 to bytes or string (depending on the model type)
    """
    # Decode base64 to bytes
    decoded_bytes = base64.b64decode(base64_str)

    if model == "text":
        context = decoded_bytes.decode("utf-8")

    elif model == "image":
        context = decoded_bytes

    else:
        raise ValueError("model type is not supported")

    return context


def render_prompt(template_path: Union[str, Path], context: str, query: str, few_shots: str) -> str:
    """
    Reads a prompt template file and replaces <context>, <query>, and <few_shots> placeholders.
    """
    template = Path(template_path).read_text(encoding="utf-8")
    return template.replace("<context>", context).replace("<query>", query).replace("<few_shots>", few_shots or "")


def parse_as_json(answer: str) -> LLMResponse:
    """
    Extracts a JSON block from a model response and parses it using the LLMResponse schema.
    """
    raw = answer.strip()
    try:
        json_str = raw.split("```json")[1].split("```")[0].strip()
        data = json.loads(json_str)
        return LLMResponse(**data)
    except (IndexError, json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Failed to parse LLM output as LLMResponse:\n{raw}") from e


# -----------------
