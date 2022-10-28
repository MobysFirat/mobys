import cv2
import os
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def make_sketch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (19, 19), sigmaX=0, sigmaY=0)
    final_result = cv2.divide(grayed, 255 - blurred, scale=256)
    return final_result

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sketch',methods=['POST'])
def sketch():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        img = cv2.imread(UPLOAD_FOLDER+'/'+filename)
        sketch_img = make_sketch(img)
        sketch_img_name = filename.split('.')[0]+"_sketch.jpg"
        _ = cv2.imwrite(UPLOAD_FOLDER+'/'+sketch_img_name, sketch_img)
        goruntu = cv2.imread(UPLOAD_FOLDER+'/'+filename) #istenen görüntünün adresi
        rgb = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
        (h, w) = goruntu.shape[:2] #w:image-width, h:image-height
        x, y = int(w/2), int(h/2)
        r = rgb[y, x, 0]
        g = rgb[y, x, 1]
        b = rgb[y, x, 2]
        rgb_text = 'RGB: ' + str(r) + ' ' + str(g) + ' ' + str(b)
        return render_template('home.html',org_img_name=filename,sketch_img_name=sketch_img_name), rgb_text


if __name__ == '__main__':
    app.run(debug=True)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                