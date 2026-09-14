<?php
declare(strict_types=1);require __DIR__.'/app/bootstrap.php';
$post=$_POST;$oid=(string)($post['merchant_oid']??'');$status=(string)($post['status']??'');$total=(string)($post['total_amount']??'');$incoming=(string)($post['hash']??'');
if($oid===''||$status===''||$total===''||$incoming===''){http_response_code(400);exit('PAYTR notification failed: missing data');}
$expected=base64_encode(hash_hmac('sha256',$oid.(string)cfg('paytr.merchant_salt').$status.$total,(string)cfg('paytr.merchant_key'),true));
if(!hash_equals($expected,$incoming)){http_response_code(400);exit('PAYTR notification failed: bad hash');}
$s=db()->prepare('SELECT id,total,payment_status FROM orders WHERE order_no=?');$s->execute([$oid]);$o=$s->fetch();if(!$o){http_response_code(404);exit('PAYTR notification failed: order not found');}
$expectedMinor=(int)round((float)$o['total']*100);if(!ctype_digit($total)||(int)$total!==$expectedMinor){error_log('PAYTR amount mismatch order='.$oid.' expected='.$expectedMinor.' got='.$total);http_response_code(400);exit('PAYTR notification failed: amount mismatch');}
try{if($status==='success'){complete_paid_order($oid);}elseif($o['payment_status']!=='paid'){cancel_order_release_stock((int)$o['id'],'failed');}}catch(Throwable $e){error_log('PAYTR callback order='.$oid.' error='.$e->getMessage());http_response_code(500);exit('PAYTR notification failed');}
echo 'OK';
