#!/usr/bin/env python3
"""
LightKnight Practice Portal Generator — Creates the elite multi-lesson dashboard.
Reads lessons.json and generates a stunning portal page with embedded branding.
"""
import json, base64, os, sys

LOGO_PATH = r"D:\lighknight\logo.png"
WM_PATH   = r"D:\lighknight\myWaterMark.jpg"
PORTAL_DIR = r"D:\humming-the-W-Y"

def b64(path):
    ext = os.path.splitext(path)[1].lower().lstrip(".")
    mime = {"png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg"}.get(ext,"image/png")
    return f"data:{mime};base64,{base64.b64encode(open(path,'rb').read()).decode()}"

def generate():
    logo_uri = b64(LOGO_PATH)
    wm_uri   = b64(WM_PATH)
    lessons  = json.loads(open(os.path.join(PORTAL_DIR, "lessons.json"), "r", encoding="utf-8").read())

    lesson_cards = ""
    for i, L in enumerate(lessons):
        lesson_cards += f"""
        <a href="{L['path']}" class="lesson-card" style="--delay:{i*0.1}s; --accent:{L.get('color','#c5a44e')};">
            <div class="card-glow"></div>
            <div class="card-badge">{L.get('syllables','')}</div>
            <h3 class="card-title-ar">{L.get('titleAr','')}</h3>
            <h4 class="card-title-en">{L.get('title','')}</h4>
            <div class="card-meta">
                <span class="card-instances">{L.get('instances',0)} instances</span>
                <span class="card-date">{L.get('dateAdded','')}</span>
            </div>
            <div class="card-arrow">→</div>
        </a>
        """

    html = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>LightKnight — Quranic Practice</title>
<meta name="description" content="Elite Quranic recitation practice platform by LightKnight Academy">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Amiri:wght@400;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
    --navy: #1a2744;
    --navy-light: #2a3a5e;
    --navy-dark: #0f1a30;
    --gold: #c5a44e;
    --gold-light: #d4b86a;
    --gold-dim: rgba(197,164,78,0.15);
    --text: #e8e6e3;
    --text-dim: #8a95a8;
    --card-bg: rgba(42,58,94,0.4);
}}
html {{ scroll-behavior: smooth; }}
body {{
    background: var(--navy-dark);
    color: var(--text);
    font-family: 'Inter', -apple-system, sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
}}

/* ── Animated Background ───────────────────────── */
.bg-grid {{
    position: fixed;
    inset: 0;
    z-index: 0;
    background:
        radial-gradient(ellipse 80% 60% at 50% 0%, rgba(197,164,78,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(42,58,94,0.5) 0%, transparent 60%),
        linear-gradient(180deg, var(--navy-dark) 0%, var(--navy) 50%, var(--navy-dark) 100%);
    pointer-events: none;
}}
.bg-particles {{
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}}
.particle {{
    position: absolute;
    width: 2px;
    height: 2px;
    background: var(--gold);
    border-radius: 50%;
    opacity: 0;
    animation: float-up 8s ease-in-out infinite;
}}
@keyframes float-up {{
    0% {{ opacity: 0; transform: translateY(100vh) scale(0); }}
    10% {{ opacity: 0.6; }}
    90% {{ opacity: 0.2; }}
    100% {{ opacity: 0; transform: translateY(-10vh) scale(1.5); }}
}}

/* ── Header ───────────────────────── */
.portal-header {{
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 60px 24px 40px;
}}
.logo-container {{
    position: relative;
    display: inline-block;
    margin-bottom: 24px;
}}
.logo-ring {{
    position: absolute;
    inset: -16px;
    border: 1px solid rgba(197,164,78,0.15);
    border-radius: 50%;
    animation: ring-spin 20s linear infinite;
}}
.logo-ring::before {{
    content: '';
    position: absolute;
    top: -3px;
    left: 50%;
    width: 6px;
    height: 6px;
    background: var(--gold);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--gold);
}}
@keyframes ring-spin {{ to {{ transform: rotate(360deg); }} }}
.logo-img {{
    width: 140px;
    height: 140px;
    object-fit: contain;
    border-radius: 24px;
    filter: drop-shadow(0 0 40px rgba(197,164,78,0.3));
}}
.portal-title {{
    font-size: clamp(28px, 5vw, 44px);
    font-weight: 900;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 50%, var(--gold) 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer-text 4s ease-in-out infinite;
}}
@keyframes shimmer-text {{
    0%,100% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
}}
.portal-subtitle {{
    color: var(--text-dim);
    font-size: 15px;
    margin-top: 10px;
    font-weight: 400;
    letter-spacing: 0.02em;
}}
.portal-divider {{
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 20px auto;
}}

