export function renderMarket(root, API){
  root.innerHTML = `
    <section class="card">
      <h2>Market Prices (Mock)</h2>
      <form id="mform">
        <label>Crop</label>
        <input name="crop" placeholder="wheat" />
        <button class="primary">Fetch</button>
      </form>
      <pre id="mout"></pre>
    </section>
  `
  const form = root.querySelector('#mform')
  const out = root.querySelector('#mout')
  form.onsubmit = async (e)=>{
    e.preventDefault()
    out.textContent = 'Loading...'
    const crop = form.crop.value.trim()
    const url = crop ? `${API}/market?crop=${encodeURIComponent(crop)}` : `${API}/market`
    try{
      const r = await fetch(url)
      const data = await r.json()
      out.textContent = JSON.stringify(data, null, 2)
    }catch(err){ out.textContent = 'Error: '+err }
  }
}
