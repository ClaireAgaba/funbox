import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'app_data.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP,
                last_active TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS quiz_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                question_id INTEGER,
                question_text TEXT,
                option_id TEXT,
                option_text TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS heart_drawings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                image_data TEXT,
                created_at TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS heart_taps (
                session_id TEXT PRIMARY KEY,
                tap_count INTEGER,
                updated_at TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS proposals (
                session_id TEXT PRIMARY KEY,
                accepted INTEGER,
                accepted_at TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS vouchers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                voucher_id TEXT,
                voucher_title TEXT,
                claimed_at TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "We talk about padel literally all the time. Since your level is way higher than mine, when we finally play, what's the actual plan?",
        "options": [
            {"id": "a", "text": "You go easy on me like a gentleman, but I still celebrate every single point like I won a trophy 🏆", "comment": "If I win even one point against your level, I'm never letting you forget it 😂"},
            {"id": "b", "text": "I somehow manage to win through pure luck and sheer determination 💅", "comment": "Underestimate me at your own risk!"},
            {"id": "c", "text": "You do all the smashes and running, and I just look good on court 🎾", "comment": "Fair division of labor honestly."},
            {"id": "d", "text": "We just have fun, and loser buys the post-game food/drinks 🥤", "comment": "Best plan. Winner gets bragging rights too."}
        ]
    },
    {
        "id": 2,
        "question": "You're a big nature person and we've talked about sunsets. What's our ideal golden hour setup?",
        "options": [
            {"id": "a", "text": "A quiet scenic spot outdoors, chilled drinks, just talking with no rush 🌅", "comment": "Literally nothing beats this vibe."},
            {"id": "b", "text": "A drive to somewhere with a great view and good music playing 🚗🎶", "comment": "Golden hour drives hit different."},
            {"id": "c", "text": "Sitting somewhere quiet in nature and watching the sky change colors 🌄", "comment": "Peaceful and easy, exactly how it should be."},
            {"id": "d", "text": "All of the above, obviously ✨", "comment": "The only right answer."}
        ]
    },
    {
        "id": 3,
        "question": "Whenever we talk, you always have the best takeaways and insights. What happens on a long road trip drive?",
        "options": [
            {"id": "a", "text": "Deep conversations that make a 3-hour drive feel like 20 minutes 💭", "comment": "Our conversations always flow so easily."},
            {"id": "b", "text": "You dropping your smart takeaways while I handle car snacks and DJ duties 🎶", "comment": "A match made in heaven."},
            {"id": "c", "text": "Taking random turns just to see where the road takes us 🛣️", "comment": "Spontaneous adventures are always the best memories."},
            {"id": "d", "text": "Laughing so much our cheeks hurt before we even get there 😂", "comment": "Guaranteed 100% of the time."}
        ]
    },
    {
        "id": 4,
        "question": "Honest question: when are we actually doing this road trip and catching that sunset?",
        "options": [
            {"id": "a", "text": "As soon as we pick a weekend (after our padel match) 🎾🌅", "comment": "Deal! It's officially on the calendar."},
            {"id": "b", "text": "Whenever you're free, I'm already in 🚗💨", "comment": "Love the enthusiasm!"},
            {"id": "c", "text": "I'm already putting together the road trip playlist 🎵", "comment": "It better have some good ones on it!"},
            {"id": "d", "text": "Right after I finish this app 😉", "comment": "That's what I like to hear."}
        ]
    }
]

LOVE_COMPLIMENTS = [
    "You're genuinely so smart and I love your takeaways from our conversations 🧠✨",
    "How much you love nature and being outdoors 🌿🌅",
    "Even though your padel level is way higher than mine, you're so down to earth about it 🎾",
    "How effortless and easy our conversations always feel 😊",
    "Looking forward to that road trip, good music, and catching the sunset with you 🚗🌄",
    "You have the best perspective on things and I really admire that 💫",
    "I still think I could score a couple points against you on court though 😉",
    "Getting to know you has been such a sweet highlight lately 💖"
]

COUPONS = [
    {
        "id": "c1",
        "icon": "🌅",
        "title": "Sunset Drive Pass",
        "desc": "An evening drive to a quiet scenic spot to watch golden hour, my treat.",
        "badge": "Nature & Chill"
    },
    {
        "id": "c2",
        "icon": "🚗",
        "title": "Road Trip Co-Pilot",
        "desc": "One spontaneous road trip. Good music, car snacks, and scenic stops.",
        "badge": "Adventure Pass"
    },
    {
        "id": "c3",
        "icon": "🎾",
        "title": "Casual Padel Match",
        "desc": "One friendly game where you promise to take it easy (and I still try to beat you).",
        "badge": "Court Challenge"
    },
    {
        "id": "c4",
        "icon": "🍕",
        "title": "Post-Game Dinner & Drinks",
        "desc": "Good food and catching up after our match, no debate on the spot.",
        "badge": "Foodie Perk"
    }
]

def touch_session(conn, session_id):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('''
        INSERT INTO sessions (session_id, created_at, last_active)
        VALUES (?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET last_active = ?
    ''', (session_id, now, now, now))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    return jsonify({"questions": QUIZ_QUESTIONS})

