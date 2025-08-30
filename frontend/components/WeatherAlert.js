export function renderWeather(root, API){
  root.innerHTML = `
    <section class="card">
      <h2>Weather & Alerts</h2>
      <form id="wform">
        <label>Pincode</label>
        <input name="pincode" value="390001" />
        <button class="primary">Get Weather</button>
      </form>
      <pre id="wout"></pre>
    </section>
  `
  const form = root.querySelector('#wform')
  const out = root.querySelector('#wout')
  form.onsubmit = async (e)=>{
    e.preventDefault()
    out.textContent = 'Loading...'
    try{
      const r = await fetch(`${API}/weather?pincode=${encodeURIComponent(form.pincode.value)}`)
      const data = await r.json()
      out.textContent = JSON.stringify(data, null, 2)
    }catch(err){ out.textContent = 'Error: '+err }
  }
}
