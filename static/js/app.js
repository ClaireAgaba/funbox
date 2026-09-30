document.addEventListener('DOMContentLoaded', () => {
    initAmbientBackground();
    initAudioSynth();
    initPanelNavigation();
    initQuiz();
    initHeartStudio();
    initProposal();
    initVouchers();
});

/* ==========================================================================
   0. Session ID Management
   ========================================================================== */
function getSessionId() {
    let sid = localStorage.getItem('padel_vibe_session_id');
    if (!sid) {
        sid = 'user_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
        localStorage.setItem('padel_vibe_session_id', sid);
    }
    return sid;
}

/* ==========================================================================
   1. Panel Stepper Navigation
   ========================================================================== */
function initPanelNavigation() {
    const stepButtons = document.querySelectorAll('.step-btn');
    stepButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const step = parseInt(btn.getAttribute('data-step'), 10);
            goToPanel(step);
        });
    });
}

window.goToPanel = function(stepNumber) {
    const panels = document.querySelectorAll('.panel');
    const stepButtons = document.querySelectorAll('.step-btn');

    panels.forEach(p => p.classList.remove('active'));
    stepButtons.forEach(b => b.classList.remove('active'));

    const targetPanel = document.getElementById(`panel-${stepNumber}`);
    const targetBtn = document.querySelector(`.step-btn[data-step="${stepNumber}"]`);

    if (targetPanel) {
        targetPanel.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    if (targetBtn) {
        targetBtn.classList.add('active');
    }
};

/* ==========================================================================
   2. Ambient Canvas: Floating Hearts, Sunsets & Padel Balls
   ========================================================================== */
function initAmbientBackground() {
    const canvas = document.getElementById('ambient-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const PARTICLE_COUNT = 24;

    class FloatingItem {
        constructor() {
            this.reset(true);
        }
        reset(randomY = false) {
            this.x = Math.random() * width;
            this.y = randomY ? Math.random() * height : height + 30;
            this.size = 12 + Math.random() * 16;
            this.speedY = 0.4 + Math.random() * 0.8;
            this.speedX = (Math.random() - 0.5) * 0.6;
            this.type = Math.random() > 0.6 ? 'heart' : (Math.random() > 0.4 ? 'padel' : 'sunset');
            this.opacity = 0.15 + Math.random() * 0.35;
            this.rotation = Math.random() * Math.PI * 2;
            this.rotationSpeed = (Math.random() - 0.5) * 0.02;
        }
        update() {
            this.y -= this.speedY;
            this.x += this.speedX;
            this.rotation += this.rotationSpeed;
            if (this.y < -40) this.reset();
        }
        draw() {
            ctx.save();
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation);
            ctx.globalAlpha = this.opacity;

            if (this.type === 'heart') {
                ctx.fillStyle = '#ff3366';
                ctx.shadowColor = '#ff2a6d';
                ctx.shadowBlur = 10;
                const s = this.size * 0.6;
                ctx.beginPath();
                ctx.moveTo(0, s * 0.3);
                ctx.bezierCurveTo(-s, -s * 0.5, -s * 0.9, s * 0.5, 0, s);
                ctx.bezierCurveTo(s * 0.9, s * 0.5, s, -s * 0.5, 0, s * 0.3);
                ctx.fill();
            } else if (this.type === 'padel') {
                ctx.fillStyle = '#ccff00';
                ctx.shadowColor = '#ccff00';
                ctx.shadowBlur = 12;
                ctx.beginPath();
                ctx.arc(0, 0, this.size * 0.45, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#111';
                ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.arc(-this.size * 0.15, 0, this.size * 0.35, -Math.PI * 0.4, Math.PI * 0.4);
                ctx.stroke();
            } else {
                ctx.fillStyle = '#ffaa00';
                ctx.shadowColor = '#ff7700';
                ctx.shadowBlur = 15;
                ctx.beginPath();
                ctx.arc(0, 0, this.size * 0.35, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.restore();
        }
    }

    for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push(new FloatingItem());
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        requestAnimationFrame(animate);
    }
    animate();
}

/* ==========================================================================
   3. Web Audio API: Romantic Sunset Ambient Synth Chords
   ========================================================================== */
function initAudioSynth() {
    const audioBtn = document.getElementById('audio-toggle');
    const audioLabel = document.getElementById('audio-label');
    const audioIcon = document.getElementById('audio-icon');
    if (!audioBtn) return;

    let audioCtx = null;
    let isPlaying = false;
    let timerId = null;

    const chords = [
        [261.63, 329.63, 392.00, 493.88], // Cmaj7
        [220.00, 261.63, 329.63, 392.00], // Am7
        [174.61, 261.63, 329.63, 349.23], // Fmaj7
        [196.00, 261.63, 293.66, 392.00]  // G7sus4
    ];
    let chordIdx = 0;

    function playChord() {
        if (!isPlaying || !audioCtx) return;
        const currentChord = chords[chordIdx];
        chordIdx = (chordIdx + 1) % chords.length;

        const now = audioCtx.currentTime;
        currentChord.forEach(freq => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now);

            gain.gain.setValueAtTime(0, now);
            gain.gain.linearRampToValueAtTime(0.045, now + 1.2);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + 4.8);

            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.start(now);
            osc.stop(now + 5.0);
        });

        timerId = setTimeout(playChord, 3800);
    }

    audioBtn.addEventListener('click', () => {
        if (!isPlaying) {
            if (!audioCtx) {
                const AudioContextClass = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AudioContextClass();
            }
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            isPlaying = true;
            audioLabel.textContent = 'Music: Playing 💖';
            audioIcon.textContent = '🔊';
            audioBtn.style.borderColor = 'var(--accent-pink)';
            playChord();
        } else {
            isPlaying = false;
            if (timerId) clearTimeout(timerId);
            audioLabel.textContent = 'Sunset Vibe';
            audioIcon.textContent = '🎵';
            audioBtn.style.borderColor = 'rgba(255, 42, 109, 0.35)';
        }
    });
}

