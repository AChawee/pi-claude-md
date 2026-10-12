## ขั้นตอนที่ 4 — สร้าง HTML Guide

**ชื่อไฟล์ output:**
```
langMode = "th"    → ~/docs/<projectName>/<moduleName>-guide.html
langMode = "en"    → ~/docs/<projectName>/<moduleName>-guide-en.html
langMode = "th+en" → ~/docs/<projectName>/<moduleName>-guide-bilingual.html
```

HTML เป็น standalone — ทุก style อยู่ใน `<style>` เดียว รูปทั้งหมด embed base64

### โครงสร้าง HTML

Layout หลักเป็น **Sidebar + Main content**:

```html
<!DOCTYPE html>
<html lang="th"><!-- en หรือ th+en ให้ใส่ lang="th" ไว้ก่อน JS switchLang จะ handle -->
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><!-- ชื่อ module --> — คู่มือการใช้งาน</title>
<!-- Thai font — โหลดเมื่อมี internet, fallback เป็น system Thai font เมื่อ offline -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
<div class="app-layout">

  <!-- LEFT SIDEBAR (sticky, 260px) -->
  <nav class="sidebar">
    <div class="sidebar-logo">
      <div class="sidebar-logo-badge"><!-- projectName --></div>
      <div class="sidebar-logo-title"><!-- ชื่อ module --></div>
      <div class="sidebar-logo-sub">
        <!-- th    → คู่มือการใช้งาน -->
        <!-- en    → User Guide -->
        <!-- th+en → <span class="i18n" data-th="คู่มือการใช้งาน" data-en="User Guide"> -->
      </div>
    </div>

    <!-- Lang toggle — แสดงเฉพาะ langMode="th+en" -->
    <div class="lang-bar">
      <span class="lang-label i18n" data-th="ภาษา" data-en="Language">ภาษา</span>
      <div class="lang-switch">
        <button class="lang-btn active" data-lang="th" onclick="switchLang('th')">ไทย</button>
        <button class="lang-btn"        data-lang="en" onclick="switchLang('en')">EN</button>
      </div>
    </div>

    <div class="sidebar-nav">
      <div class="nav-group-label">
        <span class="i18n" data-th="หน้าหลัก" data-en="Overview">หน้าหลัก</span>
      </div>
      <a href="#top" class="nav-item" data-section="top">
        <span class="nav-item-icon">🗺️</span>
        <div>
          <div class="nav-item-label">
            <span class="i18n" data-th="ภาพรวมระบบ" data-en="System Overview">ภาพรวมระบบ</span>
          </div>
          <div class="nav-item-sub">
            <span class="i18n" data-th="สารบัญทั้งหมด" data-en="Table of Contents">สารบัญทั้งหมด</span>
          </div>
        </div>
      </a>
      <div class="nav-group-label">
        <span class="i18n" data-th="ฟังก์ชั่นหลัก" data-en="Features">ฟังก์ชั่นหลัก</span>
      </div>
      <!-- วน pageMap → nav-item 1 รายการต่อ slug -->
      <a href="#<sectionId>" class="nav-item" data-section="<sectionId>">
        <span class="nav-item-icon"><!-- emoji --></span>
        <div>
          <div class="nav-item-label"><!-- title ต้นฉบับ ไม่แปล --></div>
          <div class="nav-item-sub">
            <span class="i18n">
              <template data-lang="th"><!-- subtitleTH --></template>
              <template data-lang="en"><!-- subtitleEN --></template>
              <!-- subtitleTH -->
            </span>
          </div>
        </div>
      </a>
    </div>
  </nav>

  <!-- MAIN CONTENT -->
  <main class="main-content">
    <div class="wrapper">

      <!-- TOC -->
      <div class="toc" id="top">
        <div class="toc-title">
          <span class="i18n" data-th="สารบัญ" data-en="Table of Contents">สารบัญ</span>
        </div>
        <div class="toc-grid">
          <a href="#<sectionId>" class="toc-item">
            <div class="toc-num" style="background:<!-- color hex -->;">N</div>
            <div>
              <div class="toc-label"><!-- title --></div>
              <div class="toc-path"><!-- /route/path --></div>
              <div class="toc-desc">
              <span class="i18n">
                <template data-lang="th"><!-- tocDescTH --></template>
                <template data-lang="en"><!-- tocDescEN --></template>
                <!-- tocDescTH -->
              </span>
            </div>
            </div>
          </a>
        </div>
      </div>

      <!-- SECTIONS -->
      <div id="<sectionId>" class="guide-section">...</div>

    </div>
  </main>

</div>

<script>
(function(){
  /* Scroll spy */
  var sections = document.querySelectorAll('.guide-section[id], #top');
  var items    = document.querySelectorAll('.nav-item[data-section]');
  function setActive(id){
    items.forEach(function(el){ el.classList.toggle('active', el.dataset.section===id); });
    var a = document.querySelector('.nav-item[data-section="'+id+'"]');
    if(a) a.scrollIntoView({block:'nearest'});
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){ if(e.isIntersecting) setActive(e.target.id); });
  },{threshold:0.15,rootMargin:'-5% 0px -65% 0px'});
  sections.forEach(function(s){ io.observe(s); });
  if(sections.length) setActive(sections[0].id);
  document.querySelectorAll('.nav-item[href]').forEach(function(a){
    a.addEventListener('click',function(e){
      e.preventDefault();
      var t=document.querySelector(a.getAttribute('href'));
      if(t) document.querySelector('.main-content').scrollTo({top:t.offsetTop-20,behavior:'smooth'});
    });
  });

  /* Lang switch — เฉพาะ langMode=th+en
   *
   * รูปแบบ HTML ที่รองรับ (ใช้ <template> แทน data-attribute):
   *
   *   <span class="i18n">
   *     <template data-lang="th"><strong>ข้อความ</strong>ไทย</template>
   *     <template data-lang="en"><strong>English</strong> text</template>
   *   </span>
   *
   * ข้อดี: HTML tags (<strong>, <a>, <code>, <br>) render ได้ถูกต้องทุกกรณี
   * เพราะ <template> เก็บ DOM จริง ไม่ใช่ string — ไม่มี entity escaping
   */
  window.switchLang = function(lang) {
    document.body.dataset.lang = lang;
    document.querySelectorAll('.i18n').forEach(function(el) {
      var tpl = el.querySelector('template[data-lang="' + lang + '"]');
      if (!tpl) return;
      // เก็บ template nodes ไว้ก่อน แล้วล้าง innerHTML แล้วใส่ clone กลับ + template เดิม
      var templates = Array.from(el.querySelectorAll('template'));
      el.innerHTML = '';
      templates.forEach(function(t) { el.appendChild(t); });
      el.insertBefore(tpl.content.cloneNode(true), el.firstChild);
    });
    document.querySelectorAll('.lang-btn').forEach(function(btn) {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });
    try { localStorage.setItem('guide-lang', lang); } catch(e) {}
  };
  var saved = (function(){ try{ return localStorage.getItem('guide-lang'); }catch(e){return null;} })();
  if(saved && saved !== 'th') window.switchLang(saved);

  /* Device tab — สลับ PC / Mobile screenshot ใน section เดียวกัน */
  window.showDevice = function(btn, device) {
    var block = btn.closest('.screenshot');
    block.querySelectorAll('.device-tab').forEach(function(b){ b.classList.toggle('active', b===btn); });
    block.querySelectorAll('.device-view').forEach(function(v){
      v.hidden = !v.classList.contains('device-'+device);
    });
  };
})();
</script>
</body>
```