/* ── User Info Bar ───────────────────────── */
.user-bar {{
    position: relative;
    z-index: 10;
    max-width: 600px;
    margin: 0 auto 32px;
    padding: 12px 20px;
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(197,164,78,0.1);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}}
.user-name {{
    font-weight: 600;
    font-size: 14px;
    color: var(--gold);
}}
.user-email {{
    font-size: 12px;
    color: var(--text-dim);
}}
.user-logout {{
    background: rgba(239,68,68,0.15);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.3);
    padding: 6px 14px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}}
.user-logout:hover {{ background: rgba(239,68,68,0.3); }}

/* ── Lessons Grid ───────────────────────── */
.lessons-section {{
    position: relative;
    z-index: 10;
    max-width: 900px;
    margin: 0 auto;
    padding: 0 20px 60px;
}}
.section-title {{
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-dim);
    margin-bottom: 20px;
    padding-left: 4px;
}}
.lessons-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
}}

/* ── Lesson Card ───────────────────────── */
.lesson-card {{
    position: relative;
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(197,164,78,0.08);
    border-radius: 16px;
    padding: 28px 24px 24px;
    text-decoration: none;
    color: var(--text);
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    overflow: hidden;
    animation: card-in 0.6s ease backwards;
    animation-delay: var(--delay, 0s);
}}
@keyframes card-in {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
.lesson-card:hover {{
    transform: translateY(-4px);
    border-color: rgba(197,164,78,0.3);
    box-shadow: 0 16px 48px rgba(0,0,0,0.3), 0 0 0 1px rgba(197,164,78,0.15);
}}
.card-glow {{
    position: absolute;
    top: -40%;
    left: -40%;
    width: 180%;
    height: 180%;
    background: radial-gradient(circle at 30% 30%, var(--accent, var(--gold)), transparent 60%);
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
    mix-blend-mode: soft-light;
}}
.lesson-card:hover .card-glow {{ opacity: 0.12; }}
.card-badge {{
    display: inline-block;
    background: var(--gold-dim);
    color: var(--gold);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 6px;
    margin-bottom: 14px;
}}
.card-title-ar {{
    font-family: 'Amiri', serif;
    font-size: 22px;
    color: var(--gold-light);
    margin-bottom: 6px;
    direction: rtl;
    text-align: right;
    line-height: 1.5;
}}
.card-title-en {{
    font-size: 15px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 16px;
}}
.card-meta {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: var(--text-dim);
}}
.card-arrow {{
    position: absolute;
    bottom: 20px;
    right: 20px;
    font-size: 20px;
    color: var(--gold);
    opacity: 0;
    transform: translateX(-8px);
    transition: all 0.3s;
}}
.lesson-card:hover .card-arrow {{ opacity: 1; transform: translateX(0); }}

/* ── Empty State ───────────────────────── */
.empty-state {{
    text-align: center;
    padding: 60px 20px;
    color: var(--text-dim);
}}
.empty-state .empty-icon {{ font-size: 48px; margin-bottom: 16px; opacity: 0.5; }}

