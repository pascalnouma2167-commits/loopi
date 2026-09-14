# Loopi Makarna v4 — değişiklikler

- v2→v3 migration artık kampanya/şehir verisini körlemesine sıfırlamaz; snapshot alır ve gerçek `paid` siparişlerden yeniden hesaplar.
- CSP `script-src` içinden `unsafe-inline` kaldırıldı, request nonce altyapısı eklendi. Admin ve şifre sıfırlama inline JS'leri kaldırıldı.
- 2FA enrollment'a 8/15 dakika rate limit, `otpauth://` bağlantısı ve QR kod eklendi.
- QR kod üçüncü taraf API'ye secret göndermeden tarayıcıda üretilir; CDN scripti SRI ile sabitlenmiştir.
- `bin/maintenance.php`: rate-limit/token temizliği ve gzip audit arşivleme/rotasyon.
- `bin/build-seo.php`: Apache/Nginx bağımsız statik robots/sitemap üretimi; Nginx örnek yapılandırması eklendi.
- Statik fallback `robots.txt` ve boş/geçerli `sitemap.xml` eklendi; deployment sırasında build-seo çalıştırılmalıdır.
