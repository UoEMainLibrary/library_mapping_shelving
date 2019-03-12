import numpy
import csv
import random
import mysql.connector
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.utils import to_categorical
import tensorflowjs as tfjs


"""Connect to database"""
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    #passwd="Cr@n1eri",
    port='3306',
    charset='utf8'
)

cursor = mydb.cursor()
cursor.execute("USE LibraryMapping_production;")

"""Query database """
query = """
            SELECT
                  id,
                  range_start_letters,
                  range_start_digits,
                  range_end_letters,
                  range_end_digits
            FROM
                  elements
            WHERE
                  library = 'murray'
            AND
                  range_start_letters != 'None'
            AND
                  range_start_letters != ''
            ORDER BY
                  range_start_letters;
        """
cursor.execute(query)

"""Construct list of items in each range"""
ranges = {}
digits = 0
f = open('datasets/murray.csv', 'w')
shelfmark_list = []
X = []
y = []
for c in cursor:
    print (c)
    id = c[0]
    ranges[c[0]] = {}
    ranges[c[0]]['range_start_letters'] = c[1]
    range_start_letters = c[1]
    ranges[c[0]]['range_start_digits'] = str(str(str(str(c[2]).split('.')[0]).split(' ')[0]).split(' ')[0])
    range_start_digits = str(str(str(str(c[2]).split('.')[0]).split(' ')[0]).split(' ')[0])
    ranges[c[0]]['range_end_letters'] = c[3]
    range_end_letters = c[3]
    ranges[c[0]]['range_end_digits'] = str(str(str(str(c[4]).split('.')[0]).split(' ')[0]).split(' ')[0])
    range_end_digits = str(str(str(str(c[4]).split('.')[0]).split(' ')[0]).split(' ')[0])

    shelf_mark = str(id)+','+ str(range_start_letters)+ ' ' + str(range_start_digits)
    f.write(shelf_mark)
    f.write('\n')
    #classifier data
    y.append(str(id))
    shelfmark_value = str(range_start_letters)+ ' ' + str(range_start_digits)
    datum = []
    for s in shelfmark_value:
        datum.append(ord(s))
    X.append(datum)
    shelfmark_list.append(shelf_mark)
    digits = int(range_start_digits)
    while digits < int(range_end_digits):
        digits += 1
        shelf_mark = str(id)+','+ (range_end_letters)+ ' ' + str(digits)
        f.write(shelf_mark)
        f.write('\n')
        shelfmark_list.append(shelf_mark)
        y.append(str(id))
        shelfmark_value = str(range_start_letters)+ ' ' + str(range_start_digits)
        datum = []
        for s in shelfmark_value:
            datum.append(ord(s))
        X.append(datum)
        #print (str(id)+',', range_end_letters, digits)
    #print (str(id)+',', range_end_letters, range_end_digits)
    shelf_mark = str(id)+',' + str(range_end_letters)+ ' ' + str(range_end_digits)
    y.append(str(id))
    shelfmark_value = str(range_start_letters)+ ' ' + str(range_start_digits)
    datum = []
    for s in shelfmark_value:
        datum.append(ord(s))
    X.append(datum)
    f.write(shelf_mark)
    f.write('\n')
    shelfmark_list.append(shelf_mark)

f.close()

"""Build Classifier"""

numpy.random.seed(7)

"""map y values to classes"""
y_value_map = {}
y_values = list(set(y))
print (y_values)
y2 = []
for i in y:
    y_value_map[y_values.index(i)] = i
    y2.append(y_values.index(i))

num_classes = len(list(set(y)))
length_of_slice = int(len(X))
y = to_categorical(y2)

slice_object = slice(length_of_slice)
X_train = X[slice_object]
y_train = y[slice_object]

slice_object = slice(length_of_slice)
X_test = X[slice_object]
y_test = y[slice_object]

# truncate and pad input sequences
max_shelfmark_length = 10
top_words = 50000
X_train = sequence.pad_sequences(X_train, maxlen=max_shelfmark_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_shelfmark_length)

# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vecor_length, input_length=max_shelfmark_length))
model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(LSTM(100))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='nadam', metrics=['categorical_accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=3, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
model.save('range_classifier.h5')
