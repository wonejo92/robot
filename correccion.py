import re
from collections import Counter
from nltk import text
from nltk import tokenize

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import DB_utility
conexion = DB_utility.DBConnector()


def words(text): return re.findall(r'\w+', text.lower())


WORDS = Counter(
    words(open('big.txt').read()))


def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N


def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)


def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))




def procesamientoMensaje(texto):
    menu = ['cita', 'cuenta', 'millas', 'bloquear', 'desbloquear', 'ayuda','comentario']
    texto = normalize(texto)
    mensaje = word_tokenize(texto)
    mensajeCorregido = []
    for i in range(0,len(mensaje)):
        mensajeCorregido.append(correction(mensaje[i]))
        if mensajeCorregido[i] in menu:
            return mensajeCorregido[i]


stemmer = PorterStemmer()
stop_words = set(stopwords.words('spanish'))

def datos(datosDB):
    vector = []
    for i in range(len(datosDB)):
        vector.append(datosDB[i][0])
    return vector

def ejecutarSentencia(sentencia,parametro):
    dato = conexion.execute_query(conexion.sql_dict.get(sentencia),(parametro,))
    return dato

def procesamientoPreguntasRespuestas2(mensaje):
    mensaje = normalize(mensaje)
    mensaje = word_tokenize(mensaje)
    for i  in range(len(mensaje)):
        mensaje[i] = stemmer.stem(mensaje[i])
    clean_tokens = mensaje[:]
    for token in mensaje:
        if  token in stop_words:
            clean_tokens.remove(token)
    return clean_tokens

def procesamientoPreguntasRespuestas():
    preguntasDB = conexion.execute_query(conexion.sql_dict.get('obtener_preguntas'),())
    preguntas = []
    textos = []
    for i in range(len(preguntasDB)):
        preguntas.append(preguntasDB[i][0])
    for j in range(len(preguntas)):
        textos+=procesamientoPreguntasRespuestas2(preguntas[j])
    textos.remove('hacer')
    return textos

def obtenerRespuesta(mensaje):
    pregunta = procesamientoPreguntasRespuestas2(mensaje)
    for i in range(len(pregunta)):
        if pregunta[i] == 'horario':
            numero = 1
        if pregunta[i] == 'atencion':
            numero = 1
        if pregunta[i] == 'contacto':
            numero = 2
        if pregunta[i] == 'sucursal':
            numero = 3
        if pregunta[i] == 'transaccion':
            numero = 4
        if pregunta[i] == 'linea':
            numero = 4
    respuestasDB = ejecutarSentencia('obtener_respuesta',numero)
    respuesta = datos(respuestasDB)
    respuesta = respuesta[0].split('#')
    respuesta = '\n'.join(map(str,respuesta))
    return respuesta

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s.lower()

print(normalize('Débito'))



            

    

        


    


        

    

    
    

    


    





    

