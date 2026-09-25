const STORAGE_KEY = 'zsu-orders-v1';
let orders = loadOrders();
let activeFilter = 'all';
let selectedFile = null;

const $ = (id) => document.getElementById(id);
const orderDialog = $('orderDialog');
const viewerDialog = $('viewerDialog');

function loadOrders() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (Array.isArray(saved) && saved.length) return saved;
  } catch {}
  const demoText = `ЗБРОЙНІ СИЛИ УКРАЇНИ\n\nНАВЧАЛЬНИЙ ПРИКЛАД РОЗПОРЯДЖЕННЯ\n№ 01/2026\n\nТермін виконання: 05 жовтня 2026 року\n\nЗАВДАННЯ\nПідготувати та надати узагальнену інформацію про стан виконання визначених завдань.\n\nПРИМІТКА\nЦей документ є демонстраційним прикладом для перевірки роботи дашборда. Не є службовим документом.\n`;
  return [{
    id:'demo-001', number:'01/2026', deadline:'2026-10-05',
    description:'Підготувати та надати узагальнену інформацію про стан виконання визначених завдань.',
    fileName:'Приклад_розпорядження_01-2026.txt', fileType:'text/plain',
    fileData:'data:text/plain;base64,' + btoa(unescape(encodeURIComponent(demoText))),
    createdAt:new Date().toISOString(), done:false, demo:true
  }];
}
function saveOrders() { localStorage.setItem(STORAGE_KEY, JSON.stringify(orders)); }
function uid() { return `${Date.now()}-${Math.random().toString(36).slice(2,9)}`; }
function formatDate(value) {
  if (!value) return '—';
  const [y,m,d] = value.split('-');
  return `${d}.${m}.${y}`;
}
function statusOf(order) {
  if (order.done) return 'done';
  if (order.deadline && new Date(`${order.deadline}T23:59:59`) < new Date()) return 'overdue';
  return 'progress';
}
function statusLabel(status) { return {done:'Виконано', progress:'В роботі', overdue:'Прострочено'}[status]; }
function escapeHtml(value='') {
  return value.replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}
function filteredOrders() {
  const q = $('searchInput').value.trim().toLowerCase();
  return orders.filter(o => {
    const status = statusOf(o);
    const filterOk = activeFilter === 'all' || activeFilter === status;
    const queryOk = !q || `${o.number} ${o.description}`.toLowerCase().includes(q);
    return filterOk && queryOk;
  }).sort((a,b) => (a.deadline || '9999').localeCompare(b.deadline || '9999'));
}
function render() {
  const body = $('ordersBody');
  const rows = filteredOrders();
  body.innerHTML = rows.map(o => {
    const status = statusOf(o);
    return `<tr data-id="${o.id}" title="Відкрити розпорядження">
      <td>№ ${escapeHtml(o.number)}${o.demo ? '<span style="display:block;color:#78837a;font-size:8px;letter-spacing:.08em;margin-top:4px">ДЕМО-ПРИКЛАД</span>' : ''}</td>
      <td class="deadline">${formatDate(o.deadline)}</td>
      <td class="description">${escapeHtml(o.description)}</td>
      <td><span class="status ${status}">${statusLabel(status)}</span></td>
      <td class="open-link">›</td>
    </tr>`;
  }).join('');
  $('emptyState').style.display = rows.length ? 'none' : 'block';
  $('totalCount').textContent = orders.length;
  $('progressCount').textContent = orders.filter(o => statusOf(o)==='progress').length;
  $('overdueCount').textContent = orders.filter(o => statusOf(o)==='overdue').length;
  $('doneCount').textContent = orders.filter(o => statusOf(o)==='done').length;
  body.querySelectorAll('tr').forEach(row => row.addEventListener('click', () => openOrder(row.dataset.id)));
}

