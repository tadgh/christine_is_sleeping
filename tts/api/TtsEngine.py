import abc


class TtsEngine(abc.ABC):
    @abc.abstractmethod
    def get_audio(self, content: str) -> str:
        """

        :param content: The string content to convert to Speech.
        :return: The location of the MP3 file to play.
        """


