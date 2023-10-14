# %%
import pytorch_lightning as pl

from nemo.collections.asr.models import EncDecCTCModel
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger
# from pytorch_lightning.loggers.wandb import WandbLogger

from utils.data import DataLoader, QASRDataset
from utils import get_config

# %%

config = get_config('./configs/train.yaml')
print(config)

# %%

model = EncDecCTCModel.restore_from(config.start_from, map_location='cpu')
model.cuda()

model._wer.use_cer = True


# %%

ds_train = QASRDataset(ds_fpath=config.training_labels, voc=True)
ds_val = QASRDataset(ds_fpath=config.validation_labels, voc=True)

dl_train = DataLoader(ds_train, batch_size=config.batch_size, 
                      shuffle=False,
                      collate_fn=ds_train._collate_fn)
dl_val = DataLoader(ds_val, batch_size=config.val_batch_size, 
                    collate_fn=ds_val._collate_fn)

model._train_dl = dl_train
model._validation_dl = dl_val

# %%

tb_logger = TensorBoardLogger(config.logs_dir, name=None, version='')
# wb_logger = WandbLogger(project='stt-quartznet-ar')

# %%
clb_last = ModelCheckpoint(config.checkpoint_dir, 
                           every_n_train_steps=config.n_save_ckpt,
                           save_last=True, save_top_k=0)
clb_valid = ModelCheckpoint(config.checkpoint_dir, 
                            filename="states_{val_loss:.5f}",
                            save_top_k=3, monitor='val_loss', mode='min')

# %%

trainer = pl.Trainer(
    max_epochs=config.max_epochs,
    log_every_n_steps=config.log_every_n_steps,
    val_check_interval=config.val_check_interval,
    logger=tb_logger,
    # logger=wb_logger,
    default_root_dir=config.checkpoint_dir,
    callbacks=[clb_valid, clb_last]
    )

model.set_trainer(trainer)

# %%

trainer.fit(model, ckpt_path=config.resume_from)

# %%