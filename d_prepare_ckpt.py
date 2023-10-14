# %%
import copy
from nemo.collections.asr.models import EncDecCTCModel

from omegaconf import OmegaConf, open_dict
from utils.letters import letters_ds_voc

# %%

model = EncDecCTCModel.from_pretrained('QuartzNet15x5Base-En')
# EncDecCTCModel.list_available_models()

cfg = copy.deepcopy(model._cfg)
print(OmegaConf.to_yaml(cfg))

# %%
model.change_vocabulary(letters_ds_voc)

# %%

with open_dict(model.cfg.optim):
  model.cfg.optim.lr = 3e-4
  model.cfg.optim.betas = [0.95, 0.5]  # from paper
  model.cfg.optim.weight_decay = 0.001  # Original weight decay

  model.cfg.optim.sched = {}
  model.cfg.optim.sched.name = 'CosineAnnealing'
  model.cfg.optim.sched.warmup_steps = 2048
  model.cfg.optim.sched.warmup_ratio = None
  model.cfg.optim.sched.min_lr = 1e-7
  model.cfg.optim.sched.max_steps = 300_000

print(OmegaConf.to_yaml(model.cfg.optim))

model.setup_optimization()

# %%

model.save_to('./pretrained/states0_ar.nemo')
