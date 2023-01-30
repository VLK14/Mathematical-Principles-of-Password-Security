"""Create the hash table.

This program is mainly for the insert function.
"""
import base64
import json
import math
import os
import random
from passlib.hash import des_crypt, md5_crypt
import string
import codecs
try:
    import sympy
except ImportError:
    raise ImportError("Dependency sympy is missing. Use 'pip install sympy' to install it.")
import zlib
from typing import Any, Dict, Tuple, Union

from .directories import get_full_path
from .errors import AlgorithmError, EncodingError

var = list(string.ascii_letters + string.digits)
supported_algorithms = ["des", "md5"]

__all__ = [
    "insert",
    "insert_wordlists",
    "supported_algorithms"
] 

# Function that intakes the hash, converts it to hexadecimal and returns it. If the hash uses the md5 algorithm, it will split the salt from it and leave only the hash.
def hex_encode(hash, hash_type):
    if hash_type == "md5":
        hash = str(hash).split("$")
        hash = hash[3]
        
    hash = codecs.encode(hash, 'utf-8')
    hash = codecs.encode(hash, 'hex')
    hash = codecs.decode(hash, 'utf-8')

    return hash

# Function that intakes a dictionary that stores the position of each character when generating the salt,  and a second dictionary that contains the charset, and the salt size. Then it generates the salt and returns it.
def gensalt(tmp_dict, position, salt_size):
    s = list()
    state = False

    for y in range(1, (salt_size + 1)):
        tmp = str(position[y][tmp_dict[y]])
        s.append(tmp)
        
    for w in range(salt_size, 0, -1):
        if int(tmp_dict[salt_size]) == int(len(position[salt_size]) - 1) or int(tmp_dict[w]) == int(len(position[w])):
            state = True
            tmp_dict[w] = 0
            if w != 1:
                tmp_dict[(w - 1)] += 1
        else:
            if state == False:
                tmp_dict[len(tmp_dict.keys())] += 1
            break

    return tmp_dict, ("".join(s))

def hash_function1(hash_string, hash_dict_length) -> str:
    """Calculates a hash index."""
    seed = int.from_bytes(hash_string.encode("utf-8"), "big")
    random.seed(seed)
    hash_index = random.randint(-(2 << 32), (2 << 32)) % hash_dict_length
    return str(hash_index)

def hash_function2(hash_string, hash_dict_length) -> str:
    """Calculates a different hash index to hash_function1."""
    seed = int.from_bytes(hash_string.encode("utf-8"), "big")
    random.seed(seed)
    hash_index = random.randint(-(2 << 64), (2 << 64)) % hash_dict_length
    return str(hash_index)

def secondary_insert(collision_stash, display_progress=True, collision_dict_length_multiplier=1) -> Union[Tuple[Dict[str, str], int], int]: 
    """Insert words from the collision stash into a secondary hash table.
    The actual length of the dict includes the probe limit, which makes 
    it so that you don't have to do bounds checking, the table will just rehash.
    """
    collision_dict = {}
    collision_dict_length = sympy.nextprime((len(collision_stash) * 2) * collision_dict_length_multiplier)
    probe_limit = int(math.log(collision_dict_length, 2))

    for x in map(str, range(0, collision_dict_length + probe_limit)):
        collision_dict[x] = ""

    for x in map(str, range(0, len(collision_stash))):
        if display_progress == True:
            print(f"Current word + salt insert: {int(x)+1}/{len(collision_stash)}")

        current_data = collision_stash[int(x)]
        current_index = hash_function1(current_data[0:current_data.find(":")], collision_dict_length)
        current_psl = 0

        while True:

            if current_psl == probe_limit:
                """Returns the collision_dict_length_multiplier so that the main function 
                can increase it and then recall this function."""
                return collision_dict_length_multiplier
            
            if collision_dict[current_index] == "":
                collision_dict[current_index] = current_data + f":{current_psl}"
                break

            else:
                collision_data = collision_dict[current_index][0:collision_dict[current_index].rfind(":")]
                collision_psl = int(collision_dict[current_index][collision_dict[current_index].rfind(":")+1:len(collision_dict[current_index])])

            if current_psl > collision_psl:
                collision_dict[current_index] = current_data + f":{current_psl}"

                current_data = collision_data
                current_psl = collision_psl + 1
                current_index = str(int(current_index) + 1)

            elif current_psl <= collision_psl:
                current_psl = current_psl + 1
                current_index = str(int(current_index) + 1)

    return (collision_dict, collision_dict_length)

