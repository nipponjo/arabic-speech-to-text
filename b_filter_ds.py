# %%
import numpy as np
import matplotlib.pyplot as plt
from utils import read_lines_from_file, write_lines_to_file
from utils.letters import numerals, numerals_ar, abc_latin
from tqdm import tqdm

numerals_all = set(numerals + numerals_ar)
num_lat_all = set(numerals + numerals_ar + abc_latin)

# %%

t_min_secs = 0
t_max_secs = 25

# %%
segment_lines = read_lines_from_file('./data/all_segments.txt')
sep = '\t'

# %%

durations = []
utt_g1 = []
letters = set()

segments_rm = []
segments_keep = []

for idx, line in enumerate(tqdm(segment_lines)):
    if line == '\n':
        continue

    wavid, t_start, t_end, _, *utterance = line.split(sep)

    dur_secs = float(t_end) - float(t_start)
    durations.append(dur_secs)

    utterance = ' '.join(utterance) if len(utterance) > 1 else utterance[0]

    letters.update(list(utterance))

    if not (t_min_secs < dur_secs < t_max_secs) \
       or set(utterance).intersection(num_lat_all):
        segments_rm.append(line)
        continue

    segments_keep.append(line)


durations_np = np.array(durations)


# %%

write_lines_to_file('./data/all_segments_filt_nonumlat.txt', segments_keep)

# %%

plt.hist(durations_np[durations_np > 0])

segments_rm