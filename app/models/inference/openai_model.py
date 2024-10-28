import os

from langchain_openai import ChatOpenAI as BaseChatOpenAI


class ChatOpenAI(BaseChatOpenAI):
    """A wrapper for the `langchain_aws.ChatOpenAI`."""

    def __init__(self, **kwargs):
        """Initialize the `ChatOpenAI` with specific configuration."""
        
        default_kwargs = {
            'model': os.environ['LLM_MODEL_ID'],
            'temperature': 0,
        }

        super().__init__(**(default_kwargs | kwargs))
