<?php
declare(strict_types=1);
require __DIR__.'/app/bootstrap.php';
send_csp(['https://cdnjs.cloudflare.com']);

if(!setup_token_valid()){http_response_code(503);exit('Kurulum devre dışı: güçlü IYILIK_SETUP_TOKEN tanımlanmalıdır.');}

$secret=(string)($_SESSION['new_admin_totp']??'');
$uid=(int)($_SESSION['new_admin_uid']??0);
$started=(int)($_SESSION['new_admin_started']??0);
if($secret===''||!$uid||!$started||time()-$started>600){
  unset($_SESSION['new_admin_totp'],$_SESSION['new_admin_uid'],$_SESSION['new_admin_started']);
  http_response_code(410);
  exit('Kurulum oturumunun süresi doldu. İlk yönetici kurulumunu yeniden başlatın.');
}

$s=db()->prepare("SELECT id,name,email,role,totp_secret FROM users WHERE id=? AND active=1 AND role='admin'");
$s->execute([$uid]);
$u=$s->fetch();
if(!$u){http_response_code(404);exit('Kurulum hesabı bulunamadı.');}
if(!empty($u['totp_secret'])){
  unset($_SESSION['new_admin_totp'],$_SESSION['new_admin_uid'],$_SESSION['new_admin_started']);
  header('Location: admin/login.php');exit;
}

$issuer=(string)cfg('app.name','Loopi Makarna');
$otpauth=totp_otpauth_uri($secret,(string)$u['email'],$issuer);
$msg='';
if($_SERVER['REQUEST_METHOD']==='POST'){
  $identity=(string)$uid;
  if(rate_limit_hit('setup_admin_2fa_enroll',$identity,8,15)){
    $msg='Çok fazla doğrulama denemesi. 15 dakika sonra tekrar deneyin.';
  } else {
    rate_limit_record('setup_admin_2fa_enroll',$identity);
    $code=clean_text($_POST['code']??'',6);
    if(totp_verify($secret,$code)){
      db()->prepare('UPDATE users SET totp_secret=? WHERE id=?')->execute([$secret,$uid]);
      audit_log('setup_admin_2fa_enroll','user',$uid,null,['enabled'=>true],'İlk yönetici hesabında 2FA etkinleştirildi',['id'=>null,'role'=>'system']);
      unset($_SESSION['new_admin_totp'],$_SESSION['new_admin_uid'],$_SESSION['new_admin_started']);
      session_regenerate_id(true);
      header('Location: admin/login.php');exit;
    }
    $msg='Kod doğrulanamadı. Telefon saatinin otomatik olduğundan emin olun.';
  }
}
?><!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>2FA Kurulumu · Loopi Makarna</title><link rel="stylesheet" href="styles.css"></head><body><main class="container" style="padding:60px 20px"><div class="card" style="max-width:600px;margin:auto;padding:30px"><h1>İki faktörlü doğrulama</h1><p>Authenticator uygulamanla QR kodu okutabilir veya aşağıdaki anahtarı manuel ekleyebilirsin. Bu kurulum oturumu 10 dakika geçerlidir.</p><div id="qrcode" data-otpauth="<?=htmlspecialchars($otpauth,ENT_QUOTES)?>" style="margin:18px 0"></div><p><a class="btn soft" href="<?=htmlspecialchars($otpauth,ENT_QUOTES)?>">Authenticator uygulamasında aç</a></p><p style="font-size:22px;word-break:break-all"><code><?=htmlspecialchars($secret)?></code></p><p>Hesap: <strong><?=htmlspecialchars((string)$u['email'])?></strong> · Tür: <strong>Zamana dayalı (TOTP)</strong></p><form method="post"><label>6 haneli doğrulama kodu<input class="input" inputmode="numeric" pattern="\d{6}" maxlength="6" name="code" autocomplete="one-time-code" required></label><button class="btn primary full" style="margin-top:14px">2FA'yı doğrula ve tamamla</button></form><p><?=htmlspecialchars($msg)?></p></div></main><script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js" integrity="sha512-CNgIRecGo7nphbeZ04Sc13ka07paqdeTu0WR1IM4kNcpmBAUSHSQX0FslNhTDadL4O5SAGapGt4FodqL8My0mA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script><script src="setup-admin-2fa.js"></script></body></html>
