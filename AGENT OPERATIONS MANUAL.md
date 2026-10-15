# AGENT OPERATIONS MANUAL — Keep The Flow
## Version 2.0 · October 2026

> **What is this?** This document is the single source of truth for the **Keep The Flow** Quranic Tajweed practice platform. Any AI agent — regardless of model, provider, or system — should be able to read this file and fully operate, maintain, and extend the project.

---

## Table of Contents

1. [Golden Prompt](#-golden-prompt)
2. [Project Overview](#-project-overview)
3. [Architecture](#-architecture)
4. [Complete File Map](#-complete-file-map)
5. [Supabase Database Schema](#-supabase-database-schema)
6. [Email Notification System](#-email-notification-system-6-triggers)
7. [**Lesson Production Pipeline (Branding Skill)**](#-lesson-production-pipeline-branding-skill) ← **THE MOST IMPORTANT SECTION**
8. [How To: Add a New Lesson (Deployment Steps)](#-how-to-add-a-new-lesson-deployment-steps)
9. [How To: Add a New Quiz](#-how-to-add-a-new-quiz)
10. [How To: Add Learn Section Content](#-how-to-add-learn-section-content)
11. [Quiz System](#-quiz-system)
12. [Report Feature](#-report-feature)
13. [Admin Capabilities Without Any Agent](#-admin-capabilities-without-any-agent)
14. [Credentials & Secrets](#-credentials--secrets)
15. [Critical Rules](#-critical-rules)
16. [Feature List](#-feature-list)
17. [Git Checkpoint History](#-git-checkpoint-history)

---

## 🤖 Golden Prompt

Copy-paste this block verbatim to any new AI agent:

```
I need you to work on my Keep The Flow Quranic practice website.

FIRST: Read this file COMPLETELY before doing ANYTHING:
  D:\KeepTheFlow\AGENT OPERATIONS MANUAL.md

The project is at: D:\KeepTheFlow
GitHub: https://github.com/faris11zsc/KeepTheFlow
Live site: https://keep-the-flow.vercel.app
Automation repo: D:\lighknight\automation (GitHub: https://github.com/faris11zsc/automate-schedule.git)

CRITICAL RULES:
- NEVER delete files on C:\ drive
- ALWAYS run "node D:\KeepTheFlow\validate-lessons.js" BEFORE pushing
- ALWAYS push to GitHub after changes (Vercel auto-deploys from main)
- Create git checkpoints before major changes
- The SB_HEADERS block in keeptheflow_notifier.py is a PROTECTED ZONE — NEVER edit it
- After editing keeptheflow_notifier.py, ALWAYS run: python -m py_compile D:\lighknight\automation\keeptheflow_notifier.py
- All generated files go on D:\ — never C:\

Now here's what I need: [YOUR REQUEST]
```

---

## 📋 Project Overview

**Keep The Flow** is a Quranic Tajweed practice platform for LightKnight Academy. It hosts:
- **Lessons**: Interactive Tajweed rule practice with Quranic instances, recording homework, admin grading, and deep-link sharing.
- **QuizMe**: A quiz system where the admin creates MCQ quizzes, assigns them to students, tracks scores, and receives completion reports.
- **Learn**: Educational content pages (currently: Azkar of the Adhan) with audio, tooltips, dark mode, and progress tracking.

| Property | Value |
|:---|:---|
| **Live URL** | `https://keep-the-flow.vercel.app` |
| **GitHub Repo** | `https://github.com/faris11zsc/KeepTheFlow` |
| **Hosting** | Vercel (auto-deploys from `main` branch) |
| **Database** | Supabase (REST API — no SDK, direct HTTP) |
| **Tech Stack** | Pure HTML/CSS/JS — zero frameworks, zero build step |
| **Automation Repo** | `https://github.com/faris11zsc/automate-schedule.git` (local: `D:\lighknight\automation`) |
| **Automation Schedule** | GitHub Actions cron every 5 minutes (`reminder.yml`) |
| **Admin Email** | `lightknightf1@gmail.com` |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         VERCEL (CDN)                            │
│  Auto-deploys from GitHub main branch                           │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────┐ ┌─────────────┐  │
│  │ index.html  │ │  lessons/*  │ │   qm/*   │ │   learn/*   │  │
│  │  (Portal)   │ │  (9 lessons)│ │ (QuizMe) │ │ (Learn)     │  │
│  └─────────────┘ └─────────────┘ └──────────┘ └─────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       SUPABASE                                  │
│  Tables: qrasm_recordings, qrasm_student_emails                 │
│  Stores: recordings, grades, quiz defs, quiz scores, reports,   │
│          lesson config, learn config, system state               │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Polled every 5 minutes
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 GITHUB ACTIONS (automation repo)                 │
│  reminder.yml → runs wa_reminder.py + keeptheflow_notifier.py    │
│  6 email triggers via Gmail SMTP                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Complete File Map

### Main Repository: `D:\KeepTheFlow`

| Path | Purpose |
|:---|:---|
| `index.html` | Main portal/dashboard. Student login, lesson cards. ~1.5MB (base64-embedded logos). Generated by `generate_portal.py`. |
| `lessons.json` | Lesson registry. Array of objects with `id`, `title`, `titleAr`, `rule`, `syllables`, `instances`, `path`, `assignmentId`, `color`, `dateAdded`. |
| `validate-lessons.js` | **MUST RUN BEFORE EVERY PUSH.** Verifies every lesson has admin copy-link buttons, JS reveal logic, and clipboard handlers. Exit 0 = pass. |
| `generate_portal.py` | Regenerates `index.html` from `lessons.json`. Reads `D:\lighknight\logo.png` and `D:\lighknight\myWaterMark.jpg`. |
| `patch_exit_btn.py` | One-time patch script to inject "Dashboard" back-buttons into all lessons. |
| `vercel.json` | Vercel routing. Currently: no-cache headers on `/qm/*` to prevent stale quiz data. |

### Lessons: `D:\KeepTheFlow\lessons\`

Each lesson lives in `lessons/{slug}/index.html`. Current lessons (9):

| Slug | Tajweed Rule | Instances |
|:---|:---|:---|
| `idgham-yw-5-12` | Idgham in Yaa/Waw (5-12 syl) | 143 |
| `ghunnah-5-12` | Ghunnah of Noon/Meem (5-12 syl) | 696 |
| `iqlab-ikhfa-shafawi-5-20` | Iqlab + Ikhfa Shafawi (5-20 syl) | 218 |
| `extended-humming-5-12` | Ikhfa Haqiqi (5-12 syl) | 364 |
| `ghunnah-noon-meem-5-12` | Noon/Meem Mushaddadatain (5-12 syl) | 696 |
| `idgham-yw-broad-7-12` | Idgham Yaa/Waw Broad (7-12 syl) | 52 |
| `madd-lazim-7-12` | Madd Lazim Kalimi (3-12 syl) | 15 |
| `tripled-extended-vowels` | Tripled Extended Vowels (13-200 syl) | 68 |
| `idgham-yw-7-12` | Idgham Yaa/Waw (7-12 syl) | 163 |

### QuizMe: `D:\KeepTheFlow\qm\`

| File | Purpose |
|:---|:---|
| `index.html` | QuizMe dashboard. Admin creates/edits/deletes/copies quizzes. Students see their assigned quizzes with completion status. |
| `quiz.html` | Quiz player. Students answer questions sequentially (fixed universal order — NO shuffling). Admin has super-bar for navigation/editing. |
| `audio/correct1-5.m4a` | Correct answer sound effects (random selection). |
| `audio/wrong1-2.m4a` | Wrong answer sound effects. |
| `audio/salat-alfatih.mp3` | Quiz completion ceremony audio (Salat al-Fatih prayer, 4:53, loops). Stops on page leave/tab switch/browser close. |

### Legacy QuizMe: `D:\KeepTheFlow\quizme\`

| File | Purpose |
|:---|:---|
| `index.html` | Older QuizMe dashboard version. Same structure as `qm/`. |
| `quiz.html` | Older quiz player version. |

### Learn Section: `D:\KeepTheFlow\learn\`

| Path | Purpose |
|:---|:---|
| `azkar-adhan/index.html` | "Azkar of the Adhan" interactive lesson with trimmed audio clips, tooltips, dark mode, progress tracking. |
| `azkar-adhan/audio/*.mp3` | Audio files: `dua-hawla.mp3`, `dua-raditu.mp3`, `dua-waseelah.mp3`. |

### Automation: `D:\lighknight\automation\`

| File | Purpose |
|:---|:---|
| `keeptheflow_notifier.py` | Email notifier v4.0. 6 triggers. Gmail SMTP. Supabase REST. **PROTECTED ZONE around SB_HEADERS.** |
| `wa_reminder.py` | WhatsApp reminder system. |
| `.github/workflows/reminder.yml` | GitHub Actions cron: runs every 5 min, executes both `wa_reminder.py` and `keeptheflow_notifier.py`. |
| `requirements.txt` | Python deps for automation. |

### Branding & Upload Pipeline

| File | Purpose |
|:---|:---|
| `D:\push_to_web.py` | Lesson upload pipeline. Strips Mode 1 splash, wraps in Mode 2 branding via `wrap_html.py`, updates `lessons.json`. |
| `C:\Users\sdd\.gemini\.gemini\skills\preface\scripts\wrap_html.py` | HTML branding wrapper. Mode 1 = splash page, Mode 2 = top banner. Auto-injects report buttons on new lessons. |
| `D:\lighknight\skills\branding\SKILL.md` | Branding pipeline skill documentation (PDF branding, lesson registration, notifier safety rules). |
| `D:\lighknight\skills\branding\scripts\brand_pdf.py` | PDF branding engine. Wraps raw qrasm-pdf output with logo cover, contact page, contents page, watermark. Deps: PyMuPDF, reportlab, Pillow. |

### Scounter (Syllable Research Engine)

| File | Purpose |
|:---|:---|
| `D:\lighknight\skills\scounter\SKILL.md` | Scounter skill documentation. Phonological rules, ordering rules, CSV metadata format. |
| `D:\lighknight\skills\scounter\scripts\scount.py` | Core engine. Counts Quranic syllables, filters by rule/syllables/red-lines, outputs CSV with `# META:` headers. |
| `D:\lighknight\skills\scounter\scripts\audit_corpus.py` | Corpus auditor. Validates and normalizes Quran CSV source files before research. |
| `D:\lighknight\skills\scounter\references\rules.md` | Detailed phonological rules reference (syllable types, waqf handling, cluster counting). |
| `D:\lighknight\quran_uthmani_indopak_waqf_expanded.csv` | **THE QURAN CORPUS** (~2.8 MB). Uthmani Indopak script with waqf symbols. This is the source data for ALL lesson research. |

### qRasm-PDF (Quranic Visualization Engine)

| File | Purpose |
|:---|:---|
| `D:\lighknight\skills\qrasm-pdf\SKILL.md` | qRasm-PDF skill documentation. Rendering modes, style presets, critical rules. |
| `D:\lighknight\skills\qrasm-pdf\scripts\generate_qrasm_pdf.py` | Core engine. Fetches Quran.com QCF V2 fonts, renders Quranic phrases as vector PDF. |
| `D:\lighknight\skills\qrasm-pdf\scripts\cache_word_cdn\` | Cache directory for downloaded Quran.com word data (JSON files). Do NOT delete. |

### Session Skills (Quiz & Lesson Generation from Transcripts)

| File | Purpose |
|:---|:---|
| `D:\lighknight\faris-session-quiz-SKILL.md` | Skill for generating MCQ quizzes from tutoring session transcripts. Verifies content against traditional Islamic sources. |
| `D:\lighknight\faris-session-lesson-SKILL.md` | Skill for generating interactive HTML study-revision lessons from transcripts. Includes TTS audio, images, glassmorphism UI. |

### Branding Assets (Fixed Paths — Never Move)

| Asset | Path |
|:---|:---|
| Logo | `D:\lighknight\logo.png` |
| Contact PDF | `D:\lighknight\contact_us_page.pdf` |
| Watermark | `D:\lighknight\myWaterMark.jpg` |
| Output Directory | `D:\lighknight\outputs\` |

---

## 🗄️ Supabase Database Schema

**URL:** `https://lhebavvnrwqojbhyodwc.supabase.co`
**Anon Key:** `sb_publishable_JW75ayCf5SbvyT-02GmjNQ_vFpivPTU`

### Table: `qrasm_recordings`

The main data table. Uses naming conventions in `student_name` to store different types of data:

| Column | Type | Purpose |
|:---|:---|:---|
| `id` | serial | Primary key |
| `student_name` | text | Student name OR system key (see conventions below) |
| `assignment_id` | text | Lesson assignment ID or system identifier |
| `instance_number` | int | Instance/question number |
| `audio_url` | text (NOT NULL) | Audio recording URL or system data |
| `grade` | text | Grade/rating or JSON quiz data |
| `created_at` | timestamp | Row creation time |

#### Naming Conventions (in `student_name` column)

| Pattern | Purpose |
|:---|:---|
| `{actual name}` | Real student recording row |
| `QUIZ_DEF_{student}` | Quiz definition. `grade` = JSON with questions, `assignment_id` = `quizme`, `instance_number` = quiz ID |
| `QUIZ_SCORE_{student}` | Quiz score. `grade` = score string, `audio_url` = quiz title |
| `ADMIN_FEEDBACK_{student}` | Teacher feedback on a recording |
| `EMAIL_SENT_*` | Notifier deduplication tracking (NEW_STUDENT, SUBMISSIONS, FEEDBACK, QUIZ, QUIZ_DONE, REPORT) |
| `SYSTEM_ERROR` | Error logging from notifier |
| `LESSONS_CONFIG` | Admin lesson dashboard configuration |
| `LEARN_CONFIG` | Learn section admin configuration |
| `LEARN_PAGE_*` | Learn page content |
| `ADMIN_HIDDEN` | Hidden lesson instances |
| `assignment_id='report'` | Student report. `grade` = message, `audio_url` = direct URL to the reported item |

### Table: `qrasm_student_emails`

| Column | Type | Purpose |
|:---|:---|:---|
| `student_name` | text | Student's display name |
| `email` | text | Student's email address |

---

## 📧 Email Notification System (6 Triggers)

The notifier runs every 5 minutes via GitHub Actions. File: `D:\lighknight\automation\keeptheflow_notifier.py`

| # | Trigger | Direction | Description |
|:---|:---|:---|:---|
| 1 | New Student Registers | → Admin | Admin gets email when a new student name appears |
| 2 | Student Records Instances | → Admin | Admin gets email with deep links to review each instance |
| 3 | Admin Gives Feedback | → Student | Student gets email with color-coded review links (runs at :00 and :30 only) |
| 4 | Quiz Assigned | → Student | Student gets email with quiz link when admin creates/assigns a quiz |
| 5 | Quiz Completed | → Admin | Admin gets email with student's score when they finish a quiz |
| 6 | Student Reports Issue | → Admin | Admin gets email with report message and direct link to the reported item |

### Deduplication

Each trigger tracks sent emails using rows in `qrasm_recordings` with `student_name` = `EMAIL_SENT_{TAG}` and `audio_url` = unique key. This prevents duplicate emails across runs.

### Deep Links

Lesson emails include `?admin=true&scrollTo={instanceNumber}` parameters.
Quiz emails include `?quizId={id}&student={name}` parameters.
Report emails include the full URL the student was viewing when they submitted the report.

---

## 🎯 Lesson Production Pipeline (Branding Skill)

> [!IMPORTANT]
> **This is the most critical section of this manual.** The branding pipeline is HOW every lesson on Keep The Flow is built. Without it, the website cannot grow. The pipeline has 4 phases, each using a different skill/script. A future agent MUST understand all 4 phases to produce a new lesson.

### Pipeline Overview

```
 PHASE 1: CSV Research          PHASE 2: PDF Visualization      PHASE 3: PDF Branding           PHASE 4: HTML & Deploy
 ─────────────────────          ──────────────────────────       ─────────────────────           ───────────────────────
 ┌─────────────────┐           ┌─────────────────┐              ┌─────────────────┐             ┌─────────────────┐
 │   scount.py     │           │generate_qrasm_  │              │  brand_pdf.py   │             │  wrap_html.py   │
 │   (scounter)    │ ──CSV──→  │   pdf.py         │ ──raw PDF→  │  (branding)     │ ──branded   │  push_to_web.py │
 │                 │           │   (qrasm-pdf)    │              │                 │   PDF──→    │  → KeepTheFlow  │
 └─────────────────┘           └─────────────────┘              └─────────────────┘             └─────────────────┘
  Input: Quran CSV              Input: CSV/text                  Input: raw PDF                  Input: branded PDF/HTML
  Output: filtered CSV          Output: raw Quran PDF            Output: branded PDF             Output: live website lesson
  with Tajweed matches          with QCF vector text             with logo+contacts+contents     with recording UI
```

### Phase 1: CSV Research (scounter skill)

**Purpose:** Search the entire Quran corpus for Quranic instances that match a specific Tajweed rule, filtered by syllable count and red lines.

**Skill Location:** `D:\lighknight\skills\scounter\SKILL.md`
**Script:** `D:\lighknight\skills\scounter\scripts\scount.py`
**Quran Corpus:** `D:\lighknight\quran_uthmani_indopak_waqf_expanded.csv` (~2.8 MB)

#### What The Agent Must Gather From The User

1. **Tajweed Rule** (Arabic name + which `--target-rule` to use)
2. **Red Lines** (exclusions: `madd-lazim`, `elteqa-sakenayn`, `wasl-no-lam`, `idgham-naqis-waw-yaa`, `disjointed-letters`)
3. **Syllable Range** (e.g., `5-12`, `7-12`, `5-20`)
4. **Target Mode** (`verse`, `phrase`, or `both` — usually `both`)

#### Available Target Rules

| `--target-rule` value | Arabic Name | What It Matches |
|:---|:---|:---|
| `ghunnah-mushaddadah-2plus` | غنة مشددة | Shaddah on Noon or Meem |
| `madd-hamzah-2plus` | مد | Madd with Hamza |
| `iqlab-ikhfa-shafawi` | الإقلاب والإخفاء الشفوي | Iqlab + Ikhfa Shafawi |
| `madd-lazim` | المد اللازم | Madd Lazim |
| `madd-lazim-kalimi` | المد اللازم الكلمي | Madd Lazim Kalimi |
| `idgham-naqis-waw-yaa` | إدغام النون والتنوين في الياء أو الواو | Idgham of Noon/Tanween in Yaa/Waw |

#### Example Command (Real Production Run)

```powershell
python D:\lighknight\skills\scounter\scripts\scount.py `
    D:\lighknight\quran_uthmani_indopak_waqf_expanded.csv `
    7-12 `
    --mode both `
    --target-rule idgham-naqis-waw-yaa `
    --red-lines "madd-lazim,elteqa-sakenayn,wasl-no-lam" `
    --output "D:\Idgham YW 7-12.csv"
```

**Output:** A CSV file with `# META:` header lines + columns: `surah`, `ayah`, `syllables`, `pattern`, `type`, `ref`, `text`

#### CSV Metadata (Auto-Generated)

The output CSV includes `# META:` comment lines that the branding script reads automatically:
```
# META: rule_name=Idgham Naqis (إدغام النون والتنوين في الياء أو الواو)
# META: syllable_range=7-12
# META: target_mode=both
# META: red_lines=madd-lazim,elteqa-sakenayn,wasl-no-lam
# META: instance_count=166
# META: created=2026-10-03
# META: source=quran_uthmani_indopak_waqf_expanded.csv
```

#### Validation

After generating, always run `--self-test` to verify the engine is sound:
```powershell
python D:\lighknight\skills\scounter\scripts\scount.py --self-test
```

---

### Phase 2: PDF Visualization (qrasm-pdf skill)

**Purpose:** Take the CSV output from Phase 1 and render each Quranic phrase using authentic Quran.com QCF V2 page fonts — crisp vector text, not pixelated images.

**Skill Location:** `D:\lighknight\skills\qrasm-pdf\SKILL.md`
**Script:** `D:\lighknight\skills\qrasm-pdf\scripts\generate_qrasm_pdf.py`

#### How It Works

1. Reads phrases with `(surah:ayah)` references from the CSV or a text file
2. Fetches Quran.com API word data for each ayah
3. Matches each phrase to exact word positions
4. Downloads Quran.com QCF V2 page fonts
5. Renders QCF glyphs as vector text in a PDF (zoom-safe, no pixelation)

#### Style Presets

| Style | Description |
|:---|:---|
| `classic` | Default cream/gold — matches LightKnight branding perfectly |
| `navy` | Calm navy teaching style |
| `emerald` | Green Islamic theme |
| `burgundy` | Warm red-wine theme |
| `children` | Child-friendly warm colors |
| `night` | Dark mode |
| `custom` | User specifies exact colors |

#### Example Command

```powershell
$env:PYTHONIOENCODING='utf-8'
python D:\lighknight\skills\qrasm-pdf\scripts\generate_qrasm_pdf.py `
    --style classic `
    --output "D:\lighknight\outputs\idgham_yw_raw.pdf" `
    "D:\Idgham YW 7-12.csv"
```

**Output:** A raw PDF with Quranic phrases in authentic script + a `.manifest.json` audit file + `_images/` folder

#### Critical Rules
- Default `--render-mode qcf` = vector text (always use this for final output)
- `--gap 3` keeps words close like Madani spacing
- Do NOT remove QCF glyph reversal logic — it keeps waqf symbols correct
- Do NOT trim individual word images — only trim final composed phrases
- After editing the script, always validate: `python -m py_compile D:\lighknight\skills\qrasm-pdf\scripts\generate_qrasm_pdf.py`

---

### Phase 3: PDF Branding (branding skill)

**Purpose:** Wrap the raw qrasm-pdf output with professional LightKnight branding layers.

**Skill Location:** `D:\lighknight\skills\branding\SKILL.md`
**Script:** `D:\lighknight\skills\branding\scripts\brand_pdf.py`

#### What It Adds (In Order)

| Page | Content |
|:---|:---|
| Page 1 | **Logo Cover** — Full-quality `D:\lighknight\logo.png` (632×633, contain mode, no cropping) |
| Page 2 | **Contact Page** — `D:\lighknight\contact_us_page.pdf` with clickable WhatsApp (`https://wa.me/201554712241`) + Telegram (`https://t.me/FarisAuransa`) |
| Page 3 | **Contents Page** — Describes the Tajweed rule, Quranic purity, graduated progression, authentic rasm, focused scope, footer hadith |
| Pages 4+ | **Quranic Content** — All pages from qrasm-pdf, untouched |
| Pages 2+ | **Watermark** — "byFarisAura" text in #B0B0B0, ~8pt, bottom-right corner |
| Last Page | **Back Page** (optional) — Closing du'a + LightKnight identity |

#### Two Ways to Run

**With CSV auto-read (recommended — reads metadata from scounter CSV):**
```powershell
$env:PYTHONIOENCODING='utf-8'
python D:\lighknight\skills\branding\scripts\brand_pdf.py `
    --input "D:\lighknight\outputs\idgham_yw_raw.pdf" `
    --csv "D:\Idgham YW 7-12.csv" `
    --output "D:\lighknight\outputs\Idgham YW 7-12 Branded.pdf"
```

**With explicit parameters:**
```powershell
$env:PYTHONIOENCODING='utf-8'
python D:\lighknight\skills\branding\scripts\brand_pdf.py `
    --input "D:\lighknight\outputs\idgham_yw_raw.pdf" `
    --output "D:\lighknight\outputs\Idgham YW 7-12 Branded.pdf" `
    --rule-name "Idgham of Noon and Tanween in Yaa or Waw" `
    --rule-name-ar "إدغام النون والتنوين في الياء أو الواو" `
    --syllable-range "7-12" `
    --instance-count 166 `
    --target-mode "both" `
    --red-lines "madd-lazim,elteqa-sakenayn,wasl-no-lam"
```

#### Contents Page Design Rules
- First person plural ("We have compiled..."), never individual names
- Arabic Tajweed terminology (not script variable names)
- Bilingual: English primary with Arabic terms inline
- Unicode-safe: Arial TTF fonts for full Arabic + Latin + symbol support

#### Dependencies
```powershell
pip install PyMuPDF reportlab Pillow
```

#### Branding Assets (Fixed Paths — Never Move)

| Asset | Path |
|:---|:---|
| Logo | `D:\lighknight\logo.png` |
| Contact PDF | `D:\lighknight\contact_us_page.pdf` |
| Watermark Reference | `D:\lighknight\myWaterMark.jpg` |
| Output Directory | `D:\lighknight\outputs\` |

---

### Phase 4: HTML Conversion & Web Deployment

**Purpose:** Convert the branded PDF content into an interactive HTML lesson page and deploy it to Keep The Flow.

This phase uses **TWO parallel paths** depending on what was produced:

#### Path A: If You Have a Raw HTML File (Most Common)

The `push_to_web.py` script handles everything:

**Script:** `D:\push_to_web.py`
**HTML Wrapper:** `C:\Users\sdd\.gemini\.gemini\skills\preface\scripts\wrap_html.py`

**What `wrap_html.py` Does (Mode 2 — Web Deployment Mode):**
- Injects the LightKnight branded top banner (navy/gold theme, logo, contact links)
- Injects a "Lesson Overview / Instructions" card with metadata (rule name, syllable range)
- Injects the **report button (🚩)** in the bottom-left corner for every instance
- Injects the report modal that saves to Supabase
- Injects admin copy-link and hide buttons for each instance
- Injects the exit-to-dashboard button

**What `push_to_web.py` Does:**
1. Reads the raw HTML lesson file
2. Strips any Mode 1 splash overlay (if present from PDF viewer)
3. Calls `wrap_html.py --mode 2` to inject all branding + interactive features
4. Saves to `D:\KeepTheFlow\lessons\{slug}\index.html`
5. Updates `D:\KeepTheFlow\lessons.json` with the lesson entry

#### Path B: Direct Vercel Deployment

Use the `vercel-deploy-prepper` skill (`D:\lighknight\skills\vercel-deploy-prepper\SKILL.md`) to push files to the GitHub repo which auto-deploys to Vercel.

---

### Complete Production Example (End-to-End)

Here is a real-world example of how the lesson `idgham-yw-7-12` (163 instances) was produced:

```powershell
# ── PHASE 1: Research (find Quranic instances) ────────────────────────
python D:\lighknight\skills\scounter\scripts\scount.py `
    D:\lighknight\quran_uthmani_indopak_waqf_expanded.csv `
    7-12 --mode both `
    --target-rule idgham-naqis-waw-yaa `
    --red-lines "madd-lazim,elteqa-sakenayn,wasl-no-lam" `
    --output "D:\Idgham YW 7-12.csv"
# Output: 166 matches saved to D:\Idgham YW 7-12.csv

# ── PHASE 2: Visualize (render Quranic text as PDF) ──────────────────
$env:PYTHONIOENCODING='utf-8'
python D:\lighknight\skills\qrasm-pdf\scripts\generate_qrasm_pdf.py `
    --style classic `
    --output "D:\lighknight\outputs\idgham_yw_raw.pdf" `
    "D:\Idgham YW 7-12.csv"

# ── PHASE 3: Brand (wrap with logo, contacts, contents page) ─────────
$env:PYTHONIOENCODING='utf-8'
python D:\lighknight\skills\branding\scripts\brand_pdf.py `
    --input "D:\lighknight\outputs\idgham_yw_raw.pdf" `
    --csv "D:\Idgham YW 7-12.csv" `
    --output "D:\lighknight\outputs\Idgham YW 7-12 Branded.pdf"

# ── PHASE 4: Deploy (convert to web lesson + upload) ─────────────────
# (See "How To: Add a New Lesson" section below for deployment steps)
```

---

## 📝 How To: Add a New Lesson (Deployment Steps)

> [!NOTE]
> These are the DEPLOYMENT steps only. The lesson content must first be produced using the [Lesson Production Pipeline](#-lesson-production-pipeline-branding-skill) above.

### End-to-End Deployment

1. **Prepare the entry in `D:\push_to_web.py`**: Add a new entry to the `files` list:
   ```python
   {
       "src": r"D:\Your Lesson Name.html",
       "id": "your-lesson-slug",
       "title": "Display Title",
       "titleAr": "العنوان بالعربية",
       "rule": "Tajweed Rule Name",
       "syllables": "5-12",
       "instances": 100,
       "color": "#hexcolor"
   }
   ```

2. **Run the upload pipeline**:
   ```powershell
   python D:\push_to_web.py
   ```
   This:
   - Strips Mode 1 splash (if present)
   - Wraps in Mode 2 branding via `wrap_html.py` (auto-injects report button)
   - Creates `D:\KeepTheFlow\lessons\{slug}\index.html`
   - Updates `D:\KeepTheFlow\lessons.json`

3. **Regenerate the portal** (optional — only if portal needs updating):
   ```powershell
   python D:\KeepTheFlow\generate_portal.py
   ```

4. **Validate lesson integrity**:
   ```powershell
   node D:\KeepTheFlow\validate-lessons.js
   ```
   Must exit code 0 (all passed).

5. **Register in the notifier** — edit `D:\lighknight\automation\keeptheflow_notifier.py`:
   - Find the `LESSON_PATHS` dict (look for `# ── ADD NEW LESSONS HERE`)
   - Add one line at the end: `"your_lesson_assignment_id": "lessons/your-lesson-slug",`
   - **NEVER touch the `SB_HEADERS` PROTECTED ZONE**
   - Verify syntax:
     ```powershell
     python -m py_compile D:\lighknight\automation\keeptheflow_notifier.py
     ```

6. **Commit and push both repos**:
   ```powershell
   # KeepTheFlow repo
   cd D:\KeepTheFlow
   git add -A
   git commit -m "Add new lesson: your-lesson-slug"
   git push origin main

   # Automation repo (if notifier was updated)
   cd D:\lighknight\automation
   git add -A
   git commit -m "Register new lesson in notifier: your-lesson-slug"
   git push origin main
   ```

### Manual Lesson Creation (Without Pipeline)

If creating a lesson manually (not from the branding pipeline), ensure the HTML file includes:
- `admin-hide-btn` with `data-instance="N"` for each instance
- `admin-copy-link-btn` with `data-instance="N"` for each instance
- JS reveal logic that shows copy-link buttons for admins
- JS clipboard handler for copy-link buttons
- Report button (🚩) in the bottom-left corner
- Report modal that submits to Supabase with `assignment_id='report'`

---

## 🧠 How To: Add a New Quiz

### From the Admin Dashboard (No Code Needed)

1. Go to `https://keep-the-flow.vercel.app/qm/` (or `/quizme/`)
2. Log in as admin
3. Click "Create Quiz"
4. Paste your questions in the text parser (supports multiple formats: `1. Question`, `**1.** Question`, numbered with A/B/C/D options)
5. Set the quiz title, assign to a student
6. Save — the quiz is stored in Supabase and the student gets an email notification

### From a Transcript (Using Skills)

1. Use the `faris-session-quiz` skill (`D:\lighknight\faris-session-quiz-SKILL.md`)
2. It reads a tutoring transcript, extracts teaching points, verifies against traditional sources, and generates an MCQ markdown document
3. Paste the markdown into the admin quiz parser on the dashboard

### Quiz Data Storage

- Quiz definitions: `student_name='QUIZ_DEF_{student}'`, `assignment_id='quizme'`, `instance_number={quizId}`, `grade={JSON with questions}`
- Quiz scores: `student_name='QUIZ_SCORE_{student}'`, `grade={score}`, `audio_url={title}`

### Quiz Order

**IMPORTANT**: Quizzes use a **fixed universal order** — questions are always displayed in the same order for both students and admin. There is NO random shuffling. This ensures that when a student reports "question 5", the admin sees the same question 5.

---

## 📖 How To: Add Learn Section Content

### From the Admin Dashboard

1. The Learn section is managed via the admin dashboard on `index.html`
2. Admin can add/edit/delete/reorder/hide/duplicate/preview/share Learn content
3. Configuration is persisted in Supabase as `LEARN_CONFIG` and `LEARN_PAGE_*` rows

### Manual HTML Page

1. Create a new folder under `D:\KeepTheFlow\learn\{slug}\`
2. Add an `index.html` file with the lesson content
3. Include any audio files in a `{slug}/audio/` subfolder
4. The page should follow the LightKnight styling conventions (navy/gold theme, Inter + Amiri fonts, dark mode toggle)

---

## 🎮 Quiz System

### Student Experience
- Fixed sequential order (no shuffling)
- Must answer each question before proceeding (cannot skip)
- Streak counter shows correct/wrong streaks
- Sound effects on correct/wrong answers
- Screen shake on wrong answers, particles on correct
- Completion ceremony: Salat al-Fatih audio (loops), prayer text in English + Arabic, grade-dependent colors/particles
- Ceremony audio stops on page leave, tab switch, or browser close
- Report button (🚩) in bottom-left corner to report issues with any question

### Admin Super-Bar
When `?admin=true` is in the URL, the admin gets a floating toolbar with:
- **Previous/Next** navigation (skip freely)
- **Jump to question** (enter number and go directly)
- **Reveal answer** without selecting
- **End quiz** at any point
- **Edit question** inline
- No requirement to answer before proceeding

### Quiz URL Parameters
- `?quizId={id}&student={name}` — opens a specific quiz for a student
- `?admin=true` — enables admin super-bar
- `?q={number}` — jumps directly to a specific question (used in report links)

---

## 🚩 Report Feature

### How It Works
1. Student sees a small flag button (🚩) in the bottom-left corner of every lesson instance and every quiz question
2. Clicking opens a modal where they can type a message describing the issue
3. Submitting sends a row to Supabase with:
   - `assignment_id = 'report'`
   - `grade = {message text}`
   - `audio_url = {direct URL to the reported item}`
   - `student_name = {student's name}`
4. The notifier (Trigger 6) picks this up and emails the admin with the message and a direct clickable link

### URL Generation
- **Lessons**: URL includes `?scrollTo={instanceNumber}` to scroll directly to the reported instance
- **Quizzes**: URL includes `?q={questionNumber}` to jump directly to the reported question

### Injection
- **New lessons**: The `wrap_html.py` branding wrapper automatically injects the report button and modal
- **Existing lessons**: Were patched using a dedicated injection script
- **Quizzes**: Report button is built into `qm/quiz.html`

---

## 🔧 Admin Capabilities Without Any Agent

Things the admin (Faris) can do directly from the live website without any AI agent:

| Task | Where |
|:---|:---|
| Create/edit/delete quizzes | `https://keep-the-flow.vercel.app/qm/` (admin mode) |
| Copy quiz / assign to student | QuizMe dashboard |
| View quiz scores | QuizMe dashboard |
| Review student recordings | Any lesson page with `?admin=true` |
| Grade recordings (perfect/good/retry) | Lesson page admin panel |
| Send audio feedback to students | Lesson page admin panel |
| Hide/show lesson instances | Lesson page admin panel |
| Copy direct link to any instance | Lesson page admin panel |
| Reorder/hide/add/delete lessons | Portal admin panel |
| Add/edit/delete Learn content | Portal admin panel |
| View student reports | Via email (Trigger 6) |

---

## 🔑 Credentials & Secrets

### Supabase
- **URL**: `https://lhebavvnrwqojbhyodwc.supabase.co`
- **Anon Key**: `sb_publishable_JW75ayCf5SbvyT-02GmjNQ_vFpivPTU`
- These are hardcoded in `keeptheflow_notifier.py` and in the HTML files (client-side REST)

### Gmail (for email notifications)
- Stored as GitHub Actions secrets: `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`
- Admin email recipient: `lightknightf1@gmail.com`

### GitHub Actions Secrets (automation repo)
- `NOTION_TOKEN` — for WhatsApp reminder system
- `GMAIL_ADDRESS` / `GMAIL_APP_PASSWORD` — for email sending
- `GCAL_CREDENTIALS` — for Google Calendar integration
- `SUPABASE_URL` / `SUPABASE_KEY` — Supabase connection (overrides hardcoded defaults)

### Student Auth
- Students authenticate via localStorage: `qrasm_student_name`, `qrasm_student_email`
- No passwords — name + email pair is the identity

---

## 🚨 Critical Rules

> [!CAUTION]
> These rules are ABSOLUTE. Breaking any of them can corrupt the platform, lose student data, or break email notifications.

### 1. NEVER delete files on `C:\` drive
The `C:\` drive is a red line. Do not delete, overwrite, or remove any file from `C:\` under any circumstances.

### 2. ALWAYS validate before pushing
```powershell
node D:\KeepTheFlow\validate-lessons.js
```
Must exit with code 0. If failures are detected, fix them before deploying.

### 3. ALWAYS push to GitHub after changes
Vercel auto-deploys from the `main` branch. Changes only go live after pushing.

### 4. PROTECTED ZONE in `keeptheflow_notifier.py`
Lines 33-47 contain the `SB_HEADERS` block surrounded by `PROTECTED ZONE` markers. **NEVER insert, edit, or paste anything inside or near this block.** It contains the Supabase authentication header. Corruption here crashes ALL email notifications.

### 5. After editing `keeptheflow_notifier.py`, verify syntax
```powershell
python -m py_compile D:\lighknight\automation\keeptheflow_notifier.py
```
If no error prints, the edit is safe. If `SyntaxError` — revert immediately.

### 6. Quiz order is FIXED
Never add random shuffling to quiz questions. The order must be universal and deterministic. Students and admin must see the same question at the same number.

### 7. All generated files go on `D:\`
Never save generated files to `C:\`. Use `D:\` for all outputs.

### 8. File names: use spaces, not underscores
Generated file names should use normal spaces (e.g., `My Lesson Name.html`), not underscores.

### 9. Sequential TTS only
If using Chatterbox TTS for audio generation, NEVER run two TTS processes simultaneously. Always process one at a time.

### 10. Git checkpoints before major changes
Always create a commit checkpoint before making significant modifications.

---

## ✅ Feature List

All features confirmed live on the platform:

| # | Feature | Status |
|:---|:---|:---|
| 1 | 9 Tajweed lessons with Quranic instances | ✅ Live |
| 2 | Student recording homework (per-instance audio recording) | ✅ Live |
| 3 | Admin grading system (perfect/good/retry + audio feedback) | ✅ Live |
| 4 | Admin copy-link buttons (share direct link to any instance) | ✅ Live |
| 5 | Admin hide/show instances | ✅ Live |
| 6 | Student login (name + email, localStorage) | ✅ Live |
| 7 | Dynamic student list (auto-registers from recordings) | ✅ Live |
| 8 | QuizMe system (create, edit, delete, copy, assign quizzes) | ✅ Live |
| 9 | Quiz text parser (paste questions → auto-parse MCQs) | ✅ Live |
| 10 | Fixed universal quiz order (no shuffling) | ✅ Live |
| 11 | Admin super-bar (prev/next/jump/reveal/end/edit) | ✅ Live |
| 12 | Quiz completion ceremony (Salat al-Fatih audio + prayer text) | ✅ Live |
| 13 | Quiz progress persistence | ✅ Live |
| 14 | Report button (🚩) on every lesson instance | ✅ Live |
| 15 | Report button (🚩) on every quiz question | ✅ Live |
| 16 | Report → Supabase → Email to admin with direct link | ✅ Live |
| 17 | Email Trigger 1: New student → Admin | ✅ Live |
| 18 | Email Trigger 2: New recording → Admin (with deep links) | ✅ Live |
| 19 | Email Trigger 3: Admin feedback → Student (color-coded) | ✅ Live |
| 20 | Email Trigger 4: Quiz assigned → Student | ✅ Live |
| 21 | Email Trigger 5: Quiz completed → Admin (with score) | ✅ Live |
| 22 | Email Trigger 6: Student report → Admin (with direct link) | ✅ Live |
| 23 | Learn section (Azkar of the Adhan) with audio + dark mode | ✅ Live |
| 24 | Admin lesson dashboard (edit, delete, hide, reorder, add) | ✅ Live |
| 25 | Admin Learn section management (full CRUD) | ✅ Live |
| 26 | In-lesson admin editor (edit/add/delete/reorder/duplicate cards) | ✅ Live |
| 27 | Bidi text support (dir=auto for mixed Arabic/English) | ✅ Live |
| 28 | Lesson integrity validator + pre-push hook | ✅ Live |
| 29 | Dashboard back-button on every lesson | ✅ Live |
| 30 | Portal with animated particles, gold/navy branding | ✅ Live |

---

## 📜 Git Checkpoint History

### KeepTheFlow Repo (`D:\KeepTheFlow`)

```
58f9b00 fix(quiz): enforce fixed universal order for all quizzes, remove random shuffling and shuffle button
33888d5 feat(quiz): Admin Super-Bar navigation, non-destructive shuffling, and precise question-targeted reporting
5110e78 feat: inject report modal and button to quiz player for all current and future quizzes
3a7d202 Fix report button URL logic to prevent 404s
3a4eea2 feat: cleanly inject report button in bottom-left corner of all lesson instances
7e06a8e fix: stop ceremony audio when leaving page, switching tabs, closing browser, or clicking back button
f5cbbe8 fix(quiz): wrap feedback texts in dir=auto for comprehensive bidi isolation
976be28 fix(quiz): bi-directional text layout issues when mixing Arabic and English
4b4a331 fix: all admin save functions failing silently - missing audio_url NOT NULL constraint
8d12394 docs(validator): add VALIDATORS.md for GitBrain project memory
090f7c1 fix: remove duplicate logo banner and duplicate CSS in extended-humming lesson
aa9dc1c chore: add lesson integrity validator + pre-push hook
043ef0f fix: add missing 364 admin copy-link buttons to extended-humming lesson
33e5147 Add new lesson: idgham-yw-7-12
aa80768 fix: quiz parser - handle bold format, dash options, prevent false answer key match
6348e40 feat: quiz completion ceremony - Salat al-Fatih audio (looped), prayer text, grade colors/particles
1a5ae15 feat: in-lesson admin editor - edit/add/delete/reorder/duplicate cards, edit title, undo, export
f28def9 feat: full admin-managed Learn section with all controls
3e49f3f feat: enhanced admin controls - duplicate, preview, share link, NEW badge, export/import
7876c9b fix: replace raditu audio with correct recording
1c9c392 fix: correct riwayah order
97d60c6 fix: light default, text correction, subtle audio, collapsible Learn menu, responsive tooltips
c6035bd feat: Learn section + Azkar of the Adhan lesson
b0895d1 feat: admin lesson dashboard - edit, delete, hide, reorder, add lessons
899c6c1 Add new lesson: tripled-extended-vowels
a5583b5 Update lesson to 3-12 syllables (15 instances)
f1711bd Add new lesson: madd-lazim-7-12
65ae33c feat: sort admin student list by activity
d4364c7 feat: dynamic student list - admin panel loads students from DB
469b19a fix: simplify username-taken rejection message
```

---

## 🔗 Key URLs

| URL | Purpose |
|:---|:---|
| `https://keep-the-flow.vercel.app/` | Student portal (login, lesson cards) |
| `https://keep-the-flow.vercel.app/lessons/{slug}/` | Individual lesson (add `?admin=true` for admin mode) |
| `https://keep-the-flow.vercel.app/qm/` | QuizMe dashboard |
| `https://keep-the-flow.vercel.app/qm/quiz.html?quizId={id}&student={name}` | Specific quiz |
| `https://keep-the-flow.vercel.app/learn/azkar-adhan/` | Azkar of the Adhan lesson |
| `https://github.com/faris11zsc/KeepTheFlow` | Main GitHub repo |
| `https://github.com/faris11zsc/automate-schedule` | Automation GitHub repo |

---

*Last updated: October 14, 2026*
*Manual version: 1.0*