/* ==========================================================================
   4. Panel 2: The Quiz
   ========================================================================== */
function initQuiz() {
    const quizContainer = document.getElementById('quiz-container');
    const progressFill = document.getElementById('quiz-progress-fill');
    const stepIndicator = document.getElementById('quiz-step-indicator');
    const resultCard = document.getElementById('quiz-result-card');

    let questions = [];
    let currentIdx = 0;
    const userAnswers = {};

    fetch('/api/quiz')
        .then(res => res.json())
        .then(data => {
            questions = data.questions;
            renderQuestion(0);
        })
        .catch(() => {
            questions = [
                {
                    id: 1,
                    question: "We talk about padel literally all the time. Since your level is way higher than mine, when we finally play, what's the actual plan?",
                    options: [
                        { id: "a", text: "You go easy on me, but I celebrate every single point like I won a trophy 🏆", comment: "If I score even one point against you, I'm never letting you forget it 😂" }
                    ]
                }
            ];
            renderQuestion(0);
        });

    function renderQuestion(idx) {
        if (!questions.length) return;
        currentIdx = idx;
        const q = questions[idx];

        const pct = Math.round(((idx + 1) / questions.length) * 100);
        if (progressFill) progressFill.style.width = `${pct}%`;
        if (stepIndicator) stepIndicator.textContent = `Question ${idx + 1} of ${questions.length}`;

        quizContainer.innerHTML = `
            <div class="question-box">
                <h3 class="question-text">${q.question}</h3>
                <div class="options-list">
                    ${q.options.map(opt => `
                        <button class="option-btn" data-id="${opt.id}" data-text="${encodeURIComponent(opt.text)}" data-comment="${encodeURIComponent(opt.comment)}">
                            <span>${opt.text}</span>
                        </button>
                    `).join('')}
                </div>
                <div id="option-feedback-slot"></div>
                <button id="next-q-btn" class="cta-button quiz-next-btn hidden">
                    <span>${idx === questions.length - 1 ? 'See Our Compatibility ✨' : 'Next Question →'}</span>
                </button>
            </div>
        `;

        const optionButtons = quizContainer.querySelectorAll('.option-btn');
        const feedbackSlot = quizContainer.querySelector('#option-feedback-slot');
        const nextBtn = quizContainer.querySelector('#next-q-btn');

        optionButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                optionButtons.forEach(b => b.classList.remove('selected'));
                btn.classList.add('selected');
                const comment = decodeURIComponent(btn.getAttribute('data-comment'));
                const optText = decodeURIComponent(btn.getAttribute('data-text'));
                const optId = btn.getAttribute('data-id');
                userAnswers[q.id] = optId;

                feedbackSlot.innerHTML = `<div class="option-comment">💡 ${comment}</div>`;
                nextBtn.classList.remove('hidden');

                // Save answer to server in background so Claire can see it!
                fetch('/api/save-answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionId: getSessionId(),
                        questionId: q.id,
                        questionText: q.question,
                        optionId: optId,
                        optionText: optText
                    })
                }).catch(() => {});

                if (window.confetti) {
                    confetti({
                        particleCount: 15,
                        spread: 40,
                        origin: { y: 0.7 }
                    });
                }
            });
        });

        nextBtn.addEventListener('click', () => {
            if (currentIdx + 1 < questions.length) {
                renderQuestion(currentIdx + 1);
            } else {
                finishQuiz();
            }
        });
    }

    function finishQuiz() {
        quizContainer.classList.add('hidden');
        resultCard.classList.remove('hidden');

        if (window.confetti) {
            confetti({
                particleCount: 80,
                spread: 70,
                origin: { y: 0.6 }
            });
        }
    }
}

