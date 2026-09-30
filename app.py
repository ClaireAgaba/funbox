import os
import random
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Considering you are literally Level 4+ (highest in the country 🙄) and I'm... well, vibing at my own level... what happens when we play?",
        "options": [
            {"id": "a", "text": "You go easy on me like a gentleman, but I still celebrate every single point like I won Wimbledon 🏆", "comment": "A point won against a Level 4+ counts as an international championship in my book!"},
            {"id": "b", "text": "I boldly guarantee I will beat you 6-0 through sheer willpower and questionable line calls 💅", "comment": "Confidence is 90% of the game. Watch out!"},
            {"id": "c", "text": "You do all the running and smashes while I look aesthetic and provide moral support on court 🎾", "comment": "Honest division of labor. Aesthetics matter."},
            {"id": "d", "text": "We play a friendly match once in a while, but loser admits the other is cooler. (Spoiler: It's me) 😎", "comment": "Rankings don't measure coolness, let's be real."}
        ]
    },
    {
        "id": 2,
        "question": "We're packing the car for a spontaneous road trip with no set destination. What is your designated duty?",
        "options": [
            {"id": "a", "text": "Driver & playlist curator (subject to my strict aux cord inspection 🎶)", "comment": "Every great road trip lives and dies by the playlist."},
            {"id": "b", "text": "Chief Snack Officer & Navigator (even when we take scenic 'wrong' turns) 🍫", "comment": "Getting lost with good snacks is the best part of the trip."},
            {"id": "c", "text": "Making me laugh the entire drive until my cheeks hurt 😂", "comment": "Best passenger entertainment service guaranteed."},
            {"id": "d", "text": "All of the above, plus pulling over whenever I spot a breathtaking view 📸", "comment": "10/10 road trip co-pilot etiquette."}
        ]
    },
    {
        "id": 3,
        "question": "Post-game or weekend evening: How are we handling sunset watching?",
        "options": [
            {"id": "a", "text": "Chilled drinks, favorite songs, watching golden hour with zero rush 🌅🍹", "comment": "The ultimate decompression after a hectic week."},
            {"id": "b", "text": "Deep conversations and laughing about missed padel shots 💬", "comment": "Debriefing our match highlights (and lowlights) over sunset is top tier."},
            {"id": "c", "text": "Finding a secret rooftop or hilltop spot with the prettiest view 🌄", "comment": "I'm scouting the locations as we speak."},
            {"id": "d", "text": "Analyzing if a Level 4+ vibora could technically smash into the setting sun 🚀", "comment": "Don't tempt yourself, keep the balls in the court!"}
        ]
    },
    {
        "id": 4,
        "question": "Final challenge: Are you brave enough to step on court for a casual game, knowing I plan to win regardless of your ranking?",
        "options": [
            {"id": "a", "text": "Challenge accepted! I'll prepare to be humbled by your unpredicted tactics 🫡", "comment": "That's the spirit! Prepare for chaos."},
            {"id": "b", "text": "Only if we catch a scenic sunset and grab dinner right after 🌅🍽️", "comment": "Deal! That was always part of the master plan."},
            {"id": "c", "text": "I wouldn't miss a game with you for anything 🌟", "comment": "Smooth answer... you definitely earned points for that one."},
            {"id": "d", "text": "Yes, but winner gets bragging rights until our next road trip 🚗💨", "comment": "High stakes! Game on!"}
        ]
    }
]

LOVE_COMPLIMENTS = [
    "Ranked Level 4+ on the court, but ranked #1 in charm in my book ✨",
    "I might not have your backhand, but I definitely have your attention 😉",
    "Getting to know you has been my absolute favorite plot twist this month 💫",
    "Ready for scenic sunsets, spontaneous road trips, and beating you at padel (somehow) 🌅",
    "You make every conversation feel effortlessly fun and easy 😊",
    "Even as the country's top player, you're surprisingly humble and sweet 🎾",
    "Your laugh is contagious in the best way possible 💖",
    "Secretly counting down to our next match, sunset drive, and dinner 🥂"
]

COUPONS = [
    {
        "id": "c1",
        "icon": "🌅",
        "title": "Golden Hour Sunset Pass",
        "desc": "Redeemable for an evening drive to catch the sunset, complete with iced drinks and zero rush.",
        "badge": "VIP Sunset Perk"
    },
    {
        "id": "c2",
        "icon": "🚗",
        "title": "Spontaneous Road Trip Co-Pilot",
        "desc": "One day-trip getaway. You pick the direction, I supply snacks, good vibes, and car karaoke.",
        "badge": "Adventure Mode"
    },
    {
        "id": "c3",
        "icon": "🎾",
        "title": "The Underdog Padel Match",
        "desc": "A casual friendly game where you promise not to unleash 100% tournament power (and I still try to win).",
        "badge": "Friendly Rematch"
    },
    {
        "id": "c4",
        "icon": "🍦",
        "title": "Post-Match Winner's Treat",
        "desc": "Loser buys ice cream, smoothies, or dinner. (Since you're Level 4+, the odds are high you're treating me 😉).",
        "badge": "Sweet Victory"
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
    return jsonify({
        "score": 100,
        "title": "Unbeatable Synergy: 100% Match! 🏆",
        "verdict": "Diagnostics complete: Even with the Level 4+ vs. Challenger gap, your chemistry across road trips, sunsets, and court banter is off the charts. The federation officially approves this duo.",
        "badge": "Certified MVP & Adventure Partner"
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
