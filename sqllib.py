import psycopg2
import hashlib
from google.cloud import storage
from google.oauth2 import service_account

optionstring = 'host="rowdyhacks21-8nz.gcp-us-east1.cockroachlabs.cloud", database="rowdy21.signatures", user="secureagent", password="w*24VYZ*xaG%gkbr&", sslmode="verify-full", sslrootcert="rowdyhacks21-ca.crt", port=26257'
bucket_name = "securepdf-sig-store" 
projecturl = "http://35.201.121.26" #Leaving this until DNS records update

stor_key = "blobstoragekey.json"

def connect_to_db():
    conn = psycopg2.connect(optionstring)
    return conn.cursor(), conn

#Returns the id of the user with the email passed as an argument
def queryuser(emailstr):
    cursor, conn = connect_to_db()
    cursor.execute("select id from users where email = %s;", emailstr)
    id = cursor.fetchone()
    cursor.close()
    conn.close()
    return id[0]

#Inserts a new user with the email passed as an argument. Returns the id of the new user
def insertuser(emailstr):
    cursor, conn = connect_to_db()
    cursor.execute('INSERT INTO users (email) values (%s);', emailstr)
    id = queryuser(emailstr)
    conn.commit()
    cursor.close()
    conn.close()
    return id

#Delete a user from the user table based on the email
def deleteuser_byemail(emailstr):
    cursor, conn = connect_to_db()
    cursor.execute("delete * from users where email = %s;", emailstr)
    conn.commit()
    cursor.close()
    conn.close()


#Delete a user from the user table based on the id
def deleteuser_byid(id):
    cursor, conn = connect_to_db()
    cursor.execute("delete * from users where id = %s;", id)
    conn.commit()
    cursor.close()
    conn.close()

def addsig(id, filename):
    #Here we create a hashing object then feed it the input file
    sig_id = hashlib.sha256()
    imgfile = open(filename, "rb")
    sig_id.update(imgfile.read())
    digest = sig_id.hexdigest()
    uploadpath = "images/" + digest

    #Connect to the google cloud bucket associated with the project
    client = storage.Client(credentials=service_account.Credentials.from_service_account_file(stor_key))
    bucket = client.bucket(bucket_name)
    #Upload a file with the hashed name and upload the file a the associated filename
    blob = bucket.blob(uploadpath)
    blob.upload_from_filename(filename)

    #Connect to database to add the new file
    cursor, conn = connect_to_db()
    cursor.execute("insert into signatures (id, hash, address) values (%s, %s, %s);", (id, digest, uploadpath))
    conn.commit()
    cursor.close()
    conn.close()

