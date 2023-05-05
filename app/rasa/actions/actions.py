from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from dotenv import load_dotenv
from logging import getLogger
from enum import IntEnum
import os

logger = getLogger(__name__)

env = os.getenv("ENV", "local")
env_file = f".env-{env}"
load_dotenv(dotenv_path=f"../../.env-{env}")


MODEL_NAME = os.getenv("MODEL_NAME")
CHANNEL_TYPE = IntEnum(
    "CHANNEL_TYPE", ["SMS", "TELEGRAM", "WHATSAPP", "EMAIL", "WEBSITE"]
)

logger = getLogger(__name__)


class ActionGPTFallback(Action):
    def name(self) -> str:
        return "action_gpt_fallback"

    def get_channel(self, channel: str) -> CHANNEL_TYPE:
        if channel == "telegram":
            return CHANNEL_TYPE.TELEGRAM
        elif channel == "whatsapp":
            return CHANNEL_TYPE.WHATSAPP
        elif channel == "sms":
            return CHANNEL_TYPE.SMS
        elif channel == "email":
            return CHANNEL_TYPE.EMAIL
        else:
            return CHANNEL_TYPE.WEBSITE

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # ------------
        # Get metadata
        # ------------
        data = tracker.latest_message
        metadata = data['metadata'] if data and 'metadata' in data else None
        response = metadata['response'] if metadata and 'response' in metadata else None
        tags = metadata['tags'] if metadata and 'tags' in metadata else None
        is_escalate = (
            metadata['is_escalate'] if metadata and 'is_escalate' in metadata else None
        )

        if is_escalate is True:
            response = f'{response} \n\n ⚠️💁 [ESCALATE TO HUMAN]'

        if tags is not None:
            response = f'{response} \n\n 🏷️  {",".join(tags)}'

        logger.debug(
            f"""[🤖 ActionGPTFallback]
        data: {data}
        metadata: {metadata}
        response: {response}
        tags: {tags}
        is_escalate: {is_escalate}
        """
        )
        dispatcher.utter_message(text=response)
        return []
