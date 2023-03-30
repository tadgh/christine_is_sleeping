import os
import sys
from contextlib import closing


from tts.api.TtsEngine import TtsEngine
from tts.elevenlabs.Client import Client
VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Elli": "MF3mGyEYCl7XYWbV9V6O",
    "Josh": "TxGEqnHWrfWFTfGW9XjX",
    "Arnold": "VR6AewLTigWG4xSOukaG",
    "Adam": "pNInz6obpgDQGcFmaJgB",
    "Sam": "yoZ06aMxZJJ28mfd3POQ",
    "Gary": "d9lgN8bDCShlVPABrBCa"
}

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

    @staticmethod
    def get_speaker_dict() -> dict:
        return VOICES



