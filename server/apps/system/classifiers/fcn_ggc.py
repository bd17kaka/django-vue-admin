# FCN
from tensorflow.keras import backend as K
import matplotlib.pyplot as plt
import os
import tensorflow.keras as keras
import time
from AFD.AFD_Constants import ONLY_CSV_RESULTS
from utilities.Utils import save_logs, delete_logs, get_optimal_batch_size
from tensorflow.python.framework import ops
import keras.backend as K
import tensorflow as tf
import numpy as np
import keras


class Classifier_FCN_CAM:
    def __init__(self, output_directory, input_shape, nb_classes, verbose):
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        if not os.path.exists(self.output_directory + 'train/'):
            os.makedirs(self.output_directory + 'train/')
        if not os.path.exists(self.output_directory + 'test/'):
            os.makedirs(self.output_directory + 'test/')
        self.model = self.build_model(input_shape, nb_classes)
        self.model.summary()
        print("")
        self.verbose = verbose
        self.model.save_weights(self.output_directory + 'model_init.hdf5')
        self.nb_classes =nb_classes
        self.input_shape = input_shape

    def build_model(self, input_shape, nb_classes):
        input_layer = keras.layers.Input(input_shape)

        conv1 = keras.layers.Conv1D(filters=128, kernel_size=8, padding='same')(input_layer)
        conv1 = keras.layers.BatchNormalization()(conv1)
        conv1 = keras.layers.Activation(activation='relu')(conv1)

        conv2 = keras.layers.Conv1D(filters=256, kernel_size=5, padding='same')(conv1)
        conv2 = keras.layers.BatchNormalization()(conv2)
        conv2 = keras.layers.Activation('relu')(conv2)

        conv3 = keras.layers.Conv1D(128, kernel_size=3, padding='same')(conv2)
        conv3 = keras.layers.BatchNormalization()(conv3)
        conv3 = keras.layers.Activation('relu')(conv3)

        gap_layer = keras.layers.GlobalAveragePooling1D()(conv3)

        output_layer = keras.layers.Dense(nb_classes, activation='softmax')(gap_layer)

        model = keras.models.Model(inputs=input_layer, outputs=output_layer)

        model.compile(loss='categorical_crossentropy', optimizer=keras.optimizers.Adam(),
                      metrics=['accuracy'])

        reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='loss', factor=0.5, patience=50,
                                                      min_lr=0.0001)

        file_path = self.output_directory + 'best_model.hdf5'

        model_checkpoint = keras.callbacks.ModelCheckpoint(filepath=file_path, monitor='loss',
                                                           save_best_only=True, save_weights_only=True)

        self.callbacks = [reduce_lr, model_checkpoint]

        return model

    def modify_backprop(self, model, name):

        # get layers that have an activation
        layer_dict = [layer for layer in model.layers[1:]
                          if hasattr(layer, 'activation')]

        # replace relu activation
        for layer in layer_dict:
            if layer.activation == keras.activations.relu:
                layer.activation = tf.nn.relu

            # re-instanciate a new model
        new_model = self.build_model(self.input_shape, self.nb_classes)
        new_model.load_weights(self.output_directory + 'best_model.hdf5')
        return new_model

    def guided_grad_cam(self, input_model, image, category_index, guided_model, nb_classes):
        cam = self.grad_cam(input_model, image, category_index, "Conv1D", nb_classes)
        saliency_fn = self.compile_saliency_function(guided_model)
        saliency = saliency_fn([image, 0])
        gradcam = saliency[0] * cam[..., np.newaxis]

        return gradcam
    def target_category_loss(self, x, category_index, nb_classes):
        return tf.multiply(x, K.one_hot([category_index], nb_classes))

    def register_gradient(self):
        if "GuidedBackProp" not in ops._gradient_registry._registry:
            @ops.RegisterGradient("GuidedBackProp")
            def _GuidedBackProp(op, grad):
                dtype = op.inputs[0].dtype
                return grad * tf.cast(grad > 0., dtype) * \
                       tf.cast(op.inputs[0] > 0., dtype)

    def target_category_loss_output_shape(self, input_shape):
        return input_shape

    def normalize(self, x):
        # utility function to normalize a tensor by its L2 norm
        return x / (K.sqrt(K.mean(K.square(x))) + 1e-5)

    def compile_saliency_function(self, model, activation_layer='conv1d_2'):
        input_img = model.input
        layer_dict = dict([(layer.name, layer) for layer in model.layers[1:]])
        layer_output = layer_dict[activation_layer].output
        max_output = K.max(layer_output, axis=2)
        saliency = K.gradients(K.sum(max_output), input_img)[0]
        return K.function([input_img, K.learning_phase()], [saliency])

    def grad_cam(self, input_model, image, category_index, layer_name, nb_classes):
        model = input_model
        conv_layer = model.layers[-5].output
        # [1000]-D tensor with target class index set to 1 and rest as 0
        one_hot = tf.sparse_to_dense(category_index, [nb_classes], 1.0)
        signal = tf.multiply(model.layers[-1].output, one_hot)
        loss = tf.reduce_mean(signal)

        grads = self.normalize(tf.gradients(loss, conv_layer)[0])

        conv_output = [l for l in model.layers if l.__class__.__name__ == 'Conv1D'][-1].output
        gradient_function = K.function([model.input], [conv_output, grads], K.learning_phase())

        output, grads_val = gradient_function([image])
        output, grads_val = output[0], grads_val[0]

        weights = np.mean(grads_val, axis=0)
        cam = np.zeros(output.shape[0: 1], dtype=np.float32)

        for i, w in enumerate(weights):
            cam += w * output[:, i]

        return cam

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

        self.register_gradient()

        cam_results = []
        raw_datas = []
        # 得到每一个unit对类的激活
        for class_id in range(0, y_train.shape[1]):
            y_train_ids = np.where(y_train[:, class_id] == 1)
            sequence_inputs = x_train[y_train_ids[0], ...]
            for index in range(sequence_inputs.shape[0]):

                sequence_input = sequence_inputs[np.array([index]), :, :]
                predictions = model.predict(sequence_input)
                predictions = np.argmax(predictions, axis=1)[0]
                conv_cam = self.guided_grad_cam(model,sequence_input,class_id,model,self.nb_classes)
                if not ONLY_CSV_RESULTS:
                    cam_data = (conv_cam - conv_cam.min()) / (conv_cam.max() - conv_cam.min())
                    plt.scatter(np.array(range(0,cam_data.shape[1])),sequence_input[0],c=cam_data[0],cmap=plt.cm.get_cmap('coolwarm'))
                    plt.title('class = %s'% class_id)
                    plt.ylabel('value')
                    plt.colorbar()
                    plt.savefig(self.output_directory+'train/'+'class_%sindex_%s'%(class_id,index))
                    plt.close()
                conv_cam = conv_cam.reshape((conv_cam.shape[1]))
                sequence_input = np.squeeze(sequence_input)
                cam_results.append([predictions] + list(conv_cam))
                raw_datas.append([class_id] + list(sequence_input))
                print(index)
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
        # 得到每一个unit对类的激活
        for class_id in range(0, y_val.shape[1]):
            y_test_ids = np.where(y_val[:, class_id] == 1)
            sequence_inputs = x_val[y_test_ids[0], ...]
            for index in range(sequence_inputs.shape[0]):

                sequence_input = sequence_inputs[np.array([index]), :, :]
                predictions = model.predict(sequence_input)
                predictions = np.argmax(predictions, axis=1)[0]
                conv_cam = self.guided_grad_cam(model,sequence_input,predictions,model,self.nb_classes)
                if not ONLY_CSV_RESULTS:
                    cam_data = (conv_cam - conv_cam.min()) / (conv_cam.max() - conv_cam.min())
                    plt.scatter(np.array(range(0,cam_data.shape[1])),sequence_input[0],c=cam_data[0],cmap=plt.cm.get_cmap('coolwarm'))
                    plt.title('class = %s'% class_id)
                    plt.ylabel('value')
                    plt.colorbar()
                    plt.savefig(self.output_directory+'test/'+'class_%sindex_%s'%(class_id,index))
                    plt.close()
                conv_cam = conv_cam.reshape((conv_cam.shape[1]))
                sequence_input = np.squeeze(sequence_input)
                cam_results.append([predictions] + list(conv_cam))
                raw_datas.append([class_id] + list(sequence_input))
        file_raw = open(self.output_directory + 'raw_test.csv', "w")
        file_cam = open(self.output_directory + 'cam_test.csv', "w")
        for raw_data in raw_datas:
            file_raw.write(str(raw_data).replace(" ", "")[1:-1] + '\n')
        for cam_result in cam_results:
            file_cam.write(str(cam_result).replace(" ", "")[1:-1] + '\n')
        file_cam.close()
        file_raw.close()


        if only_save_csv:
            delete_logs(self.output_directory)
        keras.backend.clear_session()
