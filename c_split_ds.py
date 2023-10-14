# %%
import numpy as np
from utils import read_lines_from_file, write_lines_to_file

# %%

all_segments = read_lines_from_file('./data/all_segments_filt_nonumlat.txt')

# %%

np.random.seed(42)
np.random.shuffle(all_segments)

all_segments[0]
all_segments[1]

# %%

val_perc = 0.01
n_val_segments = int(len(all_segments)*val_perc)

val_segments = all_segments[:n_val_segments]
train_segments = all_segments[n_val_segments:]

print(len(val_segments), len(train_segments))

# %%

write_lines_to_file('./data/train_segments_nonumlat.txt', train_segments)
write_lines_to_file('./data/val_segments_nonumlat.txt', val_segments)

# %%