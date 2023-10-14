import argparse
import os
import torchaudio
from nemo.collections.asr.models import EncDecCTCModel
from tqdm import tqdm
from utils import stt

# python infer.py --checkpoint ./checkpoints/exp0/last.ckpt --audio_dir 'I:/tts/3arabiyya/arabic-speech-corpus/test set/wav'
# python infer.py --checkpoint ./checkpoints/exp0/states_val_loss=19.79108.ckpt --audio_dir data/test_waves

def infer(args):

    model = EncDecCTCModel.load_from_checkpoint(
        args.checkpoint,
        hparams_file=args.hparams_file)
    model = model.to(args.device)
    model.eval()

    audio_fpaths = [f.path for f in os.scandir(args.audio_dir) if f.path.endswith('wav')]
    print(f"Found {len(audio_fpaths)} audio files @ {args.audio_dir}")

    with open(args.output_file_path, 'w', encoding='utf-8') as f:
        for audio_fpath in tqdm(audio_fpaths):
            fname = os.path.basename(audio_fpath)
            audio, sr = torchaudio.load(audio_fpath)
            audio = audio.to(args.device)
            
            if sr != 16000:
                audio = torchaudio.functional.resample(audio, sr, 16000)
            audio /= audio.abs().max()
            audio = audio[0]

            text_pred = stt(model, audio)
            
            f.write(f"{fname}\t{text_pred}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, 
                        default='./checkpoints/exp0/last.ckpt')
    parser.add_argument('--hparams_file', type=str, 
                        default='./logs/exp0/hparams.yaml')
    parser.add_argument('--audio_dir', type=str, 
                        default='./data/test_waves')
    parser.add_argument('--output_file_path', type=str, 
                        default='./data/infer_text.txt')
    parser.add_argument('--device', type=str, default='cuda')
    args = parser.parse_args()

    infer(args)