/* ── Login Overlay ───────────────────────── */
.login-overlay {{
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(15,26,48,0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}}
.login-card {{
    background: var(--navy);
    border: 1px solid rgba(197,164,78,0.2);
    border-radius: 24px;
    padding: 48px 36px;
    max-width: 400px;
    width: 90%;
    text-align: center;
    box-shadow: 0 24px 80px rgba(0,0,0,0.4);
    animation: login-in 0.5s ease;
}}
@keyframes login-in {{
    from {{ opacity: 0; transform: scale(0.95) translateY(16px); }}
    to {{ opacity: 1; transform: scale(1) translateY(0); }}
}}
.login-logo {{ width: 80px; height: 80px; border-radius: 16px; margin-bottom: 20px; }}
.login-title {{ font-size: 20px; font-weight: 700; color: var(--gold); margin-bottom: 6px; }}
.login-subtitle {{ font-size: 13px; color: var(--text-dim); margin-bottom: 28px; }}
.login-input {{
    width: 100%;
    padding: 14px 18px;
    border: 1px solid rgba(197,164,78,0.2);
    border-radius: 12px;
    background: var(--navy-dark);
    color: var(--text);
    font-size: 15px;
    font-family: 'Inter', sans-serif;
    outline: none;
    transition: border-color 0.2s;
    margin-bottom: 12px;
}}
.login-input:focus {{ border-color: var(--gold); }}
.login-input::placeholder {{ color: var(--text-dim); }}
.login-btn {{
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, var(--gold), var(--gold-light));
    color: var(--navy-dark);
    font-size: 15px;
    font-weight: 700;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s;
    letter-spacing: 0.02em;
    margin-top: 4px;
}}
.login-btn:hover {{ transform: translateY(-1px); box-shadow: 0 8px 24px rgba(197,164,78,0.3); }}
.login-btn:active {{ transform: translateY(0); }}

