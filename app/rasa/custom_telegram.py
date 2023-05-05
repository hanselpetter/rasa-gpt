from rasa.core.channels.telegram import TelegramInput
from rasa.shared.utils import common as rasa_common
from typing import Any, Dict, Optional, Text
from sanic.request import Request


class CustomTelegramInput(TelegramInput):

    def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:

        # For whatever reason, Rasa is unable to pass data via 'metadata' so 'meta' works for now
        metadata = request.json.get('message', {}).get('meta')

        # Debug
        rasa_common.logger.debug(f'[🤖 ActionGPTFallback]\nmetadata: {metadata}')
        return metadata if metadata is not None else None
