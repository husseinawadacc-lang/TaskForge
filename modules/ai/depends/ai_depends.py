
from modules.ai.service.ai_service import AIService


def get_ai_service() -> AIService:
    """
    Provide AIService instance

    🔥 لاحقًا:
    - ممكن نحقن OpenAI client
    - أو config
    - أو caching layer
    """
    return AIService()