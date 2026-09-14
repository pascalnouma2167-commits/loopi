# v3 Güvenlik ve İş Kuralı Düzeltmeleri

- Install hata detayları kullanıcıya sızdırılmıyor; log'a yazılıyor.
- Varsayılan/boş setup token ile kurulum tamamen reddediliyor; token yalnız environment üzerinden okunuyor.
- Admin/staff için zorunlu TOTP 2FA eklendi.
- Staff RBAC daraltıldı; finansal/ürün/kampanya/kupon/yetki işlemleri admin-only.
- Kritik admin işlemleri audit log'a yazılıyor.
- Register, forgot ve doğrulama resend rate limitleri eklendi.
- Yeni üyelerde e-posta doğrulaması zorunlu.
- Ürün görselleri gerçek MIME+image doğrulamasından sonra sunucuda yeniden WebP encode ediliyor; upload klasöründe script çalıştırma engelleniyor.
- Kampanya ve şehir başlangıç katkıları sıfırlandı.
- Kampanya toplanan tutar/destekçi sayısı admin tarafından elle değiştirilemiyor.
- Kupon uses_count yalnız ödeme onayında artıyor; pending rezervasyonlar max kullanım hesabına dahil.
- Payment callback sipariş tutarını DB toplamıyla doğruluyor.
- Manuel paid/refund yalnız admin + zorunlu gerekçe + audit log ile mümkün.
- Stok release/refund idempotent hale getirildi; geç ödeme sonrası stok yeniden rezerve edilmeye çalışılıyor.
- Ödenmiş siparişi normal kargo/status ekranından iptal etmek engellendi; refund akışı zorunlu.
- robots/sitemap gerçek base URL'den dinamik üretiliyor.
- Production'da gerçek şirket/yasal onay ve ödeme yapılandırması yoksa sipariş API'si fail-closed.
- v2 -> v3 migration SQL eklendi.
