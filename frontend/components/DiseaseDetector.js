export function renderDisease(root, API){
  root.innerHTML = `
    <section class="card">
      <h2>Pest / Disease Detection</h2>
      <form id="imgForm">
        <input type="file" name="img" accept="image/*" capture="environment" required />
        <button class="primary" type="submit">Analyze</button>
      </form>
      <img class="preview" id="prev" />
      <pre id="imgOut"></pre>
    </section>
  `
  const form = root.querySelector('#imgForm')
  const out = root.querySelector('#imgOut')
  const prev = root.querySelector('#prev')

  form.img.onchange = ()=>{
    const f = form.img.files[0]
    if(f) prev.src = URL.createObjectURL(f)
  }

  form.onsubmit = async (e)=>{
    e.preventDefault()
    out.textContent = 'Uploading...'
    const fd = new FormData()
    fd.append('file', form.img.files[0])
    try{
      const r = await fetch(`${API}/detect_disease`,{method:'POST', body: fd})
      const data = await r.json()
      out.textContent = JSON.stringify(data, null, 2)
    }catch(err){ out.textContent = 'Error: '+err }
  }
}
