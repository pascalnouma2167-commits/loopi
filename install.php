<?php
declare(strict_types=1);require __DIR__.'/app/bootstrap.php';
if(!setup_token_valid()){http_response_code(503);exit('Kurulum devre dışı: güçlü IYILIK_SETUP_TOKEN tanımlanmalıdır.');}
$msg='';
try{$adminExists=(int)db()->query("SELECT COUNT(*) FROM users WHERE role='admin'")->fetchColumn()>0;}catch(Throwable $e){$adminExists=false;}
if($adminExists){http_response_code(404);exit('Kurulum kapalı.');}
if($_SERVER['REQUEST_METHOD']==='POST'){
  if(!hash_equals((string)cfg('setup_token'),(string)($_POST['setup_token']??''))) $msg='Kurulum anahtarı hatalı.';
  else {try{$pdo=db();foreach(['schema.sql','seed.sql'] as $file){$sql=file_get_contents(__DIR__.'/database/'.$file);foreach(preg_split('/;\s*(?:\r?\n|$)/',$sql) as $stmt){$stmt=trim($stmt);if($stmt!=='')$pdo->exec($stmt);}}$msg='Veritabanı hazır. Şimdi ilk yönetici hesabını oluşturabilirsiniz: setup-admin.php';}catch(Throwable $e){error_log('Loopi Makarna install error: '.$e->getMessage());$msg='Kurulum sırasında bir sunucu hatası oluştu. Ayrıntılar sunucu günlüğüne kaydedildi.';}}
}
?><!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Loopi Makarna Kurulum</title><link rel="stylesheet" href="styles.css"></head><body><main class="container" style="padding:60px 20px"><div class="card" style="max-width:650px;margin:auto;padding:30px"><h1>Canlı altyapı kurulumu</h1><p>Kurulum yalnızca güçlü sunucu ortam değişkenleriyle çalışır. Veritabanı ve setup anahtarı kaynak kodunda tutulmaz.</p><form method="post"><label>Kurulum anahtarı<input class="input" name="setup_token" type="password" required></label><button class="btn primary" style="margin-top:14px">Veritabanını hazırla</button></form><p><?=htmlspecialchars($msg)?></p></div></main></body></html>
