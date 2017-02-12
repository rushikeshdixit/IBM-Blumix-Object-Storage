print (30 * '-')
print ("   M A I N - M E N U")
print (30 * '-')
print ("1. Create containers")
print ("2. List your containers")
print ("3. Create file")
print ("4. Encrypt file")
print ("5. Upload file")
print ("6. Download file")
print ("7. Decrypt file")
print ("8. List details")
print ("9. Delete an object")
print ("10. Delete container")
print ("11. Exit")
print (30 * '-')


import swiftclient.client as swiftclient
import gnupg
import keystoneclient
import easygui
import Tkinter
import tkFileDialog
import os
from tkFileDialog  import askdirectory
import humanize
import ntpath
#import tkinter as tk
#from tkinter import filedialog
#import urllib3

auth_url='<URL>/v3'
projectId='<ID>'
region_name='<regionname>'
userId='<userID>'
password='Your Password'

conn = swiftclient.Connection(key=password, authurl=auth_url, auth_version='3', os_options={"project_id": projectId, "user_id": userId, "region_name": region_name})


#encrypt file
gpg=gnupg.GPG(gnupghome='<specify path>')
#generate RSA keys
input_data=gpg.gen_key_input(key_type="RSA", key_length=1024, passphrase='abcd')
key=gpg.gen_key(input_data)
global fa
container_name='<container name>'
def next_file_name():
    num = 1
    while True:
        file_name = 'file%d.gpg' % num
        if not os.path.exists(file_name):
            return file_name
        num += 1

running=True
while running:
    #validation for integer value
    is_valid=0
    while not is_valid :
        try :
                choice = int ( raw_input('Enter your choice [1-11] : ') )
                is_valid = 1 ## set it to 1 to validate input and to terminate the while..not loop
        except ValueError, e :
                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])
    if choice == 1:
        # Create a new container

        conn.put_container(container_name)
        print "\nContainer %s created successfully." % container_name
    elif choice == 2:
        # List your containers
        print ("\nContainer List:")
        for container in conn.get_account()[1]:
            print container['name']
    elif choice == 3:
        #create file
        root = Tkinter.Tk()
        root.withdraw()
        root.update()
        fa = tkFileDialog.askopenfilenames(parent=root,initialdir="/",title='Choose a file')
        size=0
        for filenames in fa:
            #d=os.path.basename(filenames)
            size += os.path.getsize(filenames)
            #print root.tk.splitlist(d)
        #file_name=os.path.basename(fa)

        #size=os.stat(lst).stsize
        a=humanize.naturalsize(size)
        print('File created successfully')
        print(a)

        #open(file_name, 'w').write('Hello')
        #print ("File Created")
    elif choice == 4:
        #open file and encrypt using public key
        if size<=1048576:
            for s in fa:
                with open(s,'rb') as f:

                    status = gpg.encrypt_file(f,recipients=None, symmetric="AES256", output=next_file_name(), passphrase='abcd', armor=False)
                    print("File successfully encrypted")
        else:
            print('File too large, select another file')
    elif choice == 5:
        #upload file
        encrypted_file='output.gpg'
        with open(encrypted_file,'r') as e:
            conn.put_object(container_name,encrypted_file,contents=e.read())
            print("File successfully uploaded")
    elif choice == 6:
        # Download an object and save it
        obj = conn.get_object(container_name, encrypted_file)
        with open(encrypted_file, 'w') as my_example:
               my_example.write(obj[1])
               print "\nObject %s downloaded successfully." % encrypted_file
    elif choice == 7:
        #decrypt the file data that was downloaded from the IBM Bluemix
        encrypted_file='output.gpg'
        with open(encrypted_file, 'rb') as f:
            status = gpg.decrypt_file(f, passphrase='abcd', output='decrypted_file.txt')
            print("File decrypted successfully")
    elif choice == 8:
            # List objects in a container, and prints out each object name, the file size, and last modified date
            print ("\nObject List:")
            for container in conn.get_account()[1]:
                for data in conn.get_container(container['name'])[1]:
                    print 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
    elif choice == 9:
        #delete an object
        file_name=raw_input('Enter File name with extension:')
        conn.delete_object(container_name, file_name)
        print "\nObject %s deleted successfully." % file_name
    elif choice == 10:
        # To delete a container. Note: The container must be empty!
        conn.delete_container(container_name)
        print "\nContainer %s deleted successfully.\n" % container_name
    elif choice == 11:
        break
    else:
        print ("Invalid number. Try again...")
        break
