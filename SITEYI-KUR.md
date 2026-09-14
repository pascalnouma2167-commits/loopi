# Loopi Makarna — Kolay Kurulum

Bu pakette ana site dosyası artık ZIP'in en üst seviyesindeki **index.php** dosyasıdır.

## En kısa kurulum

1. ZIP'i bilgisayarında aç.
2. İçindeki dosya ve klasörlerin **tamamını** hostingindeki web kök klasörüne yükle. Bu klasör çoğu hostingde `public_html`, `httpdocs` veya `www` adını taşır.
3. Alan adını açtığında sunucu otomatik olarak kökteki `index.php` dosyasını çalıştırır.
4. MySQL veritabanını oluştur ve gerekli ortam değişkenlerini hosting panelinden tanımla. Değerlerin listesi `config.example.php` ve `README-CANLI-KURULUM.md` içindedir.
5. En az 32 karakterlik rastgele `IYILIK_SETUP_TOKEN` değeri tanımla.
6. Tarayıcıdan `https://alanadiniz.com/install.php` adresine git; ekrandaki alana `IYILIK_SETUP_TOKEN` değerini girerek veritabanını kur.
7. Ardından `https://alanadiniz.com/setup-admin.php` adresini aç; kurulum anahtarını forma girerek ilk yönetici hesabını ve 2FA'yı oluştur.
8. Kurulum bittikten sonra hosting panelinden `IYILIK_SETUP_TOKEN` değerini değiştir veya kaldır. Kurulum ekranı tekrar kullanılamaz hale gelmelidir.

## Yönetici paneli

Kurulumdan sonra yönetici girişi:

`https://alanadiniz.com/admin/login.php`

Bu adres müşteri menülerinde gösterilmez. Yönetici/staff girişinde parola ve 2FA kullanılır.

## Önemli

Bu sürüm artık statik HTML değildir. `index.php` dosyasına bilgisayarında çift tıklamak siteyi çalıştırmaz. PHP 8.x, MySQL ve HTTPS destekli bir hosting/sunucu gerekir.

Apache kullanan standart paylaşımlı hostinglerde bu paketteki `.htaccess` özel klasörleri (`app`, `database`, `bin`, `storage`) dış erişime kapatır. Nginx kullanıyorsan `deploy-nginx.example.conf` içindeki engelleme kurallarını sunucu yapılandırmana eklemelisin.

Canlı ödeme almadan önce PayTR, e-posta, kargo, şirket/yasal bilgiler ve `LEGAL_APPROVED=1` ayarlarını gerçek değerlerle tamamla. Gerçek API anahtarlarını JavaScript/HTML dosyalarına yazma.
