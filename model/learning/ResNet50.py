import tensorflow as tf
from keras.layers import Conv2D, BatchNormalization, Activation, Add, GlobalAveragePooling2D, Dense, Dropout
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model


def identity_block(X, filters):
    F1, F2, F3 = filters

    X_shortcut = X

    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(1, 1), padding='valid')(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F2, kernel_size=(3, 3), strides=(1, 1), padding='same')(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), padding='valid')(X)
    X = BatchNormalization(axis=3)(X)

    X = Add()([X, X_shortcut])
    X = Dropout(rate=0.1)(X)  # Пример значения параметра dropout rate
    X = Activation('relu')(X)

    return X


def convolutional_block(X, filters, stride=2):
    F1, F2, F3 = filters

    X_shortcut = X

    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(stride, stride), padding='valid')(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F2, kernel_size=(3, 3), strides=(1, 1), padding='same')(X)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), padding='valid')(X)
    X = BatchNormalization(axis=3)(X)

    X_shortcut = Conv2D(filters=F3, kernel_size=(1, 1), strides=(stride, stride), padding='valid')(X_shortcut)
    X_shortcut = BatchNormalization(axis=3)(X_shortcut)

    X = Add()([X, X_shortcut])
    X = Dropout(rate=0.2)(X)  # Пример значения параметра dropout rate
    X = Activation('relu')(X)

    return X


def ResNet50(input_shape=(64, 64, 3), classes=6):
    X_input = tf.keras.Input(input_shape)

    X = Conv2D(filters=64, kernel_size=(7, 7), strides=(2, 2), padding='same')(X_input)
    X = BatchNormalization(axis=3)(X)
    X = Activation('relu')(X)
    X = tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same')(X)

    X = convolutional_block(X, filters=[64, 64, 256], stride=1)
    X = identity_block(X, filters=[64, 64, 256])
    X = identity_block(X, filters=[64, 64, 256])

    X = convolutional_block(X, filters=[128, 128, 512])
    X = identity_block(X, filters=[128, 128, 512])
    X = identity_block(X, filters=[128, 128, 512])
    X = identity_block(X, filters=[128, 128, 512])

    X = convolutional_block(X, filters=[256, 256, 1024])
    X = identity_block(X, filters=[256, 256, 1024])
    X = identity_block(X, filters=[256, 256, 1024])
    X = identity_block(X, filters=[256, 256, 1024])
    X = identity_block(X, filters=[256, 256, 1024])
    X = identity_block(X, filters=[256, 256, 1024])

    X = convolutional_block(X, filters=[512, 512, 2048])
    X = identity_block(X, filters=[512, 512, 2048])
    X = identity_block(X, filters=[512, 512, 2048])

    X = GlobalAveragePooling2D()(X)
    X = Dense(classes, activation='softmax')(X)

    model = Model(inputs=X_input, outputs=X, name='ResNet50')

    return model

train = False
continue_train = False

if train:
    model = ResNet50(input_shape=(48, 48, 3), classes=5)
    model.summary()
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
elif continue_train:
    model = load_model("../data/saved_models/trained_model_res_net.h5")

if train or continue_train:
    # Define the paths to the train and validation directories
    train_data_dir = '../data/train'
    val_data_dir = '../data/test'

    # Set the image dimensions and the number of classes
    input_shape = (48, 48)
    num_classes = 5

    # Set the batch size for training and validation
    batch_size = 32

    # Create the train generator with data augmentation
    train_datagen = ImageDataGenerator(
            rescale=1./255,            # Normalize pixel values to [0, 1]
            rotation_range=10,         # Random rotation
            width_shift_range=0.1,     # Random horizontal shift
            height_shift_range=0.1,    # Random vertical shift
            shear_range=0.1,           # Shear transformation
            zoom_range=0.1,            # Random zoom
            horizontal_flip=True      # Random horizontal flip
        )
    train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=input_shape,
            batch_size=batch_size,
            class_mode='categorical'
        )

    # Create the validation generator without data augmentation
    val_datagen = ImageDataGenerator(rescale=1./255)  # Only rescale pixel values
    val_generator = val_datagen.flow_from_directory(
            val_data_dir,
            target_size=input_shape,
            batch_size=batch_size,
            class_mode='categorical'
        )



    model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=200
    )

    model.save("../data/saved_models/trained_model_res_net.h5")

