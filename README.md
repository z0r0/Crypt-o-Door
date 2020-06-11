# Crypt-o-Door v1.0 A "Secure" PHP Backdooring tool

Copyright (C) 2012  Ian "z0r0" Abreu


## Contact 
Email: (z0r0@shurikenlabs.com)
Twitter: @_z0r0_



## Disclaimer 
Use this tool at your own Risk.
I take no responsibility For it's use, 
or the actions of it's users. This is meant
 to be used as a TOOL for secure vulnerability research only!



## Usage 
./generate.py

What it will do:
	-Will generate two unique RSA Key pairs.
	-Will make every shell tied to it's unique backdoor
	-Will output CLI.py and shell.php
Now:
	-Just upload shell.php to a webserver
	-Call up CLI.py --host=shurikenlabs.com --path=/shell.php
Then:	
	-Profit?


## TODO
1.) Impliment PHP driven RSA encrypt, and Decrypt functions 
	-(removing OpenSSL as a dependancy)
	- Probably best to use libsodium as a dependency here.

2.) Create self decrypting backdoor on runtime.
	
3.) Create a tool that logs fast_cgi's exec calls,so we'll actually be able to easily detect the use of web backdoors.
	
4.) RSA Stateful-shell? (think ssh over php)
	
5.) The ability to issue out new keys during operation.

