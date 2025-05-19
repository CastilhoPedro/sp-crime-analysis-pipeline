import glob
import os
import userpaths as usr


filepath = os.path.join(usr.get_my_documents(), 'temp')
os.makedirs(filepath, exist_ok=True)

landzonepath = os.path.join(filepath, 'landing zone')
os.makedirs(landzonepath, exist_ok=True)

def kill_folders():
    [os.remove(os.path.join(landzonepath, i)) for i in os.listdir(landzonepath)]
    os.rmdir(landzonepath)
    os.rmdir(filepath)
