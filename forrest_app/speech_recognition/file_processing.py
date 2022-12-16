from pydub import AudioSegment
import math
from .audio_processing import audio_processing


def file_processing(filename: str) -> str:
    split_wav = SplitWavAudioMubin('files', filename)
    cnt_files = split_wav.multiple_split(filename, min_per_split=1)
    res = []
    for i in range(cnt_files):
        filename_n = str(i) + f'_{filename}'
        res.append(audio_processing(filename_n))

    return ','.join(res)


class SplitWavAudioMubin:
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename

        self.audio = AudioSegment.from_wav(self.filepath)

    def get_duration(self):
        return self.audio.duration_seconds

    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 120 * 1000
        t2 = to_min * 120 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '/' + split_filename, format="wav")

    def multiple_split(self, filename, min_per_split):
        total_mins = math.ceil(self.get_duration() / 120)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + f'{filename}'
            self.single_split(i, i + min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

        return total_mins
