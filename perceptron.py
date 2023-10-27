import numpy as np
import cv2
import keras
import tensorflow
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D, Dropout
from keras.utils import to_categorical
import emnist

image_path = ""

val_loss = 0.0
val_acc = 0.0
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
        x_train = self.emnist_images[:50000]
        y_train = self.emnist_labels[:50000]
        x_test  = self.emnist_images[50000:]
        y_test  = self.emnist_labels[50000:]

        y_train = y_train - 1
        y_test = y_test - 1

        x_train.reshape((x_train.shape[0], 28, 28, 1))
        x_test.reshape((x_test.shape[0], 28, 28, 1))

        x_train = x_train / 255
        x_test = x_test / 255

        x_train = tensorflow.convert_to_tensor(x_train)
        y_train = tensorflow.convert_to_tensor(y_train)
        x_test = tensorflow.convert_to_tensor(x_test)
        y_test = tensorflow.convert_to_tensor(y_test)

        y_train = to_categorical(y_train, num_classes=256)
        y_test = to_categorical(y_test, num_classes=256)

        return x_train, x_test, y_train, y_test

    def init_CNN_Model(self):
        self.model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1))),
        self.model.add(MaxPool2D(2, 2)),
        self.model.add(Dropout(0.25)),
        self.model.add(Flatten()),
        self.model.add(Dense(64, activation='relu')),
        self.model.add(Dense(32, activation='relu')),
        self.model.add(Dense(16, activation='relu')),
        self.model.add(Dense(8, activation='relu')),
        self.model.add(Dense(256, activation='softmax'))
        if self.model:
            self.model_setup(self.model)

    def model_setup(self, model):
        self.model = model
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        x_train, x_test, y_train, y_test = self.init_training_data()
        model.fit(x_train, y_train, epochs=1, batch_size=32)
        val_loss, val_acc = model.evaluate(x_test, y_test)
        print('validation accuracy:', val_acc)
        print('validation loss:', val_loss)
        boolean = True

    def image_analysis(self):
        img_src   = image_path
        image = cv2.imread(img_src)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # odcien szarosci
        ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # czarno-bialy odwrocony
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # znajdowanie konturow

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        detected_letters = []

        for contour in contours:
            down_left, upper_left, down_right, upper_right = cv2.boundingRect(contour)

            # Jeśli obszar jest odpowiednio duży (np. eliminuje małe zakłócenia)
            if down_right > 50 and upper_right > 50:
                # Wyizoluj segment obrazu z literą
                letter_image = thresh[upper_left:upper_left + upper_right, down_left:down_left + down_right]

                # parametryzacja segmentu tak, aby segment=model
                letter_image = cv2.resize(letter_image, (28, 28))

                letter_image = letter_image / 255.0  # Normalizacja do zakresu 0-1
                # klasyfikacja litery
                prediction = self.model.predict(np.array([letter_image]))
                predicted_class = np.argmax(prediction)

                # Dodanie do listy znalezionych liter
                detected_letters.append((down_left, upper_left, down_right, upper_right, chr(predicted_class + 65)))  # +65, ponieważ EMNIST reprezentuje litery od 0 (A) do 61 (Z)

            # metoda rectangle rysuje obwódke na wykrytej literce
            for down_left, upper_left, down_right, upper_right, letter in detected_letters:
                cv2.rectangle(thresh, (down_left, upper_left), (down_left + down_right, upper_left + upper_right), (0, 255, 0), 2)
                cv2.putText(thresh, letter, (down_left, upper_left), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('Detected Letters', thresh)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print(len(detected_letters), detected_letters)

def run():
    neural_obj = NeuralCNN()
    neural_obj.preprocess_image()
    neural_obj.get_training_data()
    neural_obj.init_CNN_Model()
    neural_obj.image_analysis()