def genpass(hash_type, hash_encoder, current_word, hash_dict_length, hash_dict1, hash_dict2, hash_file_directory, collision_stash, collision_dict, collision_dict_length, compression, display_progress):        
    if hash_type == "md5": 
        current_hash = hex_encode(hash_encoder, hash_type)
    elif hash_type == "des":
        current_hash = hex_encode(hash_encoder, hash_type)
    
    data_to_insert = current_hash + ":" + current_word
    data_index1 = hash_function1(current_hash, hash_dict_length)

    if hash_dict1[data_index1] == "":
        hash_dict1[data_index1] = data_to_insert
    else:
        current_dict = "hash_dict1"
        collision = hash_dict1[data_index1]
        collision_hash = collision[0:collision.find(":")]
        collision_loop = 0
        hash_dict1[data_index1] = data_to_insert

        """Start a loop where the collisions will try and find a permanent place. 
        If the loop exceeds 10 runs, break and add to the collision stash,
        which will be sorted after the main insertion."""
        while True:

            if current_dict == "hash_dict1":
                collision_index2 = hash_function2(collision_hash, hash_dict_length)
                if hash_dict2[collision_index2] == "":
                    hash_dict2[collision_index2] = collision
                    break
                else:
                    new_collision = hash_dict2[collision_index2]
                    hash_dict2[collision_index2] = collision

                    collision = new_collision
                    collision_hash = collision[0:collision.find(":")]
                    current_dict = "hash_dict2"

            elif current_dict == "hash_dict2":
                collision_index1 = hash_function1(collision_hash, hash_dict_length)
                if hash_dict1[collision_index1] == "":
                    hash_dict1[collision_index1] = collision
                    break
                else:
                    new_collision = hash_dict1[collision_index1]
                    hash_dict1[collision_index1] = collision

                    collision = new_collision
                    collision_hash = collision[0:collision.find(":")]
                    current_dict = "hash_dict1"

            collision_loop = collision_loop + 1
            if collision_loop == 10:
                collision_stash.append(collision)
                break

    hash_file = open(hash_file_directory, "w")
    content_to_write = json.dumps([hash_dict1, hash_dict2, {}, [0]])
    hash_file.write(content_to_write)
    hash_file.close()
    del hash_dict1, hash_dict2 #clear some memory
   
    if collision_stash != []:
        """Insert any collision cycles into the secondary hash table."""
        if collision_dict != {}:
            for x in map(str, range(0, len(collision_dict))):
                if collision_dict[x] != "":
                    word = collision_dict[x][collision_dict[x].find(":")+1:collision_dict[x].rfind(":")]
                    collision_stash.append(word)

        response = secondary_insert(collision_stash, display_progress=display_progress)
        if isinstance(response, int):
            """Keep calling the function again and again to rehash until we dont need to anymore."""
            while True:
                collision_dict_length_multiplier = response
                response = secondary_insert(collision_stash, display_progress=display_progress, collision_dict_length_multiplier=(collision_dict_length_multiplier * 2))
                if isinstance(response, tuple):
                    """We dont need to rehash anymore."""
                    collision_dict = response[0]
                    collision_dict_length = response[1]
                    break
        else:
            collision_dict = response[0]
            collision_dict_length = response[1]
    
    hash_file = open(hash_file_directory, "r") 
    hash_file_content = json.loads(hash_file.read())
    hash_file.close()
    
    content_to_write = json.dumps([hash_file_content[0], hash_file_content[1], collision_dict, [collision_dict_length]])
    if compression == True:
        """Compress the content so it takes up less space in the file."""
        content_to_write = content_to_write.encode("utf-8")
        content_to_write = zlib.compress(content_to_write, 9)
        content_to_write = base64.b64encode(content_to_write)
        content_to_write = content_to_write.decode("utf-8")

    hash_file = open(hash_file_directory, "w")
    hash_file.write(content_to_write)
    hash_file.close()

