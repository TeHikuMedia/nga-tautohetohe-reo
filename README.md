# Corpus of Te Reo derived from the New Zealand Hansard

This repository gives all the Te Reo that has been spoken in the New Zealand parliament, as recorded in the \
[Hansard reports](https://www.parliament.nz/en/pb/hansard-debates/). The repository contains
two important CSV files. The first (hansardrāindex) is an index of each day of debates in the New Zealand Hansard, and the second (hansardreomāori) is a corpus of te reo Māori extracted from the Hansard. Speeches are broken into paragraphs or into segments of text (referred to as an utterance), and each utterance is scored 
by how many Māori words it contains. The corpus consists of all utterances that have more than 50% of the total words in Te Reo (not including ambiguous words, such as `he`, that could be either English or Māori).

The graph below shows the usage of te reo Māori in the New Zealand parliament over time. This counts all te reo Māori words from speech segments that were rated as being 70% or more te reo Māori, as a percentage of all the words spoken in parliament during that year. 

![Te reo usage in the New Zealand parliament](https://github.com/TeHikuMedia/nga-tautohetohe-reo/blob/master/plot/reo-speeches-by-year.png)

## The files

### hansardrāindex.csv
* retrieved (date): timestamp from when the text was retrieved
* url (text): source url
* volume (integer): Hansard volume - all integers apart from first 6 volumes
* format (text): text string describing the format of the source document (e.g., `OCR`, `PDF`, `HTML`)
* date1 (text): date extracted from text. Sometimes the text spans multiple days, if the break between the days could not be determined.
* date2 (date): date1 converted into numerical format (`YYYY-MM-DD`)
* reo (integer): number of words that are likely to be Māori
* ambiguous (integer): number of words in that could be either English or Māori (e.g, `a`, `he`, `to`)
* other (integer): number of words that are likely to not be Māori
* percent (number): percentage of total words that are classified as `reo`
* incomplete (text): a reason if the document is incomplete (e.g., `Awaiting authorised reo`), empty otherwise

### hansardreomāori.csv
* url (text): source url
* volume (text): Hansard volume - all integers apart from first 6 volumes
* format (text): Source format of the text - OCR, PDF, or HTML
* date1 (text): Date of speech extracted from text
* date2 (date): date1 converted into numerical format (`YYYY-MM-DD`)
* utterance (integer): sequential number identifying each chunk of text within the document
* speaker (text): name of the speaker
* reo (integer): number of words in the utterance that are likely to be Māori
* ambiguous (integer): number of words in the utterance that could be either English or Māori (e.g, `a`, `he`, `to`)
* other (integer): number of words in the utterance that are likely to not be Māori
* percent (number): percentage of total words in the utterance that are classified as `reo`
* text (text): text extracted from the document, with line-breaks removed

## Scripts
The script for scoring words as either English or Māori is at https://github.com/TeHikuMedia/nga-kupu, and the script that was used for extracting and processing the Hansard is at https://github.com/TeHikuMedia/nga-tautohetohe.

## Public domain
The Hansard is in the public domain. You are free to re-use this content without restriction. If you carry out analysis of the text recorded in this repository, however, we would appreciate acknowledgement.

