import abc


class TtsEngine(abc.ABC):
    @abc.abstractmethod
    def get_audio(self, content: str) -> str:
        """

        :param content: The string content to convert to Speech.
        :return: The location of the MP3 file to play.
        """
    @staticmethod
    def get_speaker_dict() -> dict:
        """

        :return: A dictionary of display name -> speaker ID that the current TTS engine supports
        """

