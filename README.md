# 🎾 Padel & Chemistry Check 💘
### An Interactive Romantic Web Experience Built in Python (Flask)

Designed for a fun, playful "getting-to-know-each-other" vibe with padel banter, interactive heart art, a runaway proposal button, and redeemable vouchers!

---

## 🌟 Interactive Features Included

1. **Ambient Romantic Theme & Padel Aesthetic:**
   - Midnight violet velvet glassmorphism with neon blush pink & padel lime accents.
   - Interactive ambient canvas with floating glowing hearts and neon padel balls.
   - Built-in **Romantic Lofi Ambient Synth** (Web Audio API) with 1-click play/pause.

2. **Act 1: The Partner Vibe Exam (Quiz):**
   - 4 witty, flirtatious padel & dating questions with instant funny feedback on every choice.
   - Grand celebration at the end with confetti and a **"Certified Grand Slam Partner"** compatibility trophy (100% Chemistry guaranteed).

3. **Act 2: The Heart Studio:**
   - **The Beating Cardioid Heart:** A mathematical heart drawn via parametric curves. Clicking/tapping "pumps" the heart, triggering particle waves and unlocking sweet getting-to-know-you compliments and jokes.
   - **Draw Me a Heart Canvas:** Touch & mouse canvas with neon glowing strokes where he can draw his own heart. Features a "Rate My Heart" button with hilarious, affectionate ratings.

4. **Act 3: The Runaway "NO" Button:**
   - "Will you officially be my padel partner & go on our next date together?"
   - A glowing **YES** button and an evasive **NO** button that dodges his finger/cursor across the screen while giving funny padel excuses (*"Net violation!"*, *"Ball out of bounds!"*, *"Racket slipped?"*).
   - Clicking YES unlocks a full-screen confetti explosion and an **Official Licensed Padel Partner Certificate**.

5. **Act 4: VIP Court Vouchers:**
   - Interactive scratch/click coupons (Post-game smoothie, Ball retriever pass, Dinner date choice, Post-match massage).

6. **Act 5: Sweet Note:**
   - A warm, cute message celebrating the new connection.

---

## 🚀 How to Run Locally

```bash
# In this directory:
source .venv/bin/activate
python app.py
```
Open your browser at `http://127.0.0.1:5001`!

---

## 🌐 How to Deploy for Free & Get a Shareable Link

You can deploy this in 2-3 minutes using any of these free hosting services:

### Option 1: Render.com (Recommended - 100% Free & Simplest)
1. Push this folder to a GitHub repository (e.g., `padel-vibe-check`).
2. Go to [Render.com](https://render.com) and click **New > Web Service**.
3. Connect your GitHub repository.
4. Render will automatically detect Python:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Create Web Service**.
6. Within 2 minutes, Render gives you a public link (e.g. `https://padel-vibe.onrender.com`) that you can text him!

### Option 2: Vercel
1. Install Vercel CLI or import the repo on [vercel.com](https://vercel.com).
2. The included `vercel.json` already has the serverless Python configuration ready.
3. Deploy and get an instant `.vercel.app` link.

---

## 🎨 How to Customize
- **Questions & Answers:** Edit `QUIZ_QUESTIONS` in `app.py`.
- **Compliments:** Edit `LOVE_COMPLIMENTS` in `app.py`.
- **Coupons:** Edit `COUPONS` in `app.py`.
- **Note:** Edit the text in `templates/index.html` under Section 5.
