from pathlib import Path
root=Path('/mnt/data/shopapply')
# schema add old_price
p=root/'database/schema.sql'; s=p.read_text(); s=s.replace("  price DECIMAL(12,2) NOT NULL,\n", "  price DECIMAL(12,2) NOT NULL,\n  old_price DECIMAL(12,2) NULL,\n"); p.write_text(s)
# seed replace products block
p=root/'database/seed.sql'; s=p.read_text(); a=s.index('INSERT INTO products'); b=s.index('INSERT INTO campaigns',a)
prod="""INSERT INTO products (id,name,category,description,unit,price,old_price,vat_rate,stock,badge,emoji) VALUES
(1,'Sebzeli Tarhana','Temel Gıda','Geleneksel usulle hazırlanmış sebzeli kuru tarhana.','500 g',120,150,10,60,'Çok Satan','🥣'),
(2,'Domates Salçası','Temel Gıda','Yoğun kıvamlı ev yapımı domates salçası.','650 g',119,140,10,60,'','🍅'),
(3,'Sade Erişte','Makarna','Ev yapımı kesme sade erişte.','500 g',81,90,10,50,'','🍜'),
(4,'Çilek Reçeli','Kahvaltılık','Mevsim çilekleriyle küçük partilerde hazırlanır.','380 g',120,160,10,50,'','🍓'),
(5,'Tahin','Kahvaltılık','Özenle kavrulmuş susamdan yoğun kıvamlı tahin.','500 g',170,200,10,40,'','🥄'),
(6,'Üzüm Pekmezi','Kahvaltılık','Yoğun kıvamlı geleneksel üzüm pekmezi.','460 g',149,NULL,10,40,'Yeni','🍇'),
(7,'Biber Salçası','Temel Gıda','Kırmızı biberden hazırlanmış yoğun ev salçası.','650 g',129,NULL,10,35,'Yeni','🌶️'),
(8,'Kepekli Tarhana','Temel Gıda','Kepekli unla hazırlanan geleneksel tarhana.','500 g',109,NULL,10,30,'Yeni','🥣'),
(9,'İncir Reçeli','Kahvaltılık','Olgun incirlerle küçük partilerde hazırlanır.','380 g',139,NULL,10,32,'','🫙'),
(10,'Tam Buğday Erişte','Makarna','Tam buğday unuyla hazırlanmış ev eriştesi.','500 g',99,NULL,10,30,'Yeni','🍜'),
(11,'Kayısı Reçeli','Kahvaltılık','Mevsim kayısılarıyla ev usulü hazırlanır.','380 g',135,NULL,10,25,'','🫙'),
(12,'Köy Tarhanası','Temel Gıda','Uzun fermantasyonlu klasik köy tarhanası.','500 g',129,NULL,10,25,'Çok Satan','🥣')
ON DUPLICATE KEY UPDATE name=VALUES(name),category=VALUES(category),description=VALUES(description),unit=VALUES(unit),price=VALUES(price),old_price=VALUES(old_price),vat_rate=VALUES(vat_rate),stock=VALUES(stock),badge=VALUES(badge),emoji=VALUES(emoji);
"""
s=s[:a]+prod+s[b:]; p.write_text(s)
# migration
(root/'database/migrate-v5-to-v6-shop.sql').write_text("""-- Loopi Makarna v5 -> v6 Dükkan alanları\nALTER TABLE products ADD COLUMN old_price DECIMAL(12,2) NULL AFTER price;\n-- İndirim göstermek için admin panelinde Eski fiyat alanına normal liste fiyatını, Fiyat alanına indirimli satış fiyatını girin.\n""")
# API select + conversion + update
p=root/'api/index.php'; s=p.read_text(); s=s.replace("unit,price,vat_rate,stock", "unit,price,old_price,vat_rate,stock",1); s=s.replace("$p['price']=(float)$p['price'];$p['stock']", "$p['price']=(float)$p['price'];$p['old_price']=$p['old_price']!==null?(float)$p['old_price']:null;$p['stock']",1)
old="$price=max(0,(float)($d['price']??0));$stock=max(0,(int)($d['stock']??0));"
new="$price=max(0,(float)($d['price']??0));$oldPrice=isset($d['oldPrice'])&&$d['oldPrice']!==''?max(0,(float)$d['oldPrice']):null;if($oldPrice!==null&&$oldPrice<=$price)$oldPrice=null;$stock=max(0,(int)($d['stock']??0));"
s=s.replace(old,new)
s=s.replace("UPDATE products SET name=?,category=?,description=?,unit=?,price=?,stock=?,vat_rate=? WHERE id=?", "UPDATE products SET name=?,category=?,description=?,unit=?,price=?,old_price=?,stock=?,vat_rate=? WHERE id=?")
s=s.replace("->execute([$name,$cat,$desc,$unit,$price,$stock,$vat,$id])", "->execute([$name,$cat,$desc,$unit,$price,$oldPrice,$stock,$vat,$id])")
s=s.replace("['name'=>$name,'category'=>$cat,'unit'=>$unit,'price'=>$price,'stock'=>$stock,'vat_rate'=>$vat]", "['name'=>$name,'category'=>$cat,'unit'=>$unit,'price'=>$price,'old_price'=>$oldPrice,'stock'=>$stock,'vat_rate'=>$vat]")
p.write_text(s)
# admin old price field
p=root/'admin/admin.js'; s=p.read_text(); s=s.replace('<label>Fiyat (₺)<input data-price type="number" step="0.01" min="0" value="${p.price}"></label>', '<label>Satış fiyatı (₺)<input data-price type="number" step="0.01" min="0" value="${p.price}"></label><label>Eski fiyat / üzeri çizili (₺)<input data-old-price type="number" step="0.01" min="0" value="${p.old_price??\'\'}" placeholder="İndirim yoksa boş"></label>')
s=s.replace("price:+c.querySelector('[data-price]').value,stock:", "price:+c.querySelector('[data-price]').value,oldPrice:c.querySelector('[data-old-price]').value,stock:")
s=s.replace('Fiyat, ürün adı, gramaj, KDV, stok ve ürün görselleri merkezi veritabanına kaydedilir.', 'Satış fiyatı, indirim öncesi eski fiyat, ürün adı, gramaj, KDV, stok ve ürün görselleri merkezi veritabanına kaydedilir.')
p.write_text(s)
