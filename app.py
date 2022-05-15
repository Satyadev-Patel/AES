from dataclasses import replace
from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3 
import aes
import json
import os

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret'

@app.route('/<name>',methods = ['POST','GET'])
def aes_algo(name):
    key = os.urandom(16)
    iv = os.urandom(16)
    name = bytes(name, encoding="ascii")
    encrypted = aes.AES(key).encrypt_ctr(name, iv)
    decrypted = aes.AES(key).decrypt_ctr(encrypted, iv)
    decrypted = decrypted.decode('UTF-8')
    encrypted = encrypted.decode('UTF-8','backslashreplace')
    key = key.decode('UTF-8','backslashreplace')
    iv = iv.decode('UTF-8','backslashreplace')
    # data = Object()
    # data.encrypted = encrypted
    # data.decrypted = decrypted
    # data.original = name.decode('UTF-8')
    # data.key = key
    # data.iv = iv
    # data = data.toJSON()
    data = {
        "encrypted" : encrypted,
        "decrypted" : decrypted,
        "original" : name.decode('UTF-8'),
        "key" : key,
        "iv" : iv
    }
    # print(data)
    data = json.dumps(data)
    # print(data)
    return data
    

if __name__ == '__main__':
    app.run()