def insert(wordlist, hash_type, wordlist_encoding="utf-8", display_progress=True, compression=False) -> None:
    """Insert each word in the wordlist with its corresponding hash."""
    if hash_type not in supported_algorithms:
        raise AlgorithmError(f"Hash algorithm {hash_type} is not currently supported.")

    try:
        wordlist_file = open(wordlist, "r", encoding=wordlist_encoding)
        wordlist = wordlist_file.read().splitlines()
        wordlist_file.close()
    except UnicodeDecodeError:
        raise EncodingError(f"Wordlist {wordlist} is unable to be decoded with the encoding {wordlist_encoding}.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Wordlist {wordlist} not found. It needs to be in the current directory.")

    old_wordlist_length = len(wordlist)
    wordlist = list(set(wordlist)) #remove any duplicate words
    new_wordlist_length = len(wordlist)
    duplicates_found = old_wordlist_length - new_wordlist_length

    hash_file_directory = get_full_path()
    if os.path.isfile(hash_file_directory) == False:
        raise FileNotFoundError("Create the directory (create_directory) and the file (create_file) before inserting.")
    
    hash_file = open(hash_file_directory, "r")
    hash_file_content = json.loads(hash_file.read())
    hash_file.close()

    max_load_factor = 0.5

    collision_stash = []
    if hash_file_content != [{}, {}, {}, []]:
        hash_dict_length = len(hash_file_content[0])
        hash_dict1 = hash_file_content[0]
        hash_dict2 = hash_file_content[1]
        collision_dict = hash_file_content[2]
        collision_dict_length = hash_file_content[3][0]
        """Remove any words from the wordlist that are already in any of the hash dictionaries."""
        hash_dict1_values = hash_dict1.values()
        hash_dict2_values = hash_dict2.values()
        collision_dict_values = collision_dict.values()

        for word in wordlist:
            for data in hash_dict1_values:
                if data[data.find(":")+1:len(data)] == word:
                    wordlist.remove(word)
                    duplicates_found = duplicates_found + 1

            for data in hash_dict2_values:
                if data[data.find(":")+1:len(data)] == word:
                    wordlist.remove(word)
                    duplicates_found = duplicates_found + 1

            for data in collision_dict_values:
                if data[data.find(":")+1:data.rfind(":")] == word:
                    wordlist.remove(word)
                    duplicates_found = duplicates_found + 1
        
        """Calculate if we are going to go over a load factor of 0.5 when we insert the wordlist. If so, rehash before we insert."""
        values_taken = 0
        for x in map(str, range(0, hash_dict_length)):
            if hash_dict1[x] != "":
                values_taken = values_taken + 1
            
            if hash_dict2[x] != "":
                values_taken = values_taken + 1
 
        values_taken = values_taken + len(wordlist)
        load_factor = values_taken / (hash_dict_length * 2) #the load factor includes both tables

        if load_factor >= max_load_factor:
            """Rehash."""
            rehash_list = []
            for x in map(str, range(0, hash_dict_length)):
                if hash_dict1[x] != "":
                    word = hash_dict1[x][hash_dict1[x].find(":")+1:len(hash_dict1[x])]
                    rehash_list.append(word)
                
                if hash_dict2[x] != "":
                    word = hash_dict2[x][hash_dict2[x].find(":")+1:len(hash_dict2[x])]
                    rehash_list.append(word)
            rehash_list = rehash_list + wordlist

            wordlist = rehash_list
            hash_dict_length = sympy.nextprime(len(wordlist) * 2)
            hash_dict1 = {}
            hash_dict2 = {}

            for x in map(str, range(0, hash_dict_length)):
                hash_dict1[x] = ""
                hash_dict2[x] = ""
    
    else:
        hash_dict_length = sympy.nextprime(len(wordlist) * 2)
        hash_dict1 = {}
        hash_dict2 = {}
        collision_dict = {}
        collision_dict_length = 0

        for x in map(str, range(0, hash_dict_length)):
            hash_dict1[x] = ""
            hash_dict2[x] = ""

    if display_progress == True:
        print(f"Removed {duplicates_found} duplicate(s) from wordlist.")

    for x in map(str, range(0, len(wordlist))): 

        if display_progress == True:
            print(f"Current word + salt insert: {int(x)+1}/{len(wordlist)}")

        tmp_dict, position = ({} for _ in range(2))
        current_word = wordlist[int(x)] 
        
        if hash_type == "des":
            salt_size = int(2)

            for y in range(1, (salt_size + 1)):
                tmp_dict[y] = int(0)
                position[y] = var

            for y in range(1, (int(len(var)**salt_size) + 1)):
                tmp_dict, salt = gensalt(tmp_dict, position, salt_size)
                hash_encoder = des_crypt.using(salt=salt).hash(current_word)
                genpass(hash_type, hash_encoder, current_word, hash_dict_length, hash_dict1, hash_dict2, hash_file_directory, collision_stash, collision_dict, collision_dict_length, compression, display_progress)

        elif hash_type == "md5":            
            salt_size = int(8)

            for x in range(1, (salt_size + 1)):
                tmp_dict[x] = int(0)
                position[x] = var
            
            for x in range(1, (int(len(var)**salt_size) + 1)):
                tmp_dict, salt = gensalt(tmp_dict, position, salt_size)
                hash_encoder = md5_crypt.using(salt=salt).hash(current_word)
                genpass(hash_type, hash_encoder, current_word, hash_dict_length, hash_dict1, hash_dict2, hash_file_directory, collision_stash, collision_dict, collision_dict_length, compression, display_progress)

def insert_wordlists(wordlists, hash_type, wordlist_encoding="utf-8", display_progress=True, compression=False) -> None:
    """Insert a list of wordlists."""
    if not isinstance(wordlists, list):
        raise TypeError(f"Wordlists input must be type list, not type {type(wordlists).__name__}.")

    for wordlist in wordlists:
        insert(wordlist, hash_type, wordlist_encoding=wordlist_encoding, display_progress=display_progress, compression=compression)