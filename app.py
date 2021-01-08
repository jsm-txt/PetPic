from flask import Flask, request, redirect, render_template, url_for


############################################################
# SETUP
############################################################

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017"
# mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route('/')
def pet_list():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)