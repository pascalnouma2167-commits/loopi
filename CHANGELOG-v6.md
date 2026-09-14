# Loopi Makarna v6 — Dükkan Tasarımı

- Ana ürün alanı Dükkan görünümüne dönüştürüldü.
- Kategori, gramaj, fiyat ve öne çıkanlar filtreleri eklendi.
- Fiyat/isim sıralaması ve mağaza içi arama eklendi.
- İndirimli ürünlerde eski fiyat üzeri çizili, yeni fiyat öne çıkarılmış biçimde gösteriliyor.
- İndirim yüzdesi rozetleri eklendi.
- Ürün kartından ürün detay ekranına giriş korunuyor.
- Admin ürün ekranına “Eski fiyat / üzeri çizili fiyat” alanı eklendi.
- Veritabanına `products.old_price` alanı eklendi; v5 geçişi için `database/migrate-v5-to-v6-shop.sql` hazırlandı.
- Çift tıklama önizlemesine 12 örnek ürün ve indirimli ürünler eklendi.
