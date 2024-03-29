from faster_whisper import WhisperModel
import numpy as np


class FasterWhisperModel():

    def __init__(self, size_ext: str='tiny.en'):
        '''
        size_ext: size of whisper model ('tiny, 'small', etc.) and
            extension if needed ('en'). Ex: 'tiny.en', 'small', etc.
        '''
        
        self.model = WhisperModel(size_ext)

    def transcribe_audio_array(self, audio_array: np.array) -> list:
        '''
        Returns a list of strings (or really a single string in a list) of the
        transcribed audio signal's text.

        ---
        audio_array: numpy array of audio signal data.
        '''

        segments, info = self.model.transcribe(audio_array)
        transcription = [segment.text for segment in segments]

        return transcription
    
    def transcribe_audio_file(self, audio_file: str) -> list:
        '''
        Transcribe an audio file.

        audio_file: full file path to audio file.
        '''

        segments, info = self.model.transcribe(audio_file)
        transcription = [segment.text for segment in segments]

        return transcription