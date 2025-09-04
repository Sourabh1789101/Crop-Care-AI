export function renderCropAdvisor(root, API){
  root.innerHTML = `
    <section class="card">
      <h2>Crop Recommendation</h2>
      <form id="cropForm">
        <label>N (kg/ha)</label>
        <input type="number" step="0.1" name="N" value="90" required>
        <label>P (kg/ha)</label>
        <input type="number" step="0.1" name="P" value="42" required>
        <label>K (kg/ha)</label>
        <input type="number" step="0.1" name="K" value="43" required>
        <label>Soil pH</label>
        <input type="number" step="0.1" name="ph" value="6.5" required>
        <label>Rainfall (mm)</label>
        <input type="number" step="0.1" name="rainfall" value="120">
        <button class="primary" type="submit">Recommend Crop</button>
      </form>
      <pre id="cropOut"></pre>
    </section>
  `

  const form = root.querySelector('#cropForm')
  const out = root.querySelector('#cropOut')
  form.onsubmit = async (e)=>{
    e.preventDefault()
    const payload = Object.fromEntries(new FormData(form).entries())
    for(const k of ['N','P','K','ph','rainfall']) payload[k] = Number(payload[k])
    out.textContent = 'Loading...'
    try{
      const r = await fetch(`${API}/recommend_crop`,{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)})
      const data = await r.json()
      out.textContent = JSON.stringify(data, null, 2)
    }catch(err){ out.textContent = 'Error: '+err }
  }
}