/* ==========================================================================
   5. Panel 3: Interactive Heart Studio
   ========================================================================== */
function initHeartStudio() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');
            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(target)?.classList.add('active');
        });
    });

    // Parametric Heart
    const heartCanvas = document.getElementById('parametric-heart-canvas');
    if (heartCanvas) {
        const hCtx = heartCanvas.getContext('2d');
        const hWidth = heartCanvas.width = 340;
        const hHeight = heartCanvas.height = 340;
        let heartScale = 8.5;
        let targetScale = 8.5;
        let pulseAngle = 0;
        let tapCount = 0;
        const tapCountEl = document.getElementById('tap-count');
        const complimentBox = document.getElementById('compliment-text');

        let compliments = [
            "You're genuinely so smart and I love your takeaways from our conversations 🧠✨",
            "How much you love nature and being outdoors 🌿🌅",
            "Even though your padel level is way higher than mine, you're so down to earth about it 🎾",
            "How effortless and easy our conversations always feel 😊",
            "Looking forward to that road trip, good music, and catching the sunset with you 🚗🌄",
            "You have the best perspective on things and I really admire that 💫",
            "I still think I could score a couple points against you on court though 😉",
            "Getting to know you has been such a sweet highlight lately 💖"
        ];
        let compIdx = 0;

        fetch('/api/compliments')
            .then(res => res.json())
            .then(data => { if (data.compliments?.length) compliments = data.compliments; })
            .catch(() => {});

        function drawHeart() {
            hCtx.clearRect(0, 0, hWidth, hHeight);

            heartScale += (targetScale - heartScale) * 0.12;
            pulseAngle += 0.05;
            const naturalBeat = Math.sin(pulseAngle) * 0.4;
            const currentScale = heartScale + naturalBeat;

            hCtx.save();
            hCtx.translate(hWidth / 2, hHeight / 2 - 15);

            hCtx.beginPath();
            for (let t = 0; t <= Math.PI * 2; t += 0.02) {
                const x = 16 * Math.pow(Math.sin(t), 3);
                const y = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t));
                if (t === 0) hCtx.moveTo(x * currentScale, y * currentScale);
                else hCtx.lineTo(x * currentScale, y * currentScale);
            }
            hCtx.closePath();

            const grad = hCtx.createRadialGradient(0, 0, 10, 0, 0, 120);
            grad.addColorStop(0, '#ff6584');
            grad.addColorStop(0.6, '#ff2a6d');
            grad.addColorStop(1, '#8b0032');
            hCtx.fillStyle = grad;
            hCtx.shadowColor = '#ff2a6d';
            hCtx.shadowBlur = 24;
            hCtx.fill();

            hCtx.strokeStyle = '#ffffff';
            hCtx.lineWidth = 2.5;
            hCtx.shadowBlur = 10;
            hCtx.shadowColor = '#ffffff';
            hCtx.stroke();

            // Inner Padel Ball Emblem
            hCtx.fillStyle = '#ccff00';
            hCtx.shadowColor = '#ccff00';
            hCtx.shadowBlur = 12;
            hCtx.beginPath();
            hCtx.arc(0, 10, 14, 0, Math.PI * 2);
            hCtx.fill();

            hCtx.fillStyle = '#090614';
            hCtx.font = 'bold 12px Outfit, sans-serif';
            hCtx.textAlign = 'center';
            hCtx.textBaseline = 'middle';
            hCtx.fillText('🎾', 0, 11);

            hCtx.restore();
            requestAnimationFrame(drawHeart);
        }
        drawHeart();

        heartCanvas.addEventListener('click', () => {
            targetScale = 11.2;
            setTimeout(() => { targetScale = 8.5; }, 180);

            tapCount++;
            if (tapCountEl) tapCountEl.textContent = tapCount;

            compIdx = (compIdx + 1) % compliments.length;
            if (complimentBox) {
                complimentBox.textContent = `"${compliments[compIdx]}"`;
            }

            // Sync taps count in background
            fetch('/api/save-taps', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sessionId: getSessionId(),
                    tapCount: tapCount
                })
            }).catch(() => {});

            if (window.confetti) {
                const rect = heartCanvas.getBoundingClientRect();
                const originX = (rect.left + rect.width / 2) / window.innerWidth;
                const originY = (rect.top + rect.height / 2) / window.innerHeight;
                confetti({
                    particleCount: 20,
                    spread: 55,
                    startVelocity: 25,
                    colors: ['#ff2a6d', '#ff6584', '#ffaa00', '#ffffff'],
                    origin: { x: originX, y: originY }
                });
            }
        });
    }

    // Draw Canvas
    const drawCanvas = document.getElementById('drawing-canvas');
    if (drawCanvas) {
        const dCtx = drawCanvas.getContext('2d');
        const clearBtn = document.getElementById('clear-draw-btn');
        const rateBtn = document.getElementById('rate-draw-btn');
        const feedbackCard = document.getElementById('draw-feedback-card');
        const feedbackText = document.getElementById('draw-feedback-text');
        const scoreBadge = document.getElementById('draw-score-badge');

        let isDrawing = false;
        let drawnPoints = [];

        function getPos(e) {
            const rect = drawCanvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return {
                x: (clientX - rect.left) * (drawCanvas.width / rect.width),
                y: (clientY - rect.top) * (drawCanvas.height / rect.height)
            };
        }

        function startDrawing(e) {
            e.preventDefault();
            isDrawing = true;
            const pos = getPos(e);
            dCtx.beginPath();
            dCtx.moveTo(pos.x, pos.y);
            drawnPoints.push(pos);
        }

        function draw(e) {
            if (!isDrawing) return;
            e.preventDefault();
            const pos = getPos(e);
            drawnPoints.push(pos);

            dCtx.lineWidth = 6;
            dCtx.lineCap = 'round';
            dCtx.lineJoin = 'round';
            dCtx.strokeStyle = '#ff2a6d';
            dCtx.shadowColor = '#ff6584';
            dCtx.shadowBlur = 15;

            dCtx.lineTo(pos.x, pos.y);
            dCtx.stroke();
        }

        function stopDrawing(e) {
            if (!isDrawing) return;
            e.preventDefault();
            isDrawing = false;
            dCtx.closePath();
        }

        drawCanvas.addEventListener('mousedown', startDrawing);
        drawCanvas.addEventListener('mousemove', draw);
        window.addEventListener('mouseup', stopDrawing);

        drawCanvas.addEventListener('touchstart', startDrawing, { passive: false });
        drawCanvas.addEventListener('touchmove', draw, { passive: false });
        window.addEventListener('touchend', stopDrawing);

        clearBtn?.addEventListener('click', () => {
            dCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
            drawnPoints = [];
            feedbackCard?.classList.add('hidden');
        });

        rateBtn?.addEventListener('click', () => {
            if (drawnPoints.length < 15) {
                alert("Draw a heart first! Don't leave it blank 😊");
                return;
            }

            feedbackCard?.classList.remove('hidden');
            scoreBadge.textContent = 'Symmetry: 99.9% 💖';
            feedbackText.textContent = '"Heart analyzed! Assessment: 100% genuine and undeniably cute."';

            // Save his drawn heart image to server for Claire!
            const imgData = drawCanvas.toDataURL('image/png');
            fetch('/api/save-heart', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sessionId: getSessionId(),
                    imageData: imgData
                })
            }).catch(() => {});

            if (window.confetti) {
                confetti({
                    particleCount: 50,
                    spread: 70,
                    origin: { y: 0.6 }
                });
            }
        });
    }
}

