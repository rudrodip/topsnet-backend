import os
import firebase_admin
from firebase_admin import credentials, firestore

# Get the absolute file path to the serviceAccountKey.json
current_directory = os.path.dirname(os.path.realpath(__file__))
service_account_path = os.path.join(current_directory, "serviceAccountKey.json")

# Initialize Firebase Admin SDK with the serviceAccountKey.json
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

# Get the Firestore client
db = firestore.client()
