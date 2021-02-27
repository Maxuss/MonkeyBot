from flask import Flask
from threading import Thread
import datetime


app = Flask('')

@app.route('/')
def home():
    currenttime = datetime.datetime.now()
    timestr = 'monkey bot pinged at ' + timestr
    return timestr

def run():
    app.run(host='0.0.0.0',port='8080')

def keep_alive():
    t = Thread(target=run)
    t.start()