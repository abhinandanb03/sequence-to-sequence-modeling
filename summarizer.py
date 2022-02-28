import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation # used to identify punctuations in our text
from heapq import nlargest
from videoConverter import convert_video_to_audio_ffmpeg

def summarize(text):
  nlp=spacy.load("en_core_web_sm") # importing spacy english library

  doc=nlp(text)# creating an object doc
  punctuation = ""
  punctuation=punctuation+'"' # adding some punctuations to punctuation variable

  # Finding frequency of each word in our Text
  word_freq={}
  stop_words=list(STOP_WORDS)

  for word in doc:
    if word.text.lower() not in stop_words:
      if word.text.lower() not in punctuation:
        if word.text not in word_freq.keys():
          word_freq[word.text]=1
        else:
            word_freq[word.text] +=1

  max_freq=max(word_freq.values())

  #Performing normalization
  for word in word_freq.keys():
    word_freq[word] = word_freq[word]/max_freq

  # Sentence Segmentation
  sent_tokens=[sent for sent in doc.sents]

  # Getting score for each sentence
  sent_score={}
  for sent in sent_tokens:
    for word in sent:
      if word.text.lower() in word_freq.keys():
        if sent not in sent_score.keys():
          sent_score[sent] = word_freq[word.text.lower()]
        else:
          sent_score[sent]+= word_freq[word.text.lower()]

  summary=nlargest(n=34,iterable=sent_score,key=sent_score.get) # selecting 30% of sentence with Max score
  final_summary=[word.text for word in summary]
  summary=" ".join(final_summary)
  return summary

