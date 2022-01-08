from flask import Flask, render_template,url_for,request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)

def output(output_predict):
    hasil_class=''
    index_max = np.amax(output_predict)
    result = np.where(output_predict == index_max)
    result=int(result[0])
    if result == 0 :
        hasil_class='Apel Busuk'
    elif result == 1 :
        hasil_class='Apel Segar'
    return index_max,hasil_class


def predict_label(img_path):
    list_hasil=[]

    i = image.load_img(img_path, target_size=( 224, 224 ))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 224, 224, 3)
    i = np.array(i)
    p = model.predict(i)
    
    nilai,hasil_class=output(p[0])
    
    list_hasil.append(hasil_class)
    list_hasil.append(nilai)
    
    return list_hasil


model = load_model('model_deploy2.h5')

model.make_predict_function()


@app.route('/')
def index():
	return render_template("index.html")

@app.route('/upload')
def upload():
	return render_template("upload.html")

@app.route('/prediction', methods=['GET','POST'])
def get_hours():
    if request.method == 'POST' :
        img = request.files['image']
        
        img_path = 'static/'+img.filename
        img.save(img_path)
        
        p = predict_label(img_path)
    return render_template('prediction.html', prediction = p, img_path = img_path)

if __name__ == "__main__":
	app.run(debug=True)