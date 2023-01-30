from passlib.hash import des_crypt, md5_crypt
password = str(input("Password: "))
md5 = str(md5_crypt.hash(password)).split("$")
md5 = md5[3]
print(f"DES: {des_crypt.hash(password)}\nMD5: {md5}")
