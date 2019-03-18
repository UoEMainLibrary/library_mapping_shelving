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

@app.route('/update_ranges/')
def update_ranges():
    pass

@app.route('/range/<shelfmark>')
def get_range(shelfmark):
    print (shelfmark)
    model = keras.models.load_model('range_classifier.h5')
    class_name = ''
    class_num = ''
    x = []
    for i in shelfmark:
        x.append(ord(i))
    X = []
    X.append(x)
    X = sequence.pad_sequences(X, maxlen=10)
    class_num = model.predict(X, batch_size=None, verbose=0, steps=None)[0]
    counter = 1
    floor_number = 0
    prob = 0
    while counter < len(class_num):
        if float(class_num[counter]) > prob:
            prob = class_num[counter]
            class_number = counter
        counter += 1
    #This needs updating so as to not be hard-coded
    reference_list = ['4629', '4635', '4626', '4824', '4966', '4969', '4819', '4625', '4960', '4820', '4962', '4813', '4816', '4968', '4821', '4961', '4957', '4964', '4814', '4624', '4822', '4812', '4823', '4958', '4631', '4971', '4811', '4899', '4746', '4810', '4630', '4817', '4825', '4959', '5197', '4818', '4963', '4965', '4634', '4628', '4632', '4633', '4967', '4900', '4815', '4956', '4745', '6125', '4627']
    return_value = {}
    return_value['range_id'] = reference_list[class_number]
    keras.backend.clear_session()
    return json.dumps(return_value)

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
    library_of_congress_output = float(class_num[0][1])#library_of_congress
    dewey_decimal_output = float(class_num[0][0])#dewey_decimal
    if dewey_decimal_output > library_of_congress_output:
        class_name = 'Dewey Decimal'
        class_num = 0
    else:
        class_name = 'Library of Congress'
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
    #this needs updating, so it is not hard-coded
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
