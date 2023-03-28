import os
import sys
from contextlib import closing

from boto3 import Session

from tts.api.TtsEngine import TtsEngine

VOICES = ["Lotte", "Maxim", "Ayanda", "Salli", "Ola", "Arthur", "Tomoko", "Remi", "Geraint", "Miguel", "Giorgio", "Marlene", "Ines", "Kajal", "Zhiyu", "Zeina", "Karl", "Gwyneth", "Joanna", "Lucia", "Cristiano", "Astrid", "Andres", "Vicki", "Mia", "Vitoria", "Bianca", "Chantal", "Raveena", "Daniel", "Amy", "Liam", "Ruth", "Kevin", "Brian", "Russell", "Aria", "Matthew", "Aditi", "Dora", "Enrique", "Hans", "Carmen", "Ivy", "Ewa", "Maja", "Gabrielle", "Nicole", "Filiz", "Camila", "Jacek", "Thiago", "Justin", "Celine", "Kazuha", "Kendra", "Arlet", "Ricardo", "Mads", "Hannah", "Mathieu", "Lea", "Sergio", "Hala", "Tatyana", "Penelope", "Naja", "Olivia", "Ruben", "Laura", "Takumi", "Mizuki", "Carla", "Conchita", "Jan", "Kimberly", "Liv", "Adriano", "Lupe", "Joey", "Pedro", "Seoyeon", "Emma", "Stephen"]


class PollyEngine(TtsEngine):
    @staticmethod
    def get_speaker_dict() -> dict:
        return {voice: voice for voice in VOICES}

    def __init__(self, speaker: str):
        session = Session()
        self.polly = session.client("polly")
        self.speaker = speaker
    def get_audio(self, content: str) -> str:
        response = self.polly.synthesize_speech(Text=f"{content}", OutputFormat="mp3",
                                           VoiceId=self.speaker, Engine="neural")
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(os.getcwd(), "result.mp3")

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)
        output = os.path.join(os.getcwd(), "polly_result.mp3")
        return output


