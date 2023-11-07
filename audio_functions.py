from openai import OpenAI
import sounddevice as sd
import wavio
import io
import whisper
from pydub import AudioSegment
from pydub.playback import play


class AudioManager:

    def __init__(self):
        self.client = OpenAI()
        self.model = whisper.load_model("base")

    def record_audio(self, duration=5, fs=44100):
        """
        Record audio from the microphone for a specified duration and sampling rate.
        """
        print("Recording...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print("Recording finished")
        return audio

    def save_audio(self, audio, filename="input.wav", fs=44100):
        """
        Save the recorded audio to a WAV file.
        """
        wavio.write(filename, audio, fs, sampwidth=2)
        return filename

    def transcribe_audio(self, audio_path):
        """
        Transcribe the audio at the given path using Whisper.
        """
        result = self.model.transcribe(audio_path)
        return result["text"]

    def stream_and_play(self, text):
        """
        Use OpenAI's text-to-speech API to stream the audio and play the bot's response.
        """
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        byte_stream = io.BytesIO(response.content)
        audio_segment = AudioSegment.from_file(byte_stream, format="mp3")
        play(audio_segment)
