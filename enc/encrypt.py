#!/usr/bin/python3
import sys
import functions
BLOCK = 10
MOD = 95
PADDING = '='
def pad_string(string):
	result = string 
	if len(result) % BLOCK != 0:
		while len(result) % BLOCK != 0:
			result = result + PADDING
	return result

def encrypt_helper(string, function):
	result = ""
	string = pad_string(string)
	q = len(string) // BLOCK
	keys = function.gen_keys(q)
	for i in range(q):
		part = list(string[i * BLOCK : (i + 1) * BLOCK])
		keystream = keys[i]
		for key, char in zip(keystream, part):
			result = result + chr(((ord(char) - 32 + key) % MOD) + 32)
	return result, keys

def encrypt(in_filename, out_filename, func):
	in_file = open(in_filename, "r")
	in_string = in_file.read()
	out_string, keys = encrypt_helper(in_string, func)
	out_file = open(out_filename, "w")
	out_file.write(out_string)
	key_filename = "key.txt"
	key_file = open(key_filename, "w")
	key_string = ""
	for keystream in keys:
		for key in keystream:
			key_string += chr(key)
	key_file.write(str(key_string))
	return key_filename

def main():
	args = sys.argv
	argc = len(args)
	function_name = ""
	text_filename = ""
	out_filename = ""
	obtained = 0
	for i in range(len(args)):
		 if args[i] == "-t":
		 	if i + 1 <= argc - 1:
		 		obtained += 1
		 		text_filename = args[i + 1]
		 elif args[i] == "-f":
		 	if i + 1 <= argc - 1:
		 		obtained += 1
		 		function_name = args[i + 1]
		 elif args[i] == "-o":
		 	if i + 1 <= argc - 1:
		 		obtained += 1
		 		out_filename = args[i + 1]
	
	if obtained != 3:
		print("usage: encrypt [-t textfile] [-f function] [-o outfile]")
	else:
		if function_name not in functions.FUNCTIONS:
			print("function not available")
		else:
			function = functions.create_function(function_name)
			key_filename = encrypt(text_filename, out_filename, function)
			print("key stored in \"" + key_filename +"\"")

if __name__ == "__main__":
	main()
