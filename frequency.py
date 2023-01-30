#!/usr/bin/python3
import os
import sys
from statistics import mean # Average

path = os.getcwd() # Variable that stores the directory path where the script was invoked.
alphanumeric_dictionary, position, password_size = ({} for _ in range(3)) # Dictionaries used to store the data extracted from the wordlist, the positions and password sizes. 
max_size, total_passwords, input_size, skipped_passwords = 0, 0, 0, 0 # Int variables used to store the max size of passwords seen in the wordlist, the total of passwords, the input_size variable used to define the max password size to be analyses, and the total number of skipped passwords.
imported_charset = str() # # Variable that stores the custom charset that is going to be used.
total = dict([("total", 0)]) # Dictionary used to store the total number of times each character appears and the total character seen in the wordlist.
media = list() # List variable used to store password sizes to calculate their average size.
s_val, c_val = False, False # Variable that stores a boolean value that is used to define if the script will limit the passwords size to be analyzed, or if a custom charset is going to be used.

# Function that prints the accepted script parameters when invoked, how to convert the wordlist into UTF-8 format and exists the script.
def help():
    print("-h		Help.\n-i		Input File.\n-o		Output File.\n-s		Maximum Password Size (Optional).\n-c		Input Charset File (Optional).\n\nMake sure to remove non UTF-8 characters from the wordlist. For that, use the following command:\n    iconv -f ISO-8859-1 -t UTF-8 /path/to/original_wordlist.txt -o /path/to/output_wordlist.txt")
    sys.exit(0)

# Function that checks if the s_val is True. If so, it then compares the size of the password with the defined max password size. If the password size is less or equal to the max password size, it will check if the c_val is True. If True it will invoke the check_char function and see if it returns True. If so, it will invoke the size and password functions, else it will increment the skipped_passwords variable. If the c_val or s_val variables are False, it will simply invoke the size and password functions.
def analysis(x, y):
    global skipped_passwords, s_val, c_val, input_size

    if s_val == True:
        if x <= input_size:
            if c_val == True:
                if check_char(y) == True:
                    size(int(x))
                    password(y)
                else:
                    skipped_passwords += 1
            else:
                size(int(x))
                password(y)
        else:
            skipped_passwords += 1
    else:
        if c_val == True:
            if check_char(y) == True:
                size(int(x))
                password(y)
            else:
                skipped_passwords += 1
        else:
            size(int(x))
            password(y)

# Function that checks all the characters in the given password and sees if any of their values do not exist in the given charset.
def check_char(char):
    global imported_charset

    for x in range(0, (len(char))):
        if char[x] == "\n":
            pass
        elif char[x] not in imported_charset:
            return False
        
    return True

# Function that increments the total_passwords variable and increments the corresponding size on a dictionary that stores the number and sizes of passwords seen in the wordlist. 
def size(s):
    global total_passwords
    total_passwords += 1

    if s not in password_size.keys():
        password_size[s] = int(1)
    else:
        password_size[s] = int(password_size[s] + 1)

# # Function that splits the password into characters. It then checks if the characters do not correspond to any of the defined special characters. If so, it then stores in a nested dictionary the characters as the keys and the positions and times it has been seen into the second dictionary. It also increments the value of characters seen on that position, stored in a different dictionary, increments the total number of characters and the total of times that character has been seen on the wordlist, it also checks and increments, if true, the max size of the passwords seen. 
def password(tmp):
    global alphanumeric_dictionary, total, position, max_size

    for z in range(0, len(tmp)):

        if tmp[z] != "\n" and tmp[z] != "\t" and tmp[z] != "\r" and tmp[z] != "":
            if tmp[z] not in alphanumeric_dictionary.keys():
                alphanumeric_dictionary[tmp[z]] = {f"{z}_entry" : int(1)}
                total[tmp[z]] = int(1)

                if z not in position.keys():
                    position[z] = int(1)
                else:
                    position[z] += 1
            elif f"{z}_entry" not in alphanumeric_dictionary[tmp[z]]:
                alphanumeric_dictionary[tmp[z]][f"{z}_entry"] = int(1)
                total[tmp[z]] += 1
                
                if z not in position.keys():
                    position[z] = int(1)
                else:
                    position[z] += 1
            else:
                alphanumeric_dictionary[tmp[z]][f"{z}_entry"] = int(alphanumeric_dictionary[tmp[z]][f"{z}_entry"] + 1)
                total[tmp[z]] += 1
                position[z] += 1

            total["total"] += 1

            if z > max_size: 
                max_size = z + 1

# Function that processes the received character, if it corresponds to any of the specific characters it will alter them to be accepted in the CSV interpreter, it then returns them.
def process(char):
    charset = str()
    
    if char == '"':
        charset = str('""""')
    elif char == ';':
        charset == str(';,')
    elif char == str(","):
        charset = str("\",\"")
    elif char == ' ':
        charset = str('" "')
    else:
        charset = str(char)
    
    return charset

# If condition that checks if all of the mandatory parameters are present in the script invocation and/or if the -h parameters is present. If so, it invokes the help function.
if "-h" in sys.argv or "-i" not in sys.argv or "-o" not in sys.argv:
    help()

