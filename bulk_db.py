import sqlite3
import os.path
from os import listdir, getcwd
from IPython.core.display import Image

def get_picture_list(rel_path):
    abs_path = os.path.join(os.getcwd(),rel_path)
    print ('abs_path =', abs_path)
    dir_files = os.listdir(abs_path)
    #print dir_files
    return dir_files

picture_list = get_picture_list('dataset')
print (picture_list)

def create_or_open_db(db_file):
    db_is_new = not os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if db_is_new:
        print ('Creating schema')
        sql = '''create table if not exists PICTURES(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PICTURE BLOB,
        TYPE TEXT,
        FILE_NAME TEXT);'''
        conn.execute(sql) # shortcut for conn.cursor().execute(sql)
    else:
        print ('Schema exists\n')
    return conn
def insert_picture(conn, picture_file):
    with open(picture_file, 'rb') as input_file:
        ablob = input_file.read()
        base=os.path.basename(picture_file)
        afile, ext = os.path.splitext(base)
        sql = '''INSERT INTO PICTURES
        (PICTURE, TYPE, FILE_NAME)
        VALUES(?, ?, ?);'''
        conn.execute(sql,[sqlite3.Binary(ablob), ext, afile]) 
        conn.commit()

conn = create_or_open_db('picture_db.sqlite')

conn = create_or_open_db('picture_db.sqlite')
conn.execute("DELETE FROM PICTURES")
for fn in picture_list:
    picture_file = "dataset/"+fn
    insert_picture(conn, picture_file)
     
for r in conn.execute("SELECT FILE_NAME FROM PICTURES"):
    print (r[0])
 
conn.close()
