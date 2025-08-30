const CACHE = 'sca-v1'
const ASSETS = [
  '/', '/index.html', '/app.js', '/styles.css',
  '/components/CropAdvisor.js', '/components/FertilizerAdvisor.js', '/components/DiseaseDetector.js', '/components/WeatherAlert.js', '/components/MarketPrices.js'
]
self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)))
})
self.addEventListener('fetch', e=>{
  e.respondWith(caches.match(e.request).then(r=> r || fetch(e.request)))
})
