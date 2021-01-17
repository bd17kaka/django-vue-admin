# ResNet
# when tuning start with learning rate->mini_batch_size ->
# momentum-> #hidden_units -> # learning_rate_decay -> #layers
from tensorflow.keras import backend as K
import tensorflow.keras as keras
import numpy as np
import time
import os
from AFD.AFD_Constants import ONLY_CSV_RESULTS
import matplotlib.pyplot as plt
from utilities.Utils import save_logs, delete_logs, get_optimal_batch_size


class Classifier_RESNET_CAM:
    def __init__(self, output_directory, input_shape, nb_classes, verbose=2):
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        if not os.path.exists(self.output_directory+'train/'):
            os.makedirs(self.output_directory+'train/')
        if not os.path.exists(self.output_directory+'test/'):
            os.makedirs(self.output_directory+'test/')
        self.model = self.build_model(input_shape, nb_classes)
        self.model.summary()
        print("")
        self.verbose = verbose
        self.model.save_weights(self.output_directory + 'model_init.hdf5')

    def build_model(self, input_shape, nb_classes):
        n_feature_maps = 64

        input_layer = keras.layers.Input(input_shape)

        # BLOCK 1

        conv_x = keras.layers.Conv1D(filters=n_feature_maps, kernel_size=8, padding='same')(input_layer)
        conv_x = keras.layers.BatchNormalization()(conv_x)
        conv_x = keras.layers.Activation('relu')(conv_x)

        conv_y = keras.layers.Conv1D(filters=n_feature_maps, kernel_size=5, padding='same')(conv_x)
        conv_y = keras.layers.BatchNormalization()(conv_y)
        conv_y = keras.layers.Activation('relu')(conv_y)

        conv_z = keras.layers.Conv1D(filters=n_feature_maps, kernel_size=3, padding='same')(conv_y)
        conv_z = keras.layers.BatchNormalization()(conv_z)

        # expand channels for the sum
        shortcut_y = keras.layers.Conv1D(filters=n_feature_maps, kernel_size=1, padding='same')(input_layer)
        shortcut_y = keras.layers.BatchNormalization()(shortcut_y)

        output_block_1 = keras.layers.add([shortcut_y, conv_z])
        output_block_1 = keras.layers.Activation('relu')(output_block_1)

        # BLOCK 2

        conv_x = keras.layers.Conv1D(filters=n_feature_maps * 2, kernel_size=8, padding='same')(output_block_1)
        conv_x = keras.layers.BatchNormalization()(conv_x)
        conv_x = keras.layers.Activation('relu')(conv_x)

        conv_y = keras.layers.Conv1D(filters=n_feature_maps * 2, kernel_size=5, padding='same')(conv_x)
        conv_y = keras.layers.BatchNormalization()(conv_y)
        conv_y = keras.layers.Activation('relu')(conv_y)

        conv_z = keras.layers.Conv1D(filters=n_feature_maps * 2, kernel_size=3, padding='same')(conv_y)
        conv_z = keras.layers.BatchNormalization()(conv_z)

        # expand channels for the sum
        shortcut_y = keras.layers.Conv1D(filters=n_feature_maps * 2, kernel_size=1, padding='same')(output_block_1)
        shortcut_y = keras.layers.BatchNormalization()(shortcut_y)

        output_block_2 = keras.layers.add([shortcut_y, conv_z])
        output_block_2 = keras.layers.Activation('relu')(output_block_2)

        # BLOCK 3

        conv_x = keras.layers.Conv1D(filters=n_feature_maps * 2, kernel_size=8, padding='same')(output_block_2)
        conv_x = keras.layers.BatchNormalization()(conv_x)
        conv_x = keras.layers.Activation('relu')(conv_x)

        conv_y = keras.layers.Conv1D(filters=n_feature_maps * 2, kernel_size=5, padding='same')(conv_x)
        conv_y = keras.layers.BatchNormalization()(conv_y)
        conv_y = keras.layers.Activation('relu')(conv_y)

        conv_z = keras.layers.Conv1D(filters=n_feature_maps * 2, kernel_size=3, padding='same')(conv_y)
        conv_z = keras.layers.BatchNormalization()(conv_z)

        # no need to expand channels because they are equal
        shortcut_y = keras.layers.BatchNormalization()(output_block_2)

        output_block_3 = keras.layers.add([shortcut_y, conv_z])
        output_block_3 = keras.layers.Activation('relu')(output_block_3)

        # FINAL

        gap_layer = keras.layers.GlobalAveragePooling1D()(output_block_3)

        output_layer = keras.layers.Dense(nb_classes, activation='softmax')(gap_layer)

        model = keras.models.Model(inputs=input_layer, outputs=output_layer)

        model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])

        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=50, min_lr=0.0001)

        file_path = self.output_directory + 'best_model.hdf5'

        model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor='loss',
                                                           save_best_only=True)

        self.callbacks = [reduce_lr, model_checkpoint]

        return model

    def fit(self, x_train, y_train, x_val, y_val, y_true, batch, epochs, only_save_csv):
        # x_val and y_val are only used to monitor the test loss and NOT for training
        batch_size = batch

        # mini_batch_size = int(min(x_train.shape[0] / 10, batch_size))
        mini_batch_size = get_optimal_batch_size(x_train.shape[0], batch_size, 0.1)
        print('mini_batch_size is ' + str(mini_batch_size))
        start_time = time.time()

        hist = self.model.fit(x_train, y_train, batch_size=mini_batch_size, epochs=epochs,
                              verbose=self.verbose, validation_data=(x_val, y_val), callbacks=self.callbacks)

        duration = time.time() - start_time

        model = self.model
        model.load_weights(self.output_directory + 'best_model.hdf5')

        y_pred = model.predict(x_val)

        # convert the predicted from binary to integer
        y_pred = np.argmax(y_pred, axis=1)

        save_logs(self.output_directory, hist, y_pred, y_true, duration)

        if only_save_csv:
            delete_logs(self.output_directory)


        # 加载模型权重

        # 得到每一个unit对类的激活
        class_weights = model.layers[-1].get_weights()[0]

        # 取出最后一层（GAP层）和softmax层
        conv_layers = [layer for layer in model.layers if layer.__class__.__name__ == 'Conv1D']
        final_conv = conv_layers[-1].name
        final_softmax = model.layers[-1].name
        out_names = [final_conv, final_softmax]

        # 得到GAP层的输出和softmax层的输出
        inp = model.input
        outputs = [layer.output for layer in model.layers if layer.name in out_names]
        eval_functions = [K.function([inp] , [out],K.learning_phase()) for out in outputs]

        cam_results = []
        raw_datas = []
        for class_id in range(0, y_train.shape[1]):
            y_train_ids = np.where(y_train[:, class_id] == 1)
            sequence_inputs = x_train[y_train_ids[0], ...]
            for index in range(sequence_inputs.shape[0]):
                sequence_input = sequence_inputs[np.array([index]), :, :]
                outputs = []
                # 得到对这个序列模型在GAP层和softmax层的输出
                layer_outputs = [func([sequence_input, 1.])[0] for func in eval_functions]
                for layer_activations in layer_outputs:
                    outputs.append(layer_activations)

                # conv_out保存了GAP的输出，conv_out 中的数据表示了128个unit对序列上每个点的激活
                conv_out, predictions = outputs
                conv_out = conv_out[0, :, :]
                conv_out = (conv_out - conv_out.min(axis=0, keepdims=True)) / \
                           (conv_out.max(axis=0, keepdims=True) - conv_out.min(axis=0, keepdims=True))
                conv_out = (conv_out * 2.) - 1.

                conv_out = conv_out.transpose((1, 0))  # (C, T)
                conv_channels = conv_out.shape[0]

                # class_weights 保存了每个unit对每一个类的激活
                conv_cam = class_weights[:conv_channels, [class_id]] * conv_out
                conv_cam = np.sum(conv_cam, axis=0)

                conv_cam /= conv_cam.max()

                sequence_input = np.squeeze(sequence_input)
                conv_cam = np.squeeze(conv_cam)

                cam_results.append([class_id] + list(conv_cam))
                raw_datas.append([class_id] + list(sequence_input))

                if not ONLY_CSV_RESULTS:
                    cam_data = (conv_cam - conv_cam.min()) / (conv_cam.max() - conv_cam.min())
                    plt.scatter(np.array(range(0,cam_data.shape[0])),sequence_input,c=cam_data,cmap=plt.cm.get_cmap('coolwarm'))
                    plt.title('class = %s'% class_id)
                    plt.ylabel('value')
                    plt.colorbar()
                    plt.savefig(self.output_directory+'train/'+'class_%sindex_%s'%(class_id,index))
                    plt.close()

        file_raw = open(self.output_directory + 'raw_train.csv', "w")
        file_cam = open(self.output_directory + 'cam_train.csv', "w")
        for raw_data in raw_datas:
            file_raw.write(str(raw_data).replace(" ", "")[1:-1] + '\n')
        for cam_result in cam_results:
            file_cam.write(str(cam_result).replace(" ", "")[1:-1] + '\n')
        file_cam.close()
        file_raw.close()

        cam_results = []
        raw_datas = []
        for class_id in range(0, y_val.shape[1]):
            y_test_ids = np.where(y_val[:, class_id] == 1)
            sequence_inputs = x_val[y_test_ids[0], ...]
            for index in range(sequence_inputs.shape[0]):
                sequence_input = sequence_inputs[np.array([index]), :, :]
                outputs = []
                # 得到对这个序列模型在GAP层和softmax层的输出
                layer_outputs = [func([sequence_input, 1.])[0] for func in eval_functions]
                for layer_activations in layer_outputs:
                    outputs.append(layer_activations)

                # conv_out保存了GAP的输出，conv_out 中的数据表示了128个unit对序列上每个点的激活
                conv_out, predictions = outputs
                conv_out = conv_out[0, :, :]
                conv_out = (conv_out - conv_out.min(axis=0, keepdims=True)) / \
                           (conv_out.max(axis=0, keepdims=True) - conv_out.min(axis=0, keepdims=True))
                conv_out = (conv_out * 2.) - 1.

                conv_out = conv_out.transpose((1, 0))  # (C, T)
                conv_channels = conv_out.shape[0]

                # class_weights 保存了每个unit对每一个类的激活
                conv_cam = class_weights[:conv_channels, [class_id]] * conv_out
                conv_cam = np.sum(conv_cam, axis=0)

                conv_cam /= conv_cam.max()

                sequence_input = np.squeeze(sequence_input)
                conv_cam = np.squeeze(conv_cam)

                cam_results.append([class_id] + list(conv_cam))
                raw_datas.append([class_id] + list(sequence_input))

                if not ONLY_CSV_RESULTS:
                    cam_data = (conv_cam - conv_cam.min()) / (conv_cam.max() - conv_cam.min())
                    plt.scatter(np.array(range(0,cam_data.shape[0])),sequence_input,c=cam_data,cmap=plt.cm.get_cmap('coolwarm'))
                    plt.title('class = %s'% class_id)
                    plt.ylabel('value')
                    plt.colorbar()
                    plt.savefig(self.output_directory+'test/'+'class_%sindex_%s'%(class_id,index))
                    plt.close()

        file_raw = open(self.output_directory + 'raw_test.csv', "w")
        file_cam = open(self.output_directory + 'cam_test.csv', "w")
        for raw_data in raw_datas:
            file_raw.write(str(raw_data).replace(" ", "")[1:-1] + '\n')
        for cam_result in cam_results:
            file_cam.write(str(cam_result).replace(" ", "")[1:-1] + '\n')
        file_cam.close()
        file_raw.close()

