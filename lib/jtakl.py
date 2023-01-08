

import glob
import os
import pathlib
import hashlib
import time
import pyopenjtalk
import numpy as np
from scipy.io import wavfile


DELETE_EPOCH_SEC = 60


class Jtalk():

    def __init__(self):
        # wavディレクトリ取得
        self.wav_dir: str = _get_wav_dir()
        # wavディレクトリ内のデータを消去
        _remove_files(self.wav_dir)


    def create_wav(self, text:str) -> str:
        # 音声ファイル生成
        hash_str = hashlib.md5(text.encode()).hexdigest()
        self.wav_path = f"{_get_wav_dir()}{hash_str}.wav"
        x, sr = pyopenjtalk.tts(text)
        wavfile.write(self.wav_path, sr, x.astype(np.int16))
        return self.wav_path
        

    def del_old_wav(self):
        """古いwavファイルを消去します。"""
        wav_files = glob.glob(f'{self.wav_dir}*')
        epoch_sec = time.time()     # 現在のエポック秒
        for file in wav_files:
            create_sec = os.path.getatime(file)  # ファイルを生成したエポック秒
            if (epoch_sec - create_sec) > DELETE_EPOCH_SEC:
                os.remove(file)


def _remove_files(dir: str):
    files = glob.glob(f'{dir}*')
    for file in files:   
        os.remove(file)


def _get_wav_dir() -> pathlib.Path:
    path = f'{pathlib.Path(__file__).parent.parent}/wav/'
    return path


if __name__ == '__main__':
    """test"""
    pass