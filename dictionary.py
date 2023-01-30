#!/usr/bin/python3

import os
import sys
import math
import networkx as nx
import matplotlib.pyplot as plt
import threading

path = os.getcwd() # Variable that stores the directory path where the script was invoked.
threadLock = threading.Lock() # Locking mechanism that allows the script to synchronize threads.
split_number, possible_combinations, total_possible_combinations, t = 0, 1, 1, 1 # Variable that stores the number of files the dictionary is going to be written to. Variable that stores the total number of passwords to be generated, the total size of possible passwords, and a variable that stores the number of threads to use when generating passwords using Graph Theory. 
alphanumeric_dictionary, frequency, position, tmp_dict, graph_dict = ({} for _ in range(5)) # Dictionaries used to store the data generated from the frequency script, the processed dataset ordered from highest to lowest values of each position, a dictionary that will store the position of each character when generating a word using lexicographical order, a dictionary that will save all the necessary values to generate the graph.
lexicographical, graph, matrix, index, cont = False, False, False, False, False # Variables that store boolean values that are used to define if the script will use Lexicographic order or Graph theory, if the script will index the processed dataset to the input file for analysis, and a simple variable that allows the script to prompt the user for confirmation to continue to execute or exit the script.

# Python treading class, that defines two functions to create custom threads and run them.
class GThread(threading.Thread):
    def __init__(self, threadID, vertex, l, tempFile):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.vertex = vertex
        self.l = l
        self.tempFile = tempFile

    def run(self):
        graph_word_gen(self.vertex, self.l, self.tempFile)

# Function that prints the accepted script parameters when invoked and exists the script.
def help():
    print("-h		Help.\n-i		Input File.\n-o		Output File.\n-p		Password Size.\n-l		Generate Dictionary Using Lexicographic Order.\n-g		Generate Dictionary Using Graph Theory.\n-m		Generate A Graph Adjacency Matrix And Write It To matrix.txt File (Optional, And Only Appliable When Using Graph Theory).\n-th		Number Of Threads Used To Generate The Wordlist When Using Graph Theory (Optional, Used To Speed-Up The Process of Calculating All Possible Paths From 0 To x Size).\n-a		Index Processed Dataset to Input File (Optional).\n-s		Number Of Files To Be Used To Store The Dictionary, (Optional).\n\nMake sure to specify the method the Script will use to generate the dictionary. The Script can only generate dictionaries either using Lexicographic Order or Graph Theory, not both at the same time.")
    sys.exit(0)

# Function that intakes the file theoretical byte size and converts it into the shortest display file size using the standard Multiple-byte units table.
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"

    try:
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)

        return "%s %s" % (s, size_name[i])
    except:
        print("Error!\nFile Size Too Big To Calculate.\Try Splinting The File Or Increasing The Number Of Files The Script Will Write To.\nExiting!")
        sys.exit(0)

# Function that alters the contents of FileToSave variable, to have a list of files the passwords are going to be written to, with a number in it (1 to the split_number value) to differentiate them.
def fileslipt():
    global FileToSave
    tmp = str(FileToSave).split("/")
    tmpf = list()
    FileToSave = dict([])

    if "." in tmp[(len(tmp) - 1)]:
        tmp2 = str(tmp[(len(tmp) - 1)]).split(".")

        for x in range(0, int(split_number + 1)):
            tmpf.append(f"{tmp2[0]}_{x}.{tmp2[1]}")        
    else:
        tmp2 = str(tmp[(len(tmp) - 1)])

        for x in range(0, int(split_number + 1)):
            tmpf.append(f"{tmp2}_{x}")
    
    tmp.remove(tmp[(len(tmp) - 1)])
    tmp = "/".join(tmp)
    
    for x in range(1, int(split_number + 1)):
        if x != split_number:
            FileToSave[x] = {f"{tmp}/{tmpf[x]}" : int(possible_combinations/split_number)}
        else:
            FileToSave[x] = {f"{tmp}/{tmpf[x]}" : (int(possible_combinations/split_number) + int(possible_combinations%split_number))}
    
# Function that processes the received character, if it corresponds to any of the changed character altered for the CSV interpreter, it returns them to normal.
def process(char):
    charset = str()

    if char == '""""':
        charset = str('"')
    elif char == ';,':
        charset == str(';')
    elif char == str("\",\""):
        charset = str(",")
    elif char == '" "':
        charset = str(' ')
    else:
        charset = str(char)
    
    return charset

