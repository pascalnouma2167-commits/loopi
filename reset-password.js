'use strict';
let csrf='';
fetch('api/index.php?route=me').then(r=>r.json()).then(x=>{csrf=x.csrf||'';});
const form=document.querySelector('#f');
form.addEventListener('submit',async e=>{
  e.preventDefault();
  const r=await fetch('api/index.php?route=reset',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify({token:form.dataset.resetToken||'',password:document.querySelector('#p').value})});
  const j=await r.json();
  document.querySelector('#m').textContent=j.ok?'Şifren yenilendi. Artık giriş yapabilirsin.':j.message;
});