/* ==========================================================================
   6. Panel 4: The Proposal (Runaway NO)
   ========================================================================== */
function initProposal() {
    const noBtn = document.getElementById('no-btn');
    const yesBtn = document.getElementById('yes-btn');
    const celebrationCard = document.getElementById('celebration-card');
    const buttonsArea = document.getElementById('proposal-buttons-area');

    if (!noBtn || !yesBtn) return;

    const wittyExcuses = [
        "Nope, not an option! 😂",
        "Road trip is mandatory 🚗",
        "Padel match is pending 🎾",
        "You can't escape this sunset 🌅",
        "Try the other button 😉",
        "Error: 'No' does not exist!",
        "Are you sure? Try again!",
        "Nice try, champ!"
    ];
    let excuseIdx = 0;

    function dodge() {
        const maxOffset = 110;
        const randomX = (Math.random() - 0.5) * maxOffset * 2;
        const randomY = (Math.random() - 0.5) * 50;

        noBtn.style.transform = `translate(${randomX}px, ${randomY}px) scale(0.9)`;
        noBtn.innerText = wittyExcuses[excuseIdx % wittyExcuses.length];
        excuseIdx++;
    }

    noBtn.addEventListener('mouseenter', dodge);
    noBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        dodge();
    });

    yesBtn.addEventListener('click', () => {
        celebrationCard?.classList.remove('hidden');
        celebrationCard?.scrollIntoView({ behavior: 'smooth' });

        // Save YES acceptance to server!
        fetch('/api/save-proposal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                sessionId: getSessionId()
            })
        }).catch(() => {});

        const duration = 2.5 * 1000;
        const end = Date.now() + duration;

        (function frame() {
            confetti({
                particleCount: 4,
                angle: 60,
                spread: 55,
                origin: { x: 0 }
            });
            confetti({
                particleCount: 4,
                angle: 120,
                spread: 55,
                origin: { x: 1 }
            });

            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        }());
    });
}

