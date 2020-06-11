#!/usr/bin/env python3 

import os
import shutil
from Crypto.PublicKey import RSA

def empty_callback():
	return

def replace(fileToSearch,keyPath,keyWord):
	key= open(keyPath).read()
	file=open(fileToSearch).read()
	file=file.replace(keyWord,key)
	
	f = open(fileToSearch,'w')
	f.write(file)
	f.close() 
	
	return	

def insert_keys():
	replace('./shell.php','./shell/pub.key','[PUBLIC-KEY]')
	replace('./shell.php','./shell/priv.key','[PRIVATE-KEY]')
	return
	
def setup_files():
	current_directory=os.getcwd()
	
	local_dir=(current_directory + "/local")
	shell_dir=(current_directory + "/shell")
	
	if not os.path.exists(local_dir):
		os.makedirs(local_dir)
	if not os.path.exists(shell_dir):
		os.makedirs(shell_dir)

	if os.path.exists(current_directory + "CLI.py"):
		try:
			os.remove(current_directory + "CLI.py")
		except:
			print("Cannot remove CLI.py, Permissions Problem")
			os.exit(-1)	
	shutil.copyfile('./src/CLI.py', './CLI.py')
	os.chmod('./CLI.py', 0o755)
	shutil.copyfile('./src/shell.php', './shell.php')	

def save_key(path, keydata, keytype):
	with open(path, 'wb') as content_file:
		os.chmod(path, 0o600)
		if keytype == "private":
			content_file.write(keydata.exportKey('PEM'))
		else:
			content_file.write(keydata.exportKey('OpenSSH'))

def generate_key():
	
	print("Setting up Files..")
	setup_files()
	
	print("Generating CLI Keypair..")
	key = RSA.generate(2048)
	save_key('./local/priv.key', key, "private")
	save_key('./shell/pub.key', key, "public")

	print("Generating Shell Keypair..")
	key = RSA.generate(2048)
	save_key('./shell/priv.key', key, "private")
	save_key('./local/pub.key', key, "public")
	
	print("Linking The Shells..")
	insert_keys()
	
if __name__ == "__main__":
	generate_key()
