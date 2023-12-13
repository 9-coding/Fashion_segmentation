import firebase_admin
from firebase_admin import credentials, firestore, storage, initialize_app
from datetime import datetime
import os

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

def isFileExists(imageName, opt):
    imagePath = f"result/{imageName}/{imageName}"
    jacketPath = f"result/{imageName}/crops/jacket/{imageName}"
    shirtPath = f"result/{imageName}/crops/shirt/{imageName}"
    dressPath = f"result/{imageName}/crops/dress/{imageName}"
    pantsPath = f"result/{imageName}/crops/pants/{imageName}"
    shortsPath = f"result/{imageName}/crops/shorts/{imageName}"
    skirtPath = f"result/{imageName}/crops/skirts/{imageName}"
    shoePath = f"result/{imageName}/crops/shoe/{imageName}"
    if os.path.exists(imagePath) and opt == 0:
        return imagePath
    elif os.path.exists(jacketPath) and opt == 1:
        return jacketPath
    elif os.path.exists(shirtPath) and opt == 1:
        return shirtPath
    elif os.path.exists(dressPath) and opt == 1:
        return dressPath
    elif os.path.exists(pantsPath) and opt == 2:
        return pantsPath
    elif os.path.exists(shortsPath) and opt == 2:
        return shortsPath
    elif os.path.exists(skirtPath) and opt == 2:
        return skirtPath
    elif os.path.exists(shoePath) and opt == 3:
        return shoePath
    else:
        return None

def uploadStorage(imagePath, imageName, opt):
    option = [f'Result/{imageName}', f'Top/{imageName}', f'Bottom/{imageName}', f'shoe/{imageName}']

    bucket = storage.bucket()
    blob = bucket.blob(option[opt])
    path = isFileExists(imageName, opt)
    blob.upload_from_filename(path)
    blob.make_public()

    return blob.public_url


def uploadFirestore(imgSrc, time, imagePath, imageName):
    resultUrl = uploadStorage(imagePath, imageName, 0)
    topUrl = uploadStorage(imagePath, imageName, 1)
    bottomUrl = uploadStorage(imagePath, imageName, 2)
    shoeUrl = uploadStorage(imagePath, imageName, 3)
    doc_ref = db.collection(u'modelResult').document(f'{imageName}')
    doc_ref.set({
        u'ctg': "result",
        u'date': time,
        u'downloadURL': resultUrl,
        u'imgSrc': imgSrc,
        u'crop-topURL': topUrl,
        u'crop-bottomURL': bottomUrl,
        u'crop-shoeURL': shoeUrl
    })
