# %%
import os
import xml.etree.ElementTree as ET
import glob
from tqdm import tqdm

# %%

xml_dirpath = 'I:/speech/qasr/qasr_annotation_v1.0/mgb2.1/release/train_20210109/xml'

out_segments_filepath = './data/all_segments.txt'
out_speakers_filepath = './data/all_speakers.txt'

xml_filepaths = glob.glob(f"{xml_dirpath}/*.xml")
keys = ['starttime', 'endtime', 'speaker_id', 'utterance']
sep = '\t'

# %%

def parse_segments(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    head = root[0]
    body = root[1]
    segments = body[0]
    speakers_node = head[2]

    speakers_info = [c.attrib for c in speakers_node]

    segment_list = []
    for segment in segments:
        segment_dict = segment.attrib
        words = [e.text for e in segment]
        segment_dict['words'] = words
        segment_dict['utterance'] = ' '.join(words)
        who = segment_dict['who']
        segment_dict['speaker_id'] = who.split('_')[-2].removeprefix('speaker')

        segment_list.append(segment_dict)
    
    return segment_list, speakers_info


# %% save a txt file that includes all segments 

# segments: fid|starttime|endtime|speaker_id|utterance
# speakers: id|name|normalizedName|speakerGender|speakerUnique

with open(out_segments_filepath, 'w', encoding='utf-8') as f_seg, \
     open(out_speakers_filepath, 'w', encoding='utf-8') as f_spe:

    for xml_fpath in tqdm(xml_filepaths):

        segment_list, speakers_info = parse_segments(xml_fpath)

        xml_fname = os.path.basename(xml_fpath).removesuffix('.xml')

        for i, segment in enumerate(segment_list):
            segment_str = xml_fname + sep + sep.join(segment[k] for k in keys)
            f_seg.write(segment_str + '\n')        
        
        for i, speaker_info in enumerate(speakers_info):
            speaker_str = sep.join(speaker_info.values())
            f_spe.write(speaker_str + '\n')
            

# %%



