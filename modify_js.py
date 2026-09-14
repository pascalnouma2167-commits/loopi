from pathlib import Path
import re
root=Path('/mnt/data/shopapply')
for fname in ['preview-app.js','app.js']:
    p=root/fname
    s=p.read_text()
    s=s.replace("let fav=[],query='',cat='Tümü',selectedCampaignId=null,selectedReviewRating=5;","let fav=[],query='',cat='Tümü',shopGram='Tümü',shopMaxPrice=500,shopDiscount=false,shopNew=false,shopBest=false,shopSort='recommended',selectedCampaignId=null,selectedReviewRating=5;")
    pattern=r"function renderProducts\(\)\{.*?\}\nfunction renderChips\(\)\{.*?\}\n"
    repl=r'''function shopCategory(p){const n=(p.name||'').toLocaleLowerCase('tr');if(n.includes('tarhana'))return 'Tarhana';if(n.includes('erişte')||n.includes('eriste'))return 'Erişte';if(n.includes('salça')||n.includes('salca'))return 'Salça';if(n.includes('reçel')||n.includes('recel'))return 'Reçel';if(n.includes('tahin')||n.includes('pekmez'))return 'Tahin & Pekmez';return 'Diğer Lezzetler'}
function shopImage(p){if(p.image)return p.image;const c=shopCategory(p),n=(p.name||'').toLocaleLowerCase('tr');if(c==='Tarhana')return 'assets/hero-tarhana.webp';if(c==='Erişte')return 'assets/hero-eriste.webp';if(c==='Salça')return 'assets/hero-salca.webp';if(c==='Reçel')return 'assets/hero-recel.webp';if(n.includes('tahin'))return 'assets/hero-tahin.webp';if(n.includes('pekmez'))return 'assets/hero-recel.webp';return 'assets/hero-onayli.webp'}
function renderProducts(){const grid=$('#productGrid');if(!grid)return;let rows=state.products.filter(p=>{const c=shopCategory(p),grams=parseInt(String(p.unit||'').replace(/\D/g,''))||0;const q=(`${p.name} ${p.desc||''} ${c}`).toLocaleLowerCase('tr');if(cat!=='Tümü'&&c!==cat)return false;if(shopGram!=='Tümü'){const g=+shopGram;if(g===650){if(grams<650)return false}else if(grams!==g)return false}if(+p.price>shopMaxPrice)return false;if(shopDiscount&&!(+p.old_price>+p.price))return false;if(shopNew&&!String(p.badge||'').toLocaleLowerCase('tr').includes('yeni'))return false;if(shopBest&&!String(p.badge||'').toLocaleLowerCase('tr').includes('çok'))return false;if(query&&!q.includes(query.toLocaleLowerCase('tr')))return false;return true});if(shopSort==='priceAsc')rows.sort((a,b)=>+a.price-+b.price);if(shopSort==='priceDesc')rows.sort((a,b)=>+b.price-+a.price);if(shopSort==='name')rows.sort((a,b)=>String(a.name).localeCompare(String(b.name),'tr'));$('#shopCount')&&($('#shopCount').textContent=rows.length);grid.innerHTML=rows.map(p=>{const r=productRating(p.id),old=+p.old_price||0,discount=old>+p.price?Math.round((1-(+p.price/old))*100):0,img=shopImage(p);return `<article class="shop-card"><div class="shop-card-media"><img src="${esc(img)}" alt="${esc(p.name)}" loading="lazy">${discount?`<span class="discount-badge">%${discount} İndirim</span>`:(p.badge?`<span class="new-badge">${esc(p.badge)}</span>`:'')}<button class="shop-fav" type="button" aria-label="Favorilere ekle">♡</button></div><div class="shop-card-body"><small>Loopi Makarna${p.desc?' · Ev Yapımı':''}</small><button class="shop-name" type="button" data-open-product="${p.id}">${esc(p.name)}</button><span class="shop-unit">${esc(p.unit||'')}</span>${r?`<div class="shop-rating">${stars(r.avg)} <span>(${r.count})</span></div>`:'<div class="shop-rating">★★★★★ <span>(Yeni)</span></div>'}<div class="shop-price">${old>+p.price?`<del>${money(old)}</del>`:''}<strong>${money(p.price)}</strong></div><button class="shop-add" data-add="${p.id}" ${p.stock<1?'disabled':''}>🛒 ${p.stock<1?'Tükendi':'Sepete Ekle'}</button></div></article>`}).join('')||'<div class="shop-empty">Filtrelerine uygun ürün bulunamadı.</div>';$$('[data-add]').forEach(b=>b.onclick=()=>addCart(+b.dataset.add));$$('[data-open-product]').forEach(b=>b.onclick=()=>openProductDetail(+b.dataset.openProduct));$$('.shop-fav').forEach(b=>b.onclick=()=>{b.textContent=b.textContent==='♡'?'♥':'♡';b.classList.toggle('active')})}
function renderChips(){}
'''
    s2,n=re.subn(pattern,lambda m: repl,s,flags=re.S)
    if n!=1:
        raise SystemExit(f'render replace count {n} in {fname}')
    # Bind shop controls after search handlers marker
    marker="['searchDesktop','searchMobile'].forEach(id=>$('#'+id)?.addEventListener('input',e=>{query=e.target.value;renderProducts()}));"
    add=marker+"$$('[name=\"shopCat\"]').forEach(x=>x.onchange=()=>{cat=x.value;renderProducts()});$$('[name=\"shopGram\"]').forEach(x=>x.onchange=()=>{shopGram=x.value;renderProducts()});$('#shopPrice')?.addEventListener('input',e=>{shopMaxPrice=+e.target.value;$('#shopPriceLabel').textContent=e.target.value+' TL';renderProducts()});$('#filterDiscount')?.addEventListener('change',e=>{shopDiscount=e.target.checked;renderProducts()});$('#filterNew')?.addEventListener('change',e=>{shopNew=e.target.checked;renderProducts()});$('#filterBest')?.addEventListener('change',e=>{shopBest=e.target.checked;renderProducts()});$('#shopSort')?.addEventListener('change',e=>{shopSort=e.target.value;renderProducts()});$('#shopClear')?.addEventListener('click',()=>{cat='Tümü';shopGram='Tümü';shopMaxPrice=500;shopDiscount=shopNew=shopBest=false;query='';$$('[name=\"shopCat\"]').forEach(x=>x.checked=x.value==='Tümü');$$('[name=\"shopGram\"]').forEach(x=>x.checked=x.value==='Tümü');['filterDiscount','filterNew','filterBest'].forEach(id=>{if($('#'+id))$('#'+id).checked=false});if($('#shopPrice'))$('#shopPrice').value=500;if($('#shopPriceLabel'))$('#shopPriceLabel').textContent='500 TL';if($('#searchMobile'))$('#searchMobile').value='';renderProducts()});"
    if marker not in s2: raise SystemExit('bind marker missing '+fname)
    s2=s2.replace(marker,add)
    p.write_text(s2)