@app.route('/api/compliments', methods=['GET'])
def get_compliments():
    return jsonify({"compliments": LOVE_COMPLIMENTS})

@app.route('/api/coupons', methods=['GET'])
def get_coupons():
    return jsonify({"coupons": COUPONS})

# --- Activity Saving Endpoints ---

@app.route('/api/save-answer', methods=['POST'])
def save_answer():
    data = request.get_json() or {}
    session_id = data.get('sessionId', 'guest')
    q_id = data.get('questionId')
    q_text = data.get('questionText', '')
    opt_id = data.get('optionId')
    opt_text = data.get('optionText', '')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        touch_session(conn, session_id)
        # Update or insert answer for this question
        conn.execute('''
            DELETE FROM quiz_answers WHERE session_id = ? AND question_id = ?
        ''', (session_id, q_id))
        conn.execute('''
            INSERT INTO quiz_answers (session_id, question_id, question_text, option_id, option_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, q_id, q_text, opt_id, opt_text, now))
        conn.commit()

    return jsonify({"status": "saved"})

@app.route('/api/save-heart', methods=['POST'])
def save_heart():
    data = request.get_json() or {}
    session_id = data.get('sessionId', 'guest')
    image_data = data.get('imageData', '')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if image_data:
        with get_db() as conn:
            touch_session(conn, session_id)
            conn.execute('''
                INSERT INTO heart_drawings (session_id, image_data, created_at)
                VALUES (?, ?, ?)
            ''', (session_id, image_data, now))
            conn.commit()

    return jsonify({"status": "heart_saved"})

@app.route('/api/save-taps', methods=['POST'])
def save_taps():
    data = request.get_json() or {}
    session_id = data.get('sessionId', 'guest')
    tap_count = int(data.get('tapCount', 0))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        touch_session(conn, session_id)
        conn.execute('''
            INSERT INTO heart_taps (session_id, tap_count, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET tap_count = ?, updated_at = ?
        ''', (session_id, tap_count, now, tap_count, now))
        conn.commit()

    return jsonify({"status": "taps_saved"})

@app.route('/api/save-proposal', methods=['POST'])
def save_proposal():
    data = request.get_json() or {}
    session_id = data.get('sessionId', 'guest')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        touch_session(conn, session_id)
        conn.execute('''
            INSERT INTO proposals (session_id, accepted, accepted_at)
            VALUES (?, 1, ?)
            ON CONFLICT(session_id) DO UPDATE SET accepted = 1, accepted_at = ?
        ''', (session_id, now, now))
        conn.commit()

    return jsonify({"status": "accepted"})

@app.route('/api/save-voucher', methods=['POST'])
def save_voucher():
    data = request.get_json() or {}
    session_id = data.get('sessionId', 'guest')
    v_id = data.get('voucherId')
    v_title = data.get('voucherTitle', '')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        touch_session(conn, session_id)
        # Avoid duplicate claims in db
        existing = conn.execute('''
            SELECT id FROM vouchers WHERE session_id = ? AND voucher_id = ?
        ''', (session_id, v_id)).fetchone()
        if not existing:
            conn.execute('''
                INSERT INTO vouchers (session_id, voucher_id, voucher_title, claimed_at)
                VALUES (?, ?, ?, ?)
            ''', (session_id, v_id, v_title, now))
            conn.commit()

    return jsonify({"status": "voucher_saved"})

# --- Private Results Dashboard for Claire ---

@app.route('/results')
@app.route('/dashboard')
def results():
    with get_db() as conn:
        sessions = conn.execute('''
            SELECT session_id, created_at, last_active FROM sessions ORDER BY last_active DESC
        ''').fetchall()

        all_results = []
        for s in sessions:
            sid = s['session_id']
            answers = conn.execute('''
                SELECT question_id, question_text, option_text, created_at 
                FROM quiz_answers 
                WHERE session_id = ? 
                ORDER BY question_id ASC
            ''', (sid,)).fetchall()

            drawings = conn.execute('''
                SELECT image_data, created_at 
                FROM heart_drawings 
                WHERE session_id = ? 
                ORDER BY id DESC LIMIT 5
            ''', (sid,)).fetchall()

            taps = conn.execute('''
                SELECT tap_count, updated_at FROM heart_taps WHERE session_id = ?
            ''', (sid,)).fetchone()

            proposal = conn.execute('''
                SELECT accepted, accepted_at FROM proposals WHERE session_id = ?
            ''', (sid,)).fetchone()

            vouchers = conn.execute('''
                SELECT voucher_id, voucher_title, claimed_at FROM vouchers WHERE session_id = ?
            ''', (sid,)).fetchall()

            all_results.append({
                "session_id": sid,
                "created_at": s['created_at'],
                "last_active": s['last_active'],
                "answers": [dict(a) for a in answers],
                "drawings": [dict(d) for d in drawings],
                "tap_count": taps['tap_count'] if taps else 0,
                "accepted_proposal": bool(proposal and proposal['accepted']),
                "accepted_at": proposal['accepted_at'] if proposal else None,
                "vouchers": [dict(v) for v in vouchers]
            })

    return render_template('results.html', results=all_results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
