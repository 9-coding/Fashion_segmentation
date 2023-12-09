import firebase_admin
from firebase_admin import credentials, firestore, storage, initialize_app
from datetime import datetime

# Firebase 인증 정보 및 초기화
cred = credentials.Certificate('mykey.json')

initialize_app(cred, {'storageBucket': "cloc-bdf74.appspot.com"})
db = firestore.client()
i = 0

def uploadStorage(imagePath, imageName):
    bucket = storage.bucket()
    blob = bucket.blob(f'Result/{imageName}')
    blob.upload_from_filename(imagePath)
    blob.make_public()

    return blob.public_url

