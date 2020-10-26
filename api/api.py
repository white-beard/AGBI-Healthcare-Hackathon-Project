from tensorflow.keras.models import Model
from tensorflow.keras.layers import *
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from PIL import Image
import io
from tensorflow.keras.applications import Xception


app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



def make_model():
    base_model = Xception(include_top = False , input_shape = (71,71,3), weights=None)

    for layer in base_model.layers:
        layer.trainable = True

    model = base_model.output
    model = Flatten()(model)

    model = Dense(512, kernel_initializer='he_uniform')(model)
    model = Dropout(0.2)(model)
    model = BatchNormalization()(model)
    model = Activation('relu')(model)

    model = Dense(128, kernel_initializer='he_uniform')(model)
    model = Dropout(0.2)(model)
    model = BatchNormalization()(model)
    model = Activation('relu')(model)

    model = Dense(52, kernel_initializer='he_uniform')(model)
    model = Dropout(0.2)(model)
    model = BatchNormalization()(model)
    model = Activation('relu')(model)

    model = Dense(16, kernel_initializer='he_uniform')(model)
    model = Dropout(0.2)(model)
    model = BatchNormalization()(model)
    model = Activation('relu')(model)

    output = Dense(7, activation='softmax')(model)

    return Model(inputs=base_model.input, outputs=output)


def process_image(image):

    if image.mode != "RGB":
        image = image.convert("RGB")
    
    img = image.resize((71,71))
    img = img_to_array(img)
    img = img.astype('float32')
    img /= 255.0
    img = np.array([img])
    return img

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def upload_img_prediction():

    result = {'success': False}

    if request.method == 'POST':
        if request.files.get('image'):
            image = request.files['image']
            # print(image.filename)
            #if allowed_file(image.filename):                 
            image = image.read()                 
            image = Image.open(io.BytesIO(image))
            print('Image is allowed')
            img = process_image(image)
            prediction = model.predict(img)
            
            
            for i in range(len(classes)):
                result[classes[i]] = str(prediction[0][i])
            
            result['success'] = True

            return jsonify(result)

        return jsonify(result)        

    


if __name__ == "__main__":

    model = make_model()
    model.load_weights("XceptionNN.h5")

    classes = ['Actinic keratoses','Basal cell carcinoma','Benign keratosis-like lesions',
                'Dermatofibroma', 'Melanocytic nevi', 'Melanoma', 'Vascular lesions']            
    app.run(debug=True)
