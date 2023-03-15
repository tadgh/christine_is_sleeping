import os

import requests

TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
class Client:
    def __init__(self, api_token):
        self._api_token = api_token

    def synthesize_speech(self, voice_id: str, content: str):
        headers = {
            "accept": "audio/mpeg",
            "xi-api-key": self._api_token,
            "Content-Type": "application/json"
        }
        data = {
            "text": content,
            "voice_settings": {
                "stability": 0,
                "similarity_boost": 0
            }
        }
        response = requests.post(url=TTS_URL + voice_id, headers=headers, json=data)
        if response.status_code == 200:
            return response
        else:
            raise RuntimeError("Couldnt hit the API!")

if __name__ == "__main__":
    client = Client(api_token=os.getenv("ELEVENLABS_KEY"))
    client.synthesize_speech("21m00Tcm4TlvDq8ikWAM", "Test!")

