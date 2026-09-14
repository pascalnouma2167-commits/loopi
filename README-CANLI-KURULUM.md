# Kolay paket notu

Bu ZIP, v5 kodunun **web kökü doğrudan paket ana klasörü olacak şekilde** düzenlenmiş sürümüdür. `index.php` artık ZIP'i açar açmaz görünür. Önce `SITEYI-KUR.md` dosyasını okuyun.

# Loopi Makarna — Canlı Altyapı v4

Bu sürüm PHP 8.2+, MySQL 8+/MariaDB 10.6+, PDO MySQL, cURL, OpenSSL, GD/WebP ve HTTPS için hazırlanmıştır. Bu kolay pakette web sunucusunun **document root** dizini doğrudan ZIP içeriğinin yüklendiği klasördür; kökte `index.php` bulunur. Apache için `.htaccess`, `app/`, `database/`, `bin/`, `storage/` ve yapılandırma dosyalarını web erişimine kapatır. Nginx kullanıyorsanız `deploy-nginx.example.conf` kurallarını uygulayın.

## 1. Zorunlu ortam değişkenleri

Kaynak koda parola/anahtar yazmayın. Sunucuda en az şunları tanımlayın:

- `IYILIK_BASE_URL=https://alanadiniz.com`
- `IYILIK_DB_DSN=mysql:host=localhost;dbname=iyilik_mutfagi;charset=utf8mb4`
- `IYILIK_DB_USER=...`
- `IYILIK_DB_PASS=...`
- `IYILIK_SETUP_TOKEN=` en az 32 karakter kriptografik rastgele değer
- `RESEND_API_KEY=...`
- `ORDER_EMAIL_FROM=Loopi Makarna <siparis@alanadiniz.com>`
- `PAYTR_MERCHANT_ID`, `PAYTR_MERCHANT_KEY`, `PAYTR_MERCHANT_SALT`
- `AFTERSHIP_API_KEY` (canlı kargo için)
- `COMPANY_NAME`, `COMPANY_TAX_NUMBER`, `COMPANY_ADDRESS`, `COMPANY_CONTACT_EMAIL`
- `LEGAL_APPROVED=1` yalnızca KVKK/mesafeli satış/iade metinleri işletmeye göre tamamlanıp hukuki olarak onaylandıktan sonra

E-fatura/e-arşiv için ayrıca seçilecek özel entegratörün gerçek bağlantısı gerekir. `INVOICE_PROVIDER` ve `INVOICE_API_KEY` alanları hazırlık durumunu gösterir; sağlayıcı adaptörü eklenmeden sistem resmi fatura kesildiğini iddia etmez.

## 2. Yeni kurulum

1. Boş veritabanını oluşturun.
2. Ortam değişkenlerini tanımlayın.
3. HTTPS üzerinden `/install.php` sayfasını açıp setup token ile şemayı kurun.
4. `/setup-admin.php` ile ilk admini oluşturun.
5. Authenticator uygulamasıyla 2FA kurulumunu tamamlayın.
6. İlk admin oluşunca install/setup ekranları otomatik kapanır. Ek olarak `IYILIK_SETUP_TOKEN` ortam değişkenini sunucudan kaldırmanız önerilir.

## 3. v2'den yükseltme

Önce DB yedeği alın. Ardından `database/migrate-v2-to-v3.sql` dosyasını **bir kez** çalıştırın ve v4 kodlarını yayınlayın. Migration mevcut v2 hesaplarını kilitlememek için eski kullanıcıları doğrulanmış kabul eder; yeni kayıtlar e-posta doğrulaması gerektirir. Kampanya ve şehir katkıları koşulsuz sıfırlanmaz: migration önce snapshot alır, ardından gerçek `paid` siparişlerden yeniden hesaplar.

## 4. Ödeme, stok ve kupon akışı

Fiyatlar ve toplamlar yalnızca veritabanından hesaplanır. Sipariş oluşturulurken ürün satırları `FOR UPDATE` ile kilitlenir ve stok rezerve edilir. Kupon kullanım adedi artık bekleyen siparişte artırılmaz; ödeme onaylandığında idempotent olarak sayılır. Kupon limiti hesaplanırken son 45 dakikadaki bekleyen rezervasyonlar da hesaba katılır. 45 dakika ödenmeyen siparişler `bin/release-pending.php` ile stoktan serbest bırakılır.

PayTR callback hem HMAC imzasını hem de `total_amount` değerinin DB'deki sipariş toplamıyla birebir eşleşmesini doğrular. Kampanya/şehir katkısı yalnızca ilk başarılı ödeme sırasında işlenir. İade halinde katkı ve kupon sayacı kontrollü şekilde geri alınır; stok yalnızca bir kez geri eklenir.

Cron örneği: `*/5 * * * * php /path/to/bin/release-pending.php`

## 5. Yönetim güvenliği

Admin ve staff girişinde parola + TOTP 2FA zorunludur. İlk 2FA kurulum ekranında da 8/15 dakika rate limit uygulanır; `otpauth://` bağlantısı ve tarayıcıda yerel üretilen QR kod bulunur. Staff rolü ürün fiyatı, stok, kampanya, kargo ücretleri, kupon, kullanıcı rolleri ve ödeme override işlemlerine erişemez; yalnızca sipariş hazırlık/kargo ve standart iade iş akışını yönetir. Kritik değişiklikler `audit_logs` tablosunda aktör, IP, önceki/yeni değer, zaman ve gerekiyorsa gerekçeyle saklanır.

