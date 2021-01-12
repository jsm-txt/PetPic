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

    if mongo.db.profile.find({}) == None:
        profile = {
        'profile_picture': "https://i.guim.co.uk/img/media/20098ae982d6b3ba4d70ede3ef9b8f79ab1205ce/0_0_969_581/master/969.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=a368f449b1cc1f37412c07a1bd901fb5",
        'text': "Enter info about yourself",
        'username': "Enter a username"
        }
        mongo.db.profile.insert_one(profile)
    
       
    profiles = mongo.db.profile.find({})
    prof = list
    for profile in profiles:
        prof = profile
        
    pet_data = mongo.db.pet.find()

    context = {
        'pet_list' : pet_data,
        'profile' : prof
    }

    return render_template('pet_list.html', **context)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get("pet_name")
        photo = request.form.get("photo")
        about = request.form.get("about_pet")
        if name =="":
            return render_template('create.html')
        if photo =="":
            photo = "https://i.guim.co.uk/img/media/20098ae982d6b3ba4d70ede3ef9b8f79ab1205ce/0_0_969_581/master/969.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=a368f449b1cc1f37412c07a1bd901fb5"
        if about =="":
            about = "Nothing to see here"

        new_pet = {
            'name': name,
            'photo_url': photo,
            'about': about
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
            'caption': request.form.get("caption"),
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

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':

        profiles = mongo.db.profile.find({})
        
        prof = None
        for profile in profiles:
            prof = profile

        profile_picture = request.form.get("photo")
        text = request.form.get("caption")
        username = request.form.get("username")
        if profile_picture == "":
            profile_picture = "https://i.guim.co.uk/img/media/20098ae982d6b3ba4d70ede3ef9b8f79ab1205ce/0_0_969_581/master/969.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=a368f449b1cc1f37412c07a1bd901fb5"
        if text =="":
            text = "Enter text"
        if username =="":
            username = "Enter Username"

        mongo.db.profile.update_one({'_id':ObjectId(prof['_id'])},{
            '$set':{
            'profile_picture': profile_picture,
            'text': text,
            'username': username
            }})
        
        return redirect(url_for('pet_list'))
    else:
        return render_template('edit_profile.html')

if __name__ == '__main__':
    app.run(debug=True)