import asyncio
from pathlib import Path

import yaml
from litellm import get_llm_provider

_CONFIG_PATH = Path(__file__).parent / "config.yaml"

with open(_CONFIG_PATH) as f:
    _config = yaml.safe_load(f)

_semaphores: dict[str, asyncio.Semaphore] = {}


def get_provider(model: str) -> str:
    """Resolve the provider name for a model string using LiteLLM."""
    return get_llm_provider(model)[1]


def get_semaphore(model: str) -> asyncio.Semaphore:
    """Return the shared semaphore for the model's provider, creating it on first use."""
    provider = get_provider(model)
    if provider not in _semaphores:
        limits = _config["semaphores"]
        if provider not in limits:
            raise ValueError(
                f"No semaphore configured for provider '{provider}' (model '{model}'). "
                f"Add it to {_CONFIG_PATH}."
            )
        _semaphores[provider] = asyncio.Semaphore(limits[provider])
    return _semaphores[provider]
