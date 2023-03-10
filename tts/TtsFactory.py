from tts.polly.PollyEngine import PollyEngine
from tts.api.TtsEngine import TtsEngine

class TtsFactory:
    @staticmethod
    def get_engine(name) -> TtsEngine:
        if name == "polly":
            return PollyEngine(name)
        elif name == "elevenlabs":
            return PollyEngine(name)
