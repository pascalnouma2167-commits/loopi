# Loopi Makarna v5 — Değişiklikler

- İlk süper-admin 2FA kurulumuna 8 deneme / 15 dakika rate limit eklendi.
- İlk admin 2FA kurulum oturumu 10 dakika ile sınırlandı.
- `setup-admin-2fa.php` için `otpauth://` URI ve SRI sabitlenmiş QR kod desteği eklendi.
- İlk admin 2FA etkinleştirmesi audit log'a yazılıyor.
- Normal admin/staff 2FA kurulumu ile ilk admin kurulumu aynı `totp_otpauth_uri()` yardımcı fonksiyonunu kullanıyor.
- İlk admin oluşturulurken 2FA kurulum başlangıç zamanı session içine kaydediliyor.
