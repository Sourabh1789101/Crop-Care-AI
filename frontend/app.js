import { renderCropAdvisor } from './components/CropAdvisor.js'
import { renderFertilizer } from './components/FertilizerAdvisor.js'
import { renderDisease } from './components/DiseaseDetector.js'
import { renderWeather } from './components/WeatherAlert.js'
import { renderMarket } from './components/MarketPrices.js'

const API = localStorage.getItem('API_BASE') || 'http://localhost:8000'
const view = document.getElementById('view')

function setTab(tab){
  if(tab==='crop') renderCropAdvisor(view, API)
  if(tab==='fert') renderFertilizer(view, API)
  if(tab==='disease') renderDisease(view, API)
  if(tab==='weather') renderWeather(view, API)
  if(tab==='market') renderMarket(view, API)
}

// default
setTab('crop')

document.querySelectorAll('.tabs button').forEach(btn=>{
  btn.addEventListener('click', ()=> setTab(btn.dataset.tab))
})

// Basic Voice input (Web Speech API)
const voiceBtn = document.getElementById('voiceBtn')
let recognizing = false
let recognizer
if('webkitSpeechRecognition' in window){
  recognizer = new webkitSpeechRecognition()
  recognizer.lang = 'en-IN'
  recognizer.continuous = false
  recognizer.interimResults = false
  recognizer.onresult = (e)=>{
    const text = e.results[0][0].transcript.toLowerCase()
    // simple intents
    if(text.includes('weather')) setTab('weather')
    else if(text.includes('market')) setTab('market')
    else if(text.includes('disease')) setTab('disease')
    else if(text.includes('fertilizer')) setTab('fert')
    else setTab('crop')
  }
  voiceBtn.onclick = ()=>{
    if(recognizing){ recognizer.stop(); recognizing=false; voiceBtn.textContent='🎙️ Voice (beta)'; return }
    recognizer.start(); recognizing=true; voiceBtn.textContent='🛑 Stop Voice'
  }
}else{
  voiceBtn.disabled = true
  voiceBtn.title = 'Speech recognition not supported'
}
