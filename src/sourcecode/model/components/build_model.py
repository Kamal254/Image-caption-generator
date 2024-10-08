import os
import tqdm
from pickle import dump, load
import pickle

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Input, Embedding, Dropout, add, Dense, LSTM



from keras.layers import Masking

class Models():
    def __init__(self):
        pass

    def feature_extraction(self) ->str:


        model = VGG16()
        model = Model(inputs = model.inputs, outputs = model.layers[-2].output)

        features = {}
        datapath = "../../../artifacts/data"
        # image_dir = os.path(datapath)
        output_directory = "../../../artifacts/saved_data"
        for image_name in os.listdir(datapath):
            if image_name=="captions.txt":
                continue
            img_path = datapath + "/" + image_name
            print(img_path)
            img = load_img(img_path, target_size=(224, 224))
            img = img_to_array(img)
            img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
            img = preprocess_input(img)
            feature = model.predict(img, verbose=0)
            image_id = image_name.split('.')[0]
            features[image_id] = feature

        pickle.dump(features, open(os.path.join(output_directory, 'features.pkl'), 'wb'))


    def build_training_model(self, max_length, vocab_size) -> tf.keras.Model:
        
        inputs1 = Input(shape=(4096,))
        fe1 = Dropout(0.4)(inputs1)
        fe2 = Dense(256, activation='relu')(fe1)

        inputs2 = Input(shape=(max_length,))
        masked_inputs = Masking(mask_value=0)(inputs2)  # Explicitly handle masking
        se1 = Embedding(vocab_size, 256)(masked_inputs)
        se2 = Dropout(0.4)(se1)
        se3 = LSTM(256)(se2)

        # decoder model
        decoder1 = add([fe2, se3])
        decoder2 = Dense(256, activation='relu')(decoder1)
        outputs = Dense(vocab_size, activation='softmax')(decoder2)

        model = Model(inputs=[inputs1, inputs2], outputs=outputs)

        return model
    


build_feature_extractor = Models()
feature_extractor = build_feature_extractor.feature_extraction()