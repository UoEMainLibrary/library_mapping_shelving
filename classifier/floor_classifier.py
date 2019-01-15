import numpy
import csv
import random
import sqlite3
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.utils import to_categorical
import tensorflowjs as tfjs

#DB query to get dataset and establish classes

conn = sqlite3.connect('libraryMapsFilter.db')
cursor = conn.cursor()
cursor2 = conn.cursor()
query = """SELECT DISTINCT '1', (floor_num_catalogue)
                      FROM floor_numbers
                      WHERE floor_num_catalogue LIKE '%1%'
           UNION
           SELECT DISTINCT '2', (floor_num_catalogue)
                      FROM floor_numbers
                      WHERE floor_num_catalogue LIKE '%2%'
           UNION
           SELECT DISTINCT '3', (floor_num_catalogue)
                      FROM floor_numbers
                      WHERE floor_num_catalogue LIKE '%3%' AND floor_num_catalogue NOT LIKE 'EAS%'
           UNION
           SELECT DISTINCT '4', (floor_num_catalogue)
                      FROM floor_numbers
                      WHERE floor_num_catalogue LIKE '%4%'
           ;"""
num_classes = []
result_set = []
for result in cursor.execute(query):
    print (result)
    num_classes.append(result)
    this_class = num_classes.index(result)
    query2 = "SELECT identifier FROM floor_numbers WHERE floor_num_catalogue = '"+result[1]+"';"
    results = cursor2.execute(query2)
    for r in results:
        result_set.append([r[0], this_class])
random.shuffle(result_set)
num_classes = len(num_classes)
X = []
y = []
for r in result_set:
    datum = []
    for i in r[0]:
        datum.append(ord(i))
    X.append(datum)
    y.append(r[1])

# fix random seed for reproducibility
numpy.random.seed(7)
y = to_categorical(y)
length_of_slice = int(len(X) * 0.999)
slice_object = slice(length_of_slice)
X_train = X[slice_object]
y_train = y[slice_object]
slice_object = slice(length_of_slice, int(len(X)))
X_test = X[slice_object]
y_test = y[slice_object]

# truncate and pad input sequences
max_review_length = 25
top_words = 50000
X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)
# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length))
model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(LSTM(200))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='nadam', metrics=['categorical_accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=3, batch_size=256)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
model.save('shelfmark_floor_classifier.h5')
tfjs.converters.save_keras_model(model, "classifier_floors_main_library")