# Function that calculates the theoretical file size in bytes. It then invokes the convert_size function to calculate the shortest unite size to display and prints that information to the user. If the file is going to be divided into multiple files, it will calculate the size of each file and how many passwords are going to be written to each one.
def calculate(possible_combinations, total_possible_combinations):
    global min_size, split_number, charsize, FileToSave
    file_size = int(((possible_combinations * min_size) + possible_combinations))

    if lexicographical == True:
        print(f"Number of passwords to be generated with {min_size} character(s): {possible_combinations}. \nTotal number of possible passwords with {min_size} character(s) in the same {charsize} character set: {total_possible_combinations}. \nWhich is equivalent to {round(((possible_combinations / total_possible_combinations)*100),20)}% of the total possible passwords.")
    else:
        if min_size <= 2:
            print(f"Number of passwords generated with {min_size} character(s): {possible_combinations}. \nTotal number of possible passwords with {min_size} character(s) in the same {charsize} character set: {total_possible_combinations}. \nWhich is equivalent to {round(((possible_combinations / total_possible_combinations)*100),20)}% of the total possible passwords.")
        else:
            print(f"Number of passwords generated with {min_size} character(s): {possible_combinations}. \nWhich is equivalent to {round(((possible_combinations / total_possible_combinations)*100),20)}% of the total possible passwords.")

    if split_number != 0:
        if lexicographical == True:
            file_size = int(file_size/split_number)
            fileslipt()
            print(f"Theoretical file sizes to be written: {convert_size(file_size)}.\nEach file will contain {int(possible_combinations/split_number)} passwords.")
        else:
            print(f"Theoretical file sizes written: {convert_size(file_size)}.\nEach file contains {int(possible_combinations/split_number)} passwords.")
    else:
        if lexicographical == True:
            FileToSave = {1 : {FileToSave: int(possible_combinations)}}
            print(f"Theoretical file size to be written: {convert_size(file_size)}.")
        else:
            print(f"Theoretical file size written: {convert_size(file_size)}.")

# Function that prompts the user to see if the script should continue to execute or exist, given the previous information of the total theoretical passwords and file sizes to be generated.
def prompt_user(cont):
    try:
        while cont == False:
            t = str(input("Continue? [Y/N] "))
            if t == "y" or t == "Y":
                cont = True
            elif t == "n" or t == "N":
                sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)

# Function that uses the tmp_dict dictionary that contains the current character of each position to generate a word using lexicographic order. It then increments the value stored on the tmp_dict by one and, if the current value is equal to the length of characters present on that position, restarts the counter and increments the previous position. It then returns the generated word.
def lexicographic_order(tmp_dict):
    global position
    word = list()
    state = False

    for y in range(1, (min_size + 1)):
        tmp = process(position[y][tmp_dict[y]])
        word.append(tmp)
        
    for w in range(min_size, 0, -1):
        if int(tmp_dict[min_size]) == int(len(position[min_size]) - 1) or int(tmp_dict[w]) == int(len(position[w])):
            state = True
            tmp_dict[w] = 0
            if w != 1:
                tmp_dict[(w - 1)] += 1
        else:
            if state == False:
                tmp_dict[len(tmp_dict.keys())] += 1
            break
    
    return ("".join(word) + "\n")

