# Corpus of Te Reo derived from the New Zealand Hansard

This repository gives all the Te Reo that has been spoken in the New Zealand parliament, as recorded in the \
[Hansard](https://www.parliament.nz/en/pb/hansard-debates/). The repository contains
two CSV files. The first is an index of the New Zealand Hansard, and the second is a corpus extracted from the Hansard. Speeches are broken into paragraphs or into blocks of text (referred to as an utterance), and each utterance is scored 
by how many Māori words it contains. The corpus consists of all utterances that have more than 50% of the total words in Te Reo (not including ambiguous words, such as `he`, that could be either English or Māori).

## The files

### hansardindex.csv
* url (text): source url
* volume (integer): Hansard volume (may be missing for recent documents)
* date (date): Date of start of text (e.g., `2008-09-10`). Note that sometimes the text spans multiple days, if the break between the days could not be determined.
* reo (integer): number of words that are likely to be Māori
* ambiguous (integer): number of words in that could be either English or Māori (e.g, `a`, `he`, `to`)
* other (integer): number of words that are likely to not be Māori
* percent (number): percentage of total words that are classified as `reo`
* retrieved (date):  date retrieved (e.g., `2018-01-22`)
* format (text): text string describing the format of the source document (e.g., 'html', 'pdf', 'ocr')
* incomplete (text): a reason if the document is incomplete (e.g., `Awaiting authorised reo`), empty otherwise

### hansardcorpus.csv
* url (text): source url
* volume (integer): Hansard volume (may be missing for recent documents)
* date (date): Date of start of text (sometime the text spans multiple days) (e.g., `2008-09-10`)
* utterance (integer): sequential number identifying each chunk of text within the document
* speaker (text): name of the speaker
* reo (integer): number of words in the utterance that are likely to be Māori
* ambiguous (integer): number of words in the utterance that could be either English or Māori (e.g, `a`, `he`, `to`)
* other (integer): number of words in the utterance that are likely to not be Māori
* percent (number): percentage of total words in the utterance that are classified as `reo`
* text (text): text extracted from the document, with line-breaks removed

## Scripts
The script for scoring words as either English or Māori is at https://github.com/TeHikuMedia/nga-kupu, and the script that was used for extracting the and processing the Hansard is at https://github.com/TeHikuMedia/nga-tautohetohe.

## Public domain
The Hansard is in the public domain. You are free to re-use this content without a licence. If you carry out analysis of the text recorded in this repository, however, we would appreciate acknowledgement.

