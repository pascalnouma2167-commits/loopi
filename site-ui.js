
(function(){
  const q=s=>document.querySelector(s), qa=s=>[...document.querySelectorAll(s)];
  const menuBtn=q('#menuBtn'),mobileNav=q('#mobileNav');
  const productToggle=q('#inlineProductsToggle'),productSubmenu=q('#inlineProductsSubmenu');
  const setProductsMenu=open=>{
    if(!productToggle||!productSubmenu)return;
    productSubmenu.hidden=!open;
    productToggle.setAttribute('aria-expanded',String(open));
  };
  productToggle?.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();setProductsMenu(productSubmenu.hidden)});
  productSubmenu?.addEventListener('click',e=>{if(e.target.closest('a'))setProductsMenu(false)});
  document.addEventListener('click',e=>{if(!e.target.closest('.inline-products-menu'))setProductsMenu(false)});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!productSubmenu?.hidden){setProductsMenu(false);productToggle?.focus()}});
  const setMenu=open=>{
    if(!menuBtn||!mobileNav)return;
    mobileNav.classList.toggle('hidden',!open);
    menuBtn.setAttribute('aria-expanded',String(open));
    menuBtn.setAttribute('aria-label',open?'Menüyü kapat':'Menüyü aç');
    const icon=menuBtn.querySelector('span');
    if(icon)icon.textContent=open?'×':'☰';
  };
  if(menuBtn&&!menuBtn.hidden)menuBtn.onclick=e=>{e.preventDefault();e.stopPropagation();setMenu(mobileNav.classList.contains('hidden'))};
  if(menuBtn&&!menuBtn.hidden){
    mobileNav?.addEventListener('click',e=>{if(e.target.closest('a,button'))setMenu(false)});
    document.addEventListener('click',e=>{if(!mobileNav?.classList.contains('hidden')&&!mobileNav.contains(e.target)&&!menuBtn.contains(e.target))setMenu(false)});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!mobileNav?.classList.contains('hidden')){setMenu(false);menuBtn.focus()}});
    addEventListener('resize',()=>{if(innerWidth>1280)setMenu(false)});
  }
  const wrap=q('.products-nav-wrap'), btn=q('#productsNavBtn');
  if(wrap&&btn){
    btn.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();const open=wrap.classList.toggle('open');btn.setAttribute('aria-expanded',String(open));if(!open)q('#urunler')?.scrollIntoView({behavior:'smooth',block:'start'});});
    btn.addEventListener('keydown',e=>{if(e.key==='Escape'){wrap.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.focus()}});
    wrap.addEventListener('mouseenter',()=>{wrap.classList.add('open');btn.setAttribute('aria-expanded','true')});
    wrap.addEventListener('mouseleave',()=>{wrap.classList.remove('open');btn.setAttribute('aria-expanded','false')});
    document.addEventListener('click',e=>{if(!wrap.contains(e.target)){wrap.classList.remove('open');btn.setAttribute('aria-expanded','false')}});
  }
  qa('[data-product-query]').forEach(a=>a.addEventListener('click',()=>{
    wrap?.classList.remove('open');btn?.setAttribute('aria-expanded','false');
    const term=a.dataset.productQuery||'';
    setTimeout(()=>{
      const input=q('#searchDesktop')||q('#searchMobile');
      if(input){input.value=term;input.dispatchEvent(new Event('input',{bubbles:true}));}
    },80);
  }));
  const slides=qa('.hero-slide'), dots=q('#heroDots');
  if(!slides.length||!dots)return;
  let i=0,timer=null;
  slides.forEach((s,n)=>{const b=document.createElement('button');b.type='button';b.className='hero-dot'+(n===0?' active':'');b.setAttribute('aria-label',(n+1)+'. banner');b.onclick=()=>show(n,true);dots.appendChild(b)});
  const dotList=()=>qa('.hero-dot');
  function show(n,user){i=(n+slides.length)%slides.length;slides.forEach((s,k)=>s.classList.toggle('active',k===i));dotList().forEach((d,k)=>d.classList.toggle('active',k===i));if(user)restart();}
  function next(){show(i+1,false)}
  function restart(){clearInterval(timer);timer=setInterval(next,5000)}
  q('#heroPrev')?.addEventListener('click',()=>show(i-1,true));q('#heroNext')?.addEventListener('click',()=>show(i+1,true));
  q('.hero-carousel')?.addEventListener('mouseenter',()=>clearInterval(timer));q('.hero-carousel')?.addEventListener('mouseleave',restart);
  restart();
})();

// Uzun ikincil akışları ana sayfada tek bakışta anlaşılır hale getirir.
(function(){
  const journeys=[
    ['#abonelik','İyilik Kutusu aboneliği','Her ay yerel lezzetler, her teslimatta %10 iyilik payı','Planları gör'],
    ['#kurumsal','Kurumsal İyilik Kutuları','Çalışan ve müşteri hediyelerinde ölçülebilir sosyal etki','Seçenekleri gör']
  ];
  journeys.forEach(([selector,title,copy,action])=>{
    const section=document.querySelector(selector);
    const content=section?.querySelector(':scope > .container');
    if(!section||!content||section.querySelector(':scope > details'))return;
    section.classList.add('secondary-journey');
    const details=document.createElement('details');
    details.className='journey-details';
    const summary=document.createElement('summary');
    summary.innerHTML=`<span><b>${title}</b><small>${copy}</small></span><em>${action}<i aria-hidden="true">⌄</i></em>`;
    section.insertBefore(details,content);
    details.append(summary,content);
  });
  const openTarget=()=>{
    const section=document.querySelector(location.hash);
    const details=section?.querySelector(':scope > .journey-details');
    if(details)details.open=true;
  };
  addEventListener('hashchange',openTarget);
  openTarget();
})();

// Footer quick links
(function(){
  const map=[['footerSignupLink','memberBtn'],['footerLoginLink','loginBtn'],['footerCartLink','bagBtn'],['footerOrdersLink','goodHistoryBtn']];
  map.forEach(([from,to])=>{const a=document.getElementById(from),b=document.getElementById(to);if(a&&b)a.addEventListener('click',e=>{e.preventDefault();b.click();});});
})();
