"""CMU_ARCTIC Corpus parser."""
import random
from pathlib import Path, PurePosixPath
from librosa.util import find_files


class Parser:
    """Parser"""

    def __init__(self, root):
        seed = random.randint(1, 1000)
        random.seed(seed)

        wav_files = [
            str(PurePosixPath(wav_file).relative_to(root))
            for wav_file in find_files(root)
        ]

        self.root = root
        self.seed = seed
        self.wav_files = wav_files
        self.metadata = {}

    def sample_source(self):
        """Sample as source"""
        wav_file = random.choice(self.wav_files)
        speaker_id = self.get_speaker(wav_file)
        content = self.get_content(wav_file)

        return wav_file, speaker_id, content

    def sample_targets(self, number):
        """Sample as target"""
        wav_files = random.choices(self.wav_files, k=number)
        speaker_id = self.get_speaker(wav_files[0])

        return wav_files, speaker_id

    def load_content(self, file_path):
        """Read content"""
        speaker_id = self.get_speaker(file_path)
        context_path = Path(self.root) / speaker_id / "etc/txt.done.data"
        with context_path.open() as text_file:
            for line in text_file:
                utterance_id, utterance = line.strip().split(" ", 2)[1:]
                if utterance_id not in self.metadata:
                    self.metadata[utterance_id] = utterance[1:-3].lower()

    def get_content(self, file_path):
        """Get text for CMU_ARCTIC Corpus."""
        wav_name = Path(file_path).stem

        if wav_name in self.metadata:
            return self.metadata[wav_name]

        self.load_content(file_path)
        return self.metadata[wav_name]

    @classmethod
    def get_speaker(cls, file_path):
        """Get speaker for CMU_ARCTIC Corpus."""
        speaker_id = file_path.split("/")[0]

        return speaker_id
