import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

start = True
continue_learning = False

training_generator = ImageDataGenerator(rescale=1./255,
rotation_range=7,
horizontal_flip=True,
zoom_range=0.2)
training_dataset = training_generator.flow_from_directory('../data/train',
target_size=(48, 48),
batch_size=16,
class_mode='categorical',
shuffle=True)

number_classes = 5 # Change to 5 classes
detectors_number = 32
width, height = 48, 48
epochs = 100

if start:
    network = Sequential()

    network.add(Conv2D(filters=number_classes, kernel_size=(3, 3), activation='relu', padding='same',
                       input_shape=(width, height, 3)))
    network.add(BatchNormalization())
    network.add(Conv2D(filters=number_classes, kernel_size=(3, 3), activation='relu', padding='same'))
    network.add(BatchNormalization())
    network.add(MaxPooling2D(pool_size=(2, 2)))
    network.add(Dropout(0.2))

    network.add(Conv2D(filters=2 * number_classes, kernel_size=(3, 3), activation='relu', padding='same'))
    network.add(BatchNormalization())
    network.add(Conv2D(filters=2 * number_classes, kernel_size=(3, 3), activation='relu', padding='same'))
    network.add(BatchNormalization())
    network.add(MaxPooling2D(pool_size=(2, 2)))
    network.add(Dropout(0.2))

    network.add(Conv2D(filters=2 * 2 * number_classes, kernel_size=(3, 3), activation='relu', padding='same'))
    network.add(BatchNormalization())
    network.add(Conv2D(filters=2 * 2 * number_classes, kernel_size=(3, 3), activation='relu', padding='same'))
    network.add(BatchNormalization())
    network.add(MaxPooling2D(pool_size=(2, 2)))
    network.add(Dropout(0.2))

    network.add(Conv2D(filters=2 * 2 * 2 * number_classes, kernel_size=(3, 3), activation='relu', padding='same'))
    network.add(BatchNormalization())
    network.add(Conv2D(filters=2 * 2 * 2 * number_classes, kernel_size=(3, 3), activation='relu', padding='same'))
    network.add(BatchNormalization())
    network.add(MaxPooling2D(pool_size=(2, 2)))
    network.add(Dropout(0.2))

    network.add(Flatten())

    network.add(Dense(units=2 * number_classes, activation='relu'))
    network.add(BatchNormalization())
    network.add(Dropout(0.2))

    network.add(Dense(units=2 * number_classes, activation='relu'))
    network.add(BatchNormalization())
    network.add(Dropout(0.2))

    network.add(Dense(units=number_classes, activation='softmax'))
    print(network.summary())

    network.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

if continue_learning:
    network = load_model("../data/saved_models/trained_model_convNN.h5")

if start or continue_learning:
    network.fit(training_dataset, epochs=epochs)

    network.save("../data/saved_models/trained_model_convNN.h5")