/* ── Footer ───────────────────────── */
.portal-footer {{
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 32px 20px;
    border-top: 1px solid rgba(197,164,78,0.08);
}}
.footer-links {{ display: flex; gap: 16px; justify-content: center; margin-bottom: 10px; }}
.footer-link {{
    color: var(--text-dim);
    text-decoration: none;
    font-size: 13px;
    transition: color 0.2s;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.footer-link:hover {{ color: var(--gold); }}
.footer-copy {{ font-size: 11px; color: var(--text-dim); opacity: 0.6; }}

/* ── Responsive ───────────────────────── */
@media (max-width: 600px) {{
    .portal-header {{ padding: 40px 16px 28px; }}
    .logo-img {{ width: 100px; height: 100px; }}
    .logo-ring {{ inset: -12px; }}
    .portal-title {{ font-size: 24px; }}
    .lessons-grid {{ grid-template-columns: 1fr; gap: 12px; }}
    .lesson-card {{ padding: 22px 18px 20px; }}
    .user-bar {{ flex-direction: column; text-align: center; padding: 14px; }}
    .login-card {{ padding: 36px 24px; }}
}}
</style>
</head>
<body>

<!-- Animated Background -->
<div class="bg-grid"></div>
<div class="bg-particles" id="particles"></div>

<!-- Login Overlay -->
<div class="login-overlay" id="loginOverlay" style="display:none;">
    <div class="login-card">
        <img src="{logo_uri}" class="login-logo" alt="LightKnight">
        <div class="login-title">Welcome, Student</div>
        <div class="login-subtitle">Enter your name and email to begin</div>
        <input class="login-input" id="loginName" type="text" placeholder="Your full name" autocomplete="name">
        <input class="login-input" id="loginEmail" type="email" placeholder="Your email address" autocomplete="email">
        <button class="login-btn" id="loginBtn">Start Learning</button>
    </div>
</div>

<!-- Header -->
<header class="portal-header">
    <div class="logo-container">
        <div class="logo-ring"></div>
        <img src="{logo_uri}" class="logo-img" alt="LightKnight Academy">
    </div>
    <h1 class="portal-title">Quranic Practice</h1>
    <p class="portal-subtitle">Master Tajweed rules through guided recitation exercises</p>
    <div class="portal-divider"></div>
</header>

<!-- User Bar -->
<div class="user-bar" id="userBar" style="display:none;">
    <div>
        <div class="user-name" id="userDisplayName"></div>
        <div class="user-email" id="userDisplayEmail"></div>
    </div>
    <button class="user-logout" id="logoutBtn">Sign Out</button>
</div>

<!-- Lessons -->
<section class="lessons-section">
    <div class="section-title">Your Lessons</div>
    <div class="lessons-grid" id="lessonsGrid">
        <div class="empty-state">
            <div class="empty-icon">📖</div>
            <div>Loading lessons...</div>
        </div>
    </div>
</section>

<!-- Footer -->
<footer class="portal-footer">
    <div class="footer-links">
        <a href="https://wa.me/201554712241" class="footer-link" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.119.553 4.11 1.519 5.838L0 24l6.336-1.652A11.95 11.95 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 21.75c-1.94 0-3.76-.55-5.303-1.5l-.38-.227-3.946 1.03 1.057-3.854-.25-.396A9.72 9.72 0 012.25 12 9.75 9.75 0 0112 2.25 9.75 9.75 0 0121.75 12 9.75 9.75 0 0112 21.75z"/></svg>
            WhatsApp
        </a>
        <a href="https://t.me/FarisAuransa" class="footer-link" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 000 12a12 12 0 0012 12 12 12 0 0012-12A12 12 0 0012 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 01.171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
            Telegram
        </a>
    </div>
    <div class="footer-copy">&copy; LightKnight Academy</div>
</footer>

<script>
// ── Particles ──────────────────────────────
const particleContainer = document.getElementById('particles');
for (let i = 0; i < 20; i++) {{
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.animationDelay = Math.random() * 8 + 's';
    p.style.animationDuration = (6 + Math.random() * 6) + 's';
    particleContainer.appendChild(p);
}}

// ── Auth ──────────────────────────────
const overlay = document.getElementById('loginOverlay');
const userBar  = document.getElementById('userBar');
let currentUser = localStorage.getItem('qrasm_student_name');
let currentEmail = localStorage.getItem('qrasm_student_email');

function showUserBar() {{
    if (currentUser) {{
        userBar.style.display = 'flex';
        document.getElementById('userDisplayName').textContent = currentUser;
        document.getElementById('userDisplayEmail').textContent = currentEmail || '';
    }}
}}

if (!currentUser) {{
    overlay.style.display = 'flex';
}} else {{
    showUserBar();
}}

document.getElementById('loginBtn').addEventListener('click', () => {{
    const name = document.getElementById('loginName').value.trim();
    const email = document.getElementById('loginEmail').value.trim();
    if (!name) return alert('Please enter your name');
    if (!email || !email.includes('@')) return alert('Please enter a valid email');
    localStorage.setItem('qrasm_student_name', name);
    localStorage.setItem('qrasm_student_email', email);
    currentUser = name;
    currentEmail = email;
    overlay.style.display = 'none';
    showUserBar();
}});

document.getElementById('logoutBtn').addEventListener('click', () => {{
    localStorage.removeItem('qrasm_student_name');
    localStorage.removeItem('qrasm_student_email');
    currentUser = null;
    currentEmail = null;
    userBar.style.display = 'none';
    overlay.style.display = 'flex';
}});

// ── Load Lessons ──────────────────────────────
fetch('lessons.json')
    .then(r => r.json())
    .then(lessons => {{
        const grid = document.getElementById('lessonsGrid');
        if (!lessons || lessons.length === 0) {{
            grid.innerHTML = '<div class="empty-state"><div class="empty-icon">📖</div><div>No lessons available yet</div></div>';
            return;
        }}
        grid.innerHTML = '';
        lessons.forEach((L, i) => {{
            const card = document.createElement('a');
            card.href = L.path;
            card.className = 'lesson-card';
            card.style.setProperty('--delay', i * 0.1 + 's');
            card.style.setProperty('--accent', L.color || '#c5a44e');
            card.innerHTML = `
                <div class="card-glow"></div>
                <div class="card-badge">${{L.syllables || 'Practice'}}</div>
                <h3 class="card-title-ar">${{L.titleAr || ''}}</h3>
                <h4 class="card-title-en">${{L.title || 'Untitled Lesson'}}</h4>
                <div class="card-meta">
                    <span class="card-instances">${{L.instances || 0}} instances</span>
                    <span class="card-date">${{L.dateAdded || ''}}</span>
                </div>
                <div class="card-arrow">→</div>
            `;
            grid.appendChild(card);
        }});
    }})
    .catch(() => {{
        document.getElementById('lessonsGrid').innerHTML = '<div class="empty-state"><div class="empty-icon">⚠️</div><div>Failed to load lessons</div></div>';
    }});
</script>
</body>
</html>"""

    out = os.path.join(PORTAL_DIR, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Portal saved to {out}")

if __name__ == "__main__":
    generate()
