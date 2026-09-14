<?php
declare(strict_types=1);require __DIR__.'/app/bootstrap.php';
if(!setup_token_valid()){http_response_code(503);exit('Kurulum devre dışı: güçlü IYILIK_SETUP_TOKEN tanımlanmalıdır.');}
$count=(int)db()->query("SELECT COUNT(*) FROM users WHERE role='admin'")->fetchColumn();if($count>0){http_response_code(404);exit('Kurulum kapalı.');}
$msg='';
if($_SERVER['REQUEST_METHOD']==='POST'){
 $token=(string)($_POST['setup_token']??'');if(!hash_equals((string)cfg('setup_token'),$token)){$msg='Kurulum anahtarı hatalı.';}else{
  $name=clean_text($_POST['name']??'',120);$email=mb_strtolower(clean_text($_POST['email']??'',190));$pass=(string)($_POST['password']??'');
  if($name===''||!filter_var($email,FILTER_VALIDATE_EMAIL)||mb_strlen($pass)<12){$msg='Bilgileri kontrol edin. Şifre en az 12 karakter olmalı.';}else{
   $hash=password_hash($pass,defined('PASSWORD_ARGON2ID')?PASSWORD_ARGON2ID:PASSWORD_DEFAULT);$secret=totp_secret();$s=db()->prepare("INSERT INTO users(name,email,password_hash,phone,city,district,address,role,email_verified_at,totp_secret) VALUES(?,?,?,?,?,?,?,'admin',NOW(),NULL)");$s->execute([$name,$email,$hash,'-','-','-','Yönetici hesabı']);$uid=(int)db()->lastInsertId();audit_log('setup_admin','user',$uid,null,['email'=>$email,'role'=>'admin'],'İlk yönetici oluşturuldu',['id'=>null,'role'=>'system']);$_SESSION['new_admin_uid']=$uid;$_SESSION['new_admin_totp']=$secret;$_SESSION['new_admin_started']=time();header('Location: setup-admin-2fa.php');exit;
  }
 }
}
?><!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>İlk yönetici kurulumu</title><link rel="stylesheet" href="styles.css"></head><body><main class="container" style="padding:60px 20px"><div class="card" style="max-width:560px;margin:auto;padding:30px"><h1>İlk yönetici hesabı</h1><p>Yönetici hesabı sunucu tarafında oluşturulur ve 2FA zorunludur.</p><form method="post"><label>Kurulum anahtarı<input class="input" name="setup_token" required type="password"></label><label>Ad Soyad<input class="input" name="name" required></label><label>E-posta<input class="input" name="email" required type="email"></label><label>Güçlü şifre<input class="input" name="password" minlength="12" required type="password"></label><button class="btn primary full" style="margin-top:14px">Yönetici oluştur</button></form><p><?=htmlspecialchars($msg)?></p></div></main></body></html>
