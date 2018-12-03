import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://ex-django-firebase.firebaseio.com/'
})
dinosaurs=db.reference('dinosaurs')
users=db.reference('users')

# root = db.reference()
# Add a new user under /users.
# new_user = root.child('users').push({
#     'name' : 'Mary Anning', 
#     'since' : 1700
# })

if 0:
	users.order_by_key().limit_to_first(1).get()

import ipdb ; ipdb.set_trace()