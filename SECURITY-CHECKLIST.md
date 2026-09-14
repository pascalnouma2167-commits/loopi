# Canlıya Alma Güvenlik Kontrolü — v3

- [ ] Document root yalnızca `public/`
- [ ] HTTPS zorunlu, HSTS aktif
- [ ] DB ve API sırları yalnız ortam değişkenlerinde
- [ ] `IYILIK_SETUP_TOKEN` en az 32 rastgele karakter; ilk kurulumdan sonra kaldırıldı
- [ ] Admin/staff 2FA kuruldu
- [ ] Admin ve staff yetkileri beklenen RBAC sınırlarında test edildi
- [ ] `audit_logs` değişiklikleri kaydediyor
- [ ] Yeni müşteri e-posta doğrulaması çalışıyor
- [ ] register / forgot / verification resend rate-limit test edildi
- [ ] PayTR test siparişinde HMAC + tutar kontrolü doğrulandı
- [ ] 45 dk pending cron'u stokları yalnız bir kez geri açıyor
- [ ] Kupon kullanım limiti pending rezervasyonlarla birlikte test edildi
- [ ] Refund katkı/şehir/kupon/stok değerlerini idempotent geri alıyor
- [ ] `public/assets/products/` içinde PHP/script çalışmıyor; upload WebP olarak yeniden encode ediliyor
- [ ] Demo kampanya ve şehir katkıları sıfırlandı
- [ ] `IYILIK_BASE_URL` gerçek HTTPS domain
- [ ] Dinamik `/robots.txt` ve `/sitemap.xml` doğru domaini gösteriyor
- [ ] Resend gönderici domaini doğrulandı
- [ ] AfterShip ve PayTR gerçek anahtarları production secrets olarak tanımlandı
- [ ] KVKK, gizlilik, mesafeli satış ve iade metinleri işletmeye göre tamamlandı ve hukuk kontrolünden geçti
- [ ] `COMPANY_*` bilgileri gerçek şirket bilgileri
- [ ] `LEGAL_APPROVED=1` yalnız hukuki onaydan sonra verildi
- [ ] E-fatura/e-arşiv için gerçek GİB/özel entegratör adaptörü tamamlandı (gerekiyorsa)
- [ ] DB otomatik yedekleme ve geri yükleme testi var
- [ ] Sunucu log rotasyonu ve güvenli hata izleme var
- [ ] Bağımsız güvenlik/pentest kontrolü yapıldı

- [ ] `php bin/build-seo.php` çalıştırıldı ve sitemap gerçek HTTPS alan adını içeriyor.
- [ ] `bin/maintenance.php` günlük cron olarak tanımlandı; `storage/audit-archive` web dışı ve yedekleniyor.
- [ ] CSP tarayıcı konsolunda inline-script ihlali üretmiyor.
- [ ] v2 migration öncesi DB yedeği alındı; migration snapshot tabloları ve yeniden hesaplanan katkılar doğrulandı.


### v5 ek kontrolleri
- [ ] İlk yönetici 2FA kurulumu 10 dakikalık oturum süresini uyguluyor.
- [ ] İlk yönetici 2FA doğrulaması 8/15 dk rate limit ile korunuyor.
- [ ] QR kodu yalnızca tarayıcıda oluşturuluyor; TOTP secret üçüncü taraf servise gönderilmiyor.
- [ ] İlk yönetici 2FA etkinleştirmesi `audit_logs` tablosunda görülüyor.
