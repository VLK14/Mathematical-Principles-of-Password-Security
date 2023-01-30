import rainbowtables as rt
from rainbowtables.insert import supported_algorithms, insert, insert_wordlists
from passlib.hash import des_crypt, md5_crypt
import codecs
import os
import sys
import time

path = os.getcwd() # Variable that stores the directory path where the script was invoked.
create, ins, search, comp = False, False, False, False

# Function that prints the accepted script parameters when invoked and exists the script.
def help():
    print(f"-h		Help.\n-r		Rainbow Table File Name.\n-c		Create New Rainbow Table.\n-w		Input Wordlist.\n-i 		Insert Passwords From Wordlist.\n-a 		Algorithm To Use {supported_algorithms}.\n-s 		Search Rainbow Table For Hash Mash Up.\n-hash 		Hash To Lookup.\n-com		Compress The Rainbow Table.\n")
    sys.exit(0)

# Function that intakes the hash, converts it to hexadecimal and returns it. If the hash uses the md5 algorithm, it will split the salt from it and leave only the hash.
def hex_encode(hash, hash_type):
    if hash_type == "md5":
        try:
            m = str(hash).split("$")
            hash = m[3]
        except:
            pass

    hash = codecs.encode(hash, 'utf-8')
    hash = codecs.encode(hash, 'hex')
    hash = codecs.decode(hash, 'utf-8')

    return hash

# If condition that checks if all of the mandatory parameters are present in the script invocation and/or if the -h parameters is present. If so, it invokes the help function.
if "-h" in sys.argv or "-r" not in sys.argv or "-a" not in sys.argv or ("-w" in sys.argv and "-i" not in sys.argv) or ("-s" in sys.argv and "-hash" not in sys.argv):
    help()

#For loop that checks all values provided in the script invocation to identify any of the defined script parameters and imports the values defined after each parameter into the corresponding variables if present.
for i in range(1, len(sys.argv)):
    if "-r" in sys.argv[i]:
        try:
            rt.set_directory("/rainbow", full_path=False)
            rt.set_filename(str(sys.argv[i + 1]))
        except:
            print("Something went wrong!\nMake sure to specify the name of the Output File if it's in the same directory as the script or the full path to it!\n")
            help()
    elif "-a" in sys.argv[i]:
        try:
            hashtype = str(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the password size as a number!\n")
            help()
        else:
            if hashtype != "des" and hashtype != "md5":
                help()
    elif "-w" in sys.argv[i]:
        try:
            wordlist = str(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the name of the Input File if it's in the same directory as the script or the full path to it!\n")
            help()
        else:
            if "/" in wordlist:
                FileToSearch = wordlist
            else:
                FileToSearch = ( (str(path) + '/' + wordlist))
    elif "-c" in sys.argv[i]:
        create = True
    elif "-i" in sys.argv[i]:
        ins = True
    elif "-s" in sys.argv[i]:
        search = True
    elif "-hash" in sys.argv[i]:
        try:
            hashval = str(sys.argv[i + 1])
        except:
            hashval = str(input("Hash: "))
    elif "-com" in sys.argv[i]:
        comp = True

if create == True:
    rt.create_directory()
    rt.create_file()

    print("The set directory has been created at", rt.get_directory()) 
    print("The set file has been created at", rt.get_filename(file_extension=True))
    print("The full path of the file is", rt.get_full_path(file_extension=True))
    
    time.sleep(5)

if ins == True:
    insert(FileToSearch, hashtype, wordlist_encoding="utf-8", display_progress=True, compression=comp)

if search == True:
    h = hex_encode(hashval, hash_type = hashtype)

    lookup = rt.search(
        h, rt.get_full_path(file_extension=False), full_path=True, time_took=True, compression=comp) 

    if lookup != False:
        print("The decrypted hash is", lookup[0] + ".") #output - The decrypted hash is https://www.youtube.com/watch?v=iik25wqIuFo.
        print("It was found in", lookup[1], "seconds.") #output - It was found in 0.5 seconds.