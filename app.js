const facts=['Lambda is serverless.','WebSocket enables realtime.','DynamoDB is NoSQL.'];let i=0;setInterval(()=>fact.textContent=facts[i++%facts.length],3000);fact.textContent=facts[0];
const statusEl=document.getElementById('status');
const chat=document.getElementById('chat');

const ws=new WebSocket('wss://67p3eeaw6f.execute-api.us-east-1.amazonaws.com/production/');


ws.onopen=()=>statusEl.textContent='🟢 Connected';
ws.onclose=()=>statusEl.textContent='🔴 Disconnected';
ws.onmessage=e=>{try{const d=JSON.parse(e.data);if(d.sender===sender.value)return;add(d.sender,d.message,false);}catch{add('Server',e.data,false);}};
function add(name,msg,me){chat.innerHTML+=`<div class="row ${me?'me':''}"><small>${name}</small><br><span class="bubble">${msg}</span></div>`;chat.scrollTop=chat.scrollHeight;}
send.onclick=()=>{if(ws.readyState!==1)return alert('Socket not connected');const p={action:'sendMessage',sender:sender.value,message:msg.value};ws.send(JSON.stringify(p));add(sender.value,msg.value,true);msg.value='';};
msg.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send.click();}});