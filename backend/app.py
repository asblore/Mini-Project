from flask import Flask,render_template,request,send_file,jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rit_data_center_new'

mysql = MySQL(app)


@app.route("/")
def root():
    return "Hello, this is a Flask server listening at port 5000!"

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

@app.route('/HS1graph',methods=['GET'])
def plot1():
    try:
        cur=mysql.connection.cursor()
        try:
            fields = request.get_json()
            cur.execute("SELECT "+fields['x']+",COUNT(usn) AS NoOfStu FROM higher_studies GROUP BY "+fields['x'])
            data=cur.fetchall()
            df=pd.DataFrame(data,columns=['Country','NoOfStu'])
            f, ax = plt.subplots(figsize=(10,5))
            plt.bar(df['Country'],df['NoOfStu'])
            plt.xticks(fontsize=8, rotation=90)
            plt.xlabel('Country')
            plt.ylabel('NoOfStu')
            bytes_image = io.BytesIO()
            plt.savefig(bytes_image, format='png')
            bytes_image.seek(0)
            return send_file(bytes_image,attachment_filename='HS1.png',mimetype='image/png')
        except:
            mysql.connection.commit()
            cur.close()
            return "Fetch error"
    except:   
        return "Cannot connect to database!"

@app.route('/HS1data',methods=['POST'])
def data1():
    try:
        cur=mysql.connection.cursor()
        try:
            fields = request.get_json()
            cur.execute("SELECT "+fields['x']+",COUNT(usn) AS NoOfStu FROM higher_studies GROUP BY "+fields['x'])
            rv=cur.fetchall()
            payload = []           
            content = {}
            for result in rv:
                content = {'Country': result[0], 'NoOfStu': result[1]}
                payload.append(content)
                content = {}
            return jsonify(payload)
        except:
            mysql.connection.commit()
            cur.close()
            return "Fetch error"
    except:   
        return "Cannot connect to database!"

field=None

@app.route('/fields',methods=['POST'])
def getFields():
    global field
    field=request.get_json()
    return "Fields initialized successfully"

@app.route('/HS2graph',methods=['GET'])
def plot2():
    try:
        cur=mysql.connection.cursor()
        try:
            cur.execute("SELECT "+field['x']+",COUNT(usn) AS NoOfStu FROM higher_studies GROUP BY "+field['x'])
            data=cur.fetchall()
            df=pd.DataFrame(data,columns=['Country','NoOfStu'])
            f, ax = plt.subplots(figsize=(10,5))
            plt.bar(df['Country'],df['NoOfStu'])
            plt.xticks(fontsize=8, rotation=90)
            plt.xlabel('Country')
            plt.ylabel('NoOfStu')
            bytes_image = io.BytesIO()
            plt.savefig(bytes_image, format='png')
            bytes_image.seek(0)
            return send_file(bytes_image,attachment_filename='HS1.png',mimetype='image/png')
        except:
            mysql.connection.commit()
            cur.close()
            return "Fetch error"
    except:   
        return "Cannot connect to database!"


@app.route('/HS2data',methods=['POST'])
def data2():
    try:
        cur=mysql.connection.cursor()
        try:
            cur.execute("SELECT "+field['x']+",COUNT(usn) AS NoOfStu FROM higher_studies GROUP BY "+field['x'])
            rv=cur.fetchall()
            payload = []           
            content = {}
            for result in rv:
                content = {'Country': result[0], 'NoOfStu': result[1]}
                payload.append(content)
                content = {}
            return jsonify(payload)
        except:
            mysql.connection.commit()
            cur.close()
            return "Fetch error"
    except:   
        return "Cannot connect to database!"
