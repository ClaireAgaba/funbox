import os
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "First up: When we play padel together, what is our actual court strategy?",
        "options": [
            {"id": "a", "text": "High-IQ tactical wall play & calculated smashes 🧠", "comment": "Okay, look at us being Wimbledon contenders!"},
            {"id": "b", "text": "Laughing hysterically whenever the ball rebounds off the glass in the wrong direction 😂", "comment": "100% accurate. The glass is definitely our sworn enemy."},
            {"id": "c", "text": "You carry the team while I look cute and celebrate our points 💅", "comment": "A flawless division of labor, honestly."},
            {"id": "d", "text": "Pretending we totally understand how the scoring system works 🎾", "comment": "'Is it 30-40 or are we just making up numbers?'"}
        ]
    },
    {
        "id": 2,
        "question": "A high-speed smash is rocketing straight towards the middle. What's your move?",
        "options": [
            {"id": "a", "text": "Heroically jump across the court to save the point 💪", "comment": "Main character energy! I respect it."},
            {"id": "b", "text": "Yell 'MINE!' with absolute confidence and completely whiff the air 💨", "comment": "The dedication was there, and that's what counts."},
            {"id": "c", "text": "We both look at each other, watch the ball bounce, and blame the sun ☀️", "comment": "It's always the sun. Or the wind. Never us."},
            {"id": "d", "text": "Use the padel racket as a defensive shield and pray 🛡️", "comment": "Safety first, tournament trophy second."}
        ]
    },
    {
        "id": 3,
        "question": "Post-match protocol: What are the terms of peace after a tough set?",
        "options": [
            {"id": "a", "text": "Loser buys iced smoothies or matcha lattes immediately 🥤", "comment": "The only acceptable post-game hydration."},
            {"id": "b", "text": "Immediate dinner date to discuss key tactical blunders over food 🍕", "comment": "Post-game breakdown with good food is undefeated."},
            {"id": "c", "text": "A rematch next week because nobody accepts defeat 😤", "comment": "Challenge accepted. Bring your best serve!"},
            {"id": "d", "text": "All of the above (Non-negotiable contract) ✨", "comment": "Bingo. You passed the real test."}
        ]
    },
    {
        "id": 4,
        "question": "Honest vibe check: Since we're getting to know each other, how is it going?",
        "options": [
            {"id": "a", "text": "10/10 court chemistry & even better conversation 🌟", "comment": "Agreed! Couldn't have asked for a better partner."},
            {"id": "b", "text": "Suspiciously fun... definitely need another round soon 👀", "comment": "Consider your schedule booked!"},
            {"id": "c", "text": "I'm already secretly practicing my smashes to impress you 🎾", "comment": "Haha, don't worry, you already do!"},
            {"id": "d", "text": "Off the charts! When's our next hangout? 🚀", "comment": "Right after you finish this app!"}
        ]
    }
]

LOVE_COMPLIMENTS = [
    "You have the best smile on and off the court ✨",
    "Even when your shots hit the fence, you make it look cool 🎾",
    "Getting to know you has been my favorite part of the week 😊",
    "Your energy is contagious in the best way possible 💫",
    "I'd choose you as my padel doubles partner any day of the week 🏆",
    "You're effortlessly funny and ridiculously charming 💖",
    "Every conversation with you feels like no time has passed at all ⏳",
    "Secretly looking forward to our next match (and whatever comes after) 🥂"
]

COUPONS = [
    {
        "id": "c1",
        "icon": "🥤",
        "title": "Post-Padel Smoothie / Drink",
        "desc": "Redeemable for your favorite iced beverage, paid for by me after our next session.",
        "badge": "Valid Anytime"
    },
    {
        "id": "c2",
        "icon": "🎾",
        "title": "Ball Boy / Ball Girl Pass",
        "desc": "I will retrieve 100% of the wild balls that bounce over the fence without complaining.",
        "badge": "Special Court Perk"
    },
    {
        "id": "c3",
        "icon": "🍽️",
        "title": "Dinner Date of Your Choice",
        "desc": "You pick the spot, you pick the cuisine, zero objections permitted.",
        "badge": "VIP Date Pass"
    },
    {
        "id": "c4",
        "icon": "💆‍♂️",
        "title": "Post-Match Shoulder Reset",
        "desc": "10-minute shoulder / hand massage to recover from carrying our team.",
        "badge": "Recovery Mode"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    return jsonify({"questions": QUIZ_QUESTIONS})

@app.route('/api/quiz-grade', methods=['POST'])
def grade_quiz():
    data = request.get_json() or {}
    answers = data.get("answers", {})
    # No matter what, it's 100% chemistry!
    return jsonify({
        "score": 100,
        "title": "Championship Chemistry: A++ 🏆",
        "verdict": "Diagnostics complete: You two possess an illegal amount of court synergy and banter. The league has never seen a duo this promising.",
        "badge": "Certified Grand Slam Partner"
    })

@app.route('/api/compliments', methods=['GET'])
def get_compliments():
    return jsonify({"compliments": LOVE_COMPLIMENTS})

@app.route('/api/coupons', methods=['GET'])
def get_coupons():
    return jsonify({"coupons": COUPONS})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