### Section anatomy — 1 section ต่อ 1 slug

> **กฎการเขียน `i18n` span (langMode=th+en)**
>
> ใช้ `<template data-lang="...">` ภายใน `.i18n` เสมอ — ห้ามใช้ `data-th`/`data-en` attribute
> เพราะ HTML attribute จะ escape `<strong>` เป็น `&lt;strong&gt;` ทำให้ tag ไม่ render
>
> ```html
> <!-- ✅ ถูก — ใช้ <template> -->
> <span class="i18n">
>   <template data-lang="th">พื้นที่การผลิตที่ <strong>เป็นเจ้าของ</strong>ตะกร้า</template>
>   <template data-lang="en">Production area that <strong>owns</strong> baskets</template>
> </span>
>
> <!-- ❌ ผิด — data-attribute escape HTML -->
> <span class="i18n" data-th="พื้นที่ <strong>เป็นเจ้าของ</strong>" data-en="...">...</span>
> ```
>
> ค่าเริ่มต้น (ก่อน switchLang ถูกเรียก) ให้ใส่เนื้อหาภาษาไทยไว้นอก `<template>` โดยตรง
> JS จะ swap เนื้อหาจาก template ที่ตรงกับภาษาที่เลือกเมื่อ switchLang ถูกเรียก

