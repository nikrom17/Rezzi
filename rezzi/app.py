import re
import requests

from flask_cors import CORS
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, static_url_path='')
CORS(app)


@app.route('/')
def showMachineList():
    return render_template('rezzi.html')

if __name__ == "__main__":
    app.run()