function openOrder(id) {
  const order = orders.find(o => o.id === id);
  if (!order) return;
  $('viewerTitle').textContent = `№ ${order.number}`;
  $('viewerMeta').innerHTML = `<b>ТЕРМІН:</b> ${formatDate(order.deadline)} &nbsp; • &nbsp; <b>СТАТУС:</b> ${statusLabel(statusOf(order))} &nbsp; • &nbsp; ${escapeHtml(order.description)}`;
  const content = $('viewerContent');
  content.innerHTML = '';
  if (!order.fileData) {
    content.innerHTML = `<div class="unsupported"><strong>Файл не прикріплено</strong><span>У записі збережені реквізити розпорядження, але документ відсутній.</span></div>`;
  } else if (order.fileType === 'application/pdf') {
    const iframe = document.createElement('iframe'); iframe.src = order.fileData; iframe.title = `Розпорядження № ${order.number}`; content.appendChild(iframe);
  } else if (order.fileType.startsWith('image/')) {
    const img = document.createElement('img'); img.src = order.fileData; img.alt = `Розпорядження № ${order.number}`; img.style.maxWidth='100%'; img.style.maxHeight='100%'; img.style.objectFit='contain'; content.appendChild(img);
  } else if (order.fileType === 'text/plain') {
    const text = document.createElement('pre'); text.className='viewer-text';
    try { text.textContent = decodeURIComponent(escape(atob(order.fileData.split(',')[1]))); } catch { text.textContent='Не вдалося прочитати текстовий файл.'; }
    content.appendChild(text);
  } else {
    content.innerHTML = `<div class="unsupported"><strong>${escapeHtml(order.fileName)}</strong><span>Формат цього документа браузер не може безпосередньо відобразити. Файл збережений у записі.</span></div>`;
  }
  viewerDialog.showModal();
}

function showToast(message) { const toast=$('toast'); toast.textContent=message; toast.classList.add('show'); setTimeout(()=>toast.classList.remove('show'),2600); }
function resetForm() { $('orderForm').reset(); selectedFile=null; $('fileTitle').textContent='Перетягніть файл сюди або оберіть його'; $('fileError').textContent=''; }
$('addBtn').addEventListener('click',()=>{resetForm();orderDialog.showModal();});
$('emptyAddBtn').addEventListener('click',()=>{resetForm();orderDialog.showModal();});
$('closeDialog').addEventListener('click',()=>orderDialog.close());
$('cancelBtn').addEventListener('click',()=>orderDialog.close());
$('closeViewer').addEventListener('click',()=>viewerDialog.close());
$('searchInput').addEventListener('input',render);
document.querySelectorAll('.filter').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.filter').forEach(b=>b.classList.remove('active'));btn.classList.add('active');activeFilter=btn.dataset.filter;render();}));
$('chooseFile').addEventListener('click',()=>$('fileInput').click());
$('fileInput').addEventListener('change',e=>selectFile(e.target.files[0]));
const drop=$('fileDrop');
['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.style.borderColor='rgba(169,190,145,.7)';}));
['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.style.borderColor='';}));
drop.addEventListener('drop',e=>selectFile(e.dataTransfer.files[0]));
function selectFile(file){if(!file)return;const max=12*1024*1024;if(file.size>max){$('fileError').textContent='Файл завеликий. Для локальної версії обмеження — 12 МБ.';return;}selectedFile=file;$('fileTitle').textContent=file.name;$('fileError').textContent='';}
$('orderForm').addEventListener('submit',e=>{e.preventDefault();if(!selectedFile){$('fileError').textContent='Прикріпіть файл розпорядження.';return;}const reader=new FileReader();reader.onload=()=>{const order={id:uid(),number:$('orderNumber').value.trim(),deadline:$('deadline').value,description:$('description').value.trim(),fileName:selectedFile.name,fileType:selectedFile.type||'application/octet-stream',fileData:reader.result,createdAt:new Date().toISOString(),done:false};orders.unshift(order);saveOrders();orderDialog.close();render();showToast('Розпорядження додано до реєстру');};reader.readAsDataURL(selectedFile);});
$('currentDate').textContent=new Intl.DateTimeFormat('uk-UA',{day:'2-digit',month:'long',year:'numeric'}).format(new Date()).toUpperCase();
render();