Manuel ödeme onayı veya para iadesi yalnızca admin tarafından, gerekçe girilerek yapılabilir. PayTR kullanılıyorsa normal operasyon sırasında manuel ödeme override kullanılmamalıdır.

## 6. Üyelik güvenliği

Yeni müşteri hesabı e-posta doğrulanmadan giriş yapamaz ve sipariş veremez. Kayıt, doğrulama yeniden gönderme ve şifre sıfırlama uçlarında IP/e-posta temelli rate limit vardır. Şifreler Argon2id/`password_hash()` ile tutulur; düz metin parola saklanmaz.

## 7. Dosya yükleme

Ürün görselleri `finfo` ve gerçek resim doğrulamasından geçirilir, sunucuda GD ile yeniden WebP encode edilir. `assets/products/.htaccess` bu klasörde script/PHP çalıştırılmasını ayrıca engeller.

## 8. SEO ve yasal yayına hazırlık

`robots.php` ve `sitemap.php` dinamik uçları korunur. Apache dışı sunucularda rewrite bağımlılığı olmaması için `php bin/build-seo.php` komutu gerçek `IYILIK_BASE_URL` üzerinden statik `robots.txt` ve `sitemap.xml` üretir. Nginx için `deploy-nginx.example.conf` örneği de pakettedir. Yasal metinler işletmeye özel hale getirilmeden `LEGAL_APPROVED=1` verilmemelidir; production modunda bu onay ve şirket bilgileri tamamlanmadan sipariş oluşturma API'si fail-closed davranır.

## 9. Yayın öncesi test

`php -l` ile tüm PHP dosyalarını, tarayıcıda müşteri/admin akışlarını, PayTR test modunu, e-posta doğrulama/şifre sıfırlamayı, 2FA'yı, stok yarış koşullarını, iade/kupon geri alma akışını ve yükleme klasörünün script çalıştırmadığını doğrulayın. Mümkünse bağımsız pentest ve hukuk/mali müşavir kontrolü yaptırın.

## 10. CSP ve bakım

JavaScript CSP artık `unsafe-inline` kullanmaz; request başına nonce üretilir. Dinamik değerler mümkün olduğunca `data-*` alanları üzerinden harici JS dosyalarına aktarılır. 2FA QR ekranı yalnızca o sayfada, SRI doğrulamalı QRCode.js CDN kaynağına izin verir.

Periyodik bakım için `bin/maintenance.php` eklendi. Varsayılan olarak rate-limit logları 30 gün, kullanılmış/süresi geçmiş tokenlar 7 gün tutulur; audit kayıtları 730 gün sonra önce `storage/audit-archive/*.jsonl.gz` dosyasına arşivlenir, ancak başarılı arşiv yazımından sonra DB'den silinir. Örnek cron: `17 3 * * * php /path/to/bin/maintenance.php`. Süreler `RATE_LIMIT_RETENTION_DAYS`, `TOKEN_RETENTION_DAYS`, `AUDIT_RETENTION_DAYS` ile değiştirilebilir.


## v5 — İlk yönetici 2FA kurulumu
İlk yönetici oluşturulduktan sonra 2FA kurulumu 10 dakika içinde tamamlanmalıdır. Doğrulama ekranı 15 dakikada en fazla 8 başarısız denemeye izin verir. QR kod veya `otpauth://` bağlantısı kullanılabilir; başarılı etkinleştirme audit log'a kaydedilir.

## v7 Dükkan Yönetimi
v6'dan yükseltiyorsanız önce veritabanı yedeği alın, ardından `database/migrate-v6-to-v7-shop-admin.sql` dosyasını çalıştırın. Yönetici panelindeki **Dükkan Yönetimi** sekmesinden ürün görseli, fiyat/indirim fiyatı, gramaj, stok, etiket, satış durumu, içindekiler, alerjen, saklama koşulları ve besin değerleri yönetilebilir.
# v9 abonelik güncellemesi

Mevcut v8 veritabanında `database/migrate-v8-to-v9-subscriptions.sql` dosyasını bir kez çalıştırın. Abonelikler, ödeme sağlayıcısında tekrarlayan ödeme yetkisi açılana kadar güvenli biçimde `payment_pending` durumunda tutulur.

## İyilik payı muhasebe kuralı

İyilik payı müşteriden ayrıca tahsil edilen bir bağış değildir. Sistem, tamamlanan ve iade edilmemiş siparişlerde indirim sonrası ürün bedelini ürünlerin KDV oranlarından arındırır ve kalan tutarın %10’unu işletmenin kendi gelirinden ayrılan iyilik payı olarak kaydeder. Kargo hesaba katılmaz; iadelerde kayıt ters çevrilir. Canlıya çıkmadan önce bu işleyişi mali müşavir ve hukuk danışmanınızla, çalışacağınız yardım kuruluşunun protokolüyle birlikte doğrulayın.