```html
<section id="<sectionId>" class="guide-section">
  <div class="breadcrumb">
    <a href="#top">หน้าหลัก</a> › ชื่อ Module › ชื่อหน้า
  </div>
  <div class="section-header">
    <div class="section-icon c-<color>">🏭</div>
    <div>
      <div class="section-title">ชื่อหน้า</div>
      <div class="section-subtitle">คำอธิบายสั้น</div>
      <div class="section-url">/path · API: /api-prefix/...</div>
    </div>
  </div>

  <!-- section-intro: ใช้ <template> เพื่อให้ <strong>/<a>/<code> render ได้ -->
  <div class="section-intro">
    <span class="i18n">
      <template data-lang="th"><strong>Domain</strong> คือพื้นที่การผลิตที่เป็น &ldquo;เจ้าของ&rdquo; ตะกร้า ต้องตั้งค่าก่อนใช้งาน Trade</template>
      <template data-lang="en"><strong>Domain</strong> is a production area that owns baskets. Must be set up before using Trade.</template>
      <strong>Domain</strong> คือพื้นที่การผลิตที่เป็น "เจ้าของ" ตะกร้า ต้องตั้งค่าก่อนใช้งาน Trade
    </span>
  </div>

  <!--
    screenshot block — ถ้ามีทั้ง PC + mobile ให้ใช้รูปแบบ device-tabs
    ถ้ามีแค่ PC (--no-mobile หรือ capture เก่า) ให้ใช้ has-img ธรรมดา (ไม่มี device-tabs)

    กฎ hidden:
      - mobile div ต้องใช้ "hidden" attribute ใน HTML เท่านั้น
      - ห้ามใช้ CSS .device-mobile{display:none} เพราะจะทำให้ JS toggle ใช้ไม่ได้
      - showDevice() ใช้ v.hidden = true/false ซึ่งทำงานถูกต้องกับ hidden attribute
  -->
  <div class="screenshot has-img">
    <!-- device tabs — แสดงเฉพาะเมื่อมีรูป mobile (-mobile.png) -->
    <div class="device-tabs">
      <button class="device-tab active" onclick="showDevice(this,'pc')">🖥️ PC</button>
      <button class="device-tab"        onclick="showDevice(this,'mobile')">📱 Mobile</button>
    </div>
    <div class="device-view device-pc">
      <img src="data:image/png;base64,...PC_B64..." alt="ชื่อหน้า — PC">
    </div>
    <div class="device-view device-mobile" hidden><!-- ← hidden attribute เท่านั้น ห้ามใช้ CSS -->
      <img src="data:image/png;base64,...MOBILE_B64..." alt="ชื่อหน้า — Mobile"
           style="max-width:390px;margin:0 auto;display:block;">
    </div>
    <div class="screenshot-caption">
      <strong>ชื่อหน้าจอ</strong> —
      <span class="i18n">
        <template data-lang="th">รายการ Domain ทั้งหมด พร้อมปุ่ม Add Domain</template>
        <template data-lang="en">Full Domain list with Add Domain button</template>
        รายการ Domain ทั้งหมด พร้อมปุ่ม Add Domain
      </span>
    </div>
  </div>

  <div class="action-map">
    <div class="action-map-title">ปุ่มและการทำงานในหน้านี้</div>
    <div class="action-grid">
      <!-- action-card ตาม type: nav / submit / dialog / delete -->
    </div>
  </div>

  <div class="steps">
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <!-- step ที่มีแค่ text ธรรมดา -->
        <span class="i18n">
          <template data-lang="th">คลิกปุ่ม <strong>Add Domain</strong> ที่มุมขวาบน</template>
          <template data-lang="en">Click the <strong>Add Domain</strong> button at the top right</template>
          คลิกปุ่ม <strong>Add Domain</strong> ที่มุมขวาบน
        </span>
        <!-- ถ้ามีรูป dialog/zoom/step สำหรับ step นี้ -->
        <img class="img-zoom" src="data:image/png;base64,..." alt="dialog screenshot">
      </div>
    </div>
  </div>

  <div class="related">
    <span class="related-label">ดูเพิ่มเติม:</span>
    <a href="#<relatedSectionId>" class="related-chip">ชื่อหน้า</a>
  </div>
</section>
```

