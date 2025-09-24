<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>4K Enhancer</title>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" rel="stylesheet" />
  <style>
    :root{
      --bg:#0b1025;
      --panel:#161b35;
      --header:#0f1430;
      --muted:#a8b2d1;
      --text:#ffffff;
      --accent:#2d5bff;
      --accent-2:#4d7aff;
      --border:rgba(255,255,255,.06);
      --shadow:0 18px 40px rgba(0,0,0,.35);
      --radius:18px;
      --container:1180px;
      --grad:linear-gradient(135deg,#2d5bff 0%,#1a3cc7 100%);
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;background:var(--bg);color:var(--text);
      font-family:system-ui,Segoe UI,Roboto,Arial,sans-serif; line-height:1.6;
    }
    /* Header */
    .site-header{
      position:sticky;top:0;z-index:10;background:rgba(15,20,48,.95);
      backdrop-filter:blur(8px); box-shadow:0 8px 24px rgba(0,0,0,.35);
    }
    .container{max-width:var(--container);margin:0 auto;padding:16px 24px}
    .nav{
      display:flex;align-items:center;justify-content:space-between;
    }
    .brand{font-weight:800;font-size:20px;letter-spacing:.2px}
    .brand i{color:var(--accent);margin-right:8px}

    /* Hero */
    .hero{
      text-align:center; padding:28px 24px 8px;
      background:var(--header);
      border-bottom:1px solid var(--border);
      box-shadow:var(--shadow);
    }
    .hero h1{
      margin:6px 0 2px; font-size:30px; font-weight:900;
      background:var(--grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    }
    .hero p{color:var(--muted);margin:0 0 14px}
    .hero .btn{
      display:inline-flex;align-items:center;gap:10px;
      padding:12px 22px;border:0;border-radius:999px;
      background:var(--grad); color:#fff; cursor:pointer; font-weight:700;
      box-shadow:0 12px 30px rgba(45,91,255,.35);
      transition:transform .15s ease, box-shadow .15s ease;
    }
    .hero .btn:hover{transform:translateY(-1px); box-shadow:0 16px 38px rgba(45,91,255,.45);}

    /* Upload Card */
    .card{
      max-width:var(--container); margin:28px auto; padding:26px;
      background:var(--panel); border:1px solid var(--border);
      border-radius:var(--radius); box-shadow:var(--shadow);
    }
    .dropzone{
      position:relative; border:2px dashed var(--accent-2);
      border-radius:16px; padding:68px 18px;
      background:rgba(77,122,255,.06); text-align:center;
      transition:.2s ease;
    }
    .dropzone:hover, .dropzone.dragover{
      background:rgba(77,122,255,.12);
      box-shadow:inset 0 0 0 2px rgba(77,122,255,.15);
    }
    .dropzone i{font-size:56px;color:var(--accent);display:block;margin-bottom:14px}
    .dropzone .title{font-size:20px;font-weight:700;margin:0 0 6px}
    .dropzone .hint{color:var(--muted);margin:0}
    .hidden-input{display:none}
    .file-pill{
      margin-top:14px; display:inline-flex; align-items:center; gap:8px;
      padding:6px 12px; border-radius:999px; background:rgba(255,255,255,.06);
      color:#e8ecff; font-size:13px; border:1px solid var(--border);
    }

    /* Footer */
    footer{
      margin-top:60px; background:#121735; border-top:1px solid var(--border);
      padding:38px 0;
    }
    .links{display:flex;gap:28px;justify-content:center;flex-wrap:wrap;color:var(--muted);font-size:14px}
    .links a{color:var(--muted);text-decoration:none}
    .links a:hover{color:var(--accent)}
    .social{margin:20px 0; display:flex; gap:14px; justify-content:center}
    .social a{
      width:42px;height:42px;border-radius:50%; display:grid;place-items:center;
      background:rgba(255,255,255,.06); color:var(--muted); text-decoration:none;
      transition:.2s ease; border:1px solid var(--border)
    }
    .social a:hover{background:var(--accent);color:#fff; transform:translateY(-2px)}
    .copy{color:var(--muted);text-align:center;font-size:13px;margin-top:12px}

    @media (max-width:720px){
      .hero h1{font-size:22px}
      .dropzone{padding:56px 14px}
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header class="site-header">
    <div class="container nav">
      <div class="brand"><i class="fa-solid fa-bolt"></i>4K Enhancer</div>
    </div>
    <div class="hero">
      <h1>Enhance Your Images to 4K Quality</h1>
      <p>Upgrade your photos with crystal-clear 4K resolution</p>
      <button id="trigger-upload" class="btn"><i class="fa-solid fa-upload"></i> Upload Image</button>
    </div>
  </header>

  <!-- Upload card -->
  <main class="card">
    <div id="dropzone" class="dropzone" role="button" aria-label="Upload image area" tabindex="0">
      <i class="fa-solid fa-cloud-arrow-up"></i>
      <p class="title">Drag & Drop your image here</p>
      <p class="hint">or click to browse files</p>
      <input id="file-input" class="hidden-input" type="file" accept="image/*" />
      <div id="file-pill" class="file-pill" style="display:none">
        <i class="fa-regular fa-file-image"></i><span id="file-name"></span>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer>
    <div class="container">
      <nav class="links">
        <a href="#">Privacy Policy</a>
        <a href="#">Terms of Service</a>
        <a href="#">Contact Us</a>
        <a href="#">API Documentation</a>
        <a href="#">About</a>
      </nav>
      <div class="social">
        <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
        <a href="#" aria-label="Twitter / X"><i class="fab fa-twitter"></i></a>
        <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
        <a href="#" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
        <a href="#" aria-label="GitHub"><i class="fab fa-github"></i></a>
      </div>
      <div class="copy">© 2023 4K Enhancer. All rights reserved.</div>
    </div>
  </footer>

  <script>
    const dz = document.getElementById('dropzone');
    const input = document.getElementById('file-input');
    const pill = document.getElementById('file-pill');
    const fname = document.getElementById('file-name');
    const trigger = document.getElementById('trigger-upload');

    // open dialog from header button
    trigger.addEventListener('click', () => input.click());

    // click / keyboard on zone
    dz.addEventListener('click', () => input.click());
    dz.addEventListener('keydown', (e)=>{ if(e.key==='Enter' || e.key===' '){ e.preventDefault(); input.click(); } });

    // drag & drop
    ['dragenter','dragover'].forEach(ev => dz.addEventListener(ev, (e)=>{ e.preventDefault(); dz.classList.add('dragover'); }));
    ['dragleave','drop'].forEach(ev => dz.addEventListener(ev, (e)=>{ e.preventDefault(); dz.classList.remove('dragover'); }));
    dz.addEventListener('drop', (e)=>{
      const file = e.dataTransfer.files?.[0];
      if(file) handleFile(file);
    });

    input.addEventListener('change', (e)=>{
      const file = e.target.files?.[0];
      if(file) handleFile(file);
    });

    function handleFile(file){
      if(!file.type.startsWith('image/')){ alert('Please choose an image'); return; }
      fname.textContent = `${file.name} — ${(file.size/1024).toFixed(0)} KB`;
      pill.style.display = 'inline-flex';
      // هنا فقط واجهة؛ اربط الحدث بباك-إندك لاحقًا إذا رغبت
    }
  </script>
</body>
</html>