/* ==========================================================================
   7. Panel 5: Vouchers
   ========================================================================== */
function initVouchers() {
    const vouchersGrid = document.getElementById('vouchers-grid');
    if (!vouchersGrid) return;

    fetch('/api/coupons')
        .then(res => res.json())
        .then(data => renderCoupons(data.coupons))
        .catch(() => renderCoupons([]));

    function renderCoupons(coupons) {
        vouchersGrid.innerHTML = coupons.map(c => `
            <div class="voucher-card" data-id="${c.id}" data-title="${encodeURIComponent(c.title)}">
                <div>
                    <div class="voucher-header">
                        <span class="voucher-icon">${c.icon}</span>
                        <span class="voucher-badge">${c.badge}</span>
                    </div>
                    <h4 class="voucher-title">${c.title}</h4>
                    <p class="voucher-desc">${c.desc}</p>
                </div>
                <div class="voucher-action">Click to Claim 🎟️</div>
            </div>
        `).join('');

        const cards = vouchersGrid.querySelectorAll('.voucher-card');
        cards.forEach(card => {
            card.addEventListener('click', () => {
                if (card.classList.contains('redeemed')) return;
                card.classList.add('redeemed');
                const action = card.querySelector('.voucher-action');
                if (action) action.textContent = 'Claimed! 💖';

                const vId = card.getAttribute('data-id');
                const vTitle = decodeURIComponent(card.getAttribute('data-title'));

                // Save claimed voucher to server!
                fetch('/api/save-voucher', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionId: getSessionId(),
                        voucherId: vId,
                        voucherTitle: vTitle
                    })
                }).catch(() => {});

                if (window.confetti) {
                    confetti({
                        particleCount: 25,
                        spread: 50,
                        origin: { y: 0.7 }
                    });
                }
            });
        });
    }
}
