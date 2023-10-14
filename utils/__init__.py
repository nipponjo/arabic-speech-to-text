import torch

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class DictConfig(object):
    """Creates a Config object from a dict 
       such that object attributes correspond to dict keys.    
    """

    def __init__(self, config_dict):
        self.__dict__.update(config_dict)

    def __str__(self):
        return '\n'.join(f"{key}: {val}" for key, val in self.__dict__.items())

    def __repr__(self):
        return self.__str__()


def get_config(fname):
    with open(fname, 'r') as stream:
        config_dict = yaml.load(stream, Loader)
    config = DictConfig(config_dict)
    return config


@torch.inference_mode()
def stt(model, signal, return_logits=False):
    signal_len = torch.LongTensor([signal.size(0)]).to(signal.device, non_blocking=True)
    logits, logits_len, _ = model.forward(input_signal=signal[None], 
                                          input_signal_length=signal_len)   

    current_hypotheses, _ = model.decoding.ctc_decoder_predictions_tensor(
        logits, decoder_lengths=logits_len, return_hypotheses=True,)

    text_pred = current_hypotheses[0].text

    if return_logits:
        return text_pred, logits

    return text_pred

def read_lines_from_file(path, 
                         encoding: str = 'utf-8', 
                         ignore_empty: bool = False):
    lines = []
    with open(path, 'r', encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if not ignore_empty or line != '': 
                lines.append(line)
    return lines

def write_lines_to_file(path, lines, 
                        mode: str = 'w', 
                        encoding: str = 'utf-8'):
    with open(path, mode, encoding=encoding) as f:
        for i, line in enumerate(lines):
            if i == len(lines)-1:
                f.write(line)
                break
            f.write(line + '\n')  