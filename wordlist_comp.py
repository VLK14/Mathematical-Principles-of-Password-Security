import os
import sys
import subprocess

path = os.getcwd() # Variable that stores the directory path where the script was invoked.
pcounter, counter, split_number = 0, 0, 0 # Variable that stores the number of words not present in the generated dictionary, and variable that stores the number of files the wordlist was split into.

# Function that prints the accepted script parameters when invoked and exists the script.
def help():
    print("-h		Help.\n-i		Original Wordlist File.\n-o		Generated Wordlist File(s) (If Multiple Files, Only Provide The Common File Name Part).\n-s		Number Of Files That The Wordlist Was Split Into (Optional).\n")
    sys.exit(0)

# If condition that checks if all of the mandatory parameters are present in the script invocation and/or if the -h parameters is present. If so, it invokes the help function.
if "-h" in sys.argv or "-i" not in sys.argv or "-o" not in sys.argv:
    help()

#For loop that checks all values provided in the script invocation to identify any of the defined script parameters and imports the values defined after each parameter into the corresponding variables if present.
for i in range(1, len(sys.argv)):
    if "-i" in sys.argv[i]:
        try:
            analyzes_file = str(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the name of the Input File if it's in the same directory as the script or the full path to it!\n")
            help()
        else:
            if "/" in analyzes_file:
                FileToSearch = analyzes_file
            else:
                FileToSearch = ( (str(path) + '/' + analyzes_file))
    elif "-o" in sys.argv[i]:
        try:
            outputfile = str(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the name of the Output File if it's in the same directory as the script or the full path to it!\n")
            help()
        else:
            if "/" in outputfile:
                FileToSearch2 = outputfile
            else:
                FileToSearch2 = ( (str(path) + '/' + outputfile))
    elif "-s"  in sys.argv[i]:
        try:
            split_number = int(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the number of files that were used to store the dictionary as a number!\n")
            help()

# Function that tries to open the file defined on the FileToSearch variable and imports its content. Then it greps all words from FileToSearch variable  and checks if they are present in the FileToSearch2 variable, if not the counter variable is incremented. Lastly it reports the total number of missing words from the original wordlist. 
try:
    tempFile = open( FileToSearch, 'r' )
except IOError:
    print(f"File \"{FileToSearch}\" Can't Be Accessed!")
else:
    df = list(tempFile)

    for x in range(0, len(df)):
        if "\n" in df[x]:
            tmp = str(df[x]).split("\n")
            tmp = tmp[0]
        else:
            tmp = str(df[x])

        pcounter += 1

        if split_number == 0:
            output = os.popen(f"grep '{tmp}' {FileToSearch2}").read()
        else:
            for z in range(1, (split_number + 1)):
                output = os.popen(f"grep '{tmp}' {FileToSearch2}{z}.txt").read()

                if output != "":
                    break

        if output == "":
            counter += 1

if counter != 0:
    print(f"Done!\nNumber of words in the original wordlist: {pcounter}!\nNumber of words from the original wordlist that aren't present in the generated dictionary: {counter}!\nWhich is equivalent to {round(((counter / pcounter)*100),20)}%!")
else:
    print(f"Done!\n\nNumber of words in the original wordlist: {pcounter}!\nNo missing words from the original wordlist!")