import torch
import torchaudio

from torch.utils.data import Dataset, DataLoader
from utils import read_lines_from_file
from .letters import letters_ds_unvoc, letters_ds_voc, letters_unk, arab_replace

letter_voc_to_id = {let: i for i, let in enumerate(letters_ds_voc)}
letter_voc_to_id['<unk>'] = len(letter_voc_to_id)

letter_unvoc_to_id = {let: i for i, let in enumerate(letters_ds_unvoc)}
letter_unvoc_to_id['<unk>'] = len(letter_unvoc_to_id)

from nemo.collections.asr.data.audio_to_text import _speech_collate_fn


def process_utterance(utt, voc=False):
    utt_new = []
    last_chr = ''
    for c in utt:    
        if c == last_chr == ' ':
            continue
        if c in letters_unk:     
            continue
        if c in arab_replace.keys():
            c = arab_replace[c]
        if c in (letters_ds_voc if voc else letters_ds_unvoc):
            utt_new.append(c)
            last_chr = c
    return utt_new


class QASRDataset(Dataset):
    def __init__(self, 
                 wavs_dir: str = 'I:/speech/qasr/qasr_wav_v1.0',
                 ds_fpath: str = './all_segments.txt',
                 pad_id: int = 0,
                 return_idx: bool = False,
                 voc: bool = False):
        
        self.sample_rate = 16000
        self.wavs_dir = wavs_dir
        self.data = read_lines_from_file(ds_fpath)
        self.pad_id = pad_id
        self.return_idx = return_idx
        self.voc = voc
        self.letter_to_id = letter_voc_to_id if voc else letter_unvoc_to_id

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):

        wavid, t_start, t_end, _, utterance = self.data[index].split('\t')

        wav_fpath = f"{self.wavs_dir}/{wavid}.wav"
        
        frame_offset = int(float(t_start)*self.sample_rate)
        num_frames = int((float(t_end) - float(t_start))*self.sample_rate)
        audio, _ = torchaudio.load(wav_fpath, 
                                   frame_offset=frame_offset, 
                                   num_frames=num_frames)
        
        audio = audio[0]
        audio /= audio.abs().max()

        audio_len = torch.tensor(audio.size(0)).long()

        utterance_list = process_utterance(utterance, self.voc)
        utterance_ids = [self.letter_to_id[let] for let in utterance_list]
        utterance_ids = torch.tensor(utterance_ids).long()
        utterance_ids_len = torch.tensor(utterance_ids.size(0)).long()

        if self.return_idx:
            return audio, audio_len, utterance_ids, utterance_ids_len, index

        return audio, audio_len, utterance_ids, utterance_ids_len
    
    def _collate_fn(self, batch):
        return _speech_collate_fn(batch, pad_id=self.pad_id)

