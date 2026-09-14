# Loopi Makarna v9 — Abonelik

- Üç İyilik Kutusu abonelik planı eklendi.
- Aylık ve iki ayda bir teslimat seçenekleri eklendi.
- Yıllık alışveriş ve %10 iyilik payı hesaplayıcısı eklendi.
- Üyelik hesabına abonelik listeleme, duraklatma, yeniden başlatma ve iptal akışı eklendi.
- Abonelik kayıtları ve yönetici listesi için güvenli API uçları eklendi.
- Tekrarlayan ödeme yetkisi hazır olana kadar abonelikler `payment_pending` durumunda tutulur; kart verisi uygulamada saklanmaz.
- `database/migrate-v8-to-v9-subscriptions.sql` veritabanı geçişi eklendi.
- v9.1: Orta genişliklerde masaüstü menüsünün üst üste binmesi engellendi; menü daha erken mobil düzene geçiyor.
- v9.1: Abonelik kartları, hesaplayıcı, form ve uzun Türkçe metinler için taşma/kırılma düzeltmeleri eklendi.
- v9.2: Sol üstteki Ürünler kontrolü yerel HTML'de de çalışan bağlantı yedeği, klavye erişimi ve güvenilir mega menü açma/kapama davranışıyla düzeltildi.

## Canlıya geçiş notu

v8 kurulumunda önce `database/migrate-v8-to-v9-subscriptions.sql` çalıştırılmalıdır. Otomatik tahsilat için ödeme sağlayıcısında tekrarlayan ödeme/tokenizasyon sözleşmesi ayrıca etkinleştirilmelidir.
