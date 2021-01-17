# LSTM
import tensorflow.keras as keras
import numpy as np
import time

from utilities.Utils import save_logs, delete_logs, get_optimal_batch_size


class Classifier_LSTM:
    def __init__(self, output_directory, input_shape, nb_classes, verbose=2):
        self.output_directory = output_directory
        self.model = self.build_model(input_shape, nb_classes)
        self.model.summary()
        print("")
        self.verbose = verbose

    def build_model(self, input_shape, nb_classes):
        # input_layer = keras.layers.Input(input_shape)
        # input_layer_flattened = keras.layers.Flatten()(input_layer)

        model = keras.models.Sequential()
        # in LSTM-FCN, there are three options (8,64,128) for the number of units and we test (32,64,128)
        model.add(keras.layers.LSTM(64, input_shape=input_shape, return_sequences=True))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(nb_classes, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=200, min_lr=0.1)

        file_path = self.output_directory + 'best_model.hdf5'

        model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor='loss', save_best_only=True)

        self.callbacks = [reduce_lr, model_checkpoint]

        return model

    def fit(self, x_train, y_train, x_val, y_val, y_true, batch, epochs, only_save_csv):
        # x_val and y_val are only used to monitor the test loss and NOT for training
        batch_size = batch
        nb_epochs = epochs

        # mini_batch_size = int(min(x_train.shape[0] / 10, batch_size))
        mini_batch_size = get_optimal_batch_size(x_train.shape[0], batch_size, 0.2)
        print('mini_batch_size is ' + str(mini_batch_size))

        start_time = time.time()

        hist = self.model.fit(x_train, y_train, batch_size=mini_batch_size, epochs=nb_epochs,
                              verbose=self.verbose, validation_data=(x_val, y_val), callbacks=self.callbacks)

        duration = time.time() - start_time

        y_pred = self.model.predict(x_val)

        # convert the predicted from binary to integer
        y_pred = np.argmax(y_pred, axis=1)

        save_logs(self.output_directory, hist, y_pred, y_true, duration)

        if only_save_csv:
            delete_logs(self.output_directory)

        keras.backend.clear_session()