# arabic-speech-to-text

This repository contains the code for training the QuartzNet ASR model ([NeMo](https://github.com/NVIDIA/NeMo)) on the [QCRI-AL Jazeera Corpus](https://arabicspeech.org/resources/qasr). 

## Data preprocessing

Download the [QCRI-AL Jazeera Corpus](https://arabicspeech.org/resources/qasr). The script `a_preprocess_xml.py` extracts the text segments from the xml files.
The script `b_filter_ds.py` removes segments that include latin script or numerals.
The script `c_split_ds.py` creates a training set and a test set from the segments.

## TODO

- [ ] Upload pretrained model
- [ ] ...



<!-- ## Acknowledgements

QCRI-AL Jazeera Corpus, used by XXX, was developed by Qatar Computing Research Institute (“QCRI”), an institute within the Hamad Bin Khalifa University (“HBKU”) a member of the Qatar Foundation for Education, Science and Community Development and the Data provided courtesy of Al Jazeera. -->