# Function that on a for loop calculates the max total size of characters seen in a single position. Then, another for loop runs to extract the first character of each position and append it to a list, duplicated entries are then removed from the list, and then the contents of the list are added to a dictionary that stores the data needed to generate a simple union graph from the characters of each position. The dictionary will contain each character as a key (vertex) and has the items (edges), a list representing all the connections that the key has on that position. The for loop will then repeat to generate the list and the graph for the second character of each position, and add the edges to existing vertices, or create a new vertex if not in the dictionary, and so on until it was a simple union graph.  Then it check is there are any isolated vertex present in the dictionary and, in case there are vertex with 0 or 1 edge, it will create an artificial edge between the isolated vertices and the vertex with the highest degree (in this case the most seen characters of the imported dataset). This process is based on the pending vertex theorem. The function also checks if the index variable is true, and if so, it opens the file stored in the FileToSearch variable and appends a new table that contains all the necessary information to generate the simple union graph. Finally, it generates the graph, it adds the Vertices, then the Edges and returns the graph. adicionar aresta artificial.
def graph_theory():
    global position, graph_dict, index, alphanumeric_dictionary
    counter, position_size, tmpsize = 0, 0, 0
    tmplist3 = list()

    for keys in position.keys():
        if int(len(position[keys])) > position_size:
            position_size = int(len(position[keys]))
        
    for z in range(0, position_size):
        tmplist = list()

        for x in range(1, int(max_size + 1)):
            try:
                if index == True:
                    tmplist.append(position[x][counter])
                else:
                    tmplist.append(process(position[x][counter]))
            except:
                pass
    
        counter += 1
        tmplist = list(dict.fromkeys(tmplist))

        for x in range(0, len(tmplist)):
            tmplist2 = list()

            for y in range(0, len(tmplist)):
                if len(tmplist) == 1:
                    pass
                elif tmplist[x] == tmplist[y]:
                    pass
                elif tmplist[y] not in tmplist2:
                    tmplist2.append(tmplist[y])
            
            if tmplist[x] not in graph_dict.keys():
                graph_dict[tmplist[x]] = tmplist2
            else:
                tmp = graph_dict[tmplist[x]] + tmplist2
                tmp = list(dict.fromkeys(tmp))
                graph_dict[tmplist[x]] = tmp
    
    for keys in graph_dict.keys():
        if len(list(graph_dict[keys])) <= 1:
            k = list(alphanumeric_dictionary.keys())
            tmplist = list(graph_dict[k[0]])

            graph_dict[keys] = (list(k[0]) + graph_dict[keys])
            tmplist.append(keys)
            tmplist = list(dict.fromkeys(tmplist))
            graph_dict[k[0]] = tmplist
            
    if index == True:
        try:
            tempFile = open( FileToSearch, 'a+' )
        except:
            print(f"File \"{FileToSearch}\" Can't Be Accessed!")
        else:
            for keys in graph_dict.keys():
                if int(len(graph_dict[keys])) > tmpsize:
                    tmpsize = int(len(graph_dict[keys]))
            
            for x in range(2, (tmpsize + 1)):
                tmplist3.append("")

            tempFile.write(f"\n\nVertices, Edges,{','.join(tmplist3)},Total\n")

            for keys in graph_dict.keys():
                tmp = list()

                for x in range(len(graph_dict[keys]), (tmpsize + 1)):
                    if len(graph_dict[keys]) == 0 and x == tmpsize:
                        break
                    tmp.append("")

                tempFile.write(f"{keys}, {', '.join(graph_dict[keys])}{','.join(tmp)}, {len(graph_dict[keys])}\n")
    
    G = nx.Graph()

    for keys in graph_dict.keys():
        G.add_node(process(keys))

    for keys in graph_dict.keys():
        for x in range(0, len(graph_dict[keys])):
            G.add_edge(keys, process(graph_dict[keys][x]))
    
    return G

# Function that generates an adjacency matrix of the Graph created and writes it to \"matrix.txt\" file for analysis.
def gen_matrix(G):
    global path
    print("Generating Matrix!")

    try:
        tempFile = open( f"{path}/matrix.txt", 'w+' )
    except IOError:
        print(f"File \"{path}/matrix.txt\" Can't Be Accessed!")
    else:
        a = nx.to_numpy_matrix(G, nodelist= list(graph_dict.keys()))
        tmp_list = list()

        for keys in graph_dict.keys():
            tmp_list.append(keys)

        tempFile.write(f"     {', '.join(tmp_list)}\n")

        for x in range(0, len(list(graph_dict.keys()))):
            tmpstr = str(a[x]).split("\n")
            tmpstr = str("".join(tmpstr)).split("  ")
            tmpstr = str(" ".join(tmpstr)).split("[[")
            tmpstr = str(tmpstr[1]).split(("]]")) 

            if x == 0:
                tempFile.write(f"{tmp_list[x]}, [[{tmpstr[0]}]\n")
            elif x == (len(list(graph_dict.keys())) - 1):
                tempFile.write(f"{tmp_list[x]}, [{tmpstr[0]}]]")
            else:
                tempFile.write(f"{tmp_list[x]}, [{tmpstr[0]}]\n")