### CSS

```css
:root {
  --green:#16a34a; --green-light:#dcfce7;
  --blue:#2563eb;  --blue-light:#dbeafe;
  --red:#dc2626;   --red-light:#fee2e2;
  --amber:#d97706; --amber-light:#fef3c7;
  --gray:#64748b;  --gray-light:#f1f5f9;
  --gray-border:#e2e8f0;
  --primary:var(--blue); --primary-light:var(--blue-light);
}
* { box-sizing:border-box; margin:0; padding:0; }
html,body { height:100%; overflow:hidden; }
body { font-family:'Sarabun','Noto Sans Thai','Leelawadee UI','Leelawadee','Tahoma',
                   -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
       background:#f8fafc; color:#1e293b; line-height:1.6; display:flex; flex-direction:column; }
.app-layout { display:flex; flex:1; overflow:hidden; }
.sidebar {
  width:260px; min-width:260px; background:#1e293b; color:white;
  display:flex; flex-direction:column; height:100%; overflow-y:auto; flex-shrink:0;
}
.sidebar-logo { padding:20px 20px 16px; border-bottom:1px solid rgba(255,255,255,.1); }
.sidebar-logo-badge {
  display:inline-block; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.2);
  border-radius:6px; padding:3px 8px; font-size:10px; color:rgba(255,255,255,.7); margin-bottom:8px;
}
.sidebar-logo-title { font-size:14px; font-weight:700; color:white; line-height:1.3; }
.sidebar-logo-sub   { font-size:11px; color:rgba(255,255,255,.45); margin-top:3px; }
.sidebar-nav { padding:10px 0; flex:1; }
.nav-group-label {
  font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.08em;
  color:rgba(255,255,255,.3); padding:10px 20px 4px;
}
.nav-item {
  display:flex; align-items:center; gap:10px; padding:9px 18px;
  font-size:13px; font-weight:500; color:rgba(255,255,255,.65);
  text-decoration:none; transition:background .15s,color .15s; border-left:3px solid transparent;
}
.nav-item:hover  { background:rgba(255,255,255,.07); color:white; }
.nav-item.active { background:rgba(255,255,255,.1); color:white; border-left-color:#4ade80; }
.nav-item-icon   { font-size:14px; width:20px; text-align:center; flex-shrink:0; }
.nav-item-label  { flex:1; }
.nav-item-sub    { font-size:10px; color:rgba(255,255,255,.35); margin-top:1px; }
.main-content { flex:1; overflow-y:auto; background:#f3f4f6; }
.wrapper { max-width:880px; }
.section-intro {
  background:white; border:1px solid var(--gray-border); border-radius:8px;
  padding:14px 18px; margin-bottom:20px; font-size:14px; color:#475569; line-height:1.75;
  border-left:4px solid #94a3b8;
}
.section-intro strong { color:#0f172a; }
.toc { background:white; padding:40px 48px; border-bottom:1px solid #e2e8f0; }
.toc-title {
  font-size:11px; font-weight:700; text-transform:uppercase;
  letter-spacing:.08em; color:#94a3b8; margin-bottom:20px;
}
.toc-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.toc-item {
  display:flex; align-items:flex-start; gap:12px; padding:12px 14px;
  border-radius:8px; text-decoration:none; color:#334155;
  border:1px solid #e2e8f0; transition:background .15s;
}
.toc-item:hover  { background:var(--primary-light); border-color:var(--primary); }
.toc-num {
  width:28px; height:28px; border-radius:50%; background:var(--primary);
  color:white; display:flex; align-items:center; justify-content:center;
  font-weight:700; font-size:13px; flex-shrink:0; margin-top:2px;
}
.toc-label { font-size:14px; font-weight:600; }
.toc-path  { font-size:11px; color:#94a3b8; font-family:monospace; margin-top:2px; }
.toc-desc  { font-size:12px; color:#64748b; margin-top:4px; line-height:1.5; }
.guide-section {
  background:white; border-radius:12px; border:1px solid #e2e8f0;
  padding:32px; margin-bottom:32px;
}
.breadcrumb { font-size:12px; color:#94a3b8; margin-bottom:16px; }
.breadcrumb a { color:#64748b; text-decoration:none; }
.section-header { display:flex; align-items:flex-start; gap:16px; margin-bottom:24px; }
.section-icon {
  width:44px; height:44px; border-radius:10px; background:var(--primary-light);
  display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0;
}
.c-green { background:#dcfce7; color:#16a34a; }
.c-blue  { background:#dbeafe; color:#2563eb; }
.c-red   { background:#fee2e2; color:#dc2626; }
.c-amber { background:#fef3c7; color:#d97706; }
.section-title    { font-size:20px; font-weight:700; color:#0f172a; }
.section-subtitle { font-size:13px; color:#64748b; margin-top:2px; }
.screenshot.has-img   { border:1px solid #e2e8f0; border-radius:8px; overflow:hidden; margin:16px 0; }
.screenshot.has-img img { width:100%; display:block; }
.screenshot-caption   { border-top:1px solid #e2e8f0; background:#f8fafc; padding:12px 16px; font-size:13px; }
.screenshot.no-img    { border:2px dashed #e2e8f0; border-radius:8px; padding:48px; text-align:center; color:#94a3b8; font-size:14px; margin:16px 0; }
.action-map       { background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:16px; margin:20px 0; }
.action-map-title { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:#94a3b8; margin-bottom:12px; }
.action-grid      { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:10px; }
.action-card      { display:flex; flex-direction:column; gap:6px; padding:12px 14px; border-radius:8px; border:1px solid #e2e8f0; background:white; text-decoration:none; color:inherit; }
.action-card.action-nav    { border-color:var(--blue); transition:box-shadow .15s,background .15s; }
.action-card.action-nav:hover { background:var(--blue-light); box-shadow:0 2px 8px rgba(37,99,235,.15); }
.action-card.action-submit { border-color:var(--green); }
.action-card.action-dialog { border-color:var(--amber); }
.action-card.action-delete { border-color:var(--red); }
.action-top   { display:flex; align-items:center; justify-content:space-between; gap:8px; }
.action-label { font-weight:600; font-size:14px; color:#1e293b; }
.action-badge { font-size:10px; font-weight:700; padding:2px 7px; border-radius:10px; white-space:nowrap; flex-shrink:0; }
.action-badge.nav    { background:var(--blue-light);  color:var(--blue);  }
.action-badge.submit { background:var(--green-light); color:var(--green); }
.action-badge.dialog { background:var(--amber-light); color:var(--amber); }
.action-badge.delete { background:var(--red-light);   color:var(--red);   }
.action-dest  { font-size:12px; color:var(--blue); font-weight:500; }
.action-desc  { font-size:12px; color:#64748b; }
.steps  { display:flex; flex-direction:column; margin:20px 0; }
.step   { display:flex; gap:16px; position:relative; padding-bottom:20px; }
.step:last-child { padding-bottom:0; }
.step::before { content:''; position:absolute; left:15px; top:32px; bottom:0; width:2px; background:#e2e8f0; }
.step:last-child::before { display:none; }
.step-num  { width:32px; height:32px; border-radius:50%; background:var(--primary); color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:14px; flex-shrink:0; }
.step-body { padding-top:6px; font-size:14px; line-height:1.6; }
.img-zoom       { border:1px solid #e2e8f0; border-radius:8px; display:block; max-width:560px; width:100%; margin:10px 0; box-shadow:0 2px 8px rgba(0,0,0,.07); }
.img-inline     { display:inline-block; vertical-align:middle; max-height:28px; border:1px solid #e2e8f0; border-radius:4px; margin:0 4px; }
.img-zoom-block { background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px 14px; margin:12px 0; }
.img-zoom-label { font-size:11px; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:.05em; margin-bottom:8px; }
.box-warn { border-left:4px solid var(--red);   background:var(--red-light);   padding:12px 16px; border-radius:0 6px 6px 0; margin:16px 0; font-size:14px; }
.box-info { border-left:4px solid var(--blue);  background:var(--blue-light);  padding:12px 16px; border-radius:0 6px 6px 0; margin:16px 0; font-size:14px; }
.box-tip  { border-left:4px solid var(--green); background:var(--green-light); padding:12px 16px; border-radius:0 6px 6px 0; margin:16px 0; font-size:14px; }
.badge        { display:inline-block; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; }
.badge-green  { background:var(--green-light); color:var(--green); }
.badge-red    { background:var(--red-light);   color:var(--red);   }
.badge-blue   { background:var(--blue-light);  color:var(--blue);  }
.badge-amber  { background:var(--amber-light); color:var(--amber); }
.badge-gray   { background:var(--gray-light);  color:var(--gray);  }
.related      { display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:24px; padding-top:16px; border-top:1px solid #e2e8f0; }
.related-label { font-size:12px; color:#94a3b8; font-weight:600; white-space:nowrap; }
.related-chip  { font-size:12px; padding:4px 12px; background:var(--gray-light); border-radius:12px; color:#475569; text-decoration:none; border:1px solid #e2e8f0; transition:background .15s; }
.related-chip:hover { background:var(--primary-light); color:var(--primary); border-color:var(--primary); }
.lang-bar     { display:flex; align-items:center; justify-content:space-between; padding:10px 20px; border-bottom:1px solid rgba(255,255,255,.08); font-size:11px; color:rgba(255,255,255,.45); }
.lang-switch  { display:flex; gap:4px; }
.lang-btn     { padding:3px 10px; border-radius:4px; font-size:11px; font-weight:700; background:transparent; border:1px solid rgba(255,255,255,.2); color:rgba(255,255,255,.5); cursor:pointer; transition:all .15s; }
.lang-btn:hover  { background:rgba(255,255,255,.1); color:white; }
.lang-btn.active { background:rgba(255,255,255,.15); color:white; border-color:rgba(255,255,255,.4); }
/* device tabs — PC / Mobile screenshot switcher
 * ⚠️  ห้ามใช้ .device-mobile { display:none } ใน CSS เด็ดขาด
 *     ให้ใช้ hidden attribute ใน HTML แทน: <div class="device-view device-mobile" hidden>
 *     เพราะ CSS class rule จะชนะ v.style.display='' ทำให้ toggle ไม่ทำงาน */
.device-tabs   { display:flex; gap:6px; padding:10px 14px 0; background:#f8fafc; border-bottom:1px solid #e2e8f0; }
.device-tab    { padding:5px 14px; border-radius:6px 6px 0 0; border:1px solid #e2e8f0; border-bottom:none;
                 font-size:12px; font-weight:600; background:white; color:#64748b; cursor:pointer; transition:all .15s; }
.device-tab:hover  { color:#1e293b; }
.device-tab.active { background:white; color:#0f172a; border-color:#cbd5e1; border-bottom-color:white; margin-bottom:-1px; z-index:1; position:relative; }
.device-view   { padding:0; }
.device-mobile img { border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,.12); }
table { width:100%; border-collapse:collapse; margin:16px 0; }
th    { text-transform:uppercase; font-size:11px; letter-spacing:.05em; color:#64748b; padding:8px 12px; border-bottom:2px solid #e2e8f0; text-align:left; }
td    { padding:10px 12px; border-bottom:1px solid #f1f5f9; font-size:14px; }
```
