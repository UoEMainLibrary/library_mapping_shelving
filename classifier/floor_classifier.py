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

#class 0 is dewey shelfmarks
#class 1 is LOC shelfmarks


#DB query to get dataset and establish classes

conn = sqlite3.connect('libraryMapsFilter.db')
cursor = conn.cursor()
cursor2 = conn.cursor()
query = "SELECT DISTINCT(floor_num_catalogue) FROM floor_numbers WHERE floor_num_catalogue LIKE '%STANDARD LOAN%' AND floor_num_catalogue NOT LIKE '%EAS%'  OR floor_num_catalogue LIKE '%REFERENCE%'  AND floor_num_catalogue NOT LIKE '%EAS%';"
num_classes = []
result_set = []
for result in cursor.execute(query):
    print (result)
    num_classes.append(result)
    this_class = num_classes.index(result)
    query2 = "SELECT identifier FROM floor_numbers WHERE floor_num_catalogue = '"+result[0]+"';"
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
length_of_slice = int(len(X) * 0.9)
slice_object = slice(length_of_slice)
X_train = X[slice_object]
y_train = y[slice_object]
slice_object = slice(length_of_slice, int(len(X)))
X_test = X[slice_object]
y_test = y[slice_object]


# truncate and pad input sequences
max_review_length = 25
top_words = 5000
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
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=3, batch_size=256)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
model.save('shelfmark_floor_classifier.h5')
tfjs.converters.save_keras_model(model, "classifier_floors_main_library")