# preview products expansion
p=root/'preview-app.js'; s=p.read_text()
start=s.index("  state={...state,products:[")
end=s.index("  ],campaigns:[",start)
new_products="""  state={...state,products:[
    {id:1,name:'Sebzeli Tarhana',cat:'Temel Gıda',desc:'Geleneksel usulle hazırlanmış sebzeli kuru tarhana.',unit:'500 g',price:120,old_price:150,stock:60,badge:'Çok Satan',image:'assets/hero-tarhana.webp',emoji:'🥣'},
    {id:2,name:'Domates Salçası',cat:'Temel Gıda',desc:'Yoğun kıvamlı ev yapımı domates salçası.',unit:'650 g',price:119,old_price:140,stock:60,badge:'',image:'assets/hero-salca.webp',emoji:'🍅'},
    {id:3,name:'Sade Erişte',cat:'Makarna',desc:'Ev yapımı, kesme sade erişte.',unit:'500 g',price:81,old_price:90,stock:50,badge:'',image:'assets/hero-eriste.webp',emoji:'🍜'},
    {id:4,name:'Çilek Reçeli',cat:'Kahvaltılık',desc:'Mevsim çilekleriyle küçük partilerde hazırlanır.',unit:'380 g',price:120,old_price:160,stock:50,badge:'',image:'assets/hero-recel.webp',emoji:'🍓'},
    {id:5,name:'Tahin',cat:'Kahvaltılık',desc:'Özenle kavrulmuş susamdan yoğun kıvamlı tahin.',unit:'500 g',price:170,old_price:200,stock:40,badge:'',image:'assets/hero-tahin.webp',emoji:'🥄'},
    {id:6,name:'Üzüm Pekmezi',cat:'Kahvaltılık',desc:'Yoğun kıvamlı geleneksel üzüm pekmezi.',unit:'460 g',price:149,old_price:null,stock:40,badge:'Yeni',image:'assets/hero-recel.webp',emoji:'🍇'},
    {id:7,name:'Biber Salçası',cat:'Temel Gıda',desc:'Kırmızı biberden hazırlanmış yoğun ev salçası.',unit:'650 g',price:129,old_price:null,stock:35,badge:'Yeni',image:'assets/hero-salca.webp',emoji:'🌶️'},
    {id:8,name:'Kepekli Tarhana',cat:'Temel Gıda',desc:'Kepekli unla hazırlanan geleneksel tarhana.',unit:'500 g',price:109,old_price:null,stock:30,badge:'Yeni',image:'assets/hero-tarhana.webp',emoji:'🥣'},
    {id:9,name:'İncir Reçeli',cat:'Kahvaltılık',desc:'Olgun incirlerle küçük partilerde hazırlanır.',unit:'380 g',price:139,old_price:null,stock:32,badge:'',image:'assets/hero-recel.webp',emoji:'🫙'},
    {id:10,name:'Tam Buğday Erişte',cat:'Makarna',desc:'Tam buğday unuyla hazırlanmış ev eriştesi.',unit:'500 g',price:99,old_price:null,stock:30,badge:'Yeni',image:'assets/hero-eriste.webp',emoji:'🍜'},
    {id:11,name:'Kayısı Reçeli',cat:'Kahvaltılık',desc:'Mevsim kayısılarıyla ev usulü hazırlanır.',unit:'380 g',price:135,old_price:null,stock:25,badge:'',image:'assets/hero-recel.webp',emoji:'🫙'},
    {id:12,name:'Köy Tarhanası',cat:'Temel Gıda',desc:'Uzun fermantasyonlu klasik köy tarhanası.',unit:'500 g',price:129,old_price:null,stock:25,badge:'Çok Satan',image:'assets/hero-tarhana.webp',emoji:'🥣'}
"""
s=s[:start]+new_products+s[end:]
p.write_text(s)
