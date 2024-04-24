from flask import Flask, request, jsonify, render_template, redirect
import json 

import prediction
import requests

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def home():
     return render_template('index.html')

import cv2

@app.route('/process', methods = ['POST'])
def process():
    data = request.get_json()
    print(data)
    # img = requests.get(data['url'])
    # img = cv2.imread(data['file'])
    # cv2.imwrite(filename= data['name'], img= img)
    
    # pred = prediction.prediction(str(img))

    # print(pred)
    # return jsonify({'prediction': pred})
    print("Happening")
    return jsonify({"name": "Paulie"})

@app.route('/route1', methods=['GET'])
def route1():
    return render_template("imagvid.html")

@app.route('/route2', methods=['GET'])
def route2():
    return render_template("live.html")

@app.route('/route3', methods = ['GET'])
def route3():
    return render_template("learn_more.html")



# @app.route("/login", methods = ['GET'])
# def login():
#     return render_template('login.html')

# @app.route("/register", methods = ["GET"])
# def register():
#     return render_template("register.html")

# @app.route("/hindi", methods = ["GET"])
# def hindi():
#     return render_template("hindi.html")

if __name__ == "__main__":
    app.run(debug=True)