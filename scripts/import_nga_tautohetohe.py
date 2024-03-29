#!/usr/bin/env python3
import re
import argparse
import urllib.parse
import os
import logging
import csv
import textutils
import pandas as pd
from reo_toolkit import is_maori


HANSARD_GIT_BASE = "https://github.com/TeHikuMedia/nga-tautohetohe-reo/raw/master/"
CORPUS_NAME = "nga-tautohetohe-reo"


def main():

  log = logging.getLogger(CORPUS_NAME)

  parser = argparse.ArgumentParser()
  parser.add_argument('--csv-file', help="Path to hansardreomāori.csv")
  parser.add_argument('--text-file', help="Path to output file")
  parser.add_argument('--log-level', default='INFO', help="Log level (default: INFO)")

  args = parser.parse_args()

  logging.basicConfig(
      level=args.log_level,
      format='[%(asctime)s] | %(levelname)s | %(message)s',
      datefmt='%H:%M:%S')

  # download csv file
  csv_data = pd.read_csv(args.csv_file)

  # split file by format
  ocr = csv_data[csv_data['format'] == 'OCR']
  not_ocr = csv_data[csv_data['format'] != 'OCR'] 

  # parse csv and apply thresholds -- ocr data
  ocr_plain_text = ''
  for line in ocr.text.values:
    ocr_plain_text += line + '\n'
  
  # parse csv and apply thresholds -- non-ocr data
  other_plain_text = ''
  for line in not_ocr.text.values:
    other_plain_text += line + '\n'

  # output as plain text, with metadata
  out_filename = 'corpus/ocr-hansardreomāori.txt'
  textutils.write_kupu_tōkau(
    output_filename=out_filename,
    corpus_name=CORPUS_NAME,
    plain_text=ocr_plain_text,
    data_path='',
    source_url=urllib.parse.urljoin(
      HANSARD_GIT_BASE, "hansardreomāori.csv"),
    copyright_holder="None",
    notes="Te Reo Māori content from the NZ Hansard.")

  out_filename = args.text_file
  textutils.write_kupu_tōkau(
    output_filename=out_filename,
    corpus_name=CORPUS_NAME,
    plain_text=other_plain_text,
    data_path='',
    source_url=urllib.parse.urljoin(
      HANSARD_GIT_BASE, "hansardreomāori.csv"),
    copyright_holder="None",
    notes="Te Reo Māori content from the NZ Hansard.")

if __name__ == "__main__":
  main()
