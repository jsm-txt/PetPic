from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


############################################################
# SETUP
############################################################

app = Flask(__name__)

############################################################
# ROUTES
############################################################

@app.route('/')
def pet_list():
    
    pet_list = ['poodle','cow']
    context = {
        'pet_list' : pet_list,
    }
    
    return render_template('pet_list.html', **context)

if __name__ == '__main__':
    app.run(debug=True)