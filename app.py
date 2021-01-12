from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


############################################################
# SETUP
############################################################

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/petDatabase"
mongo = PyMongo(app)

############################################################
# ROUTES
############################################################

@app.route('/')
def pet_list():
    
    pet_data = mongo.db.pet.find()

    context = {
        'pet_list' : pet_data
    }

    return render_template('pet_list.html', **context)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        new_pet = {
            'name': request.form.get("pet_name"),
            'photo_url': request.form.get("photo"),
        }
        result = mongo.db.pet.insert_one(new_pet)
        pet_id = result.inserted_id

        return redirect(url_for('pet', pet_id= pet_id))
    else:
        return render_template('create.html')


@app.route('/pet/<pet_id>')
def pet(pet_id):
    
    pet_display = mongo.db.pet.find_one({'_id': ObjectId(pet_id)})
    pet_images = mongo.db.pet_pictures.find({'pet_id': pet_id})
    context = {
        'pet' : pet_display,
        'pet_pictures' : pet_images
    }
    return render_template('pet.html', **context)


@app.route('/images/<pet_id>', methods=['GET', 'POST'])
def images(pet_id):
    if request.method == 'POST':
        pet_picture = {
            'pet_pictures': request.form.get("photo"),
            'pet_id': pet_id
        }
        mongo.db.pet_pictures.insert_one(pet_picture)
        

        return redirect(url_for('pet', pet_id= pet_id))
    else:
        return render_template('images.html')


@app.route('/remove/<pet_id>', methods=['GET', 'POST'])
def remove(pet_id):
    if request.method == 'POST':
    
        picture_id = request.form.get("delete")
        print(picture_id)
        mongo.db.pet_pictures.delete_one({'_id': ObjectId(picture_id)})

        return redirect(url_for('pet', pet_id= pet_id))
    else:

        pet_display = mongo.db.pet.find_one({'_id': ObjectId(pet_id)})
        pet_images = mongo.db.pet_pictures.find({'pet_id': pet_id})
        context = {
                    'pet' : pet_display,
                    'pet_pictures' : pet_images
                }
        return render_template('remove.html', **context)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
    
        pet_id = request.form.get("delete")
        
        mongo.db.pet.delete_one({'_id': ObjectId(pet_id)})

        return redirect(url_for('pet_list'))
    else:
        
        pet_data = mongo.db.pet.find()

        context = {
            'pet_list' : pet_data
        }

        return render_template('remove_pet.html', **context)

if __name__ == '__main__':
    app.run(debug=True)