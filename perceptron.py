import numpy as np
import cv2
import keras
import tensorflow
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D, Dropout
from keras.utils import to_categorical
import emnist
import string
import matplotlib.pyplot as plt

import gui_py.gui

image_path = ""

class NeuralCNN:
    def __init__(self):
        self.emnist_data = emnist.extract_training_samples('byclass')
        self.emnist_images = 0
        self.emnist_labels = 0
        self.model = keras.models.Sequential()
        self.processed_images = []

    def preprocess_image(self):
        if image_path is not None:
            for image in image_path:
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                resized_gray_image = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_LINEAR)
                normalized_gray_image = cv2.normalize(resized_gray_image, None, 0, 255, cv2.NORM_MINMAX)
                self.processed_images.append(normalized_gray_image)
            return np.array(self.processed_images)

    def get_training_data(self):
        if self.emnist_data:
            self.emnist_images, self.emnist_labels = self.emnist_data
            if self.emnist_images.any() & self.emnist_labels.any():
                self.init_training_data()
        else:
            print(BufferError)

    def init_training_data(self):
        self.x_train = self.emnist_images[:50000]
        self.y_train = self.emnist_labels[:50000]
        self.x_test  = self.emnist_images[50000:]
        self.y_test  = self.emnist_labels[50000:]

        self.y_train = self.y_train - 1
        self.y_test = self.y_test - 1

        self.x_train.reshape((self.x_train.shape[0], 28, 28, 1))
        self.x_test.reshape((self.x_test.shape[0], 28, 28, 1))

        self.x_train = self.x_train / 255
        self.x_test = self.x_test / 255

        self.x_train = tensorflow.convert_to_tensor(self.x_train)
        self.y_train = tensorflow.convert_to_tensor(self.y_train)
        self.x_test = tensorflow.convert_to_tensor(self.x_test)
        self.y_test = tensorflow.convert_to_tensor(self.y_test)

        self.y_train = to_categorical(self.y_train, num_classes=256)
        self.y_test = to_categorical(self.y_test, num_classes=256)

        return self.x_train, self.x_test, self.y_train, self.y_test

    def init_CNN_Model(self):
        self.model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
        self.model.add(MaxPool2D(2, 2))
        self.model.add(Dropout(0.25))
        self.model.add(Flatten())
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(32, activation='relu'))
        self.model.add(Dense(16, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(256, activation='softmax'))
        if self.model:
            self.model_setup(self.model)

    def model_setup(self, model):
        self.model = model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        x_train, x_test, y_train, y_test = self.init_training_data()

        self.history = model.fit(x_train, y_train, epochs=5, batch_size=32)
        self.val_loss, self.val_acc = model.evaluate(x_test, y_test)

        print('validation accuracy:', self.val_acc)
        print('validation loss:', self.val_loss)
        gui_py.gui.gui_acc = self.val_acc
        gui_py.gui.gui_loss = self.val_loss

    def generate_plot(self):
        epochs = range(1, len(self.history.history['accuracy']) + 1)
        plt.plot(epochs, self.history.history['accuracy'], label='accuracy')
        plt.plot(epochs, self.history.history['loss'], label='loss')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 1])
        plt.legend(loc='lower right')


    def image_analysis(self):
        img_src   = image_path
        image = cv2.imread(img_src)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # odcien szarosci
        ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # czarno-bialy odwrocony
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # znajdowanie konturow

        detected_letters = []

        for contour in contours:
            down_left, upper_left, down_right, upper_right = cv2.boundingRect(contour)

            # Jeśli obszar jest odpowiednio duży (np. eliminuje małe zakłócenia)
            if down_right > 5 and upper_right > 5:
                # Wyizoluj segment obrazu z literą
                letter_image = thresh[upper_left:upper_left + upper_right, down_left:down_left + down_right]

                # parametryzacja segmentu tak, aby segment=model
                letter_image = cv2.resize(letter_image, (28, 28))
                letter_image = letter_image.astype('float32')

                letter_image = letter_image / 255.0  # Normalizacja do zakresu 0-1
                # klasyfikacja litery
                prediction = self.model.predict(np.array([letter_image]))

                letters = string.printable
                number_to_letter = {i + 1: letters[i] for i in range(len(letters))}
                predictable = number_to_letter[np.argmax(self.y_test[contour])]
                predicted_class = np.argmax(prediction)
                detected_letter = chr(predicted_class + 65)  # +65, ponieważ EMNIST reprezentuje litery od 0 (A) do 61 (Z)
                print(predictable)


                # Dodanie do listy znalezionych liter
                detected_letters.append((down_left, upper_left, down_right, upper_right, chr(predicted_class + 65)))  # +65, ponieważ EMNIST reprezentuje litery od 0 (A) do 61 (Z)

                cv2.waitKey(0)
                cv2.destroyAllWindows()

                print(len(detected_letters), detected_letter)




def run():
    neural_obj = NeuralCNN()
    neural_obj.preprocess_image()
    neural_obj.get_training_data()
    neural_obj.init_CNN_Model()
    neural_obj.image_analysis()

