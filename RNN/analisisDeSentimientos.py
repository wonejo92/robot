
from keras.models import Sequential
from keras import layers
from keras import regularizers
from keras import backend as K
from keras.callbacks import ModelCheckpoint
import keras
import pandas as pd

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import regularizers

from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, Dropout
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
import re
from translate import Translator
print("Librerias listas")





data = pd.read_csv('RNN\data.csv', encoding = 'latin')


data.drop(['Unnamed: 0'], axis= 1)



data.dtypes
data['text'] = data['text'].astype('str')
data['processed_tweets'] = data['processed_tweets'].astype('str')

max_words = 5000
max_len = 300

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(data.processed_tweets)
sequences = tokenizer.texts_to_sequences(data.processed_tweets)
tweets = pad_sequences(sequences, maxlen=max_len)
print(tweets)




model2 = keras.models.load_model('C:/Users/ismae/Desktop/New folder/robot/RNN/rnn_model.hdf5')

def predecir(comentario:str):
  translator = Translator(from_lang="spanish", to_lang="english")
  translation = translator.translate(comentario)
  
  sequence = tokenizer.texts_to_sequences([translation])
  test = pad_sequences(sequence, maxlen=max_len)
  pred = model2.predict(test)
  print(pred)
  if pred > 0.5:
    print('Comentario Positivo')
    return 1
  else:
    print('Comentario Negativo')
    return 0

