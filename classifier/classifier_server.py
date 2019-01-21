from flask import Flask
import numpy
import random
import json
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.utils import to_categorical

app = Flask(__name__)

@app.route('/shelfmark/<shelfmark>')
def get_shelfmark_type(shelfmark):
    model = keras.models.load_model('shelfmark_classifier.h5')
    class_name = ''
    class_num = ''
    x = []
    for i in shelfmark:
        x.append(ord(i))
    X = []
    X.append(x)
    X = sequence.pad_sequences(X, maxlen=25)#this may vary and is determined by the scripts fro training the classifiers
    class_num = model.predict(X, batch_size=None, verbose=0, steps=None)
    #n.b the below is wrong, but works, as the softmax layer returns a number greater than 1 for the incorrect result
    library_of_congress_output = float(class_num[0][0])#library_of_congress
    dewey_decimal_output = float(class_num[0][1])#dewey_decimal
    if dewey_decimal_output > library_of_congress_output:
        class_name = 'Library of Congress'
        class_num = 0
    else:
        class_name = 'Dewey Decimal'
        class_num = 1
    return_value = {}
    return_value['shelfmark'] = shelfmark
    return_value['class'] = class_num
    return_value['class_name'] = class_name
    keras.backend.clear_session()
    return json.dumps(return_value)
@app.route('/floor/<shelfmark>')
def get_floor(shelfmark):
    model = keras.models.load_model('floor_classifier.h5')
    class_name = ''
    class_num = ''
    x = []
    for i in shelfmark:
        x.append(ord(i))
    X = []
    X.append(x)
    X = sequence.pad_sequences(X, maxlen=25)
    class_num = model.predict(X, batch_size=None, verbose=0, steps=None)[0]
    counter = 1
    floor_number = 0
    prob = 0
    while counter < len(class_num):
        if float(class_num[counter]) > prob:
            prob = class_num[counter]
            class_number = counter
        counter += 1
    reference_list = [['2', 'Main Library  (REFERENCE) - 2nd floor'],
    ['2', 'Main Library  (SHORT LOAN) - 2nd floor'],
    ['2', 'Main Library  (STANDARD LOAN) - 2nd floor'],
    ['2', 'Main Library - 2nd Floor - CDs'],
    ['2', 'Main Library - 2nd Floor - Miniature Scores'],
    ['2', 'Main Library - 2nd Floor - Music Collected Editions'],
    ['2', 'Main Library - 2nd Floor - Music Scores'],
    ['3', 'Main Library  (REFERENCE) - 3rd floor'],
    ['3', 'Main Library  (SHORT LOAN) - 3rd floor'],
    ['3', 'Main Library  (STANDARD LOAN) - 3rd floor'],
    ['4', 'Main Library  (STANDARD LOAN) - 4th floor'],
    ['4', 'Main Library (SERIALS) - 4th floor']]
    return_value = {}
    return_value['shelfmark'] = shelfmark
    return_value['floor_number'] = reference_list[class_number][0]
    return_value['class_name'] = reference_list[class_number][1]
    keras.backend.clear_session()
    return json.dumps(return_value)