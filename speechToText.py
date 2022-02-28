from deepspeech import Model
import numpy as np
import os
import wave


model_file_path = 'deepspeech-0.9.3-models.pbmm'
lm_file_path = 'deepspeech-0.9.3-models.scorer'
beam_width = 500
lm_alpha =0.93
lm_beta = 1.18

model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)

model.setScorerAlphaBeta(lm_alpha,lm_beta)
model.setBeamWidth(beam_width)

stream = model.createStream()

def read_wav_file(filename):
  with wave.open(filename , "rb") as w:
    rate = w.getframerate()
    frames = w.getnframes()
    buffer = w.readframes(frames)
  return buffer , rate

def transcribe_streaming(audio_file):
  buffer,rate = read_wav_file(audio_file)
  offset =0
  batch_size=655369999
  text=''

  while offset < len(buffer):
    end_offset = offset + batch_size
    chunk = buffer[offset:end_offset]
    data16 = np.frombuffer(chunk ,dtype=np.int16)

    stream.feedAudioContent(data16)
    text=stream.intermediateDecode()
    print(text)
    offset=end_offset
  return text