# Function that, when invoked by the threads, generates all possible paths on a for loop between two nodes until x size, then it compares the size of the path with the passwords size and if both are the same, locks the thread, writes to the file, increments the passwords generated using Graph Theory and unlocks the thread. It intakes as values the vertex used as a beginning of the path, a list of vertices to be the end of the paths and the file to write to.
def graph_word_gen(vertex, l, tempFile):
    global possible_combinations, min_size, G

    for x in range(0, len(l)):
        for gpath in nx.all_simple_paths(G, source = process(vertex), target = process(l[x]), cutoff = (min_size - 1)):
            if len(list(gpath)) == min_size:
                threadLock.acquire()
                possible_combinations += 1              
                tempFile.write(f"{''.join(list(gpath))}\n")
                threadLock.release()

# If condition that checks if all of the mandatory parameters are present in the script invocation and/or if the -h parameters is present. If so, it invokes the help function.
if "-h" in sys.argv or "-i" not in sys.argv or "-o" not in sys.argv or "-p" not in sys.argv or "-l" not in sys.argv and "-g" not in sys.argv or ("-l" in sys.argv and "-g" in sys.argv) or ("-l" in sys.argv and "-m" in sys.argv) or ("-l" in sys.argv and "-th" in sys.argv):
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
                FileToSave = outputfile
            else:
                FileToSave = ( (str(path) + '/' + outputfile))        
    elif "-p" in sys.argv[i]:
        try:
            min_size = int(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the password size as a number!\n")
            help()
    elif "-l" in sys.argv[i]:
        lexicographical = True
    elif "-g" in sys.argv[i]:
        graph = True
    elif "-m" in sys.argv[i]:
        matrix = True
    elif "-th" in sys.argv[i]:
        try:
            t = int(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the number of threads or that there are no other \"-th\" parameters on the script invocation!\n")
            help()
    elif "-a" in sys.argv[i]:
        index = True
    elif "-s" in sys.argv[i]:
        try:
            split_number = int(sys.argv[i + 1])
        except:
            print("Something went wrong!\nMake sure to specify the number of files to be used to store the dictionary as a number!\n")
            help()

# Function that tries to open the file defined on the FileToSearch variable and imports the data from the first table into a dictionary, storing the characters as the keys and the number of appearances on each position as the items.
try:
    tempFile = open( FileToSearch, 'r' )
except IOError:
    print(f"File \"{FileToSearch}\" Can't Be Accessed!")
else:
    df = list(tempFile)

    for x in range(0, len(df)):
        if "Character" in df[x]:
            tmp = str(df[x]).split(", ")
            max_size = int(tmp[(len(tmp) - 3)])
        elif "Total" in df[x]:
            break
        elif df[x] != "\n":
            tmp = str(df[x]).split(", ")

            for z in range(1,(len(tmp) - 2)):
                if tmp[0] not in alphanumeric_dictionary.keys():
                    alphanumeric_dictionary[tmp[0]] = {z : tmp[z]}
                else:
                    alphanumeric_dictionary[tmp[0]][z] = int(tmp[z])

# Function that processes all the dataset and stores the information on a nested dictionary. The dictionary contains the position number as the keys, and as the items a second dictionary that contains the characters as the keys and the corresponding number of appearances on that position as the items.
for x in range(1, (max_size + 1)):
    for keys in alphanumeric_dictionary.keys():
        if x not in frequency.keys():
            frequency[x] = {keys : int(alphanumeric_dictionary[keys][x])}
        elif keys not in frequency[x]:
            frequency[x][keys] = int(alphanumeric_dictionary[keys][x])

# For loop function that organizes the previous dictionary by order from highest to lowest on each position.
for keys in frequency.keys():
    frequency[keys] = dict(sorted(frequency[keys].items(), key=lambda item: item[1], reverse=True))

# For loop functions that processes the previous organized dictionary and create a new one that stores the character position as keys and a list of characters previously ordered as the values. On each position, characters that have 0 entries on that position are removed from the list.
for k in frequency.keys():
    tmp = list()

    for key in frequency[k].keys():
        if frequency[k][key] == 0:
            pass
        else:
            tmp.append(key)

    position[k] = tmp

# If condition that checks if the index variable is True. If so, it opens the file stored in the FileToSearch variable and appends a new table that contains the processed character positions with the corresponding characters ordered from highest to lowest for analysis.
if index == True:
    try:
        tempFile = open( FileToSearch, 'a+' )
    except:
        print(f"File \"{FileToSearch}\" Can't Be Accessed!")
    else:
        tmp_list = list(["Position"])
        total = list()
        
        for x in range(1, (max_size + 1)):
            tmp_list.append(f" {x}")
            total.append(str(len(position[x])))

        tempFile.write("\n\n" + ",".join(tmp_list) + "\n")

        for x in range(0, len(alphanumeric_dictionary.keys())):
            tmp_list = list()

            for keys in position.keys():
                tmp = position[keys]
                try:
                    tmp_list.append(tmp[x])
                except:
                    tmp_list.append("")

            tempFile.write(f"Value {x + 1},{','.join(tmp_list)}\n")
        
        tempFile.write(f"Total,{','.join(total)}\n")
        tempFile.close()

# For loop function that calculates total number of possible passwords in the given character set.
for x in range(1, (min_size + 1)):
    total_possible_combinations = int(total_possible_combinations * len(alphanumeric_dictionary.keys()))

charsize = int(len(alphanumeric_dictionary.keys()))

# If condition that checks if the lexicographical variable is True. If so, it will compare the password size provided on the script invocation and the max password size that can be created using the analyzed dataset. If the password size provided is larger, it will inform the user and exit the script. Else, on a for loop function it will generate a dictionary that stores the position of each character when generating a word using Lexicographical Order, and a second for loop function that calculates the total number of passwords of the given size, generated from the processed dataset. Then it invokes the calculate function and prompts the user for confirmation to continue to execute or exit the script.
if lexicographical == True:
    if min_size > max_size:
        print(f"Can Not Generate Passwords Larger Than {max_size} Characters Using Lexicographical Order And The Given Dataset. \nExiting!")
        sys.exit(0)

    for x in range(1, (min_size + 1)):
        tmp_dict[x] = int(0)

    for x in range(1, (min_size + 1)):
        possible_combinations = int(possible_combinations * len(position[x]))

    calculate(possible_combinations, total_possible_combinations)
    prompt_user(cont)

# If condition that checks if the graph variable is True. If so, it generates the graph, then it divides the list of vertices used on the Graph with the number of threads, and generates a dictionary containing the vertices for each thread. It compares the password size provided on the script invocation and the max password size that can be created using the analyzed dataset and Graph Theory. If the password size provided is larger, it will inform the user and exit the script. Else, it will calculate the theoretical passwords and file sizes that the script will generate and inform the users. If the user proceeds, it will check if the adjacency matrix should be generated, and it will also prompt the user if the script should open a new window showing the generated simple union graph or not.
if graph == True:
    G = graph_theory()
    dive = int(len(graph_dict.keys())/t)
    glist1 = dict([])
    possible_combinations, tmpsize, c, i = 0, 0, 0, 1
    FileToSave = {1 : {FileToSave: int(possible_combinations)}}

    for x in range(1, (t + 1)):
        glist1[x] = list([])
    
    for keys in graph_dict.keys():
        if tmpsize <= len(graph_dict[keys]):
            tmpsize = len(graph_dict[keys])
        
        if c == (dive * i) and i != t:
            i += 1

        tmpglist = list(glist1[i])
        tmpglist.append(keys)
        glist1[i] = tmpglist
        c += 1
    
    if min_size > tmpsize:
        print(f"Can Not Generate Passwords Larger Than {tmpsize} Characters Using Graph Theory And The Given Dataset. \nExiting!")
        sys.exit(0)

    if matrix == True:
        gen_matrix(G)

    if min_size >= 3:
        file_size_min = int(((int(total_possible_combinations * 0.05) * min_size) + int(total_possible_combinations * 0.05)))
        file_size_max = int(((int(total_possible_combinations * 0.45) * min_size) + int(total_possible_combinations * 0.45)))

        print(f"Total number of possible passwords with {min_size} character(s) using the {charsize} character set: {total_possible_combinations}. \nThe maximum theoretical percentage of passwords generated using Graph Theory can be 0,45% which is equal to {int(total_possible_combinations * 0.45)} passwords and {convert_size(file_size_max)} of disk space. \nThe minimum theoretical percentage of passwords generated using Graph Theory can be 0,05% which is equal to {int(total_possible_combinations * 0.05)} passwords and {convert_size(file_size_min)} of disk space.")
        
        if min_size >= 6:
            file_size_min2 = int(((int(total_possible_combinations * 0.02) * min_size) + int(total_possible_combinations * 0.02)))
            
            print(f"Keep in mind that when generating passwords larger than 6 characters while using Graph Theory, the total file size can be below the 0,02% of total possible passwords. \nWhich is equal to {convert_size(file_size_min2)} of disk space.")
        
        prompt_user(cont)

    try:
        while cont == False:
            t = str(input("Show Graph? [Y/N] "))
            if t == "y" or t == "Y":
                pos = nx.spring_layout(G,k=20/math.sqrt(G.order())) 
                nx.draw(G, pos, with_labels=True)
                plt.show()
                cont = True
            elif t == "n" or t == "N":
                cont = True
    except KeyboardInterrupt:
        sys.exit(0)

# Removes all entries from alphanumeric_dictionary and frequency dictionaries.
alphanumeric_dictionary = frequency.clear()
print("Writing Passwords!")

# For loop function that will generate the passwords and write them to the output(s) using the corresponding mathematical theorem. When generating passwords using Graph Theory, in order for the script to accelerate the process, it takes advantage of CPU threading. It needs to do so, since when generating the passwords with Graph Theory, it will calculate all possible paths between two vertices until x size path. If Graph Theory is used, and the -s parameter was used on the script invocation, then after generating all the passwords, the script proceeds to slit the files and remove the original file.
for x in range(1, (int(len(FileToSave.keys()) + 1))):
    for key in FileToSave[x].keys():
        print(f"Writing to file: {key}")

    try:
        tempFile = open( key, 'w+' )
    except IOError:
        print(f"File \"{key}\" Can't Be Accessed!")
    else:
        if lexicographical == True:
            for z in range(1, (int(FileToSave[x][key]) + 1)):
                word = lexicographic_order(tmp_dict)
                tempFile.write(word)
        else:
            if min_size == 1:
                for key in graph_dict.keys():
                    tempFile.write(f"{process(key)}\n")
                
                possible_combinations = int(len(graph_dict.keys()))
            else:
                for key1 in graph_dict.keys():
                    threads = list()

                    for keys in glist1.keys():
                        thread = GThread(keys, key1, glist1[keys], tempFile)
                        thread.start()
                        threads.append(thread)

                    for t in threads:
                        t.join()

            tempFile.close()
            calculate(possible_combinations, total_possible_combinations)

            if split_number != 0:
                tmp = str(key).split("/")

                if "." in tmp[(len(tmp) - 1)]:
                    tmp2 = str(tmp[(len(tmp) - 1)]).split(".")
                    tmp2 = tmp2[0]
                else:
                    tmp2 = str(tmp[(len(tmp) - 1)])

                os.system(f"split -d -l {int(possible_combinations/split_number)} --additional-suffix=.txt {key} {tmp2}_")
                
                if int(possible_combinations%split_number) != 0:
                    if "." in tmp[(len(tmp) - 1)]:
                        tmp2 = str(tmp[(len(tmp) - 1)]).split(".")
                    
                        if split_number <= 9:
                            os.system(f"cat {tmp2[0]}_0{split_number}.{tmp2[1]} >> {tmp2[0]}_0{(split_number - 1)}.{tmp2[1]} && rm -r {tmp2[0]}_0{split_number}.{tmp2[1]}")
                        elif split_number == 10:
                            os.system(f"cat {tmp2[0]}_{split_number}.{tmp2[1]} >> {tmp2 [0]}_0{(split_number - 1)}.{tmp2[1]} && rm -r {tmp2[0]}_{split_number}.{tmp2[1]}")
                        else:
                            os.system(f"cat {tmp2[0]}_{split_number}.{tmp2[1]} >> {tmp2[0]}_{(split_number - 1)}.{tmp2[1]} && rm -r {tmp2[0]}_{split_number}.{tmp2[1]}")
                    else:
                        if split_number <= 9:
                            os.system(f"cat {tmp2}_0{split_number} >> {tmp2}_0{(split_number - 1)} && rm -r {tmp2[0]}_0{split_number}.{tmp2[1]}")
                        elif split_number == 10:
                            os.system(f"cat {tmp2}_{split_number} >> {tmp2}_0{(split_number - 1)} && rm -r {tmp2[0]}_{split_number}.{tmp2[1]}")
                        else:
                            os.system(f"cat {tmp2}_{split_number} >> {tmp2}_{(split_number - 1)} && rm -r {tmp2[0]}_{split_number}.{tmp2[1]}")

                os.system(f"rm -r {key}")