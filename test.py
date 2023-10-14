import argparse
import torchaudio
from nemo.collections.asr.models import EncDecCTCModel

from utils import stt

# python test_.py --checkpoint ./checkpoints/exp0/last.ckpt --audio_path 'I:/tts/3arabiyya/arabic-speech-corpus/test set/wav/ARA NORM  0001.wav' --play --write_to_file

def test(args):

    model = EncDecCTCModel.load_from_checkpoint(
    args.checkpoint, hparams_file=args.hparams_file)
    model = model.to(args.device)
    model.eval()

    audio, sr = torchaudio.load(args.audio_path)
    audio = audio.to(args.device)
    if sr != 16000:
        audio = torchaudio.functional.resample(audio, sr, 16000)
    audio /= audio.abs().max()
    audio.squeeze_(0)

    text_pred = stt(model, audio)

    print(text_pred)
        
    if args.write_to_file:
        from utils import write_lines_to_file
        write_lines_to_file(args.output_file_path, [text_pred])
        print(f"Saved text file at {args.output_file_path}")

    if args.play:
        try:
            import sounddevice as sd
            sd.play(audio.cpu()*0.3, 16000, blocking=True)
        except:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', type=str, 
                        default='./checkpoints/exp0/last.ckpt')
    parser.add_argument('--hparams_file', type=str, 
                        default='./logs/exp0/hparams.yaml')
    parser.add_argument('--audio_path', type=str, 
                        default='./data/test_waves/static0.wav')
    parser.add_argument('--play', action='store_true')
    parser.add_argument('--write_to_file', action='store_true')
    parser.add_argument('--output_file_path', type=str, 
                        default='./data/test_sample.txt')
    parser.add_argument('--device', type=str, default='cuda')
    args = parser.parse_args()

    test(args)
