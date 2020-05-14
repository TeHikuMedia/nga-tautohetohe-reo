import os
import re
from collections import Counter
from reo_toolkit import is_maori
from nltk.tokenize import word_tokenize, sent_tokenize
import unicodedata
from tqdm import tqdm
import requests
import logging
import csv
import yaml
import datetime
import toolkit


def _download_file(from_url, to_file_path, corpus_name):
    logger = logging.getLogger(corpus_name)
    logger.info("Downloading from %s to %s", from_url, to_file_path)
    response = requests.get(from_url, stream=True)
    with open(to_file_path, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)


def ensure_file(from_url, to_file_path, corpus_name, force_download=False):
    logger = logging.getLogger(corpus_name)
    if force_download or not os.path.exists(to_file_path):
        os.makedirs(os.path.dirname(to_file_path), exist_ok=True)
        _download_file(from_url, to_file_path, corpus_name)
    else:
        logger.info("%s already exists, won't download again", to_file_path)


def tidy_text(text):
    paras = []
    for para in text.split("\n"):
        sents = []
        para = para.strip()
        for sent in sent_tokenize(para):
            tokens = word_tokenize(sent)
            words = sum(1 for token in tokens if re.search('[A-zāēīōū]', token, re.IGNORECASE))
            nums = sum(1 for token in tokens if re.search('[0-9]', token))
            if nums > words:
                logging.debug('Rejected this sentence due to too many numbers: {}'.format(sent))
                continue
            if is_maori(sent) and re.search('[a-zāēīōū]', sent, re.IGNORECASE):
                sents.append(sent)
        paras.append(' '.join(sents))

    text = '\n\n'.join(paras)
    return re.sub("\n{3,}", "\n\n", text)


class folded_unicode(str):
    pass


def folded_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')


def write_front_matter(file_handle, meta_data):

    yaml.add_representer(folded_unicode, folded_unicode_representer)
    if ("notes" in meta_data):
        meta_data["notes"] = folded_unicode(meta_data["notes"])

    file_handle.write("---\n")
    yaml.dump(meta_data, file_handle,
              default_flow_style=False, allow_unicode=True)
    file_handle.write("---\n")


def write_kupu_tōkau(output_filename, corpus_name, plain_text, data_path, **meta_data_args):

    logger = logging.getLogger(corpus_name)

    meta_data = {
        "Corpus": corpus_name,
        "Filename": output_filename
    }
    meta_data.update(meta_data_args)
    meta_data["Processed Date"] = datetime.datetime.now()

    out_file_path = os.path.join(output_filename)

    os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

    logger.info("Writing to %s", out_file_path)
    with open(out_file_path, "w", encoding="utf-8") as file_handle:
        # write the front matter
        write_front_matter(file_handle, meta_data)
        # write actual text content
        file_handle.write(plain_text)
