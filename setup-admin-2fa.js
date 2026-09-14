'use strict';
const box=document.getElementById('qrcode');
if(box&&box.dataset.otpauth&&window.QRCode){new QRCode(box,{text:box.dataset.otpauth,width:180,height:180,correctLevel:QRCode.CorrectLevel.M});}
