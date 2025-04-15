from beeai_framework.adapters.litellm.chat import LiteLLMChatModel
from beeai_framework.backend.constants import ProviderName


class OllamaAIChatModel(LiteLLMChatModel):
    @property
    def provider_id(self) -> ProviderName:
        return "ollama"

    def __init__(self, model_id: str | None = None, settings: dict | None = None, model: str | None = None,
                 temperature=0):
        self.model = model,
        self.base_url = "http://localhost:11434/v1",
        self.api_key = "ollama",
        self.temperature = temperature

        _settings = settings.copy() if settings is not None else {}

        super().__init__(
            model_id=model_id,
            provider_id="ollama",
            settings=_settings,
        )
