import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    return jsonify({"questions": QUIZ_QUESTIONS})

@app.route('/api/quiz-grade', methods=['POST'])
def grade_quiz():
    return jsonify({
        "score": 100,
        "title": "100% Vibe Match ✨",
        "verdict": "Okay yeah, our chemistry is undeniably great. The road trip, sunset watching, and padel game are officially happening.",
        "badge": "Approved by ACL"
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
