

import os
import pathlib
import hashlib
import pyopenjtalk
import numpy as np
from scipy.io import wavfile



class Jtalk():

    def __init__(self):
        # wavディレクトリ取得
        self.wav_dir: str = _get_wav_dir()


    def create_wav(self, text:str) -> str:
        hash_str = hashlib.md5(text.encode()).hexdigest()
        self.wav_path = f"{_get_wav_dir()}/{hash_str}.wav"
        x, sr = pyopenjtalk.tts(text)
        wavfile.write(self.wav_path, sr, x.astype(np.int16))
        return self.wav_path


    def del_wav(self) -> bool:
        os.remove(self.wav_path)


def _get_wav_dir() -> pathlib.Path:
    path = f'{pathlib.Path(__file__).parent.parent}/wav'
    return path
