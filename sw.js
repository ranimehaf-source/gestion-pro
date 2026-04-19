const VERSION = '1.0.0';
const CACHE = 'gestion-pro-v' + VERSION;
const ASSETS = ['./', './index.html', './manifest.json',
  'https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&family=Roboto:wght@300;400;500;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js'];
self.addEventListener('install', e => {self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS).catch(() => {})));});
self.addEventListener('activate', e => {e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));});
self.addEventListener('fetch', e => {if(e.request.method !== 'GET')return;e.respondWith(fetch(e.request).then(res => {const clone=res.clone();caches.open(CACHE).then(c => c.put(e.request, clone));return res;}).catch(() => caches.match(e.request)));});
self.addEventListener('message', e => {if(e.data === 'skipWaiting')self.skipWaiting();});
