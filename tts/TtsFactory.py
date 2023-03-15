from tts.elevenlabs.ElevenLabsEngine import ElevenLabsEngine
from tts.polly.PollyEngine import PollyEngine
from tts.api.TtsEngine import TtsEngine

class TtsFactory:
    @staticmethod
    def get_engine(name: str , voice: str ) -> TtsEngine:
        if name == "polly":
            return PollyEngine(voice)
        elif name == "elevenlabs":
            return ElevenLabsEngine(voice)
