from tkinter import Label
import MySQLdb
import cv2 as cv
from click import password_option
from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField, form,validators
from passlib.hash import sha256_crypt
import datetime
import cv2
import numpy as np
import time


class RegisterForm(Form):
    name = StringField( "İsim Soyisim",validators = [validators.length(min=4,max=25)])
    username = StringField( "Kullanıcı Adı",validators = [validators.length(min=4,max=25)])
    email = StringField( "email adresi",validators = [validators.Email(message= "Lütfen geçerli bir Email adresi giriniz..")])
    password = PasswordField("Parola",validators = [validators.DataRequired(message= "Lütfen bir paralo belirleyiniz."),validators.EqualTo(fieldname= "confirm",message= "Parolanız uyuşmuyor")])
    confirm = PasswordField("Parola Doğrula")
    
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

def layout():

    cursor = mysql.connection.cursor()

    sorgu = "Select * From product "
    
    result = cursor.execute(sorgu)
    
    if result > 0:
        rows = cursor.fetchall()
        return render_template("Layout.html",products=rows)
        cursor.close() 


app = Flask(__name__)

app.secret_key = "Market"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSSWORD"] = ""
app.config["MYSQL_DB"] = "market"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

def add_value_in_db(quantity, code, price):
    totalPrice = quantity * price

    cursor = mysql.connection.cursor()
    sorgu = "INSERT INTO sepet VALUES(NULL,% s,% s,% s,% s,NULL)"
    cursor.execute(sorgu, (code, quantity, totalPrice, session["userID"],))
    mysql.connection.commit()
    print("Ürün Eklendi")
    return True


mysql = MySQL(app)

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    
    quantity = int(request.form['quantity'])
    code = request.form['code']
    price = int(request.form['price'])

    add_value_in_db(quantity, code, price)
    return layout()

#@app.route('/addCamera', methods=['POST'])
def add_product_to_cart_camera(row):
    print(row)
    quantity = 1
    code = row['code']
    price = row['price']
    totalPrice = quantity * price

    cursor = mysql.connection.cursor()
    sorgu = "INSERT INTO sepet VALUES(NULL,% s,% s,% s,% s,NULL)"
    cursor.execute(sorgu, (code, quantity, totalPrice, session["userID"],))
    mysql.connection.commit()
    print("Ürün Eklendi")
    return True
  

def getDatatoProduct(value):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From product where en_name = %s"
    result = cursor.execute(sorgu, (value,))
    if result > 0:
        row = cursor.fetchone()
        #print(row)
        return add_product_to_cart_camera(row)


@app.route("/sepet")
def items():
 
    cursor = mysql.connection.cursor()
    sorgu = "Select * From sepet as sp inner join product as pd on sp.sepet_item = pd.code where sepet_user_id = %s"
    
    result = cursor.execute(sorgu, (session["userID"],))
    
    if result > 0:

        rows = cursor.fetchall()
        return render_template("CheckOut.html",items=rows)
        cursor.close() 
    else:
        return render_template("Sepet.html")

@app.route("/camera")
def camera():
    net = cv2.dnn.readNet("weights/yolov3-tiny.weights", "cfg/yolov3-tiny.cfg")
    classes = []
    with open("coco_classes.txt", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    cap = cv2.VideoCapture(0)

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0

    # Yolov’u kullanarak görüntüyü tanımak için

    while True:
        _, frame = cap.read()
        frame_id += 1

        height, width = frame.shape[:2]

        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 1.0/255, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Görüntüyü ekranda göstermek için bu kodu kullanılıyoruz.
        class_ids = []
        confidences = []
        boxes = []
        label = []
        max_value =[]
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)
        #Son olarak modelin bounding box( çerçeve) oluşturmak için tespit edilmiş görüntüyü kayıt ediyoruz.
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)
                print("Bulunan Değer :", label)
                value = [label]
                getDatatoProduct(label)


        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv2.imshow("Image", frame)
        key = cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            
            break
    print( "ürün:",value)

    #add_product_to_cart_camera(urun)
    #add_value_in_db(1,label.code,label.price)
    
    cap.release()
    cv2.destroyAllWindows()
    return layout()
    


@app.route("/")
def products():
    return layout()

@app.route('/empty')
def empty_cart():

  session.clear()
  return redirect(url_for('.products'))

 
@app.route('/delete/<string:code>')
def delete_product(code):

    all_total_price = 0
    all_total_quantity = 0
    session.modified = True

    for item in session['cart_item'].items():
        if item[0] == code:    
            session['cart_item'].pop(item[0], None)
            if 'cart_item' in session:
                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            break

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price

        return redirect(url_for('.products'))

@app.route("/Category")
def profil():
    cursor = mysql.connection.cursor()

    sorgu = "Select * From ürünler "
    
    result = cursor.execute(sorgu)
    
    if result > 0:
        ürünler = cursor.fetchall()
        return render_template("CategoryIndex.html",ürünler=ürünler)
    else:
        return render_template("CategoryIndex.html")
    
@app.route("/AddCategory")
def AddCategory():
    
        return render_template("AddCategory.html")

@app.route("/DeleteCategory")
def DeleteCategory():
    
        return render_template("DeleteCategory.html")

@app.route("/EditCategory")
def EditCategory():
    
        return render_template("EditCategory.html")
        

@app.route("/ProductIndex")
def ProductIndex():
    
        return render_template("ProductIndex.html")


        

@app.route("/checkout")
def checkout():
    
        return render_template("CheckOut.html")

@app.route("/kayıt", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST":
        
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO users (name,email,username,password) VALUES(%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()
        cursor.close() 

        flash("Başarıyla Kayıt oldunuz...","success")
        
    
        return redirect(url_for("login"))
    else:

        return render_template("kayıt.html" ,form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()

        sorgu = "Select * From users where username = %s "

        result = cursor.execute(sorgu,(username,))

        if result > 0 :
            # Kullanıcıların Bilgilerini alır 
            data = cursor.fetchone()
            hash =  sha256_crypt.hash(data["password"])

            if sha256_crypt.verify(password_entered,hash):

                flash("Başarı ile giriş Yapıldı ...","success")

                getUserID = "Select id from users where username = %s"
                sonuc = cursor.execute(getUserID, (username,))
                userID = cursor.fetchone()
                session["logged_in"] = True
                session["username"] = username
                session["userID"] = userID
                return layout()

            else:
                flash("Yanlış Parola Girildi ...","danger")
                return redirect(url_for("login"))

        else:
            flash("Hatalı Kullanıcı Adı","danger")
            return redirect(url_for("login"))
    return render_template("giriş.html",form = form)

@app.route("/logout")
def logout():
    session.clear()
    return layout()

if __name__ == "__main__":
    app.run(debug=True)