#For loop that checks all values provided in the script invocation to identify any of the defined script parameters and imports the values defined after each parameter into the corresponding variables if present.
for i in range(1, len(sys.argv)):
    if "-i" in sys.argv[i]:
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
    elif "-o" in sys.argv[i]:
        try:
            output = str(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the name of the Output File if it's in the same directory as the script or the full path to it!\n")
            help()
        else:
            if "/" in output:
                FileToSave = output
            else:
                FileToSave = ( (str(path) + '/' + output))
    elif "-s" in sys.argv[i]:
        s_val = True
        try:
            input_size = int(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the max password size as a number!\n")
            help()
    elif "-c" in sys.argv[i]:
        c_val = True
        try:
            char = str(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the name of the Charset File if it's in the same directory as the script or the full path to it!\n")
            help()
        else:
            if "/" in output:
                FileCharset = char
            else:
                FileCharset = ( (str(path) + '/' + char))
            
            try:
                tempFile = open( FileCharset, 'r' )
            except IOError:
                print(f"File \"{FileCharset}\" Can't Be Accessed!")
            else:
                df = list(tempFile)
                imported_charset = df[0]

# Function that tries to open the file defined on the FileToSearch variable and imports the data into a list. Each new line is interpreted as a new value on the list. Then it checks if the last character is equal to the newline character code. If so, it invokes the analysis function, providing the size of the password -1 and the password itself. If not, it then invokes the analysis function, providing the full size of the password and the password itself.
try:
    tempFile = open( FileToSearch, 'r' )
except IOError:
    print(f"File \"{FileToSearch}\" Can't Be Accessed!")
else:
    df = list(tempFile)

    for x in range(0, len(df)):
        tmp = str(df[x])

        if tmp[len(tmp) - 1] == "\n":
            analysis((len(tmp) - 1), tmp)
        else:
            analysis(len(tmp), tmp)

# Function that tries to open the file defined on the FileToSave variable. It then processes, generates and writes three tables to the file. The first one contains the characters seen in the wordlist, the positions that they were seen and the times that they were seen in each position and in total. It also writes the total characters seen in each position and in total, and it calculates those values as percentages. The second table contains the same characters seen in the wordlist and their positions, but their values are calculated  as percentages. The third and last table contains the password sizes and the times they were seen, the total number of passwords and the total number of passwords skipped. All those values are written as both numbers and as percentages. It also calculates the average password size processed by the script. All three tables are ordered from highest to lowest by times each character has appeared.
try:
    tempFile = open( FileToSave, 'w+' )
except:
    print(f"File \"{FileToSave}\" Can't Be Accessed!")
else:
    lable = str("Character")
    total_position = str("Total")
    total_percentage = str("%")

    for x in range(0, max_size):
        lable = str(lable) + str(f", {x + 1}")
        total_position = str(total_position) + str(f", {position[x]}")
        total_percentage = str(total_percentage) + str(f", {round(((position[x]/total['total'])*100),2)}%")

    lable2 = str(lable)
    lable = str(lable) + str(f", Total, %")
    total_position = str(total_position) + str(f", {total['total']}, 100%")
    total_percentage = str(total_percentage) + str(f", , 100%")
    total = dict(sorted(total.items(), key=lambda item: item[1], reverse=True))

    tempFile.write(f"{lable}\n")

    for keys in total.keys():
        if keys == "total":
            pass
        else:
            charset = process(keys)

            for z in range(0, max_size):
                try:
                    charset = str(charset) + str(f", {alphanumeric_dictionary[keys][f'{z}_entry']}")
                except:
                    charset = str(charset) + str(f", 0")
            
            charset = str(charset) + str(f", {total[keys]}, {round(((total[keys]/total['total'])*100),2)}%")
            tempFile.write(f"{charset}\n")

    tempFile.write(f"{total_position}\n{total_percentage}\n\n\n{lable2}\n")

    for keys in total.keys():
        if keys == "total":
            pass
        else:
            charset = process(keys)

            for z in range(0, max_size):
                try:
                    charset = str(charset) + str(f", {round(((alphanumeric_dictionary[keys][f'{z}_entry']/position[z])*100),2)}%")
                except:
                    charset = str(charset) + str(f", 0%")
        
            tempFile.write(f"{charset}\n")

    tempFile.write("\n\nPassword Length, Nº, %\n")

    for keys in sorted(password_size.keys()):
        tempFile.write(f"{keys}, {password_size[keys]}, {round(((password_size[keys]/total_passwords) * 100),2)}%\n")

        for x in range(0, password_size[keys]):
            media.append(keys)

    tempFile.write(f"Total, {total_passwords}, {round(((total_passwords/(total_passwords + skipped_passwords))*100),2)}%\n")
    tempFile.write(f"Average, , {mean(media)}\n")
    tempFile.write(f"Passwords Skipped, {skipped_passwords}, {round(((skipped_passwords/(total_passwords + skipped_passwords))*100),2)}%\n")