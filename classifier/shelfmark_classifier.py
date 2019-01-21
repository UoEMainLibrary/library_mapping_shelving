import numpy
import csv
import random
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

# fix random seed for reproducibility
numpy.random.seed(7)

X = []
y = []

X_0 = []
X_1 = []
y_0 = []
y_1 = []



with open('datasets/dewey.csv', newline='', errors="surrogateescape") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        datum = []
        for r in row:
            for i in r:
                datum.append(ord(i))
        X_0.append(datum)
        y_0.append(0)


with open('datasets/library_of_congress.csv', newline='', errors="surrogateescape") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        datum = []
        for r in row:
            for i in r:
                datum.append(ord(i))
        X_1.append(datum)
        y_1.append(1)

random.shuffle(X_0)
random.shuffle(X_1)
random.shuffle(y_0)
random.shuffle(y_1)

counter = 0
while counter < int(len(X_0)-1):
    counter += 1
    X.append(X_0[counter])
    X.append(X_1[counter])
    y.append(y_0[counter])
    y.append(y_1[counter])

y = to_categorical(y)
num_classes = 2 #needs fixing once UTS and other classification systems are added
length_of_slice = int(len(X_0) /2)
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
model.add(LSTM(100))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='nadam', metrics=['categorical_accuracy'])
print(model.summary())
model.fit(X_train, y_train, epochs=3, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
model.save('shelfmark_classifier.h5')
