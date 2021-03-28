import psycopg2
import hashlib
import os
import requests
from google.cloud import storage
from google.oauth2 import service_account


#We have secrets in a public git repo. This is bad. This is very, very bad.
#However, due to time constraints and the ephemeral nature of this project, we're choosing to ignore this
#If we had time to do it the right way, we'd create a server with access to the database and then send requests to that
optionstring = 'host="rowdyhacks21-8nz.gcp-us-east1.cockroachlabs.cloud", database="rowdy21.signatures", user="secureagent", password="w*24VYZ*xaG%gkbr&", sslmode="verify-full", sslrootcert="rowdyhacks21-ca.crt", port=26257'
bucket_name = "securepdf-sig-store"
projecturl = "http://pdfauth.tech"
stor_key = "blobstoragekey.json"


def connect_to_db():
    conn = psycopg2.connect(optionstring)
    return conn.cursor(), conn


# Returns the id of the user with the email passed as an argument
def queryuser(emailstr):
    cursor, conn = connect_to_db()
    cursor.execute("select id from users where email = %s;", emailstr)
    id = cursor.fetchone()
    cursor.close()
    conn.close()
    return id[0]


# Inserts a new user with the email passed as an argument. Returns the id of the new user
def insertuser(emailstr):
    cursor, conn = connect_to_db()
    cursor.execute('INSERT INTO users (email) values (%s);', emailstr)
    id = queryuser(emailstr)
    conn.commit()
    cursor.close()
    conn.close()
    return id


# Delete a user from the user table based on the email
def deleteuser_byemail(emailstr):
    cursor, conn = connect_to_db()
    cursor.execute("delete * from users where email = %s;", emailstr)
    conn.commit()
    cursor.close()
    conn.close()


# Delete a user from the user table based on the id
def deleteuser_byid(id):
    cursor, conn = connect_to_db()
    cursor.execute("delete * from users where id = %s;", id)
    conn.commit()
    cursor.close()
    conn.close()


def addsig(id, filename):
    # Here we create a hashing object then feed it the input file
    sig_id = hashlib.sha256()
    imgfile = open(filename, "rb")
    sig_id.update(imgfile.read())
    digest = sig_id.hexdigest()
    uploadpath = "images/" + digest

    # Connect to the google cloud bucket associated with the project
    client = storage.Client(credentials=service_account.Credentials.from_service_account_file(stor_key))
    bucket = client.bucket(bucket_name)
    # Upload a file with the hashed name and upload the file a the associated filename
    blob = bucket.blob(uploadpath)
    blob.upload_from_filename(filename)

    # Connect to database to add the new file
    cursor, conn = connect_to_db()
    cursor.execute("insert into signatures (id, hash, address) values (%s, %s, %s);", (id, digest, uploadpath))
    conn.commit()
    cursor.close()
    conn.close()


# Returns a list of image file names, which are images on disk in the cache directory
def getsigs(id):
    # Make sure cache directory exists
    if not os.path.exists(os.path.join(os.getcwd(), "cache")):
        os.mkdir("cache")

    # Get all rows with the right ID
    cursor, conn = connect_to_db()
    cursor.execute("select hash, address from signatures where id = %s;", id)
    signatures = cursor.fetchall()
    hashlist = []

    # Download each file found in the row and then add the filename to the list of saved files
    for row in signatures:
        if not os.path.exists(os.path.join(os.getcwd(), "cache", row[0])):  # Check if the file exists on local disk
            tmpimg = requests.get(projecturl + "/" + row[1])  # If not, grab from server
            open("cache/" + row[0], 'wb').write(tmpimg.content)
        hashlist.append("cache/" + row[0])
    cursor.close()
    conn.close()
    return hashlist
