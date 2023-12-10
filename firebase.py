import firebase_admin
from firebase_admin import credentials, firestore, storage, initialize_app
from datetime import datetime

# Firebase 인증 정보 및 초기화
cred = credentials.Certificate('mykey.json')

initialize_app(cred, {'storageBucket': "cloc-bdf74.appspot.com"})
db = firestore.client()

def getStorage(imageName):
    bucket = storage.bucket()
    blob = bucket.blob(f'Cloth/{imageName}')
    updated_time = blob.updated
    time = blob.metadata.updated
    return time

def uploadStorage(imagePath, imageName):
    bucket = storage.bucket()
    blob = bucket.blob(f'Result/{imageName}')
    blob.upload_from_filename(imagePath)
    blob.make_public()

    return blob.public_url

def uploadFirestore(imgSrc, time, imagePath, imageName):
    resultUrl = uploadStorage(imagePath, imageName)
    doc_ref = db.collection(u'modelResult').document(u'user01')
    doc_ref.set({
        u'ctg': "result",
        u'date': time,
        u'downloadURL': resultUrl,
        u'imgSrc': imgSrc
    })

