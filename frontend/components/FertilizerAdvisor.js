export function renderFertilizer(root, API){
  root.innerHTML = `
    <section class="card">
      <h2>Fertilizer Guidance</h2>
      <form id="fertForm">
        <label>Crop</label>
        <select name="crop">
          <option>wheat</option>
          <option>rice</option>
          <option>maize</option>
        </select>
        <label>N (kg/ha)</label>
        <input type="number" step="0.1" name="N" value="90" required>
        <label>P (kg/ha)</label>
        <input type="number" step="0.1" name="P" value="42" required>
        <label>K (kg/ha)</label>
        <input type="number" step="0.1" name="K" value="43" required>
        <label>Soil pH</label>
        <input type="number" step="0.1" name="ph" value="6.5" required>
        <button class="primary" type="submit">Get Plan</button>
      </form>
      <pre id="fertOut"></pre>
    </section>
  `
  const form = root.querySelector('#fertForm')
  const out = root.querySelector('#fertOut')
  form.onsubmit = async (e)=>{
    e.preventDefault()
    const payload = Object.fromEntries(new FormData(form).entries())
    for(const k of ['N','P','K','ph']) payload[k] = Number(payload[k])
    out.textContent = 'Loading...'
    try{
      const r = await fetch(`${API}/recommend_fertilizer`,{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)})
      const data = await r.json()
      out.textContent = JSON.stringify(data, null, 2)
    }catch(err){ out.textContent = 'Error: '+err }
  }
}
