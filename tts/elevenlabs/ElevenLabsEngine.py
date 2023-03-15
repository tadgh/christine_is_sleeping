import os
import sys
from contextlib import closing


from tts.api.TtsEngine import TtsEngine
from tts.elevenlabs.Client import Client


class ElevenLabsEngine(TtsEngine):
    def __init__(self, speaker: str):
        api_token = os.getenv("ELEVENLABS_KEY")
        self.client = Client(api_token)
        self.speaker = speaker

    def get_audio(self, content: str) -> str:
        response = self.client.synthesize_speech(voice_id=self.speaker, content=content)
        output = os.path.join(os.getcwd(), "elevenlabs.mp3")
        with open(output, "wb") as file:
            file.write(response.content)
        return output

