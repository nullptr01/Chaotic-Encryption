#!/usr/bin/python3
import sys
BLOCK = 10
MOD = 95
def decrypt_helper(keys, string):
	result = ""
	q = len(string) // BLOCK
	for i in range(q):
		part = list(string[i * BLOCK: (i + 1) * BLOCK])
		keystream = keys[i]
		for key, char in zip(keystream, part):
			result = result + chr(((ord(char) - 32 - key) % MOD) + 32)
	return result
def decrypt(in_filename, key_filename):
	key_file = open(key_filename, "r")
	key_string = key_file.read()
	keys = []
	q = len(key_string) // BLOCK
	for i in range(q):
		keystream = []
		for j in range(BLOCK):	
			key = ord(key_string[(i * BLOCK) + j])
			keystream.append(key)
		keys.append(keystream)
	in_file = open(in_filename, "r")
	string = in_file.read()
	original = decrypt_helper(keys, string)
	out_file = open("./original.txt", "w")
	out_file.write(original)
	return "original.txt"
def main():
	args = sys.argv
	argc = len(args)
	ciphertext_filename = ""
	key_filename = ""
	obtained = 0
	for i in range(len(args)):
		 if args[i] == "-t":
		 	if i + 1 <= argc - 1:
		 		obtained += 1
		 		ciphertext_filename = args[i + 1]
		 elif args[i] == "-k":
		 	if i + 1 <= argc - 1:
		 		obtained += 1
		 		key_filename = args[i + 1]
	if obtained != 2:
		print("usage: encrypt [-t ciphertext] [-k keyfile]")
	else:
		out_filename = decrypt(ciphertext_filename, key_filename)
		print("original text saved as \"" + out_filename + "\"")
if __name__ == "__main__":
	main()
