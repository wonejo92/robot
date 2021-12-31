# nltk
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import warnings
warnings.filterwarnings('ignore')
import re
import string
import pickle
from translate import Translator
print("Librerias Importadas")


#PROCESAMIENTO DE LENGUAJE NATURAL
nltk.download('stopwords')
stopword = set(stopwords.words('english'))

nltk.download('punkt')
nltk.download('wordnet')

urlPattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
userPattern = '@[^\s]+'
def process_tweets(tweet):
  # Pasar a minusculas
    tweet = tweet.lower()
    tweet=tweet[1:]
    # Eliminacion de URL
    tweet = re.sub(urlPattern,'',tweet)
    # Eliminacion de los nombres de usuario
    tweet = re.sub(userPattern,'', tweet)
    #Eliminacion de puntuaciones
    tweet = tweet.translate(str.maketrans("","",string.punctuation))
    # Tokenizando las palabras
    tokens = word_tokenize(tweet)
    # Eliminacion de Stop Words
    final_tokens = [w for w in tokens if w not in stopword]
    # Lematizacion
    wordLemm = WordNetLemmatizer()
    finalwords=[]
    for w in final_tokens:
      if len(w)>1:
        word = wordLemm.lemmatize(w)
        finalwords.append(word)
    return ' '.join(finalwords)
print("Funcion lista")


def predict(vectoriser, model, text):
    # Predict the sentiment
    processes_text = [process_tweets(sen) for sen in text]
    textdata = vectoriser.transform(processes_text)
    sentiment = model.predict(textdata)
    print(sentiment)
    return sentiment


import pickle

def load_models():
    # Load the vectoriser.
    file = open('vectoriser.pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()
    # Load the LR Model.
    file = open('logisticRegression.pickle', 'rb')
    lg = pickle.load(file)
    file.close()
    return vectoriser, lg


def predecir(comentario:str):

    translator = Translator(from_lang="spanish", to_lang="english")
    translation = translator.translate(comentario)
    print(translation)

#if __name__ == "__main__":
    # Loading the models.
    #vectoriser, lg = load_models()

    # Text to classify should be in a list.
    #text = ["thanks for your help, excellent service"]

    #predict(vectoriser, lg, text)



