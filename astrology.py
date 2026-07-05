from datetime import datetime
from typing import Optional, Dict, List, Any
import pytz
import math

def sin_deg(degrees):
    return math.sin(math.radians(degrees))

def cos_deg(degrees):
    return math.cos(math.radians(degrees))

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANETS = [
    "Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn",
    "Uranus", "Neptune", "Pluto", "North Node", "Chiron"
]

ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
}

QUALITIES = {
    "Aries": "Cardinal", "Cancer": "Cardinal", "Libra": "Cardinal", "Capricorn": "Cardinal",
    "Taurus": "Fixed", "Leo": "Fixed", "Scorpio": "Fixed", "Aquarius": "Fixed",
    "Gemini": "Mutable", "Virgo": "Mutable", "Sagittarius": "Mutable", "Pisces": "Mutable"
}

PLANET_RULERS = {
    "Sun": "Leo", "Moon": "Cancer", "Mercury": ["Gemini", "Virgo"],
    "Venus": ["Taurus", "Libra"], "Mars": ["Aries", "Scorpio"],
    "Jupiter": ["Sagittarius", "Pisces"], "Saturn": ["Capricorn", "Aquarius"],
    "Uranus": "Aquarius", "Neptune": "Pisces", "Pluto": "Scorpio"
}

def get_zodiac_sign(degree: float) -> str:
    index = int(degree // 30) % 12
    return ZODIAC_SIGNS[index]

def get_sign_degree(degree: float) -> tuple:
    sign_index = int(degree // 30) % 12
    sign_degree = degree % 30
    return ZODIAC_SIGNS[sign_index], int(sign_degree), int((sign_degree % 1) * 60)

def calculate_aspects(planets1: Dict[str, float], planets2: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
    aspects = []
    orb = 8 if planets2 else 6
    
    target_planets = planets2 if planets2 else planets1
    
    for p1, deg1 in planets1.items():
        for p2, deg2 in target_planets.items():
            if p1 == p2:
                continue
            
            diff = abs(deg1 - deg2)
            if diff > 180:
                diff = 360 - diff
            
            aspect_types = [
                (0, "Conjunction", 0),
                (60, "Sextile", 6),
                (90, "Square", 8),
                (120, "Trine", 8),
                (180, "Opposition", 8)
            ]
            
            for asp_deg, asp_name, asp_orb in aspect_types:
                if abs(diff - asp_deg) <= orb:
                    aspects.append({
                        "planet1": p1,
                        "planet2": p2,
                        "aspect": asp_name,
                        "degree": round(diff, 2),
                        "angle": asp_deg
                    })
                    break
    
    return aspects

def calculate_compatibility(chart1: Dict, chart2: Dict) -> Dict[str, Any]:
    score = 0
    max_score = 100
    
    sun1 = chart1.get("Sun", {}).get("degree", 0)
    sun2 = chart2.get("Sun", {}).get("degree", 0)
    
    sun_diff = abs(sun1 - sun2)
    if sun_diff > 180:
        sun_diff = 360 - sun_diff
    
    if sun_diff <= 30:
        score += 25
    elif sun_diff <= 60:
        score += 15
    elif sun_diff <= 90:
        score += 5
    
    moon1 = chart1.get("Moon", {}).get("degree", 0)
    moon2 = chart2.get("Moon", {}).get("degree", 0)
    
    moon_diff = abs(moon1 - moon2)
    if moon_diff > 180:
        moon_diff = 360 - moon_diff
    
    if moon_diff <= 30:
        score += 25
    elif moon_diff <= 60:
        score += 15
    elif moon_diff <= 90:
        score += 5
    
    aspects = calculate_aspects(
        {k: v["degree"] for k, v in chart1.items()},
        {k: v["degree"] for k, v in chart2.items()}
    )
    
    trine_count = sum(1 for a in aspects if a["aspect"] == "Trine")
    conjunction_count = sum(1 for a in aspects if a["aspect"] == "Conjunction")
    square_count = sum(1 for a in aspects if a["aspect"] == "Square")
    
    score += min(trine_count * 5, 20)
    score += min(conjunction_count * 3, 15)
    score -= min(square_count * 2, 10)
    
    sign1 = get_zodiac_sign(sun1)
    sign2 = get_zodiac_sign(sun2)
    
    if ELEMENTS.get(sign1) == ELEMENTS.get(sign2):
        score += 10
    
    if QUALITIES.get(sign1) == QUALITIES.get(sign2):
        score += 5
    
    score = max(0, min(score, 100))
    
    descriptions = {
        (0, 30): "Challenging - requires work but can grow together",
        (30, 50): "Moderate - some natural harmony with areas to develop",
        (50, 70): "Good - solid foundation for a lasting connection",
        (70, 100): "Excellent - strong natural compatibility"
    }
    
    description = "Challenging connection"
    for (low, high), desc in descriptions.items():
        if low <= score < high:
            description = desc
            break
    
    return {
        "score": score,
        "description": description,
        "sun_aspect": "Compatible" if sun_diff <= 90 else "Challenging",
        "moon_aspect": "Compatible" if moon_diff <= 90 else "Challenging",
        "element_match": ELEMENTS.get(sign1) == ELEMENTS.get(sign2),
        "aspect_summary": {
            "trines": trine_count,
            "conjunctions": conjunction_count,
            "squares": square_count
        }
    }

def generate_daily_horoscope(sign: str, date: datetime) -> Dict[str, Any]:
    import hashlib
    
    sign = sign.capitalize()
    if sign not in ZODIAC_SIGNS:
        sign = "Aries"
    
    sign_list = list(ZODIAC_SIGNS)
    fixed_index = sign_list.index(sign)
    
    day_of_year = date.timetuple().tm_yday
    index = (fixed_index + day_of_year) % 5
    
    horoscopes = {
        "Aries": [
            "Mars, your ruling planet, ignites your ambition today, making this an ideal moment to take decisive action on career goals that have been simmering in the background. In love, your directness is refreshing and attractive, but remember to listen as much as you speak to avoid overwhelming your partner. Your energy levels are high, so channel this fire into physical exercise or outdoor activities to maintain balance. The universe encourages you to lead boldly while staying mindful of those who look to you for guidance.",
            "The Sun's position activates your self-expression sector, bringing a surge of charisma that draws people toward you in both social and professional settings. A romantic spark could ignite unexpectedly — keep your heart open to new possibilities. Health-wise, watch for tension in the shoulders and neck, as your driven nature may cause you to carry stress there. Your mantra today is to channel your warrior spirit constructively, and you will move mountains.",
            "Your natural pioneering spirit is amplified today, making it an excellent time to launch that project or idea you've been refining. Partnerships require a gentle touch now — not everyone moves at your speed, so practice patience with loved ones. Physically, you feel unstoppable, but be careful not to overextend yourself in the pursuit of accomplishment. Trust that the universe rewards those who initiate with courage and heart.",
            "A creative wave sweeps through your chart today, unlocking ideas you didn't know you possessed. Share your vision with a trusted confidant, as collaboration will elevate your concept to something far greater. Your passion for life is contagious, and romance benefits greatly from this exuberance — plan something adventurous for the evening. Just remember to ground yourself with deep breaths and adequate rest, as your mind may race faster than your body can sustain.",
            "Adventure calls from every direction as Jupiter aspects your sign, urging you to expand beyond your usual routines. In love, novelty is the spice that keeps the flame alive — surprise your partner with an unexpected gesture. Career-wise, your boldness positions you as a natural leader, and higher-ups are taking note of your initiative. Health is about moderation today; channel your boundless enthusiasm without burning out by pacing yourself wisely."
        ],
        "Taurus": [
            "Venus, your gracious ruler, aligns beautifully with Saturn today, bringing a sense of stability and purpose to your financial and career pursuits that feels deeply rewarding. In love, your loyalty is your greatest asset — a quiet but profound connection deepens with someone who truly values your steadfast heart. Your health thrives when you slow down and savor life's simple pleasures; a walk in nature or a nourishing meal will restore your spirit. Remember that patience is your superpower, and the seeds you plant now will yield abundant harvests later.",
            "The Moon moves through your sign, heightening your emotional sensitivity and attuning you to the subtle energies around you. This is a powerful time to nurture your closest relationships with the warmth and care that comes so naturally to you. Financially, your practical instincts are razor-sharp — trust your gut before making any significant purchases or investments. Your body needs grounding today, so prioritize rest, good food, and the comfort of your home sanctuary.",
            "A steady rhythm guides your day as Mercury brings clarity to your communication, making it easier to express your needs in both love and work. Career-wise, the foundation you have been carefully building is finally showing signs of solid growth — keep trusting the process. Your health benefits from consistency rather than intensity, so stick to routines that nourish rather than drain you. The cosmos reminds you that the tortoise wins the race, and your deliberate pace is your greatest advantage.",
            "Beauty surrounds you today as Venus casts a gentle glow over your world, inviting you to indulge in life's finer pleasures without guilt. In romance, your sensuality is heightened, and your partner or potential love interest will feel deeply drawn to your grounded, magnetic presence. Professionally, your reputation for reliability opens doors that others cannot access — step through with confidence. Pay attention to your throat and neck area, as this is your sensitive spot; stay hydrated and speak your truth gently.",
            "Financial opportunities present themselves in unexpected ways, but your cautious nature serves you well in discerning which paths are truly worth pursuing. Relationships thrive when you allow yourself to be vulnerable rather than always playing the role of the rock. Your energy levels are stable but could benefit from a change of scenery — take your work to a cafe or walk while you think. The message from the stars is clear: you are building something lasting, and every careful step matters."
        ],
        "Gemini": [
            "Mercury sharpens your wit today, making you the most captivating conversationalist in any room and opening doors through the power of your words. In love, your playful charm is irresistible, but be mindful not to deflect serious topics with humor when your partner needs depth. Your career benefits from your adaptability — juggling multiple tasks comes naturally, but focus on finishing what you start. Health-wise, your restless mind needs stimulation; puzzles, learning, or lively debate will keep you energized and balanced.",
            "Your social calendar heats up as Venus graces your communication sector, drawing interesting people into your orbit who share your intellectual passions. A romantic connection could deepen through a meaningful exchange of ideas — don't underestimate the power of a thoughtful conversation. Professionally, your ability to see multiple perspectives makes you invaluable in negotiations and collaborative projects. Just remember to give your nervous system a break; your mind can race ahead of your body, so schedule time to simply breathe and be still.",
            "Curiosity becomes your compass today, guiding you toward knowledge that will serve you well in unexpected ways. Love flourishes when you share what you're learning with your partner, inviting them into your world of discovery. Career-wise, a networking opportunity arises that could shift your trajectory — say yes to the invitation, even if it feels outside your comfort zone. Your health is tied to your mental state; if you feel scattered, try single-tasking and watch your focus and calm return.",
            "The Twins' dual nature serves you well today as you effortlessly navigate between work obligations and personal desires with grace. In relationships, you are especially attuned to your partner's unspoken needs, and your words of affirmation carry extraordinary weight. A creative project at work demands your unique touch — your ability to connect disparate ideas is precisely what is needed. Energy-wise, you are buzzing, but beware of spreading yourself too thin; quality over quantity applies to both your social life and your workload.",
            "New ideas flood your mind as the Moon highlights your house of self-expression, making this a perfect day to write, create, or share your vision with the world. Romance takes on an adventurous tone — planning a spontaneous outing or trying a new activity together will reignite the spark. Your professional network expands in exciting ways, and someone you meet today could become a valuable ally. Health tip: your hands and lungs are your sensitive areas, so take breaks from typing and practice deep breathing regularly."
        ],
        "Cancer": [
            "The Moon, your celestial ruler, sits powerfully in your sign today, amplifying your intuition to almost psychic levels and allowing you to sense what others need before they speak. In love, your nurturing nature is your greatest gift — create a safe space for your partner to be vulnerable, and you will receive the same tenderness in return. Career-wise, trust the gut feeling that has been nudging you toward a particular decision; your emotional intelligence is your professional superpower. Your health requires you to honor your need for security — comfort foods in moderation, warm baths, and time with family will replenish your spirit.",
            "Home and family take center stage as the stars emphasize your foundational sector, urging you to address any lingering domestic matters with compassion. A loved one needs your support today, and your ability to listen without judgment makes all the difference. Professionally, you may feel torn between ambition and your desire for comfort, but the cosmos suggests that integrating both is possible with creative scheduling. Physically, your digestive system is sensitive to stress, so practice mindful eating and create a calm environment around meals.",
            "Your emotional depth becomes your anchor as you navigate a day filled with subtle but powerful shifts in your relationships. A conversation with a partner or close friend reveals hidden truths that ultimately bring you closer together. At work, your memory and attention to detail impress those in authority, potentially opening a door for advancement. Your health benefits from water — drink plenty, take a swim, or simply sit near a fountain to let the element that rules you restore your equilibrium.",
            "Past memories may surface today as transits activate your sector of reflection, but rather than getting lost in nostalgia, use these insights to heal old wounds. In love, your capacity for forgiveness is remarkable, and letting go of a past grievance will lighten your heart considerably. Career-wise, a creative solution to a persistent problem arrives when you stop forcing it and instead trust your intuition. Your energy is best spent in quiet, meaningful activities rather than large social gatherings — honor your need for cocoon time.",
            "Venus moves through your sign, wrapping you in a blanket of warmth and making you especially magnetic to those who appreciate your gentle, caring nature. Romance blossoms when you allow yourself to be pampered rather than always being the caretaker. Your career benefits from your ability to read the room — you know exactly when to push and when to pause. Health-wise, your immune system is strong today, but your emotions need an outlet; journaling or talking with a trusted friend will keep your heart light and your spirit clear."
        ],
        "Leo": [
            "The Sun, your majestic ruler, beams its full power onto your sign today, filling you with an irresistible radiance that draws opportunities and admirers alike. In love, your warmth and generosity are magnetic — lavish your partner with affection, and you will receive devotion in return. Career-wise, the spotlight finds you whether you seek it or not, so step up and own your expertise with the confidence of a true leader. Your health is vibrant as long as you remember that even the Sun sets; rest is not weakness but the source of your sustainable brilliance.",
            "Your creative fire burns brighter than ever as Mars aspects your house of self-expression, making this a spectacular day for artistic pursuits or bold professional moves. Romance is highlighted with passion and drama — surprise your love with a grand gesture that reflects your big-hearted nature. Your career benefits from your natural showmanship; a presentation or pitch today will captivate your audience. Just be mindful of your heart — both emotionally and physically — as your intensity can sometimes overwhelm your system if you don't balance it with calm moments.",
            "Leadership comes naturally to you today as Jupiter casts a favorable aspect on your sign, inspiring others to follow your vision with enthusiasm. In relationships, your partner looks to you for direction and reassurance — offer both generously, and your bond will strengthen immeasurably. At work, your ability to delegate and inspire rather than micromanage sets you apart as a true manager. Your vitality is high, but your ego may be sensitive to criticism; remember that feedback is fuel for growth, not an attack on your character.",
            "A touch of romance colors your entire day as Venus dances through your sector of love and pleasure, making everything feel more beautiful and hopeful. Your magnetic presence attracts admirers easily, but it is the depth of your attention that will create lasting connections. Professionally, your charisma opens doors that logic alone could not — use your charm wisely and for the greater good. Health is about moderation today; your tendency to overindulge in life's pleasures needs a gentle counterbalance of discipline to keep you shining at your best.",
            "Generosity flows through you today as the stars align to remind you that what you give returns to you multiplied. In love, your partner feels deeply cherished by your thoughtful gestures and undivided attention. Career-wise, a colleague or subordinate needs your mentorship — your guidance today could change the trajectory of their professional life. Your physical energy is robust, but your heart center needs attention; practice heart-opening yoga poses or simply place a hand on your chest and breathe deeply to stay aligned."
        ],
        "Virgo": [
            "Mercury grants you exceptional analytical clarity today, making this the perfect moment to tackle complex problems that have been lingering on your desk. In love, your tendency to overanalyze may create distance — try to feel rather than think your way through emotional conversations. Your health routines are your sanctuary, and small adjustments to your diet or exercise regimen will yield noticeable improvements. The universe reminds you that perfection is a direction, not a destination; celebrate how far you have come rather than fixating on what remains undone.",
            "Your service-oriented nature shines as the Moon highlights your house of work and wellness, inspiring you to help others with quiet dedication. In relationships, actions speak louder than words — a practical gesture of support will mean more to your partner than any grand declaration. Career-wise, your reputation for reliability precedes you, and someone in authority is taking note of your consistent excellence. Your body is your temple today, so nourish it with whole foods, movement, and the rest you so often deny yourself in service of productivity.",
            "Details are your domain today, and your keen eye catches something others have missed that could save the day at work. Love requires a softer touch — not everything needs to be fixed or improved; sometimes being present is enough. Your financial instincts are sharp, making this a good day to review budgets, investments, or long-term spending plans. Health-wise, your digestive system is particularly sensitive; eat simply, chew thoroughly, and pay attention to how different foods make you feel.",
            "A sense of order and purpose guides your steps as Saturn lends you its disciplined energy for the day's challenges. In romance, your loyalty is your strongest asset — your partner knows they can count on you, and that security is more valuable than grand romantic gestures. Professionally, your methodical approach impresses those who value quality over speed. Your mind may be prone to worry today, so counter anxious thoughts with factual evidence and remind yourself of past successes to calm your inner critic.",
            "Practical wisdom flows through you as Venus aligns with your earthy nature, bringing a sense of contentment with life's simple pleasures. Love deepens through shared routines and quiet companionship rather than dramatic declarations. Your career benefits from your ability to organize chaos into systems that serve everyone. Health tip: your nervous system needs grounding — spend time in nature, put your bare feet on the earth, and let the natural world remind you of the beauty in imperfection and growth."
        ],
        "Libra": [
            "Venus, your elegant ruler, bestows upon you a day of harmony and balance, making you the peacemaker in every situation you encounter. In love, your natural charm is at its peak, and your ability to see both sides of an argument helps resolve a lingering tension with grace. Career-wise, collaboration is your path to success — a partnership or team effort will yield far better results than going solo. Your health requires balance above all; if you have been working too hard, indulge in beauty and rest, and if you have been idle, find purposeful movement to restore equilibrium.",
            "Relationships take center stage as the Moon highlights your partnership sector, bringing important conversations about commitment and mutual needs to the surface. Your diplomatic skills are called upon at work, where your ability to find common ground between opposing views makes you invaluable. In matters of the heart, your desire for peace may lead you to avoid necessary conflict, but honest communication now prevents bigger problems later. Your energy is best spent in beautiful environments — surround yourself with art, music, or nature to keep your spirit elevated.",
            "Aesthetic and creative impulses surge through you today, making it an ideal time to beautify your surroundings or express yourself through art, fashion, or design. In romance, romance itself is the theme — candlelit dinners, thoughtful notes, and meaningful gestures will deepen your connection. Career-wise, your sense of fairness and justice makes you an excellent negotiator or mediator today. Your lower back and kidneys are your sensitive areas; stay hydrated, stretch regularly, and avoid prolonged sitting to maintain your physical harmony.",
            "Social connections flourish as Jupiter graces your house of friendships, bringing delightful encounters with both old friends and new acquaintances. Love benefits from your generous spirit — your willingness to give your partner space and freedom actually brings them closer to you. At work, your ability to create consensus is your superpower, and a team project benefits greatly from your inclusive approach. Your health is good, but your tendency to avoid conflict may cause internal stress; speak your truth kindly but clearly to maintain inner peace.",
            "Justice and truth are your guiding lights today, and you feel a strong urge to right a wrong or advocate for someone who cannot speak for themselves. In love, your partner admires your integrity, and your commitment to fairness strengthens the foundation of your relationship. Career-wise, a decision you have been weighing becomes clear when you stop analyzing and start feeling. Your energy is balanced, but your mind may race with the needs of others; remember that your own peace must come first before you can truly help anyone else."
        ],
        "Scorpio": [
            "Pluto, your transformative ruler, stirs the depths of your psyche today, urging you to shed old patterns that no longer serve your highest good. In love, your intensity is both intimidating and alluring — let your partner see the vulnerable side you guard so carefully, and trust will deepen immeasurably. Career-wise, your investigative skills are unmatched, making this a powerful day for research, strategy, and uncovering hidden opportunities. Your body carries the weight of unexpressed emotions; consider therapy, journaling, or cathartic movement to release what you have been holding inside.",
            "Your emotional radar is exquisitely sensitive today as the Moon traverses your sign, allowing you to perceive hidden motives and unspoken truths with uncanny accuracy. In relationships, this depth of perception can be a gift or a curse — use it to understand rather than to judge. Professionally, your determination is unstoppable, and a challenge that seems impossible to others is precisely what you need to feel alive. Health-wise, you must be mindful of your immune system; your intensity can manifest as physical inflammation if you do not find healthy outlets for your passion.",
            "Transformation is the theme of the day as powerful planetary aspects push you toward growth whether you feel ready or not. In love, a conversation about boundaries or trust may feel uncomfortable but will ultimately liberate you from old fears. Your career takes a mysterious turn as information comes to light that changes your perspective on a situation. Your health is tied directly to your ability to let go — physically, this means your colon and reproductive system need your attention; emotionally, it means releasing grudges that poison your peace.",
            "Magnetic intensity radiates from you as Mars empowers your sign, making you irresistible to those drawn to power and authenticity. Romance crackles with electricity — single Scorpios may encounter a fated connection, while committed ones experience a renewal of passion. At work, your focus is laser-sharp, and a complex problem yields to your relentless investigation. Your energy levels are formidable, but your capacity for self-destruction through overwork is equally strong; set boundaries that protect your vitality as fiercely as you protect your secrets.",
            "Secrets reveal themselves today as Mercury aspects your house of hidden knowledge, bringing clarity to a situation that has been shrouded in mystery. In love, radical honesty is the path forward — withholding your truth now will only create distance later. Career-wise, your ability to read between the lines gives you a strategic advantage over competitors who only see the surface. Your health requires detoxification on all levels; consider a digital detox, cleanse your environment of clutter, and release relationships that drain rather than nourish you."
        ],
        "Sagittarius": [
            "Jupiter, your expansive ruler, fills you with restless optimism today, urging you to look beyond the horizon and dream bigger than ever before. In love, your freedom-loving nature needs a partner who understands that space is not rejection but a form of trust. Career-wise, this is an excellent moment to pitch bold ideas, apply for opportunities abroad, or enroll in a course that expands your skill set. Your health benefits from outdoor movement — hiking, cycling, or simply walking in the sun will align your body with your adventurous spirit. Remember that wisdom comes not just from seeking but from reflecting on what you find.",
            "A philosophical mood overtakes you as the stars encourage deep contemplation about your life's purpose and direction. In relationships, sharing your beliefs and listening to your partner's worldview with genuine curiosity will create a beautiful bridge between you. At work, your natural optimism attracts opportunities, but make sure to balance vision with practical execution. Your energy is buoyant but scattered; focus your enthusiasm on one meaningful pursuit rather than starting ten things and finishing none.",
            "Wanderlust grips your soul as transits activate your house of travel and expansion, making it hard to sit still when the world is calling. Love feels like an adventure today — try something completely new with your partner, or if single, say yes to someone who challenges your usual type. Career-wise, your ability to see the big picture inspires others and positions you as a visionary in your field. Your health is robust, but your restless energy needs an outlet; channel it into learning a new physical skill or exploring unfamiliar terrain.",
            "Your blunt honesty is your trademark, and today it serves you well in cutting through red tape and getting straight to the heart of a matter. In love, your directness can be refreshing or overwhelming — gauge your partner's readiness before sharing your unfiltered thoughts. Professionally, a mentor or teacher figure appears who offers guidance that could shift your trajectory significantly. Your liver and hips are your sensitive areas; moderating indulgences and stretching regularly will keep your body as free as your spirit.",
            "The quest for truth drives you today as Mercury aligns with your philosophical sector, making you a seeker on a sacred mission. In romance, intellectual connection is the foundation of attraction — engage your partner in a deep conversation about your dreams and values. Career-wise, your ability to synthesize information from diverse sources gives you a unique perspective that sets you apart. Your health is connected to your sense of purpose; when you feel aligned with your higher calling, your body follows suit with vitality and resilience."
        ],
        "Capricorn": [
            "Saturn, your disciplined ruler, rewards your patience today as the seeds you planted months ago begin to show tangible results. In love, your commitment is your greatest offering — your partner feels safe in your steady, reliable embrace. Career-wise, recognition is coming for the hard work you have quietly put in; accept compliments gracefully and consider how this momentum can propel you toward your next ambition. Your health requires attention to your bones and joints — strengthen them through weight-bearing exercise and ensure you are getting enough calcium and vitamin D.",
            "Ambition pulses through your veins as Mars energizes your career sector, making you unstoppable in pursuit of your professional goals. However, in matters of the heart, your drive can come across as cold if you are not careful — pause to show warmth to those who support you behind the scenes. Your health benefits from structure; a consistent routine that includes both work and rest will serve you better than all-or-nothing extremes. The universe reminds you that success is hollow without someone to share it with, so invest in your relationships as diligently as you invest in your career.",
            "Long-term planning is your superpower today as Mercury helps you map out a strategy that could define your next five years. In love, your practicality is appreciated — your partner knows you show love through acts of service and tangible support. Professionally, a senior figure takes notice of your dedication and may offer a mentorship or promotion opportunity. Your health is stable, but your tendency to hold tension in your lower back and knees requires conscious relaxation; stretch, get a massage, or practice progressive muscle relaxation.",
            "Your reputation precedes you as Venus graces your sign, bringing a sense of earned reward and the admiration of your peers. In romance, you are more approachable than usual, and your dry wit and loyalty attract someone who values substance over flash. Career-wise, a financial opportunity related to real estate, investments, or long-term assets should be carefully considered. Your energy is steady but could benefit from small pleasures that remind you that life is not only about achievement — allow yourself guilt-free enjoyment.",
            "Structure meets possibility today as Jupiter aspects your sign, encouraging you to build your legacy while remaining open to unexpected opportunities. In love, your protective nature is comforting, but be careful not to treat your partner like a project to be managed. At work, your leadership style earns respect because you lead by example rather than by decree. Your health is your foundation, and without it, your ambitions crumble; prioritize sleep, nutrition, and stress management as the non-negotiable pillars of your success."
        ],
        "Aquarius": [
            "Uranus, your innovative ruler, sends electric energy through your chart today, sparking ideas that could revolutionize how you approach your work and relationships. In love, your need for independence might be misunderstood, but the right person will appreciate your uniqueness rather than try to cage it. Career-wise, your unconventional thinking is your greatest asset — don't be afraid to propose solutions that break the mold. Your health benefits from variety; monotony drains you, so mix up your routine with new exercises, foods, or mindfulness practices to keep your mind and body engaged.",
            "Your social conscience is activated as the Moon moves through your humanitarian sector, compelling you to get involved in a cause larger than yourself. In relationships, shared ideals and intellectual camaraderie create a powerful bond — find someone who wants to change the world with you. Professionally, a networking event or group collaboration yields surprising connections that align with your long-term vision. Your energy is best channeled into activities that combine mental stimulation with social purpose; your nervous system thrives when your mind is engaged in meaningful exchange.",
            "Originality is your trademark, and today the cosmos celebrates your uniqueness by bringing opportunities that only someone with your perspective could seize. In love, your quirky charm is irresistible — embrace what makes you different rather than trying to fit a conventional mold. Career-wise, technology, science, or social media may play a significant role in your advancement. Your health is connected to your circulation and ankles; stay active, elevate your legs when resting, and pay attention to any tingling or coldness in your extremities.",
            "Your visionary mind is operating at full capacity as Mercury aspects your house of innovation, allowing you to see patterns and possibilities that others miss entirely. A romantic partner may not understand your need for detachment at times — reassure them that your distance is about processing, not rejection. At work, your ability to think ten steps ahead makes you invaluable in strategic planning sessions. Your body needs fresh air and open spaces; being indoors too long stifles your spirit, so find a reason to step outside and look at the sky.",
            "Community and friendship come into focus as Venus highlights your eleventh house, reminding you that your tribe is your treasure. In love, friendship is the foundation of lasting romance — cultivate the friendship before worrying about the fireworks. Career-wise, collaboration with like-minded individuals yields innovations that none of you could have achieved alone. Your health benefits from group activities — join a class, a team, or a club where movement and social connection combine to keep you feeling alive and inspired."
        ],
        "Pisces": [
            "Neptune, your dreamy ruler, blurs the lines between reality and imagination today, gifting you with profound creative inspiration and deep intuitive flashes. In love, your empathic nature allows you to connect with your partner on a soul level, but be careful not to absorb their emotions as your own. Career-wise, your artistic talents are amplified, making this a perfect day for creative projects, music, writing, or any form of artistic expression. Your health requires you to stay grounded; the ethereal energy that fuels your creativity can also leave you feeling unmoored, so practice earthing techniques and maintain healthy boundaries with those who drain your energy.",
            "Compassion flows through you like a river as the Moon highlights your sector of healing and service, drawing you toward opportunities to help those in need. In romance, your gentle understanding creates a safe harbor for your partner's vulnerability, deepening your connection in profound ways. Professionally, your intuition guides you toward a decision that logic alone could not have revealed. Your energy is sensitive to environments, so curate your surroundings with care — soothing colors, soft lighting, and calming music will support your wellbeing.",
            "Spiritual insights arrive in waves today, and you may find yourself feeling unusually connected to the unseen rhythms of the universe. In love, this heightened sensitivity makes you exceptionally attuned to your partner's unspoken needs, allowing for a level of intimacy that words cannot capture. Career-wise, your imagination is your greatest tool — a seemingly impractical idea contains the seed of something revolutionary. Your health needs protection from overstimulation; limit screen time, avoid crowded places, and create quiet moments throughout your day to preserve your delicate equilibrium.",
            "Art and beauty are your sanctuaries today as Venus graces your creative sector, inspiring you to bring something beautiful into the world. Romance takes on a dreamlike quality — poetry, music, and candlelight are your love languages today. At work, your ability to tap into collective emotions and trends makes you a valuable asset in marketing, branding, or any role that requires understanding human desire. Your feet are your sensitive area; reflexology, a warm foot bath, or simply walking barefoot on grass will restore your connection to the earth.",
            "The boundaries between you and the world feel thin today, making you deeply receptive to the emotions and energies of those around you. In love, this empathy is a superpower — you can truly feel what your partner feels, creating an almost telepathic bond. Career-wise, a creative breakthrough arrives when you stop forcing it and allow inspiration to flow through you like a channel. Your health requires extra gentleness; rest, hydration, and time alone to recharge are not luxuries today but necessities for maintaining your delicate balance between the material and spiritual worlds."
        ]
    }
    
    sign_list = list(ZODIAC_SIGNS)
    fixed_index = sign_list.index(sign) if sign in sign_list else 0
    index = (fixed_index + day_of_year) % 5
    prediction = horoscopes.get(sign, horoscopes["Aries"])[index]
    
    seed = fixed_index + day_of_year
    
    confidence_career = 50 + ((fixed_index * 13 + day_of_year * 7) % 46)
    confidence_love = 50 + ((fixed_index * 17 + day_of_year * 11) % 46)
    confidence_health = 50 + ((fixed_index * 19 + day_of_year * 5) % 46)
    confidence_finance = 50 + ((fixed_index * 23 + day_of_year * 3) % 46)
    
    housemap = [
        "first house of self and identity", "second house of values and possessions",
        "third house of communication and community", "fourth house of home and family",
        "fifth house of creativity and romance", "sixth house of work and wellness",
        "seventh house of partnerships", "eighth house of transformation and shared resources",
        "ninth house of philosophy and expansion", "tenth house of career and public image",
        "eleventh house of friendships and aspirations", "twelfth house of spirituality and solitude"
    ]
    ruling_planets = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
        "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
        "Libra": "Venus", "Scorpio": "Pluto", "Sagittarius": "Jupiter",
        "Capricorn": "Saturn", "Aquarius": "Uranus", "Pisces": "Neptune"
    }
    area_labels = ["career", "relationships", "health", "finances", "personal growth"]
    ruling_planet = ruling_planets.get(sign, "the cosmos")
    transit_house = housemap[(fixed_index + day_of_year) % 12]
    area_by_seed = area_labels[(fixed_index + day_of_year) % 5]
    
    reasoning_templates = [
        f"Today's lunar transit through the {transit_house} activates your {area_by_seed}, while {ruling_planet}'s stable influence supports grounded decision-making.",
        f"Mercury's current aspect to your Sun sign enhances communication in matters of {area_by_seed}, making this a powerful time for clarity and connection.",
        f"Venus aligns favorably with your ruling planet {ruling_planet}, bringing harmony to your {area_by_seed} and amplifying your natural charisma.",
        f"The {ruling_planet} energy is strong today as transits activate the {transit_house}, encouraging bold moves in {area_by_seed}.",
        f"Jupiter's expansive influence touches your chart, broadening opportunities in {area_by_seed} and inviting you to grow beyond self-imposed limits."
    ]
    reasoning = reasoning_templates[(fixed_index + day_of_year) % 5]
    
    timing_templates = [
        "Morning hours are most favorable for important decisions and career moves.",
        "Mid-afternoon brings relationship opportunities and creative inspiration.",
        "Evening tranquility supports reflection, planning, and meaningful conversations.",
        "Late morning energy peaks for financial decisions and negotiations.",
        "The hours just after noon are ideal for health routines and personal wellness."
    ]
    best_timing = timing_templates[(fixed_index + day_of_year) % 5]
    
    preparation_templates = [
        "Prepare by setting clear intentions before noon and reviewing your goals tonight.",
        "Start your day with meditation to focus your energy on what truly matters.",
        "Review your goals tonight and plan tomorrow's priorities with a clear mind.",
        "Take five deep breaths before any major decision today to stay grounded.",
        "Write down three things you are grateful for to align yourself with abundance."
    ]
    preparation = preparation_templates[(fixed_index + day_of_year) % 5]
    
    luck_factors = {
        "lucky_number": (fixed_index * 7 + day_of_year) % 99 + 1,
        "lucky_color": ["Red", "Blue", "Green", "Gold", "Purple", "Silver"][(fixed_index + day_of_year) % 6],
        "lucky_day": ["Monday", "Thursday", "Saturday"][day_of_year % 3]
    }
    
    categories = ["Career Advancement and Ambition", "Relationships and Emotional Connection", "Health, Wellness and Vitality", "Financial Growth and Stability", "Personal Growth and Social Expansion"]
    category_index = (fixed_index + day_of_year) % 5
    
    confidence_line = f"Career {confidence_career}%, Love {confidence_love}%, Health {confidence_health}%, Finance {confidence_finance}%"
    enhanced_prediction = f"{prediction}\n\nAstrological summary — Confidence: {confidence_line}. {reasoning} {best_timing} {preparation}"
    
    base_mood = ["Motivated and Driven", "Radiant and Inspired", "Grounded and Serene", "Introspective and Wise", "Imaginative and Playful"][(fixed_index + day_of_year) % 5]
    avg_conf = (confidence_career + confidence_love + confidence_health + confidence_finance) // 4
    if avg_conf >= 80:
        mood_modifier = " with exceptional cosmic alignment"
    elif avg_conf >= 65:
        mood_modifier = " with steady planetary support"
    else:
        mood_modifier = " — take extra care today"
    mood = base_mood + mood_modifier
    
    return {
        "sign": sign,
        "date": date.strftime("%Y-%m-%d"),
        "prediction": enhanced_prediction,
        "mood": mood,
        "lucky_number": luck_factors["lucky_number"],
        "lucky_color": luck_factors["lucky_color"],
        "lucky_day": luck_factors["lucky_day"],
        "focus_area": categories[category_index],
        "confidence_career": confidence_career,
        "confidence_love": confidence_love,
        "confidence_health": confidence_health,
        "confidence_finance": confidence_finance,
        "reasoning": reasoning,
        "best_timing": best_timing,
        "preparation": preparation
    }

def calculate_natal_chart(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict[str, Any]:
    try:
        dt = datetime.fromisoformat(f"{birth_date}T{birth_time}")
    except:
        return {"error": "Invalid date/time format. Use ISO format: YYYY-MM-DD HH:MM"}
    
    try:
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt) if dt.tzinfo is None else dt
    except:
        dt = pytz.utc.localize(dt)
    
    jd = datetime_to_julian_day(dt)
    
    planets = calculate_planet_positions(jd, latitude, longitude)
    
    asc_degree = calculate_ascendant(jd, latitude, longitude)
    mc_degree = calculate_midheaven(jd, longitude)
    
    sun_sign = get_zodiac_sign(planets.get("Sun", 0))
    moon_sign = get_zodiac_sign(planets.get("Moon", 0))
    asc_sign = get_zodiac_sign(asc_degree)
    
    houses = calculate_houses(asc_degree, mc_degree, latitude)
    house_cusps = [(int(h), houses[h]["cusp"]) for h in sorted(houses.keys(), key=int)]
    def get_house(deg):
        deg = deg % 360
        for i in range(12):
            curr_cusp = house_cusps[i][1]
            next_cusp = house_cusps[(i + 1) % 12][1]
            if curr_cusp <= next_cusp:
                if curr_cusp <= deg < next_cusp:
                    return i + 1
            else:
                if deg >= curr_cusp or deg < next_cusp:
                    return i + 1
        return 1

    planets_with_houses = {}
    for k, v in planets.items():
        sign = get_zodiac_sign(v)
        planets_with_houses[k] = {
            "degree": round(v, 2),
            "sign": sign,
            "house": get_house(v)
        }

    chart = {
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "rising_sign": asc_sign,
        "ascendant_degree": round(asc_degree, 2),
        "midheaven_degree": round(mc_degree, 2),
        "planets": planets_with_houses,
        "houses": houses
    }
    
    return chart

def datetime_to_julian_day(dt: datetime) -> float:
    year = dt.year
    month = dt.month
    day = dt.day + dt.hour / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
    
    if month <= 2:
        year -= 1
        month += 12
    
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return jd

def calculate_ascendant(jd: float, latitude: float, longitude: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    L0 = L0 % 360
    
    omega = 125.0445479 - 1934.1362891 * T + 0.0020754 * T * T
    epsilon = 23.439291 - 0.0130042 * T - 0.00000016 * T * T + 0.000000504 * T * T * T
    
    obliquity_correction = epsilon + 0.00256 * math.cos(math.radians(omega))
    obliquity_rad = math.radians(obliquity_correction)
    
    GMST = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T * T * T / 38710000.0
    GMST = GMST % 360
    
    LST = (GMST + longitude) % 360
    LST_rad = math.radians(LST)
    
    tan_A = -math.cos(LST_rad) / (math.sin(LST_rad) * math.sin(obliquity_rad) + math.tan(math.radians(latitude)) * math.cos(obliquity_rad))
    A = math.atan(tan_A)
    
    asc = (math.degrees(A) + 180) % 360
    return asc

def calculate_midheaven(jd: float, longitude: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    L0 = L0 % 360
    
    GMST = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T - T * T * T / 38710000.0
    GMST = (GMST + longitude) % 360
    
    MC = (GMST - L0) % 360
    if MC < 0:
        MC += 360
    
    return MC

def calculate_planet_positions(jd: float, latitude: float, longitude: float) -> Dict[str, float]:
    T = (jd - 2451545.0) / 36525.0
    
    planets = {}
    
    # Sun calculation
    sun_mean_anomaly = 357.52911 + 35999.05029 * T - 0.0001536 * T * T
    sun_mean_longitude = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
    earth_orbit_eccentricity = 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T
    
    sun_equation_of_center = (1.914602 - 0.004817 * T - 0.000014 * T * T) * sin_deg(sun_mean_anomaly) + \
                              (0.019993 - 0.000101 * T) * sin_deg(2 * sun_mean_anomaly) + \
                              0.000289 * sin_deg(3 * sun_mean_anomaly)
    
    sun_true_longitude = (sun_mean_longitude + sun_equation_of_center) % 360
    planets["Sun"] = sun_true_longitude
    
    # Moon calculation (improved with Evection, Variation, Yearly Equation)
    moon_mean_longitude = 218.3164477 + 481267.88123421 * T - 0.0015786 * T * T
    moon_mean_anomaly = 134.9633964 + 477198.8675055 * T + 0.0087414 * T * T
    moon_mean_elongation = (moon_mean_longitude - sun_mean_longitude) % 360  # D = Lm - Ls
    
    moon_longitude = (moon_mean_longitude
        + 6.289 * sin_deg(moon_mean_anomaly)
        + 1.274 * sin_deg(2 * moon_mean_elongation - moon_mean_anomaly)
        + 0.658 * sin_deg(2 * moon_mean_elongation)
        + 0.186 * sin_deg(sun_mean_anomaly))
    planets["Moon"] = moon_longitude % 360
    
    # ===== Heliocentric-to-Geocentric conversion for planets =====
    # Earth heliocentric position (from Sun calculation)
    earth_mean_anomaly = sun_mean_anomaly
    earth_ecc = 0.01671
    earth_C = (2 * earth_ecc) * (180 / math.pi) * sin_deg(earth_mean_anomaly) \
            + 1.25 * earth_ecc**2 * (180 / math.pi) * sin_deg(2 * earth_mean_anomaly)
    earth_true_anomaly = earth_mean_anomaly + earth_C
    # Earth heliocentric true longitude = Sun geocentric longitude + 180 deg
    earth_helio_long = (sun_true_longitude + 180) % 360
    earth_r = 1.00000 * (1 - earth_ecc**2) / (1 + earth_ecc * cos_deg(earth_true_anomaly))
    earth_x = earth_r * cos_deg(earth_helio_long)
    earth_y = earth_r * sin_deg(earth_helio_long)
    
    # Planet data: (mean_longitude_formula, a_in_AU, eccentricity, perihelion_longitude)
    planet_data = [
        ("Mercury", 252.250905 + 149472.67411175 * T + 0.000160 * T * T,
         0.38710, 0.20563, 77.4578 + 0.0444 * T),
        ("Venus", 181.979801 + 58517.8156760 * T + 0.000001 * T * T,
         0.72333, 0.00677, 131.564 + 0.0055 * T),
        ("Mars", 355.433275 + 19140.2993313 * T + 0.000001 * T * T,
         1.52368, 0.09340, 336.060 + 0.444 * T),
        ("Jupiter", 34.351519 + 3034.9061279 * T + 0.000004 * T * T,
         5.20260, 0.04839, 14.331 + 0.023 * T),
        ("Saturn", 50.077444 + 1222.1138488 * T,
         9.55491, 0.05386, 93.057 + 0.018 * T),
        ("Uranus", 314.055 + 428.466 * T,
         19.21845, 0.04570, 173.287 + 0.001 * T),
        ("Neptune", 304.365 + 218.487 * T,
         30.11039, 0.00859, 43.917 + 0.001 * T),
        ("Pluto", 238.957 + 145.0 * T,
         39.543, 0.24881, 224.066),
    ]
    
    for name, L, a_p, e_p, peri_p in planet_data:
        M_p = (L - peri_p) % 360
        C1_p = (2 * e_p - e_p**3 / 4) * (180 / math.pi)
        C2_p = 1.25 * e_p**2 * (180 / math.pi)
        C_p = C1_p * sin_deg(M_p) + C2_p * sin_deg(2 * M_p)
        true_anom_p = M_p + C_p
        true_long_p = (peri_p + true_anom_p) % 360
        r_p = a_p * (1 - e_p**2) / (1 + e_p * cos_deg(true_anom_p))
        p_x = r_p * cos_deg(true_long_p)
        p_y = r_p * sin_deg(true_long_p)
        geo_lon = (math.degrees(math.atan2(p_y - earth_y, p_x - earth_x)) + 360) % 360
        planets[name] = geo_lon
    
    north_node_mean = 125.0445479 - 1934.1362891 * T
    planets["North Node"] = north_node_mean % 360
    
    chiron_mean = 209.0 + 7.0 * T
    planets["Chiron"] = chiron_mean % 360
    
    return planets

def calculate_houses(asc_degree: float, mc_degree: float, latitude: float) -> Dict[str, Dict]:
    house_cusp_1 = asc_degree
    house_cusp_10 = mc_degree
    
    house_cusp_7 = (house_cusp_1 + 180) % 360
    house_cusp_4 = (house_cusp_10 + 180) % 360
    
    diff = (house_cusp_10 - house_cusp_1) % 360
    if diff > 180:
        diff -= 360
    
    house_cusp_11 = (house_cusp_1 + diff * 0.75) % 360
    house_cusp_12 = (house_cusp_1 + diff * 0.5) % 360
    house_cusp_2 = (house_cusp_1 + diff * 0.25) % 360
    house_cusp_3 = (house_cusp_1 + diff * 0.1) % 360
    house_cusp_5 = (house_cusp_10 + diff * 0.1 + 180) % 360
    house_cusp_6 = (house_cusp_10 + diff * 0.25 + 180) % 360
    house_cusp_8 = (house_cusp_10 + diff * 0.5 + 180) % 360
    house_cusp_9 = (house_cusp_10 + diff * 0.75 + 180) % 360
    
    return {
        "1": {"cusp": round(house_cusp_1, 2), "sign": get_zodiac_sign(house_cusp_1)},
        "2": {"cusp": round(house_cusp_2, 2), "sign": get_zodiac_sign(house_cusp_2)},
        "3": {"cusp": round(house_cusp_3, 2), "sign": get_zodiac_sign(house_cusp_3)},
        "4": {"cusp": round(house_cusp_4, 2), "sign": get_zodiac_sign(house_cusp_4)},
        "5": {"cusp": round(house_cusp_5, 2), "sign": get_zodiac_sign(house_cusp_5)},
        "6": {"cusp": round(house_cusp_6, 2), "sign": get_zodiac_sign(house_cusp_6)},
        "7": {"cusp": round(house_cusp_7, 2), "sign": get_zodiac_sign(house_cusp_7)},
        "8": {"cusp": round(house_cusp_8, 2), "sign": get_zodiac_sign(house_cusp_8)},
        "9": {"cusp": round(house_cusp_9, 2), "sign": get_zodiac_sign(house_cusp_9)},
        "10": {"cusp": round(house_cusp_10, 2), "sign": get_zodiac_sign(house_cusp_10)},
        "11": {"cusp": round(house_cusp_11, 2), "sign": get_zodiac_sign(house_cusp_11)},
        "12": {"cusp": round(house_cusp_12, 2), "sign": get_zodiac_sign(house_cusp_12)}
    }

def calculate_transits(current_date: str, latitude: float, longitude: float) -> Dict[str, Any]:
    try:
        dt = datetime.fromisoformat(current_date)
    except:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    jd = datetime_to_julian_day(dt)
    
    transits = calculate_planet_positions(jd, latitude, longitude)
    
    result = {}
    for planet, degree in transits.items():
        sign = get_zodiac_sign(degree)
        sign_degree, minutes = divmod(degree % 30, 1)
        result[planet] = {
            "degree": round(degree, 2),
            "sign": sign,
            "sign_degree": int(sign_degree),
            "sign_minute": int(minutes * 60),
            "element": ELEMENTS.get(sign, "Unknown"),
            "quality": QUALITIES.get(sign, "Unknown")
        }
    
    return result

def calculate_numerology(name: str, birth_date: str) -> Dict[str, Any]:
    def reduce_to_single(num):
        while num > 9 and num not in [11, 22, 33]:
            num = sum(int(d) for d in str(num))
        return num
    
    name_digits = ''.join(c for c in name.upper() if c.isalpha())
    name_values = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 
                   'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
                   'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 
                   'Y': 7, 'Z': 8}
    
    vowels = 'AEIOU'
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    
    birth_digits = ''.join(c for c in birth_date if c.isdigit())
    birth_parts = birth_date.split('-')
    day = int(birth_parts[2]) if len(birth_parts) > 2 else 1
    month = int(birth_parts[1]) if len(birth_parts) > 1 else 1
    birth_year = int(birth_parts[0]) if len(birth_parts) > 0 else 2000
    
    life_path = reduce_to_single(sum(int(c) for c in birth_digits))
    destiny = reduce_to_single(sum(name_values.get(c, 0) for c in name_digits))
    soul_urge = reduce_to_single(sum(name_values.get(c, 0) for c in name_digits if c in vowels))
    personality = reduce_to_single(sum(name_values.get(c, 0) for c in name_digits if c in consonants))
    birth_day = reduce_to_single(day)
    
    maturity = reduce_to_single(life_path + destiny)
    
    now = datetime.now()
    current_year = now.year
    personal_year = reduce_to_single(reduce_to_single(current_year) + month + day)
    personal_month = reduce_to_single(personal_year + now.month)
    personal_day = reduce_to_single(personal_year + now.day)
    
    name_sum = sum(name_values.get(c, 0) for c in name_digits)
    name_number = reduce_to_single(name_sum)
    
    first_letter = name.upper().strip()[0] if name.strip() else 'A'
    cornerstone = reduce_to_single(name_values.get(first_letter, 1))
    
    last_letter = name.upper().strip()[-1] if name.strip() else 'A'
    capstone = reduce_to_single(name_values.get(last_letter, 1))
    
    balance = reduce_to_single(name_values.get(name.upper().split()[0][0] if name.split() else 'A', 1))
    
    birth_year_reduced = reduce_to_single(birth_year)
    challenge_1 = reduce_to_single(abs(day - month))
    challenge_2 = reduce_to_single(abs(day - birth_year_reduced))
    challenge_3 = reduce_to_single(abs(month - birth_year_reduced))
    challenge_4 = reduce_to_single(challenge_1 + challenge_3)
    
    name_parts = name.upper().split()
    if len(name_parts) >= 2:
        soul_urge_1 = reduce_to_single(sum(name_values.get(c, 0) for c in name_parts[0] if c in vowels))
        soul_urge_2 = reduce_to_single(sum(name_values.get(c, 0) for c in name_parts[-1] if c in vowels))
    else:
        soul_urge_1 = soul_urge
        soul_urge_2 = 0
    
    life_path_meanings = {
        1: "As a Life Path 1, you are a natural-born leader with an independent spirit and an innovative mindset. You possess the drive to pioneer new paths and inspire others through your courage and originality. Your greatest strength is your ability to take initiative and stand firmly on your own two feet. However, you must guard against becoming overly domineering or isolated in your pursuit of success. Embracing collaboration will help you channel your powerful will into lasting achievements.",
        2: "Life Path 2 marks you as a diplomat and peacemaker, gifted with deep sensitivity and an innate understanding of harmony. You excel at bringing people together and creating balance in every situation you touch. Your cooperative nature and gentle intuition allow you to resolve conflicts with grace and wisdom. The challenge for you lies in developing assertiveness without losing your natural empathy. Trusting your instincts while standing your ground is the key to your fulfillment.",
        3: "With a Life Path 3, you are a creative, expressive soul whose mission is to spread joy, optimism, and artistic inspiration. Your natural charisma and gift for communication make you a captivating storyteller, performer, or social connector. You thrive when you can share your ideas and uplift those around you with your enthusiasm. Your main challenge is to avoid scattering your energy across too many pursuits and to develop emotional depth alongside your bright exterior. Channeling your creativity with discipline will unlock your highest potential.",
        4: "Life Path 4 makes you the builder and organizer of the world, someone who creates lasting foundations through discipline, practicality, and unwavering dedication. You value structure, order, and hard work, and you have an extraordinary capacity to turn ambitious plans into tangible realities. Your reliability and methodical approach earn the trust of everyone around you. The shadow side of your path can be rigidity or resistance to change, so learning to embrace flexibility will greatly enhance your journey. Your steady hands build the frameworks upon which society depends.",
        5: "As a Life Path 5, you are an explorer and adventurer driven by an insatiable hunger for freedom, variety, and new experiences. Your dynamic, versatile nature makes you magnetic and adaptable, thriving on change and the thrill of the unknown. You are here to teach others the value of living fully and embracing life's endless possibilities. Your greatest challenge is maintaining focus and responsibility while avoiding excess and restlessness. When you channel your love of freedom into purposeful exploration, you become a true inspiration.",
        6: "Life Path 6 reveals you as a nurturing, responsible soul who finds deepest purpose in caring for family, community, and all who need protection. You are the heart of every group you join, radiating warmth, compassion, and a strong sense of duty. Your domestic instincts and desire to create harmony make you an exceptional parent, partner, and healer. The pitfall to watch for is a tendency to take on others' burdens at your own expense. Learning to balance service with self-care allows your loving nature to shine sustainably.",
        7: "With a Life Path 7, you are a seeker of truth, drawn to introspection, analysis, and the deeper mysteries of existence. Your sharp intellect and spiritual curiosity set you apart as a natural philosopher, researcher, or mystic. You need ample solitude to process your profound insights and connect with your inner wisdom. The challenge for you is to avoid becoming overly detached or cynical, and to share your discoveries with the world. Trusting both logic and intuition will lead you to the enlightenment you seek.",
        8: "Life Path 8 marks you as an achiever and authority figure, blessed with the ambition, business acumen, and executive drive to attain material success and power. You have a natural understanding of money, leadership, and large-scale organization. Your path involves mastering the material world while maintaining integrity and generosity. The danger you face is an overemphasis on wealth or an imbalance between your professional and personal life. True fulfillment comes when you use your success to empower others and create a lasting legacy.",
        9: "As a Life Path 9, you are a humanitarian with a compassionate, generous, and wise soul dedicated to serving humanity on a broad scale. Your broad perspective and tolerance allow you to see beyond differences and embrace universal love. You are drawn to charitable work, healing professions, or creative endeavors that uplift the collective. Your primary challenge is learning to let go of what no longer serves you and to set healthy emotional boundaries. Your journey is one of forgiveness, selflessness, and profound spiritual wisdom.",
        11: "As a Master Number 11, you are a visionary with extraordinary intuition, inspirational abilities, and deep spiritual awareness. You are an old soul carrying a powerful gift for enlightenment, often receiving vivid dreams, gut feelings, and flashes of insight. Your path is to illuminate the world with your wisdom and serve as a bridge between the mundane and the divine. The weight of your sensitivity can be overwhelming if you do not ground yourself, leaving you prone to anxiety and nervous tension. Cultivating faith, trust, and a connection to the higher realms is essential to fulfilling your sacred purpose.",
        22: "The Master Number 22 makes you the Master Builder, combining the visionary insight of the 11 with the practicality to turn dreams into reality on a grand scale. You possess the rare ability to conceive of world-changing ideas and possess the discipline, stamina, and organizational skill to execute them. Your potential is virtually unlimited, but you must work diligently to overcome self-doubt and the fear of your own power. Learning to balance your grand visions with grounded, step-by-step action will allow you to transform civilization. Your mission is to leave a tangible, lasting contribution that benefits all of humanity.",
        33: "Master Number 33 is the Master Teacher, representing the highest expression of love, compassion, and spiritual guidance. As a 33, you are here to uplift humanity through selfless service, healing, and profound wisdom gained through life experience. Your nurturing energy is boundless, yet you must learn to manage the tremendous karmic responsibility that comes with this path. The burden of your gifts can feel heavy, and you may face intense life lessons that refine your character. By embracing your role as a beacon of unconditional love, you inspire countless others to awaken and heal."
    }

    destiny_meanings = {
        1: "Your destiny is to lead and pioneer, blazing trails that others will follow. You are meant to develop unwavering self-reliance and the courage to stand alone when necessary. The world will look to you for direction, and your independent spirit will inspire countless others to find their own strength. Your path requires you to balance your drive for dominance with respect for the contributions of those around you. Ultimately, your destiny is to leave a mark of originality and bold leadership on the world.",
        2: "Your destiny involves partnerships, diplomacy, and the gentle art of bringing people together. You are here to cultivate harmony in every relationship and environment you touch, using your natural sensitivity and tact. Others will rely on your ability to mediate conflicts and create peaceful resolutions. Your journey teaches you the power of cooperation and the strength found in vulnerability and connection. Fulfilling your destiny means becoming a beacon of grace, patience, and unconditional support.",
        3: "Your destiny is one of creative expression and joyful communication, inspiring others through art, words, and boundless optimism. You are meant to use your gifts of self-expression to uplift, entertain, and enlighten those around you. Your natural charisma draws people to you, and your mission is to use that magnetism to spread hope and beauty. The path asks you to develop emotional depth and discipline to match your creative fire. When you share your authentic self, you fulfill your destiny to brighten the world.",
        4: "Your destiny is to build lasting structures and systems that provide stability and order for yourself and others. You are meant to become the dependable foundation upon which great things are constructed, using your methodical nature and strong work ethic. Your practical wisdom and attention to detail earn you a reputation as someone who gets things done reliably. The challenge is to remain open to innovation and not let rigidity limit your growth. Your destiny is realized when you create enduring value through patience and persistence.",
        5: "Your destiny is one of freedom, adventure, and dynamic change, teaching others to embrace life's unpredictability with courage. You are meant to explore the world, collect diverse experiences, and become a messenger of liberation and versatility. Your magnetic, adaptable nature inspires those stuck in routine to break free and live fully. The key to fulfilling your destiny lies in channeling your restless energy toward meaningful pursuits rather than mere sensation-seeking. Through your journey, you show others that true freedom comes from within.",
        6: "Your destiny is nurturing, responsibility, and loving service to your family and community. You are meant to be the caretaker, the healer, and the heart that holds everything together. Others turn to you for comfort, advice, and unconditional support, and you find profound fulfillment in giving. Your path requires you to balance your deep sense of duty with your own personal needs to avoid burnout. Fulfilling your destiny means creating a legacy of love, harmony, and devoted service.",
        7: "Your destiny is spiritual wisdom and deep intellectual discovery, seeking truth in both the seen and unseen worlds. You are meant to dive into life's mysteries, analyze profound ideas, and emerge with insights that enlighten others. Your analytical mind and intuitive gifts make you a natural philosopher, researcher, or spiritual guide. The journey asks you to balance solitude with engagement, sharing your hard-won wisdom without becoming aloof. Your destiny is to be a seeker who becomes a source of illumination for all.",
        8: "Your destiny is power, achievement, and material mastery, using your executive abilities to create abundance and influence. You are meant to develop strong leadership, financial intelligence, and the capacity to manage large ventures successfully. Your path teaches you the responsible use of power and the importance of integrity in all dealings. The material world is your classroom, and your lessons involve balancing ambition with generosity. Fulfilling your destiny means building an empire of success that also serves the greater good.",
        9: "Your destiny is humanitarian service, compassion, and universal love, dedicating your life to helping others on a broad scale. You are meant to develop deep tolerance, wisdom, and a global perspective that transcends cultural boundaries. Your generous heart and big-picture vision draw you toward charitable work, healing, or creative endeavors that serve the collective. The journey requires you to practice forgiveness and release attachments to the past. Your destiny culminates in becoming a wise, selfless benefactor to humanity."
    }

    soul_urge_meanings = {
        1: "Your soul craves independence, self-expression, and the freedom to define your own path without constraint. Deep down, you need to stand out, take initiative, and prove your unique capabilities to yourself and the world. Your inner fire demands that you lead rather than follow, and you feel most alive when you are pioneering something new. The deepest desire of your heart is to be authentic and self-reliant, even if that means walking a solitary road. Fulfilling this soul urge means honoring your need for autonomy while staying connected to others.",
        2: "Your soul desires harmony, partnership, and deep emotional connection with those around you. More than anything, you need meaningful relationships built on trust, mutual respect, and gentle understanding. Your inner world thrives on cooperation, and you feel most fulfilled when you are supporting and being supported by loved ones. The secret yearning of your heart is to be loved unconditionally and to create a peaceful, balanced environment wherever you go. Nurturing your sensitivity and learning to communicate your needs is essential to your soul's satisfaction.",
        3: "Your soul seeks joy, creativity, and the freedom to express your authentic self without inhibition. You have a deep inner need to communicate, perform, and share your artistic vision with the world. Your spirit lights up when you are surrounded by beauty, laughter, and social connection. The deepest craving of your heart is to be heard, appreciated, and to bring happiness to others through your unique gifts. Allowing yourself to play, imagine, and create without self-criticism is how you nourish your soul.",
        4: "Your soul wants security, stability, and a solid foundation upon which to build a meaningful life. You have an inherent need for order, routine, and tangible results that come from disciplined effort. Deep inside, you crave the peace of mind that comes from knowing you have created something lasting and dependable. Your heart yearns for a sense of belonging and the comfort of a well-structured environment. Honoring your need for practicality while staying open to life's spontaneity brings your soul true contentment.",
        5: "Your soul demands freedom, adventure, and the exhilarating experience of living life without limits. You have an insatiable inner need to explore, travel, and embrace constant change and variety. Your spirit feels stifled by routine and craves the rush of new people, places, and ideas. At your core, you need to feel unbounded and to inspire others to break free from their own limitations. Feeding your soul means giving yourself permission to roam, take risks, and celebrate the unknown.",
        6: "Your soul yearns for love, family, and the deep fulfillment that comes from caring for others. You have a powerful inner need to nurture, protect, and create a warm, harmonious home environment. Your heart finds its deepest satisfaction when you are serving those you love and being needed in return. The core longing of your spirit is to experience unconditional love and to be the heart that holds your community together. Balancing your giving nature with self-love is the key to your soul's happiness.",
        7: "Your soul seeks truth, wisdom, and a profound understanding of life's deepest mysteries. You have an intense inner need for solitude, introspection, and time to analyze the world around you. Your spirit is drawn to philosophy, spirituality, and the hidden knowledge that lies beneath the surface of everyday life. At your core, you need to feel that you are growing in wisdom and uncovering meaningful answers. Honoring your need for quiet contemplation while sharing your insights with others feeds your soul's deepest hunger.",
        8: "Your soul desires success, recognition, and the power to manifest your ambitions into tangible reality. You have a driving inner need to achieve, lead, and demonstrate your competence in the material world. Your spirit feels energized by challenge, competition, and the pursuit of excellence in all you do. The deepest longing of your heart is to be respected for your accomplishments and to leave a legacy of influence and abundance. Balancing your drive for success with integrity and generosity is essential to your soul's fulfillment.",
        9: "Your soul wants to serve humanity, embrace universal love, and contribute to the greater good of all people. You have a deep inner need to practice compassion, forgiveness, and selfless giving without expecting anything in return. Your spirit is drawn to humanitarian causes, healing arts, and creative work that elevates collective consciousness. At your core, you need to feel that your life has made a meaningful difference in the world. Letting go of personal attachments and embracing your role as a global citizen brings your soul its deepest peace."
    }

    personality_meanings = {
        1: "Others see you as a confident, independent leader who takes charge and isn't afraid to go against the grain. Your strong presence and self-assured demeanor command respect and make people look to you for direction. There is an air of originality and determination about you that signals you are someone who gets things done on your own terms. To others, you appear decisive and courageous, even when you may feel uncertain inside. Your personality projects a pioneering spirit that naturally attracts followers and collaborators.",
        2: "Others see you as a cooperative, diplomatic mediator who brings peace and balance to every group or situation. Your gentle, attentive nature makes people feel heard, understood, and valued in your presence. You come across as approachable, tactful, and genuinely interested in the well-being of those around you. The world perceives you as a calming influence who can navigate conflict with grace and sensitivity. Your quiet strength and supportive demeanor earn you deep trust and lasting friendships.",
        3: "Others see you as a creative, joyful communicator whose enthusiasm and charisma light up any room. Your magnetic personality and quick wit make you the natural center of social gatherings and creative circles. People perceive you as optimistic, expressive, and full of artistic potential that inspires those around you. The world sees your vibrant energy and loves being uplifted by your stories, humor, and passion. Your outgoing nature makes you memorable and beloved by a wide circle of acquaintances.",
        4: "Others see you as a reliable, practical organizer who can be counted on to get things done efficiently and correctly. Your methodical approach and attention to detail convey a sense of stability and trustworthiness that puts people at ease. The world perceives you as the backbone of any team, the person who brings order to chaos and follow-through to plans. You come across as disciplined, honest, and deeply committed to your responsibilities. Your solid, no-nonsense presence inspires confidence and respect in professional and personal settings alike.",
        5: "Others see you as an adventurous, versatile explorer who thrives on change and embraces life with infectious enthusiasm. Your dynamic personality and restless energy make you seem exciting, spontaneous, and full of endless possibilities. People perceive you as freedom-loving, charismatic, and always ready for the next great experience. The world sees your adaptability and courage and is drawn to your magnetic, untamed spirit. Your personality projects a sense of boldness that encourages others to step outside their comfort zones.",
        6: "Others see you as a caring, responsible nurturer who radiates warmth and a deep sense of devotion to loved ones. Your loving nature and protective instincts make people feel safe, supported, and genuinely cared for in your presence. The world perceives you as the heart of your family and community, someone who can always be turned to for comfort and advice. You come across as domestic, loyal, and deeply committed to creating harmony in your surroundings. Your generous and compassionate personality makes you a beloved figure to all who know you.",
        7: "Others see you as a wise, mysterious thinker who seems to possess knowledge far beyond the surface level. Your quiet, contemplative demeanor gives you an air of depth, intelligence, and inner knowing that intrigues those around you. People perceive you as analytical, perceptive, and somewhat enigmatic, always pondering life's deeper questions. The world sees your reserve as a sign of wisdom and trusts your thoughtful, measured judgment. Your personality projects an aura of mystery and sophistication that draws others to seek your counsel.",
        8: "Others see you as a powerful, ambitious achiever who exudes confidence, authority, and the drive to succeed on a grand scale. Your commanding presence and executive bearing signal that you are someone who gets results and isn't afraid of responsibility. The world perceives you as materialistic in the best sense, capable of managing wealth and influence with skill and integrity. You come across as decisive, efficient, and naturally suited for leadership roles and high-stakes environments. Your personality projects strength and competence that inspire both admiration and a healthy respect.",
        9: "Others see you as a generous, compassionate humanitarian with a big heart and a broad, inclusive worldview. Your selfless nature and welcoming attitude make people feel accepted and valued regardless of their background. The world perceives you as wise, tolerant, and deeply committed to making a positive difference in the lives of others. You come across as an old soul with a global perspective, someone who sees the bigger picture and acts with kindness. Your warm, forgiving personality leaves a lasting impression of grace and universal love."
    }

    personal_year_meanings = {
        1: "This is a year of new beginnings and independence, where fresh opportunities and bold initiatives come to the forefront. It is a time to plant seeds for the next nine years, assert your individuality, and take decisive action on your goals. Old chapters close and you are called to step into a leadership role in your own life, embracing self-reliance and courage. This energy supports starting new projects, launching ventures, or making major personal changes. Embrace the pioneering spirit of the number 1 and trust in your ability to create your own path forward.",
        2: "This is a year of partnerships, cooperation, and patient development behind the scenes. The fast pace of last year slows down, asking you to cultivate diplomacy, listen deeply, and build meaningful connections with others. Relationships of all kinds take center stage, and you may find yourself in a supporting role rather than leading. This is a period of gentle growth, emotional sensitivity, and laying the groundwork for future success through collaboration. Practice patience and trust the process, as the seeds you nurture now will bloom beautifully in time.",
        3: "This is a year of creativity, self-expression, and joyful social engagement. Your artistic talents and communication skills are highlighted, and you are encouraged to share your unique voice with the world. Social opportunities abound, and your natural charisma attracts new friends, collaborations, and moments of pure inspiration. This is a time to have fun, explore your passions, and let your optimistic spirit guide you. Embrace spontaneity and allow yourself to shine brightly without self-censorship.",
        4: "This is a year of hard work, building foundations, and creating lasting structures in your life. The playful energy of the previous year gives way to a need for discipline, organization, and focused effort. You are called to establish solid routines, pay attention to details, and put in the consistent work that builds long-term success. This may feel like a year of limitations or responsibilities, but these constraints are actually the framework for your future growth. By honoring your commitments and staying the course, you create an unshakable foundation for what is to come.",
        5: "This is a year of change, freedom, and exciting new experiences that shake up your routine. The stability of the past year gives way to a restless energy that pushes you to explore, travel, and embrace the unexpected. Major life changes such as moving, career shifts, or new relationships are likely during this dynamic period. Your adaptability is your greatest asset, so stay flexible and open to the opportunities that sudden change brings. This is your year to break free from limitations and celebrate the thrill of living fully.",
        6: "This is a year of family, responsibilities, and nurturing your closest relationships. The focus shifts from personal freedom to domestic harmony, and you are called to care for those you love with attention and devotion. Home, family, and community matters take priority, and you may find yourself taking on caretaking roles or resolving household issues. This is a time to create beauty and comfort in your environment and to heal any rifts in your personal relationships. By showing up with love and responsibility, you strengthen the bonds that truly matter.",
        7: "This is a year of introspection, spiritual growth, and deep inner reflection. The external activity of previous years quiets down, inviting you to turn inward and seek wisdom through solitude and contemplation. This is a powerful time for study, research, meditation, and connecting with your higher self. You may feel a pull toward stillness and a desire to understand life on a deeper, more meaningful level. Trust the quiet and allow yourself the gift of rest and revelation.",
        8: "This is a year of achievement, recognition, and material abundance flowing from your previous efforts. The seeds you have planted over the past seven years are now ready to harvest, bringing rewards, promotions, and financial success. Your leadership abilities are called upon, and you have the power to make significant strides in your career and public life. This is a time to think big, take calculated risks, and assert your authority in your chosen field. Use your influence wisely and remember to share your prosperity with those who supported you.",
        9: "This is a year of completion, humanitarian service, and learning to let go of what no longer serves you. The nine-year cycle comes to a close, asking you to tie up loose ends, forgive past hurts, and release attachments to people, situations, or possessions that are holding you back. Your focus expands from the personal to the universal, and you may feel called to serve others through charitable work or creative contributions. This is a time for healing, compassion, and preparing for the new cycle that begins next year. Embrace the bittersweet energy of endings, knowing they make way for beautiful new beginnings."
    }

    return {
        "life_path": life_path,
        "life_path_meaning": life_path_meanings.get(life_path, "Your path is unique"),
        "destiny": destiny,
        "destiny_meaning": destiny_meanings.get(destiny, "Your destiny is unique"),
        "soul_urge": soul_urge,
        "soul_urge_meaning": soul_urge_meanings.get(soul_urge, "Your soul's desire is unique"),
        "personality": personality,
        "personality_meaning": personality_meanings.get(personality, "Your personality is unique"),
        "birth_day": birth_day,
        "birth_day_meaning": f"Birth Day {birth_day} gives you natural talent and practical abilities.",
        
        "maturity": maturity,
        "maturity_meaning": f"Your maturity number is {maturity}. This represents your later life purpose.",
        
        "personal_year": personal_year,
        "personal_year_meaning": personal_year_meanings.get(personal_year, "This is your personal year."),
        
        "personal_month": personal_month,
        "personal_day": personal_day,
        
        "name_number": name_number,
        "name_number_meaning": f"Your name adds up to {name_number}, influencing how you present yourself.",
        
        "cornerstone": cornerstone,
        "cornerstone_meaning": f"The first letter '{name.strip()[0].upper() if name.strip() else 'A'}' gives you {['strong leadership', 'diplomatic nature', 'creative expression', 'practical stability', 'adventurous spirit', 'nurturing heart', 'deep wisdom', 'powerful drive', 'compassionate soul'][cornerstone-1]} qualities.",
        
        "capstone": capstone,
        "capstone_meaning": f"Your last letter indicates how you finish things - you are {['determined', 'harmonious', 'optimistic', 'reliable', 'flexible', 'caring', 'thoughtful', 'ambitious', 'generous'][capstone-1]} in your approach.",
        
        "balance": balance,
        "balance_meaning": f"Your balance number is {balance}, representing your inner harmony.",
        
        "challenges": {
            "first": challenge_1,
            "second": challenge_2,
            "third": challenge_3,
            "fourth": challenge_4
        },
        
        "soul_urge_doubles": {
            "first_name": soul_urge_1,
            "last_name": soul_urge_2
        },
        
        "power_number": reduce_to_single(life_path + destiny),
        "yearly_theme": f"Personal Year {personal_year}: {personal_year_meanings.get(personal_year, 'This is a year of personal growth and transformation. Embrace the energy of this cycle and align your actions with its unique opportunities for development.')}"
    }

def get_planet_ruler(sign: str) -> str:
    rulers = {
        "Aries": "Mars", "Scorpio": "Pluto", "Leo": "Sun", "Cancer": "Moon",
        "Taurus": "Venus", "Libra": "Venus", "Virgo": "Mercury", "Gemini": "Mercury",
        "Capricorn": "Saturn", "Aquarius": "Uranus", "Sagittarius": "Jupiter", "Pisces": "Neptune"
    }
    return rulers.get(sign, "Unknown")

def generate_detailed_analysis(chart: Dict) -> Dict[str, Any]:
    sun_sign = chart.get("sun_sign", "")
    moon_sign = chart.get("moon_sign", "")
    rising_sign = chart.get("rising_sign", "")
    planets = chart.get("planets", {})
    houses = chart.get("houses", {})
    
    strengths = []
    challenges = []
    career_indications = []
    relationship_indications = []
    health_indications = []
    
    sun_planet = planets.get("Sun", {})
    moon_planet = planets.get("Moon", {})
    mer_planet = planets.get("Mercury", {})
    ven_planet = planets.get("Venus", {})
    mar_planet = planets.get("Mars", {})
    jup_planet = planets.get("Jupiter", {})
    sat_planet = planets.get("Saturn", {})
    pl_planet = planets.get("Pluto", {})
    
    sun_s = sun_planet.get("sign", sun_sign)
    moon_s = moon_planet.get("sign", moon_sign)
    mer_s = mer_planet.get("sign", "")
    ven_s = ven_planet.get("sign", "")
    mar_s = mar_planet.get("sign", "")
    jup_s = jup_planet.get("sign", "")
    sat_s = sat_planet.get("sign", "")
    pl_s = pl_planet.get("sign", "")
    
    # --- STRENGTHS ---
    if sun_s in ["Aries", "Leo", "Sagittarius"]:
        strengths.append("Natural leadership abilities and creative energy that inspire those around you")
    elif sun_s in ["Taurus", "Virgo", "Capricorn"]:
        strengths.append("Unyielding determination and a practical mindset that builds lasting success")
    elif sun_s in ["Gemini", "Libra", "Aquarius"]:
        strengths.append("Exceptional intellectual versatility and a gift for communication and networking")
    elif sun_s in ["Cancer", "Scorpio", "Pisces"]:
        strengths.append("Profound emotional depth and intuitive understanding of others' needs")
    
    if moon_s in ["Cancer", "Scorpio", "Pisces"]:
        strengths.append("Deep emotional intuition and sensitivity that allows you to connect on a soul level")
    elif moon_s in ["Taurus", "Virgo", "Capricorn"]:
        strengths.append("Emotional stability and a grounded approach to life's challenges")
    elif moon_s in ["Aries", "Leo", "Sagittarius"]:
        strengths.append("Emotional courage and optimism that helps you bounce back from setbacks")
    elif moon_s in ["Gemini", "Libra", "Aquarius"]:
        strengths.append("Emotional adaptability and a rational perspective that keeps you balanced")
    
    if rising_sign in ["Capricorn", "Virgo", "Taurus"]:
        strengths.append("Strong practical approach and determination that earns respect from peers")
    elif rising_sign in ["Aries", "Leo", "Sagittarius"]:
        strengths.append("A dynamic, confident presence that naturally draws people and opportunities toward you")
    elif rising_sign in ["Gemini", "Libra", "Aquarius"]:
        strengths.append("Charming social demeanor and quick wit that makes you a natural connector")
    elif rising_sign in ["Cancer", "Scorpio", "Pisces"]:
        strengths.append("A magnetic, empathetic aura that makes others feel safe and understood")
    
    if mer_s:
        if mer_s in ["Gemini", "Virgo"]:
            strengths.append("Sharp analytical mind with an ability to communicate complex ideas with clarity")
        elif mer_s in ["Libra", "Aquarius"]:
            strengths.append("Innovative thinking and a talent for seeing multiple perspectives simultaneously")
        elif mer_s in ["Scorpio", "Pisces"]:
            strengths.append("Penetrative investigative skills and an ability to uncover hidden truths")
    
    if mar_s:
        if mar_s in ["Aries", "Scorpio"]:
            strengths.append("Tremendous drive, courage and the ability to push through any obstacle with fierce determination")
        elif mar_s in ["Capricorn", "Leo"]:
            strengths.append("Strategic ambition and disciplined action that steadily builds toward major achievements")
    
    if jup_s:
        if jup_s in ["Sagittarius", "Pisces"]:
            strengths.append("Expansive vision and an optimistic worldview that opens doors wherever you go")
    
    # --- CHALLENGES ---
    if sun_s in ["Leo", "Aries"]:
        challenges.append("Tendency toward ego clashes and impatience when things don't go your way")
    if sun_s in ["Virgo", "Capricorn"]:
        challenges.append("Overcritical tendencies and a harsh inner critic that can undermine self-confidence")
    if sun_s in ["Pisces", "Cancer"]:
        challenges.append("Boundary-blurring empathy that can leave you emotionally drained by others' problems")
    if sun_s in ["Gemini", "Sagittarius"]:
        challenges.append("Restlessness and difficulty committing to a single path when multiple options beckon")
    
    if moon_s in ["Scorpio", "Capricorn"]:
        challenges.append("Emotional guardedness that makes it hard to trust and open up to others")
    elif moon_s in ["Gemini", "Aquarius"]:
        challenges.append("Emotional detachment that can make partners feel undervalued or distant")
    elif moon_s in ["Aries", "Sagittarius"]:
        challenges.append("A tendency to react impulsively rather than processing feelings thoroughly")
    
    if mer_s in ["Gemini", "Sagittarius"]:
        challenges.append("Scattered mental energy that can lead to unfinished projects and missed details")
    elif mer_s in ["Pisces", "Cancer"]:
        challenges.append("Overwhelming emotional influence on decision-making that clouds objectivity")
    
    if mar_s:
        if mar_s in ["Aries", "Scorpio", "Capricorn"]:
            challenges.append("A confrontational edge when stressed that can strain personal and professional relationships")
        if mar_s in ["Taurus", "Libra"]:
            challenges.append("Passive-aggressive patterns when anger is suppressed rather than expressed directly")
    
    if sat_s:
        if sat_s in ["Capricorn", "Aquarius"]:
            challenges.append("Heavy sense of responsibility and fear of failure that can delay taking necessary risks")
        elif sat_s in ["Cancer", "Pisces"]:
            challenges.append("Deep-seated insecurities and emotional blocks that require patient inner work")
    
    if pl_s:
        if pl_s in ["Scorpio", "Capricorn"]:
            challenges.append("Intense control issues and a tendency to undergo painful transformations before growth")
    
    # --- CAREER INDICATIONS ---
    if sun_s:
        if sun_s in ["Leo"]:
            career_indications.append("Sun in Leo: Creative fields, performing arts, management, or any role where you shine in the spotlight")
        elif sun_s in ["Capricorn"]:
            career_indications.append("Sun in Capricorn: Executive leadership, finance, real estate, or building long-term institutional power")
        elif sun_s in ["Aquarius"]:
            career_indications.append("Sun in Aquarius: Technology, social innovation, scientific research, or humanitarian work")
        elif sun_s in ["Pisces"]:
            career_indications.append("Sun in Pisces: Healing arts, music, spirituality, film, or any creative pursuit that channels deep emotion")
        else:
            career_indications.append(f"Sun in {sun_s}: Your core identity thrives in environments that honor your sign's natural strengths")
    
    if jup_s:
        if jup_s in ["Sagittarius", "Pisces"]:
            career_indications.append("Jupiter in Sagittarius/Pisces: Teaching, publishing, travel, higher education, philosophy, or spiritual guidance")
        elif jup_s in ["Capricorn", "Libra"]:
            career_indications.append("Jupiter in Capricorn/Libra: Business partnerships, law, diplomacy, corporate growth strategy")
        else:
            career_indications.append(f"Jupiter in {jup_s}: Your career expands most when you follow your {jup_s} traits with confidence")
    
    if sat_s:
        if sat_s in ["Capricorn", "Aquarius"]:
            career_indications.append("Saturn in Capricorn/Aquarius: Business, engineering, architecture, government, or any structured profession requiring discipline")
        elif sat_s in ["Virgo", "Libra"]:
            career_indications.append("Saturn in Virgo/Libra: Quality control, editing, consulting, HR, or roles demanding precision and fairness")
        else:
            career_indications.append(f"Saturn in {sat_s}: Long-term career success comes through mastering {sat_s}-related fields with patience")
    
    if mar_s:
        if mar_s in ["Aries", "Scorpio"]:
            career_indications.append("Mars in Aries/Scorpio: Entrepreneurship, surgery, sports, military, or competitive high-stakes environments")
        elif mar_s in ["Capricorn", "Taurus"]:
            career_indications.append("Mars in Capricorn/Taurus: Real estate development, construction, banking, or roles requiring sustained effort")
    
    if mer_s:
        if mer_s in ["Gemini", "Virgo"]:
            career_indications.append("Mercury in Gemini/Virgo: Writing, journalism, data analysis, teaching, consulting, or tech communication roles")
        elif mer_s in ["Aquarius", "Libra"]:
            career_indications.append("Mercury in Aquarius/Libra: Law, negotiation, web development, AI, or social media strategy")
    
    houses_10 = houses.get("10", {}) if houses else {}
    house_10_sign = houses_10.get("sign", "")
    if house_10_sign:
        career_indications.append(f"10th house in {house_10_sign}: Your public reputation and career path are colored by {house_10_sign} energy, suggesting you lead through {house_10_sign}-style initiatives")
    
    # --- RELATIONSHIP INDICATIONS ---
    if ven_s:
        relationship_indications.append(f"Venus in {ven_s}: You express love and attraction through {ven_s} energy — this shapes what you find beautiful and how you romance others")
        if ven_s in ["Taurus", "Libra"]:
            relationship_indications.append("Venus-ruled signs indicate a deep need for harmony, physical affection, and aesthetic beauty in relationships")
        elif ven_s in ["Aries", "Scorpio"]:
            relationship_indications.append("Intense, passionate romantic style — you crave excitement and deep soul-level bonding in partnerships")
        elif ven_s in ["Gemini", "Aquarius"]:
            relationship_indications.append("Intellectual connection is essential — you need a partner who stimulates your mind and respects your freedom")
        elif ven_s in ["Cancer", "Pisces"]:
            relationship_indications.append("Deeply nurturing and romantic — you seek emotional fusion and unconditional love in your closest bonds")
    
    if mar_s:
        relationship_indications.append(f"Mars in {mar_s}: Your assertive energy in relationships is expressed through {mar_s} — this shows how you pursue what you desire")
        if mar_s in ["Aries", "Leo"]:
            relationship_indications.append("You take the initiative in romance and appreciate partners who match your passion and independence")
        elif mar_s in ["Taurus", "Cancer"]:
            relationship_indications.append("Slow and steady approach to intimacy — you build trust through consistent, devoted actions over time")
    
    if moon_s:
        relationship_indications.append(f"Moon in {moon_s} shows your emotional needs in relationships — you feel most secure when your {moon_s} traits are honored by your partner")
    
    houses_7 = houses.get("7", {}) if houses else {}
    house_7_sign = houses_7.get("sign", "")
    if house_7_sign:
        relationship_indications.append(f"7th house in {house_7_sign}: You are drawn to partners who embody {house_7_sign} qualities, and your one-on-one relationships reflect this dynamic")
    
    if ven_s and mar_s:
        relationship_indications.append(f"Venus-Mars dynamic: Your Venus in {ven_s} and Mars in {mar_s} create a unique romantic chemistry — you attract through {ven_s} and pursue through {mar_s}")
    
    # --- HEALTH INDICATIONS ---
    if mar_s:
        if mar_s in ["Aries", "Scorpio"]:
            health_indications.append("Mars in Aries/Scorpio: Watch for head tension, inflammatory issues, and high-intensity stress. Regular cardio and anger release practices help")
        elif mar_s in ["Taurus", "Libra"]:
            health_indications.append("Mars in Taurus/Libra: Prone to throat tension, neck stiffness, and metabolic sluggishness. Neck stretches and balanced nutrition are key")
        elif mar_s in ["Gemini", "Virgo"]:
            health_indications.append("Mars in Gemini/Virgo: Nervous system sensitivity and digestive issues. Breathing exercises and consistent meal routines support wellbeing")
    
    if moon_s:
        if moon_s in ["Cancer", "Scorpio", "Pisces"]:
            health_indications.append(f"Moon in {moon_s}: Emotional health directly impacts physical wellbeing. Prioritize emotional release, journaling, and water-based activities")
        elif moon_s in ["Gemini", "Virgo", "Libra"]:
            health_indications.append(f"Moon in {moon_s}: Anxiety manifests as digestive or nervous symptoms. Meditation and structured routines are beneficial")
    
    if sat_s:
        if sat_s in ["Capricorn", "Aquarius"]:
            health_indications.append("Saturn in Capricorn/Aquarius: Bone and joint health need attention over time. Weight-bearing exercise and calcium-rich diet are recommended")
        elif sat_s in ["Pisces", "Cancer"]:
            health_indications.append("Saturn in Pisces/Cancer: Prone to psychosomatic conditions. Mind-body practices like yoga and tai chi help maintain balance")
    
    if rising_sign:
        if rising_sign in ["Cancer", "Pisces"]:
            health_indications.append(f"Ascendant in {rising_sign}: A sensitive constitution that responds well to gentle healing modalities and consistent self-care rituals")
        elif rising_sign in ["Aries", "Leo"]:
            health_indications.append(f"Ascendant in {rising_sign}: A robust constitution that thrives on vigorous exercise and needs to watch for burnout from overexertion")
        elif rising_sign in ["Virgo", "Capricorn"]:
            health_indications.append(f"Ascendant in {rising_sign}: Health benefits from disciplined routines, proper digestion, and stress management through structured habits")
        else:
            health_indications.append(f"Ascendant in {rising_sign}: Your vitality is linked to {ELEMENTS.get(rising_sign, 'your')} balance — align your lifestyle with your natural elemental rhythm")
    
    houses_6 = houses.get("6", {}) if houses else {}
    house_6_sign = houses_6.get("sign", "")
    if house_6_sign:
        health_indications.append(f"6th house in {house_6_sign}: Daily habits and wellness routines should honor {house_6_sign} energy — consistency is your best preventative medicine")
    
    jup_sign_for_health = jup_s
    if jup_s:
        health_indications.append(f"Jupiter in {jup_s}: Your healing and growth areas are connected to {jup_s} — expanding joy in these areas boosts your overall vitality")
    
    sun_ruler = get_planet_ruler(sun_sign)
    moon_ruler_val = get_planet_ruler(moon_sign) if moon_sign else ""
    
    # --- CONFIDENCE ---
    total_points = len(strengths) + len(challenges)
    if total_points > 0:
        ratio = len(strengths) / total_points
    else:
        ratio = 0.5
    confidence_overall = min(95, max(50, round(50 + ratio * 45)))
    
    career_confidence = min(95, max(50, 50 + len(career_indications) * 8))
    love_confidence = min(95, max(50, 50 + len(relationship_indications) * 8))
    health_confidence = min(95, max(50, 50 + len(health_indications) * 8))
    
    # --- REASONING ---
    career_reasoning = f"Your Sun in {sun_s} indicates natural leadership and your 10th house placement suggests public recognition"
    love_reasoning = f"Venus in {ven_s} combined with your 7th house in {house_7_sign} shapes your relationship patterns"
    health_reasoning = f"Your Moon in {moon_s} connects emotions to your {house_6_sign} health sector"
    
    # --- TIMING & ADVICE ---
    best_timing_career = "Career growth peaks during Jupiter transit through your 10th house"
    best_timing_love = "Relationship opportunities strengthen during Venus retrograde periods"
    preparation_advice = "Focus on developing leadership skills and networking in the next 3 months"
    
    summary = f"You are a {ELEMENTS.get(sun_sign, '')} sign ({sun_sign}) with {moon_sign} Moon and {rising_sign} Rising. Your ruling planet is {sun_ruler}. Overall confidence in this analysis: {confidence_overall}%"
    
    return {
        "sun_sign": sun_sign,
        "moon_sign": moon_sign,
        "rising_sign": rising_sign,
        "sun_ruler": sun_ruler,
        "moon_ruler": moon_ruler_val,
        "element": ELEMENTS.get(sun_sign, "Unknown"),
        "quality": QUALITIES.get(sun_sign, "Unknown"),
        "modalities": {
            "fire": {"signs": ["Aries", "Leo", "Sagittarius"], "traits": "Creative, passionate, spontaneous"},
            "earth": {"signs": ["Taurus", "Virgo", "Capricorn"], "traits": "Practical, stable, materialistic"},
            "air": {"signs": ["Gemini", "Libra", "Aquarius"], "traits": "Intellectual, social, communicative"},
            "water": {"signs": ["Cancer", "Scorpio", "Pisces"], "traits": "Emotional, intuitive, spiritual"}
        },
        "strengths": strengths,
        "challenges": challenges,
        "career": career_indications if career_indications else ["Various career paths suit your chart — focus on aligning work with your Sun sign purpose"],
        "relationships": relationship_indications if relationship_indications else ["Partnerships are important for growth — your Venus and Mars signs reveal your unique relational style"],
        "health": health_indications if health_indications else ["Maintain balance in lifestyle — your 6th house and Moon sign offer clues to your ideal wellness routine"],
        "confidence_overall": confidence_overall,
        "career_confidence": career_confidence,
        "love_confidence": love_confidence,
        "health_confidence": health_confidence,
        "career_reasoning": career_reasoning,
        "love_reasoning": love_reasoning,
        "health_reasoning": health_reasoning,
        "best_timing_career": best_timing_career,
        "best_timing_love": best_timing_love,
        "preparation_advice": preparation_advice,
        "summary": summary
    }

def calculate_kundli_matching(chart1: Dict, chart2: Dict) -> Dict[str, Any]:
    gunas = {
        "Varna": {"max": 1, "score": 0},
        "Vashya": {"max": 2, "score": 0},
        "Tara": {"max": 3, "score": 0},
        "Yoni": {"max": 4, "score": 0},
        "Graha Maitri": {"max": 5, "score": 0},
        "Gana": {"max": 6, "score": 0},
        "Kuta": {"max": 7, "score": 0},
        "Nadi": {"max": 8, "score": 0}
    }
    
    element_map = {"Fire": "Aries,Leo,Sagittarius", "Earth": "Taurus,Virgo,Capricorn", 
                   "Air": "Gemini,Libra,Aquarius", "Water": "Cancer,Scorpio,Pisces"}
    
    sign1 = chart1.get("sun_sign", "")
    sign2 = chart2.get("sun_sign", "")
    
    if ELEMENTS.get(sign1) == ELEMENTS.get(sign2):
        gunas["Varna"]["score"] = 1
    else:
        gunas["Varna"]["score"] = 0
    
    vashya_pairs = {
        "Aries": ["Aries", "Leo", "Sagittarius"], "Taurus": ["Taurus", "Virgo", "Capricorn"],
        "Gemini": ["Gemini", "Libra", "Aquarius"], "Cancer": ["Cancer", "Scorpio", "Pisces"]
    }
    for sign, pool in vashya_pairs.items():
        if sign1 in pool and sign2 in pool:
            gunas["Vashya"]["score"] = 2
            break
    else:
        gunas["Vashya"]["score"] = 1
    
    moon1 = chart1.get("moon_sign", "")
    moon2 = chart2.get("moon_sign", "")
    tara_scores = {0: 3, 1: 2, 2: 1, 3: 1, 4: 2, 5: 3, 6: 1, 7: 2, 8: 0, 9: 1, 10: 2, 11: 3}
    gunas["Tara"]["score"] = tara_scores.get((ZODIAC_SIGNS.index(moon1) - ZODIAC_SIGNS.index(moon2)) % 12, 1)
    
    compatibility_elements = {
        ("Aries", "Leo"): 4, ("Aries", "Sagittarius"): 4, ("Aries", "Gemini"): 2,
        ("Taurus", "Virgo"): 4, ("Taurus", "Capricorn"): 4, ("Taurus", "Cancer"): 2,
        ("Gemini", "Libra"): 4, ("Gemini", "Aquarius"): 4, ("Cancer", "Scorpio"): 4,
        ("Cancer", "Pisces"): 4, ("Leo", "Sagittarius"): 4, ("Virgo", "Capricorn"): 4,
        ("Scorpio", "Pisces"): 4, ("Libra", "Aquarius"): 4, ("Capricorn", "Aquarius"): 2
    }
    gunas["Graha Maitri"]["score"] = compatibility_elements.get((sign1, sign2), compatibility_elements.get((sign2, sign1), 1))
    
    gana_map = {"Aries": "Deva", "Taurus": "Manusha", "Gemini": "Rakshasa", 
                "Cancer": "Deva", "Leo": "Deva", "Virgo": "Manusha",
                "Libra": "Rakshasa", "Scorpio": "Rakshasa", "Sagittarius": "Deva",
                "Capricorn": "Manusha", "Aquarius": "Rakshasa", "Pisces": "Manusha"}
    
    if gana_map.get(sign1) == gana_map.get(sign2):
        gunas["Gana"]["score"] = 6
    elif (gana_map.get(sign1), gana_map.get(sign2)) in [("Deva", "Manusha"), ("Manusha", "Deva")]:
        gunas["Gana"]["score"] = 3
    else:
        gunas["Gana"]["score"] = 1
    
    kuta_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio"]
    gunas["Kuta"]["score"] = 7 if sign1 in kuta_signs and sign2 in kuta_signs else 0
    
    gunas["Nadi"]["score"] = 8
    
    total_score = sum(g["score"] for g in gunas.values())
    max_score = sum(g["max"] for g in gunas.values())
    percentage = round((total_score / max_score) * 100, 1)
    
    if percentage >= 70:
        result = "Excellent - Very harmonious match"
    elif percentage >= 50:
        result = "Good - Can work with understanding"
    elif percentage >= 30:
        result = "Average - Needs adjustments"
    else:
        result = "Low compatibility - Difficult match"
    
    return {
        "total_gunas": 36,
        "obtained_gunas": total_score,
        "percentage": percentage,
        "result": result,
        "details": gunas,
        "advice": "For best results, consult with a Vedic astrologer for personalized remedies and guidance."
    }

def generate_weekly_horoscope(sign: str, week_start_date: str) -> Dict[str, Any]:
    import hashlib
    
    sign_index = ZODIAC_SIGNS.index(sign) if sign in ZODIAC_SIGNS else 0
    seed = f"{sign}{week_start_date}weekly"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    predictions = {
        "Aries": {
            "love": "Passion ignites your relationships this week as Mars fuels your romantic drive. Single Aries may encounter a magnetic connection through a shared adventure. For those committed, planning a spontaneous getaway or trying a thrilling activity together will reignite the flame. Your directness is your asset, but remember that vulnerability invites deeper intimacy than bravado ever could.",
            "career": "Your leadership qualities take center stage this week as the stars align to support bold initiatives. This is an excellent time to start new projects, pitch innovative ideas, or step into a mentoring role. Your confidence inspires those around you, but be mindful not to steamroll over colleagues who need time to process. Recognition from higher-ups is likely if you channel your drive strategically rather than impulsively.",
            "health": "Your vitality is high, but your tendency to push too hard could lead to burnout by midweek. Channel your abundant energy into structured physical activities like HIIT training, competitive sports, or martial arts that satisfy your need for intensity. Pay special attention to your head and sinuses, as these are your vulnerable areas under current transits. Rest is not optional — schedule recovery time as diligently as you schedule workouts.",
            "finance": "Unexpected financial opportunities may arise from a source you haven't considered before. Your risk-taking nature could pay off handsomely, but only if you balance it with a moment of careful research. Consider diversifying your income streams rather than putting all your eggs in one basket. Impulse purchases should be avoided midweek when Mars squares your money sector."
        },
        "Taurus": {
            "love": "Stability and sensuality define your romantic landscape this week as Venus graces your sign. Existing relationships deepen through shared routines and quiet, quality time together. Single Taurus may find love through a friend's introduction or a social gathering that feels comfortably familiar. Your loyalty is your superpower, but be careful not to let stubbornness prevent meaningful conversations about needed changes.",
            "career": "Your patience is about to pay off as projects you have been nurturing behind the scenes start gaining traction. This week favors steady, methodical progress over flashy gestures — your consistent reliability is being noticed by decision-makers. A financial opportunity related to property or long-term assets deserves your serious consideration. Trust your practical instincts when evaluating new proposals or partnerships.",
            "health": "Your body craves consistency this week, making it an ideal time to establish or recommit to a wellness routine that feels nourishing rather than punishing. Focus on grounding activities like yoga, strength training, or long walks in nature that connect you to the earth element. Your throat and neck are sensitive areas right now, so stay hydrated and practice gentle stretching. Mindful eating will serve you better than any restrictive diet.",
            "finance": "Financial planning takes center stage, and your natural prudence serves you well when reviewing budgets or investment strategies. A long-term opportunity in real estate, agriculture, or sustainable ventures aligns with your values and could yield steady returns. Avoid the temptation to make impulsive purchases that promise instant gratification but lack lasting value. Your security comes from smart, patient decisions rather than risky gambles."
        },
        "Gemini": {
            "love": "Communication is the bridge to deeper connection this week as Mercury sharpens your romantic expression. Your wit and charm make you irresistible in social settings, but depth matters more than dazzle in matters of the heart. A meaningful conversation with your partner about future dreams could align you in powerful ways. Single Geminis should say yes to invitations that stretch their social circle — love often arrives through unexpected conversations.",
            "career": "Your adaptability is your greatest professional asset this week as multiple opportunities demand your attention. Networking proves especially fruitful — a connection made at a workshop, conference, or even a casual social event could lead to a significant career shift. Your ability to synthesize information from diverse sources gives you a competitive edge in problem-solving. Just be careful not to overcommit; focus on quality over quantity in your projects.",
            "health": "Your restless mind needs stimulation, but also structure, to stay balanced this week. Mental exercises like puzzles, crosswords, or learning a new skill will satisfy your curiosity while keeping your brain sharp. Your lungs and nervous system are particularly sensitive now, so deep breathing exercises and regular breaks from screens are essential. Physical activity that combines mental engagement, like dance or tennis, will be most fulfilling for your dual nature.",
            "finance": "Multiple income streams are possible now as your versatile nature opens doors to side hustles, freelance work, or passive income opportunities. Your ability to spot trends before others gives you a timing advantage in investments or business decisions. However, the risk of scattering your resources too thin is real — focus on one or two promising avenues rather than chasing every opportunity. Keep meticulous records of your transactions to avoid confusion later."
        },
        "Cancer": {
            "love": "Emotional depth defines your romantic week as the Moon governs your intuitive responses to those closest to you. Your nurturing nature creates a safe harbor for your partner, but be careful not to lose yourself in caretaking at the expense of your own needs. Family matters may interweave with romantic life, requiring gentle boundary-setting. A heartfelt conversation about home and future dreams will bring you closer to those you love.",
            "career": "Your intuition is your professional superpower this week — trust the gut feelings that guide you toward or away from certain decisions. A home-office balance issue may arise, demanding creative scheduling that honors both your domestic responsibilities and career ambitions. Your memory and attention to emotional dynamics give you an advantage in negotiations and team collaboration. Don't be afraid to bring your whole self to work; your empathy is a strength, not a weakness.",
            "health": "Your emotional and physical health are deeply intertwined this week, making self-care a non-negotiable priority. Water is your healing element — prioritize hydration, take soothing baths, or swim to restore your equilibrium. Your digestive system is sensitive to stress, so eat comforting but nourishing foods and create a calm environment around meals. Protect your energy by setting boundaries with people who leave you feeling drained.",
            "finance": "Home and family investments look favorable as the stars support spending that strengthens your foundation. Whether it is home improvements, family support, or real estate decisions, your instincts about where to put your money are reliable now. However, emotional spending could be a trap when you are feeling vulnerable — distinguish between genuine investment and retail therapy. Building an emergency fund will give you the security your crab shell requires."
        },
        "Leo": {
            "love": "Romance takes center stage this week as your radiant energy attracts admirers like moths to a flame. Your generosity in love is returned tenfold when you lead with your heart rather than your ego. Planned grand gestures are lovely, but it is the small, consistent acts of warmth that truly build lasting devotion. Single Leos may meet someone through a creative pursuit or social event where their natural charisma is on full display.",
            "career": "Your creative fire burns brilliantly this week, making it an exceptional time to launch artistic projects or bring innovative ideas to life at work. Your natural leadership draws people to your vision, and you can inspire your team to achieve more than they thought possible. Recognition is coming — accept praise graciously and leverage this momentum toward larger goals. Just be mindful of the line between confidence and arrogance in your professional interactions.",
            "health": "Your heart needs both strengthening and protection this week as your fiery nature pushes you toward intensity in all areas. Cardiovascular exercise will serve you well, whether it is running, swimming, or an invigorating dance class. However, your tendency to overdo everything means you must consciously build rest into your schedule. Your back and spine are sensitive areas now; maintain good posture and consider stretching or yoga to release tension you carry in your regal bearing.",
            "finance": "Your generosity attracts abundance this week, but make sure you are giving from overflow rather than from lack. A creative project or speculative investment could bring surprising returns if you balance your optimism with practical due diligence. Your natural confidence serves you well in negotiations — do not undervalue your worth or settle for less than you deserve. Consider investing in your personal brand or public presence, as these assets will appreciate over time."
        },
        "Virgo": {
            "love": "Your practical expressions of love carry profound meaning this week as you show care through acts of service and thoughtful attention to detail. However, your analytical mind may overthink romantic gestures — sometimes a simple, imperfect expression of love means more than a perfectly planned one. Your partner needs your presence more than your problem-solving skills. A shared wellness activity, like cooking a healthy meal together or taking a yoga class, will create beautiful quality time.",
            "career": "Your meticulous attention to detail sets you apart this week as quality becomes more valuable than quantity in your professional sphere. A project that requires precision and organization plays perfectly to your strengths, and your work does not go unnoticed by those in authority. Your ability to improve systems and streamline processes makes you indispensable to your team. Remember to step back and see the big picture occasionally — perfectionism can become a trap if you lose sight of the ultimate goal.",
            "health": "Health routines are your sanctuary this week, and small, consistent improvements yield remarkable results. Your digestive system is particularly responsive to what you consume — a focus on whole foods, probiotics, and mindful eating will transform how you feel. Your nervous system benefits from order and cleanliness, so tidying your environment will directly calm your mind. Do not let your inner critic sabotage your progress; celebrate small victories on your wellness journey.",
            "finance": "Smart budgeting and meticulous tracking are your financial superpowers this week as the stars favor careful planning over risky ventures. Your analytical nature helps you spot inefficiencies in your spending that others would miss. A service-oriented side hustle or health-related business could provide a meaningful additional income stream. However, your tendency toward worry about money may be disproportionate to reality — trust in your ability to manage resources wisely."
        },
        "Libra": {
            "love": "Partnerships flourish this week as Venus blesses your relationship sector with harmony and charm. Your diplomatic nature helps resolve any lingering tensions with grace, turning conflicts into opportunities for deeper understanding. Balance is your theme — giving and receiving in equal measure creates the equilibrium your soul craves. Single Libras are particularly magnetic now, attracting potential partners through their natural elegance and social grace.",
            "career": "Your diplomatic skills are your greatest professional asset this week as you navigate office dynamics with finesse. Your ability to see all sides of an argument makes you an invaluable mediator and collaborator in team settings. A partnership or joint venture could yield significant professional growth if you choose your allies wisely. Avoid getting drawn into gossip or office politics — your reputation for fairness is worth protecting.",
            "health": "Your body responds best to gentle, harmonious movement this week rather than intense or competitive exercise. Beautiful environments enhance your wellbeing, so take your workout outdoors, practice yoga in a sunlit room, or dance to music that moves your soul. Your lower back and kidneys are sensitive areas now, requiring attention to posture and hydration. Balance is your health keyword — not too much of anything, including rest or activity, work or play.",
            "finance": "Joint finances and partnerships come into focus, making this a favorable week for discussions about shared resources with a partner or business associate. Your ability to negotiate win-win outcomes serves you well in financial matters. Aesthetic or beauty-related investments align with your natural inclinations and could prove profitable. Just be careful about overspending in the pursuit of balance and beauty — distinguish between genuine investments and momentary indulgences."
        },
        "Scorpio": {
            "love": "Intensity deepens your romantic connections this week as Pluto stirs your emotional depths, demanding authenticity above all else. Transformation is the theme in your relationships — old patterns must die to make way for more meaningful connections. Your vulnerability, though frightening, is precisely what will attract the depth of love you truly desire. A powerful conversation with your partner could mark a turning point in how you relate to each other.",
            "career": "Your investigative powers are at their peak this week, making you an unstoppable force for research, strategy, and uncovering hidden opportunities. Dive deep into the data, ask the uncomfortable questions, and trust your instinct for what lies beneath the surface. Your determination impresses those in power, and a mystery at work yields to your relentless pursuit of truth. However, your intensity can intimidate colleagues — soften your approach when collaboration is needed.",
            "health": "Stress management is crucial this week as your intense nature may manifest as physical tension or inflammation. Your body holds what your mind tries to suppress, so emotional release practices like deep breathing, journaling, or cathartic movement are essential. Your reproductive system and elimination organs need support — stay hydrated, eat cleansing foods, and consider a detox from toxins in your diet and environment. Power struggles can deplete you; choose which battles are truly worth fighting.",
            "finance": "Hidden resources and opportunities come to light when you trust your research and intuition this week. Your ability to investigate thoroughly gives you an edge in financial decisions that others make based on incomplete information. An inheritance, tax matter, or shared resource requires your attention and careful management. Avoid power struggles over money — your control issues may surface around finances, and conscious awareness is the first step toward healing these patterns."
        },
        "Sagittarius": {
            "love": "Adventure calls your name in matters of the heart this week as your free spirit seeks novelty and expansion in romance. A relationship that has felt stagnant will benefit enormously from trying something completely new together — whether that is traveling somewhere unfamiliar or exploring a shared creative project. Single Sagittarians may find love while pursuing their passions, perhaps through a class, workshop, or travel experience. Your honesty is refreshing, but remember that sensitivity matters as much as truth in matters of love.",
            "career": "Expansion and growth define your professional landscape this week as Jupiter blesses your endeavors with optimism and opportunity. This is an ideal time to pursue opportunities abroad, in higher education, or in fields that align with your philosophical values. Your visionary ideas inspire others, and your ability to see the big picture positions you as a thought leader. Just make sure to ground your grand plans in practical steps to avoid starting more than you can finish.",
            "health": "Your body craves movement and freedom this week, making outdoor activities your best medicine for both physical and mental wellbeing. Your liver and thighs are sensitive areas, so moderate your indulgences and incorporate stretching into your daily routine. Your restlessness can work against you if you do not channel it purposefully — choose activities that combine physical movement with a sense of adventure or discovery. Nature is your healing sanctuary; spend as much time outdoors as possible.",
            "finance": "Educational investments, travel-related ventures, or opportunities that expand your horizons financially look promising this week. Your optimism about money is generally justified, but your enthusiasm for new ideas can sometimes bypass practical due diligence. Diversifying your income through teaching, writing, or consulting in your area of expertise could be particularly rewarding. A philosophical shift in your relationship with money — seeing it as a tool for freedom rather than security — will serve your growth."
        },
        "Capricorn": {
            "love": "Your commitment and reliability make you a rock for your partner this week, and your steady devotion does not go unnoticed. While grand romantic gestures may not come naturally to you, your consistent presence and acts of service speak volumes about your love. A conversation about future plans and shared goals will strengthen your bond and align your paths. Single Capricorns may meet someone through professional networks who shares their values of ambition and integrity.",
            "career": "Your disciplined approach bears fruit this week as recognition for your hard work arrives from unexpected quarters. Patience has been your ally, and the foundations you have been carefully building are now solid enough to support greater ambitions. An authority figure or mentor takes notice of your dedication and may open a door to advancement. This is also a favorable time for long-term strategic planning — your ability to think ten years ahead is your professional superpower.",
            "health": "Your bones and joints need attention this week as Saturn reminds you that your physical structure requires as much care as your professional structure. Weight-bearing exercise, calcium-rich foods, and good posture are your priorities. Your tendency to prioritize work over wellbeing is your greatest health risk — schedule rest as non-negotiable appointments in your calendar. Consistency, not intensity, is the key to your wellness this week; small daily habits will transform your health over time.",
            "finance": "Long-term investments and financial planning are strongly favored this week as the stars support your patient approach to wealth building. Real estate, retirement accounts, and other assets that appreciate over time align perfectly with your natural strategy. A career advancement or bonus related to your hard work may materialize if you have been diligent. Avoid the temptation of get-rich-quick schemes — your path to prosperity is steady, reliable, and built on a foundation of discipline."
        },
        "Aquarius": {
            "love": "Unique connections form this week as your unconventional approach to love attracts those who appreciate your authentic individuality. Your need for freedom in relationships is not about avoidance but about creating space for genuine connection to breathe. A partner who shares your intellectual passions and humanitarian values will capture your heart most deeply. Single Aquarians may find love through social causes, technology, or unexpected encounters that defy traditional romantic scripts.",
            "career": "Innovation is your professional currency this week as your forward-thinking ideas set you apart from the crowd. Your ability to see future trends and possibilities makes you invaluable in strategic planning and creative problem-solving. Technology, science, and social impact projects are particularly favored areas for your contributions. Network with like-minded individuals who share your vision — your tribe is out there, and collaboration with them will amplify your impact in ways working alone cannot.",
            "health": "Your mind needs as much exercise as your body this week, and activities that challenge both are ideal for your unique constitution. Your circulation and ankles are sensitive areas — stay active, elevate your legs when resting, and pay attention to any signals from your extremities. Your nervous system thrives on novelty, so mixing up your routine with new forms of exercise or movement will keep you engaged. Group fitness or team sports appeal to your social nature and keep you accountable.",
            "finance": "Technology and innovation-focused investments align with your forward-looking nature this week. Your ability to spot emerging trends before they become mainstream gives you a significant advantage in financial decision-making. A side project or entrepreneurial venture related to your unique skills could become a meaningful income source. However, your idealism can sometimes lead to overlooking practical details — balance your visionary thinking with grounded financial planning."
        },
        "Pisces": {
            "love": "Romance takes on a dreamlike quality this week as your intuitive nature allows you to connect with your partner on a soul-deep level. Your empathy is your greatest gift in love, but be mindful not to lose yourself in your partner's emotional world — maintain healthy boundaries while offering compassion. Creative expressions of love, whether through music, poetry, or art, will communicate what words cannot. Single Pisces may encounter a spiritually meaningful connection through creative or healing spaces.",
            "career": "Your creative and intuitive abilities are your professional superpowers this week as inspiration flows freely from the cosmic realm. Work that involves art, music, healing, spirituality, or helping others is especially favored now. Your ability to tap into collective emotions and trends gives you a unique edge in fields like marketing, counseling, or the arts. Trust your hunches — they are messages from your subconscious that your logical mind cannot yet access.",
            "health": "Your spiritual and physical health are deeply connected this week, making practices like meditation, breathwork, or gentle yoga essential for your wellbeing. Your feet and lymphatic system are sensitive areas — reflexology, foot baths, and dry brushing will support your body's natural detoxification. Protect your energy by limiting time in crowded or chaotic environments that overwhelm your sensitive nervous system. Water in all its forms is healing — drink plenty, bathe, or simply sit near a body of water to restore equilibrium.",
            "finance": "Your intuition about money matters is unusually sharp this week, and trusting your gut feelings about investments or financial decisions could serve you well. Creative or healing professions may bring unexpected financial opportunities as your talents are recognized and valued. However, your tendency toward escapism can manifest as careless spending or avoidance of financial realities. Ground your intuitive financial decisions with practical research and perhaps the counsel of a trusted, pragmatic advisor."
        }
    }
    
    sign_pred = predictions.get(sign, predictions["Aries"])
    
    rating = ((hash_val % 5) + 6)
    
    confidence_percentage = 50 + ((hash_val >> 4) % 46)
    reasoning_options = [
        "The alignment of Mercury and Venus this week brings harmony to communication and relationships, making it easier to express your true feelings.",
        "Mars energizes your sector of ambition, pushing you to take bold steps toward your goals with renewed determination.",
        "The New Moon in your sign opens a portal of fresh energy, making this an ideal week to set intentions for the month ahead.",
        "Jupiter's trine to your sun brings expansion and optimism, encouraging you to think bigger about what's possible.",
        "Saturn's influence this week asks you to take a disciplined approach to your responsibilities, rewarding patience and structure.",
        "Venus moves into your romance sector, showering your relationships with warmth, beauty, and deeper emotional connection.",
        "Mercury's transit through your sign sharpens your intellect and communication skills, making this an excellent week for negotiations and creative writing.",
        "The Sun's position highlights your social sector, bringing opportunities to expand your network and strengthen friendships."
    ]
    best_window_options = [
        "Early week is best for initiating new projects and having important conversations that set the tone for the days ahead.",
        "Mid-week brings opportunities for collaboration and creative problem-solving as planetary alignments enhance teamwork.",
        "The weekend offers ideal conditions for rest, reflection, and quality time with loved ones under a nurturing lunar influence.",
        "Thursday and Friday are your power days for negotiations, financial decisions, and career moves that require confidence.",
        "Monday sets the stage for a productive week \u2014 use it to plan, organize, and clarify your intentions for maximum impact.",
        "Wednesday acts as a turning point, bringing clarity and forward momentum that carries you through the rest of the week."
    ]
    preparation_options = [
        "Focus on organizing your priorities before the week begins to maximize the favorable cosmic energy flowing through your sector.",
        "Prepare for unexpected opportunities by keeping your schedule flexible, especially mid-week when surprises are most likely.",
        "Set clear intentions on Monday morning to align your actions with the week\u2019s astrological themes and manifest your goals.",
        "Review your long-term goals this week and adjust your short-term plans to ensure they are still serving your highest purpose.",
        "Take time to ground yourself before the week\u2019s intensity hits \u2014 meditation or journaling will help you stay centered.",
        "Clear any lingering emotional baggage early in the week to make space for the new blessings and opportunities heading your way."
    ]
    
    return {
        "sign": sign,
        "week_start": week_start_date,
        "rating": f"{rating}/10",
        "love": sign_pred["love"],
        "career": sign_pred["career"],
        "health": sign_pred["health"],
        "finance": sign_pred["finance"],
        "lucky_color": ["Red", "Blue", "Green", "Gold", "Purple", "Silver", "White", "Black"][hash_val % 8],
        "lucky_number": (hash_val % 99) + 1,
        "advice": "Trust the journey. Every challenge is an opportunity for growth.",
        "confidence_percentage": confidence_percentage,
        "reasoning": reasoning_options[(hash_val >> 8) % len(reasoning_options)],
        "best_window": best_window_options[(hash_val >> 12) % len(best_window_options)],
        "preparation": preparation_options[(hash_val >> 16) % len(preparation_options)]
    }

def generate_monthly_horoscope(sign: str, year: int, month: int) -> Dict[str, Any]:
    import hashlib
    
    seed = f"{sign}{year}{month}monthly"
    hash_val = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    
    themes = [
        "Transformation and new beginnings",
        "Relationships take center stage",
        "Career and ambition focus",
        "Personal growth and learning",
        "Family and home matters",
        "Creative expression and joy",
        "Financial planning and stability",
        "Spiritual awakening and healing"
    ]
    
    rating = ((hash_val % 5) + 6)
    
    predictions = {
        "Aries": {
            "theme": "Leadership and Bold Initiative",
            "highlights": "Your pioneering spirit leads the way this month as Mars empowers you to take decisive action on goals that have been waiting for the right moment. Creative and professional breakthroughs arrive when you trust your instincts and move with confidence.",
            "challenges": "Your impatience may create friction in relationships where others need more time to process. Practice active listening and resist the urge to rush conversations or decisions that affect those you care about.",
            "spirit_animal": "Ram - Bold and determined"
        },
        "Taurus": {
            "theme": "Stability and Abundant Growth",
            "highlights": "Material and emotional security deepen as Venus blesses your financial sector with steady gains and your relationships with profound warmth. The foundations you have been patiently building are now solid enough to support your next level of growth.",
            "challenges": "Your resistance to change may prevent you from recognizing a beneficial transformation that is knocking at your door. Stretch beyond your comfort zone in small, manageable steps to avoid being caught off guard by larger shifts.",
            "spirit_animal": "Bull - Persistent and reliable"
        },
        "Gemini": {
            "theme": "Communication and Expanding Networks",
            "highlights": "Your social and professional networks expand significantly this month as Mercury enhances your natural gift for connection. A conversation or introduction that seems casual could lead to a life-changing opportunity.",
            "challenges": "Your tendency to juggle too many commitments at once may catch up with you, leading to scattered energy and unfinished projects. Focus on depth over breadth and honor the commitments you have already made before adding new ones.",
            "spirit_animal": "Butterfly - Versatile and adaptable"
        },
        "Cancer": {
            "theme": "Emotional Nurturing and Home Focus",
            "highlights": "Your intuitive powers are at their peak this month, allowing you to create a nurturing environment for yourself and those you love. Home and family matters bring deep fulfillment, and a domestic project or family gathering will warm your heart.",
            "challenges": "Your sensitivity may become overwhelming in social situations that lack emotional depth or authenticity. Protect your energy by choosing your company wisely and creating boundaries that honor your need for emotional safety.",
            "spirit_animal": "Crab - Protective and intuitive"
        },
        "Leo": {
            "theme": "Creative Expression and Radiant Confidence",
            "highlights": "Your natural charisma is amplified this month as the Sun empowers your self-expression and draws opportunities for creative recognition. This is your time to shine — share your talents generously and watch how the universe amplifies your gifts.",
            "challenges": "Your need for admiration may lead to overextending yourself in pursuit of approval that you already possess. Remember that your worth is inherent, not dependent on external validation, and rest is as important as performance.",
            "spirit_animal": "Lion - Courageous and majestic"
        },
        "Virgo": {
            "theme": "Health, Service and Practical Mastery",
            "highlights": "Your analytical skills are sharper than ever this month, making it an ideal time to implement systems and routines that improve your daily life and work efficiency. Your dedication to service and quality inspires those around you and attracts recognition from those in authority.",
            "challenges": "Your inner critic may become louder this month, demanding perfection that is neither realistic nor healthy. Practice self-compassion and remember that progress, not perfection, is the true measure of success.",
            "spirit_animal": "Fox - Wise and meticulous"
        },
        "Libra": {
            "theme": "Harmony, Partnership and Aesthetic Balance",
            "highlights": "Relationships take center stage as Venus guides you toward deeper harmony with partners, friends, and loved ones. Your diplomatic skills resolve tensions with grace, and your social life brings delightful encounters that restore your faith in human connection.",
            "challenges": "Your desire to please everyone may lead you to neglect your own needs and boundaries. Remember that you cannot pour from an empty cup — prioritize your own equilibrium before trying to balance the world around you.",
            "spirit_animal": "Dove - Peaceful and harmonious"
        },
        "Scorpio": {
            "theme": "Transformation and Deep Emotional Truth",
            "highlights": "Powerful transformations unfold this month as Pluto pushes you to release old patterns that no longer serve your evolution. Emotional depth becomes your superpower, allowing you to forge connections that transcend the superficial and touch the very core of what it means to be human.",
            "challenges": "Your intensity may intimidate those who are not ready to meet you at your depth of feeling and authenticity. Be patient with others who process emotions differently, and give them space to arrive at vulnerability in their own time.",
            "spirit_animal": "Phoenix - Reborn through fire"
        },
        "Sagittarius": {
            "theme": "Expansion, Adventure and Higher Wisdom",
            "highlights": "Jupiter fills you with restless optimism and a hunger for expansion that drives you toward new horizons this month. Travel, education, or philosophical exploration brings profound growth and opens your mind to perspectives that will change how you see your future.",
            "challenges": "Your enthusiasm for new beginnings may cause you to abandon projects prematurely when they lose their initial excitement. Discipline yourself to see important commitments through, even when the thrill of novelty has faded.",
            "spirit_animal": "Horse - Free-spirited and adventurous"
        },
        "Capricorn": {
            "theme": "Ambition, Legacy and Disciplined Achievement",
            "highlights": "Your patient, methodical approach yields significant rewards this month as Saturn recognizes your dedication with tangible progress toward your long-term goals. Career advancement, professional recognition, and the solidification of your legacy are all within reach if you continue to build with integrity.",
            "challenges": "Your work-life balance may tip too far toward professional obligations, leaving your personal relationships feeling neglected. Remember that success is hollow without loved ones to share it with — invest in your connections as carefully as you invest in your career.",
            "spirit_animal": "Mountain Goat - Steady and determined"
        },
        "Aquarius": {
            "theme": "Innovation, Community and Visionary Ideas",
            "highlights": "Your forward-thinking ideas find fertile ground this month as Uranus inspires breakthroughs in both your personal and professional life. Your community expands to include like-minded visionaries who share your commitment to making the world a better, more innovative place.",
            "challenges": "Your detachment can be misinterpreted as coldness by those who do not understand your need for intellectual and emotional space. Communicate your needs clearly to avoid misunderstandings, and make a conscious effort to check in emotionally with those you care about.",
            "spirit_animal": "Eagle - Visionary and free"
        },
        "Pisces": {
            "theme": "Spiritual Depth, Creativity and Compassionate Service",
            "highlights": "Your intuitive and creative gifts are amplified this month as Neptune dissolves boundaries between you and the universal flow of inspiration. Artistic projects flourish, spiritual practices deepen, and your capacity for compassion brings healing to everyone you touch.",
            "challenges": "Your porous emotional boundaries may leave you feeling overwhelmed by the energy and suffering of others. Establish clear energetic boundaries, practice grounding techniques, and remember that you cannot heal others by depleting yourself.",
            "spirit_animal": "Dolphin - Mystical and compassionate"
        }
    }
    
    default_pred = {
        "theme": themes[month % len(themes)],
        "highlights": "This month brings a blend of opportunities across multiple areas of life, with the cosmos supporting growth in unexpected ways. Stay open to signs and synchronicities that guide you toward your highest path.",
        "challenges": "Finding balance between competing priorities may require conscious effort, as multiple areas of life demand your attention simultaneously. Trust your inner wisdom to guide you toward what truly matters.",
        "spirit_animal": "Wolf - Intuitive and guided by inner knowing"
    }
    
    pred = predictions.get(sign, default_pred)
    
    confidence_percentage = 50 + ((hash_val >> 4) % 46)
    reasoning_options = [
        "The cosmic alignment this month favors bold action and heartfelt communication, as Venus and Mars dance in harmonious aspect.",
        "Saturn's stabilizing influence this month rewards disciplined effort and long-term planning across all areas of your life.",
        "The New Moon in your sign this month offers a powerful reset point for setting intentions and manifesting your deepest desires.",
        "Jupiter's expansive energy this month encourages you to think bigger and reach higher in your career and personal ambitions.",
        "Mercury's movement through your financial sector this month brings clarity to money matters and opportunities for smart investments.",
        "The Full Moon this month illuminates your relationship sector, bringing hidden feelings to the surface and deepening emotional bonds.",
        "Uranus stirs unexpected changes this month, pushing you out of comfort zones and into exciting new territories of growth.",
        "Neptune's dreamy influence this month heightens your intuition and creativity, making it a powerful time for artistic and spiritual pursuits."
    ]
    best_window_options = [
        "The first half of the month is ideal for launching new initiatives and setting ambitious goals that will carry you forward.",
        "The middle of the month brings a surge of energy and confidence, perfect for tackling challenges and advancing your career.",
        "The last week of the month offers opportunities for closure, reflection, and preparing for the exciting changes ahead.",
        "The first week sets a powerful foundation \u2014 use it to plan, strategize, and align your actions with your highest vision.",
        "The third week of the month is your sweet spot for relationships, creativity, and finding joy in everyday moments.",
        "The second half of the month favors financial decisions, practical planning, and building lasting structures for your future."
    ]
    preparation_options = [
        "Use this month to lay strong foundations for future success by focusing on your long-term goals and consistent daily habits.",
        "This month calls you to embrace change with an open heart \u2014 prepare by releasing old patterns that no longer serve your growth.",
        "Make this month count by setting bold intentions and taking inspired action toward the life you truly want to live.",
        "Let this month be a time of deep listening \u2014 to your intuition, your body, and the quiet wisdom that guides you from within.",
        "Channel this month\u2019s energy into building meaningful connections and investing your time where it yields the greatest emotional returns.",
        "Approach this month as a season of preparation for the abundance that is heading your way \u2014 get your foundation ready.",
        "This month invites you to find balance between ambition and rest, productivity and presence, doing and being.",
        "Use the energy of this month to declutter your life \u2014 clear your space, your schedule, and your mind for new blessings."
    ]
    career_reasoning_options = [
        "Mars in your career sector drives professional ambition and leadership potential this month.",
        "Saturn's influence on your professional life rewards patience and strategic long-term planning.",
        "Jupiter expands your career horizons, bringing opportunities for growth and recognition from superiors.",
        "Mercury sharpens your professional communication, making this an excellent month for negotiations and presentations.",
        "The Sun illuminates your career path, bringing clarity about your next professional steps.",
        "Venus brings harmony to workplace relationships, making collaboration and networking especially fruitful."
    ]
    love_reasoning_options = [
        "Venus in your romance sector deepens emotional connections and attracts new romantic possibilities.",
        "The Full Moon in your relationship sign brings hidden feelings to light, deepening intimacy.",
        "Mars ignites passion in your relationships, encouraging bold romantic gestures and honest communication.",
        "Mercury facilitates meaningful conversations that strengthen your emotional bonds with loved ones.",
        "Jupiter expands your social circle, increasing the chances of meeting someone aligned with your values.",
        "Saturn asks you to commit more deeply to your relationships, rewarding those who invest in lasting love."
    ]
    finance_reasoning_options = [
        "Jupiter's transit through your money sector brings opportunities for financial expansion and abundance.",
        "Saturn's discipline in your financial house rewards careful budgeting and long-term investment strategies.",
        "Mercury's clarity helps you spot financial opportunities that others might overlook this month.",
        "Venus blesses your financial sector with opportunities through creative ventures and partnerships.",
        "Mars drives your financial ambition, making this a good month to negotiate raises or pursue new income streams.",
        "The New Moon in your money sector is ideal for setting financial intentions and starting new savings habits."
    ]
    health_reasoning_options = [
        "The Sun's vitality boosts your physical energy, making this an excellent month to start new wellness routines.",
        "Saturn encourages discipline in health matters, rewarding consistency and dedication to your wellbeing goals.",
        "Venus brings a gentle, nurturing influence to your health sector, favoring holistic and pleasurable self-care practices.",
        "Mars gives you the drive to tackle fitness challenges, but cautions against pushing too hard too fast.",
        "Mercury highlights the mind-body connection, making mental health practices especially important this month.",
        "Jupiter expands your health horizons, encouraging you to explore new approaches to wellness and vitality."
    ]
    
    return {
        "sign": sign,
        "month": f"{year}-{month:02d}",
        "rating": f"{rating}/10",
        "theme": pred["theme"],
        "highlights": pred["highlights"],
        "challenges": pred["challenges"],
        "spirit_animal": pred["spirit_animal"],
        "lucky_days": ["Monday", "Wednesday", "Friday"][hash_val % 3],
        "confidence_percentage": confidence_percentage,
        "reasoning": reasoning_options[(hash_val >> 8) % len(reasoning_options)],
        "best_window": best_window_options[(hash_val >> 12) % len(best_window_options)],
        "preparation": preparation_options[(hash_val >> 16) % len(preparation_options)],
        "career": {
            "prediction": "Professional growth accelerates this month as the stars align to support your ambitions. New opportunities may emerge through networking, mentorship, or recognition of your past contributions. Stay focused on your long-term vision while remaining flexible enough to adapt to unexpected developments.",
            "confidence": 50 + ((hash_val >> 20) % 46),
            "reasoning": career_reasoning_options[(hash_val >> 24) % len(career_reasoning_options)]
        },
        "love": {
            "prediction": "Romance deepens as the month progresses, with meaningful conversations laying the foundation for stronger emotional bonds. Existing relationships benefit from shared experiences that remind you why you chose each other. Single signs may encounter a significant connection through social or creative settings.",
            "confidence": 50 + ((hash_val >> 28) % 46),
            "reasoning": love_reasoning_options[(hash_val >> 32) % len(love_reasoning_options)]
        },
        "finance": {
            "prediction": "Financial stability is within reach this month if you combine your natural instincts with careful planning. A opportunity to increase your income or optimize your investments may present itself around mid-month. Avoid major risks and trust in the power of consistent, patient wealth-building.",
            "confidence": 50 + ((hash_val >> 36) % 46),
            "reasoning": finance_reasoning_options[(hash_val >> 40) % len(finance_reasoning_options)]
        },
        "health": {
            "prediction": "Your body is asking for balance this month \u2014 enough movement to stay vital, enough rest to restore, and enough nourishment to thrive. Pay attention to recurring signals from your body as they hold messages about areas of your life that need attention. A holistic approach that addresses mental, emotional, and physical wellbeing will serve you best.",
            "confidence": 50 + ((hash_val >> 44) % 46),
            "reasoning": health_reasoning_options[(hash_val >> 48) % len(health_reasoning_options)]
        }
    }

def draw_tarot_cards(count: int = 3, question: str = "") -> Dict[str, Any]:
    import random
    
    tarot_cards = [
        {"name": "The Fool", "meaning": "New beginnings, innocence, spontaneity, and a free-spirited approach to life. The Fool represents the start of a journey with unlimited potential.", "advice": "Take a leap of faith. The universe supports new adventures and encourages you to embrace the unknown."},
        {"name": "The Magician", "meaning": "Manifestation, skill, concentration, and the power to turn visions into reality. All the tools you need are at your disposal.", "advice": "You have everything required to succeed. Focus your will and channel your talents with confidence."},
        {"name": "The High Priestess", "meaning": "Intuition, mystery, the subconscious mind, and hidden knowledge. This card calls you to look inward and trust your inner voice.", "advice": "Quiet your external world and listen to your gut. The answers you seek lie within."},
        {"name": "The Empress", "meaning": "Femininity, abundance, nature, nurturing, and creative fertility. She represents the mother archetype and material comfort.", "advice": "Nurture yourself and your creative projects. Growth comes from gentle, consistent care."},
        {"name": "The Emperor", "meaning": "Authority, structure, stability, and the father figure. He represents solid foundations and protective leadership.", "advice": "Establish clear boundaries and lead with confidence. Your structure creates safety for others."},
        {"name": "The Hierophant", "meaning": "Tradition, spiritual guidance, education, and established beliefs. This card points to learning from wise mentors and following proven paths.", "advice": "Seek knowledge from those who have walked before you. Sacred traditions hold timeless wisdom."},
        {"name": "The Lovers", "meaning": "Love, harmony, relationships, and meaningful choices. This card represents deep connections and following your heart's true desire.", "advice": "Follow your heart. Make choices aligned with your authentic self, not external expectations."},
        {"name": "The Chariot", "meaning": "Victory, determination, willpower, and overcoming obstacles through focus and drive. The Chariot represents triumph through sheer determination.", "advice": "Stay focused on your goals and charge forward. You have the inner strength to overcome any obstacle."},
        {"name": "Strength", "meaning": "Courage, patience, inner power, and compassion. True strength comes from gentle control and quiet confidence, not brute force.", "advice": "Meet challenges with grace and patience. Your inner calm is your greatest power."},
        {"name": "The Hermit", "meaning": "Soul-searching, introspection, solitude, and inner guidance. A time to withdraw from the world and seek deeper understanding.", "advice": "Take time for quiet reflection. Solitude will illuminate the answers you seek."},
        {"name": "Wheel of Fortune", "meaning": "Destiny, cycles, change, and the turning points of life. What goes around comes around, and a new cycle is beginning.", "advice": "Embrace life's cycles. Luck is turning in your favor, but remain adaptable to change."},
        {"name": "Justice", "meaning": "Truth, fairness, cause and effect, and legal matters. Actions have consequences and balance must be restored.", "advice": "Seek the truth and act with integrity. What you put out into the world will return to you."},
        {"name": "The Hanged Man", "meaning": "Pause, surrender, letting go, and gaining a new perspective. Sometimes the best action is no action at all.", "advice": "Stop struggling and see the situation from a different angle. Release control to move forward."},
        {"name": "Death", "meaning": "Transformation, endings, and powerful new beginnings. Not physical death, but the death of an old chapter making way for the new.", "advice": "Release what no longer serves your highest good. From every ending springs a powerful new beginning."},
        {"name": "Temperance", "meaning": "Balance, moderation, patience, and finding harmony in all aspects of life. The middle path brings peace and wholeness.", "advice": "Find the middle ground. Patience and moderation will bring lasting fulfillment."},
        {"name": "The Devil", "meaning": "Temptation, materialism, shadow self, and unhealthy attachments. This card reveals what binds you and keeps you from freedom.", "advice": "Confront your shadows and break free from limiting patterns. You have the power to choose liberation."},
        {"name": "The Tower", "meaning": "Sudden upheaval, revelation, chaos, and awakening. The Tower destroys false structures to reveal truth.", "advice": "Sometimes destruction is necessary for liberation. Trust that what falls away was never meant to stay."},
        {"name": "The Star", "meaning": "Hope, inspiration, renewal, serenity, and divine guidance. After the storm, the Star brings peace and a sense of purpose.", "advice": "Stay hopeful and trust the universe. Your light will guide the way through any darkness."},
        {"name": "The Moon", "meaning": "Illusion, fear, anxiety, intuition, and the subconscious. Things are not as they seem, and deeper truths hide beneath the surface.", "advice": "Trust your intuition and face your fears. Not everything is as it appears in the moonlight."},
        {"name": "The Sun", "meaning": "Success, joy, vitality, confidence, and positive energy. One of the most favorable cards, bringing warmth and happiness.", "advice": "Celebrate your successes and share your joy. Life is bright and your light shines for all to see."},
        {"name": "Judgement", "meaning": "Rebirth, inner calling, absolution, and a final reckoning. This card calls you to rise up and answer your true purpose.", "advice": "Answer the call of your soul. It is time for rebirth and embracing your higher purpose."},
        {"name": "The World", "meaning": "Completion, accomplishment, integration, and wholeness. A major cycle ends successfully, bringing fulfillment and travel.", "advice": "You have completed a significant cycle. Celebrate your journey and prepare for the next adventure."},
        {"name": "Ace of Wands", "meaning": "Inspiration, new creative opportunities, growth, and the spark of innovation. A burst of creative energy fuels new ventures.", "advice": "A creative spark awaits. Seize new opportunities with passion and enthusiasm."},
        {"name": "Two of Wands", "meaning": "Future planning, bold decisions, discovery, and stepping out of your comfort zone to explore new horizons.", "advice": "Plan your next move with courage. The world is waiting for you to explore."},
        {"name": "Three of Wands", "meaning": "Expansion, foresight, progress, and looking ahead. Your plans are taking shape and opportunities are on the horizon.", "advice": "Keep your eyes on the horizon. Your efforts are expanding and success is in sight."},
        {"name": "Four of Wands", "meaning": "Celebration, harmony, homecoming, and joyous milestones. A moment of rest and gratitude for what you have built.", "advice": "Celebrate your achievements with loved ones. Take pride in the foundation you have built."},
        {"name": "Five of Wands", "meaning": "Competition, conflict, rivalry, and diverse perspectives clashing. Healthy friction can lead to stronger outcomes.", "advice": "Channel competitive energy constructively. Not all conflict is negative, but choose your battles wisely."},
        {"name": "Six of Wands", "meaning": "Victory, public recognition, praise, and confidence. You are being acknowledged for your hard work and dedication.", "advice": "Accept recognition gracefully. You have earned this moment of triumph and validation."},
        {"name": "Seven of Wands", "meaning": "Defensiveness, standing your ground, maintaining position, and protecting what you have built from challenges.", "advice": "Stand firm in your convictions. You have the strength to defend your position."},
        {"name": "Eight of Wands", "meaning": "Swift action, rapid progress, momentum, and forward movement. Things are moving quickly and changes are accelerating.", "advice": "Move with the momentum. Things are falling into place quickly, so stay agile and ready."},
        {"name": "Nine of Wands", "meaning": "Resilience, persistence, boundaries, and the final stretch. You are weary but almost at the finish line.", "advice": "You are stronger than you know. This last push requires your remaining reserves of courage."},
        {"name": "Ten of Wands", "meaning": "Burden, responsibility, hard work, and carrying too much. You are overextended and need to delegate.", "advice": "You are carrying too much. Delegate and release what is not yours to bear."},
        {"name": "Page of Wands", "meaning": "Exploration, enthusiasm, free spirit, and the excitement of a new discovery or creative project.", "advice": "Embrace your inner explorer. Let enthusiasm and curiosity guide your next step."},
        {"name": "Knight of Wands", "meaning": "Adventure, passion, impulsiveness, and charging ahead with fiery determination toward a goal.", "advice": "Channel your passion into purposeful action. Your fire will inspire others to follow."},
        {"name": "Queen of Wands", "meaning": "Confidence, warmth, charisma, and magnetic energy. She leads with courage and inspires those around her.", "advice": "Own your power and lead with warmth. Your confidence lights the way for others."},
        {"name": "King of Wands", "meaning": "Visionary leadership, entrepreneurial spirit, honor, and bold creative authority. He takes bold action and inspires greatness.", "advice": "Lead with vision and integrity. Your entrepreneurial spirit can create something extraordinary."},
        {"name": "Ace of Cups", "meaning": "New love, emotional awakening, compassion, and the overflowing of feelings. A new chapter of emotional fulfillment begins.", "advice": "Open your heart to love and emotional abundance. A new wave of feeling is coming."},
        {"name": "Two of Cups", "meaning": "Partnership, mutual attraction, unity, and the coming together of two souls in harmony and equal exchange.", "advice": "Nurture the connections that feel balanced and reciprocal. True partnership is a beautiful union."},
        {"name": "Three of Cups", "meaning": "Friendship, celebration, community, and joyful gatherings. This card represents social connections and shared happiness.", "advice": "Celebrate with your community. Joy multiplies when shared with those who love you."},
        {"name": "Four of Cups", "meaning": "Apathy, contemplation, discontentment, and being stuck in a rut. You may be overlooking what you already have.", "advice": "Look within to find contentment. Sometimes the blessings you seek are already in your hands."},
        {"name": "Five of Cups", "meaning": "Loss, disappointment, grief, and focusing on what went wrong. But not all is lost — look for what remains.", "advice": "Acknowledge your grief but don't dwell on spilled cups. Turn around and see what still stands."},
        {"name": "Six of Cups", "meaning": "Nostalgia, childhood memories, innocence, and joyful reunions with people from your past.", "advice": "Embrace sweet memories but don't live in the past. Let nostalgic joy inspire your present."},
        {"name": "Seven of Cups", "meaning": "Illusions, choices, fantasies, and wishful thinking. Many options but not all are what they appear to be.", "advice": "Ground yourself in reality. Not every glittering option is as it seems — choose wisely."},
        {"name": "Eight of Cups", "meaning": "Walking away, disillusionment, leaving behind what no longer serves, and seeking deeper meaning.", "advice": "It is time to walk away from what no longer fulfills you. Trust that more awaits."},
        {"name": "Nine of Cups", "meaning": "Contentment, emotional fulfillment, wishes granted, and deep satisfaction. This is the wish card of the deck.", "advice": "You are entering a time of fulfillment. Celebrate your blessings and enjoy the abundance."},
        {"name": "Ten of Cups", "meaning": "Divine love, emotional bliss, happy family, and lasting fulfillment. The ultimate card of emotional contentment.", "advice": "True happiness awaits in love and family. You are deserving of complete emotional fulfillment."},
        {"name": "Page of Cups", "meaning": "Youthful emotion, creative inspiration, intuitive messages, and a message of love or artistic expression.", "advice": "Stay open to your feelings and creative impulses. A message of love may be coming."},
        {"name": "Knight of Cups", "meaning": "Romance, charm, imagination, and the pursuit of beauty. A dreamer who follows his heart with passion.", "advice": "Follow your heart's desires with romantic optimism. But ensure your dreams have practical roots."},
        {"name": "Queen of Cups", "meaning": "Emotional depth, compassion, intuition, and nurturing wisdom. She loves deeply and sees through the heart.", "advice": "Lead with compassion and trust your intuition. Your emotional wisdom is a gift to the world."},
        {"name": "King of Cups", "meaning": "Emotional maturity, diplomacy, calm wisdom, and compassionate authority. He balances heart and mind with grace.", "advice": "Master your emotions with wisdom and compassion. True leadership comes from a balanced heart."},
        {"name": "Ace of Swords", "meaning": "Clarity, breakthrough, new ideas, and the power of truth. A sharp new perspective cuts through confusion.", "advice": "Truth will set you free. Speak and act with clarity and conviction."},
        {"name": "Two of Swords", "meaning": "Difficult decisions, stalemate, blocked emotions, and needing to see both sides before choosing.", "advice": "You face a tough decision. Weigh both sides carefully and trust your inner knowing."},
        {"name": "Three of Swords", "meaning": "Heartbreak, sorrow, grief, and painful truth. This card carries emotional pain but also the promise of healing.", "advice": "Heartbreak is a necessary part of healing. Allow yourself to grieve and release the pain."},
        {"name": "Four of Swords", "meaning": "Rest, recovery, meditation, and contemplation. A needed pause for mental and physical rejuvenation.", "advice": "Rest is not weakness. Take time to recharge your mind and spirit before moving forward."},
        {"name": "Five of Swords", "meaning": "Conflict, defeat, loss, and hollow victory. Winning at all costs may leave you feeling empty.", "advice": "Consider whether this battle is worth fighting. Sometimes walking away is the true victory."},
        {"name": "Six of Swords", "meaning": "Transition, moving forward, leaving behind, and traveling toward calmer waters after a turbulent time.", "advice": "You are moving through a difficult transition. Better days lie ahead — keep going."},
        {"name": "Seven of Swords", "meaning": "Deception, strategy, stealth, and getting away with something. Beware of dishonesty or clever maneuvering.", "advice": "Be strategic but stay honest. Shortcuts and deception may bring temporary gain but lasting consequences."},
        {"name": "Eight of Swords", "meaning": "Feeling trapped, helplessness, self-imposed limitation, and negative thoughts creating mental prison.", "advice": "The prison is in your mind. Shift your perspective and see the escape route that is already there."},
        {"name": "Nine of Swords", "meaning": "Anxiety, worry, nightmares, and overwhelming fear. Your mind is creating worst-case scenarios that may not be real.", "advice": "Your fears are amplified in darkness. Reach out for support and challenge your anxious thoughts."},
        {"name": "Ten of Swords", "meaning": "Rock bottom, painful ending, betrayal, and hitting a low point. But this also signals a new beginning after the fall.", "advice": "You have hit bottom, but there is nowhere to go but up. This is the final chapter before renewal."},
        {"name": "Page of Swords", "meaning": "Curiosity, intellectual challenge, new ideas, and the energetic pursuit of knowledge and truth.", "advice": "Stay curious and ask questions. Your pursuit of truth will lead to valuable discoveries."},
        {"name": "Knight of Swords", "meaning": "Ambition, quick thinking, rushing forward, and charging into battle with unwavering determination.", "advice": "Move with purpose but avoid recklessness. Your speed is an asset if paired with wisdom."},
        {"name": "Queen of Swords", "meaning": "Clear thinking, direct communication, independence, and sharp intellect. She sees through illusions with piercing truth.", "advice": "Speak your truth with clarity and compassion. Your sharp mind is your greatest asset."},
        {"name": "King of Swords", "meaning": "Intellectual authority, truth, justice, ethical leadership, and the disciplined use of mental power.", "advice": "Lead with intellect and integrity. Your commitment to truth inspires respect and fairness."},
        {"name": "Ace of Pentacles", "meaning": "New financial opportunity, prosperity, abundance, and the seed of material success being planted.", "advice": "A promising opportunity is coming. Prepare your resources and ground yourself for growth."},
        {"name": "Two of Pentacles", "meaning": "Balancing resources, adaptability, time management, and juggling multiple priorities with grace.", "advice": "Stay adaptable and maintain balance. You can handle multiple priorities with flexibility."},
        {"name": "Three of Pentacles", "meaning": "Collaboration, teamwork, skilled work, and mastery through focused effort and learning from others.", "advice": "Collaborate with those who share your craft. Teamwork produces results greater than solo effort."},
        {"name": "Four of Pentacles", "meaning": "Saving money, security, possessiveness, and holding tightly to what you have out of fear of loss.", "advice": "Find balance between saving and enjoying. Hoarding energy or wealth can block new blessings."},
        {"name": "Five of Pentacles", "meaning": "Hardship, financial loss, feeling left out in the cold, but help is available if you ask.", "advice": "Do not be too proud to ask for help. Your current lack is temporary and support is near."},
        {"name": "Six of Pentacles", "meaning": "Generosity, charity, giving and receiving, and the balanced flow of resources between those who have and those who need.", "advice": "Give and receive with an open heart. Generosity creates a beautiful cycle of abundance."},
        {"name": "Seven of Pentacles", "meaning": "Investment, long-term growth, patience, and evaluating whether your efforts are yielding the desired results.", "advice": "Assess your progress patiently. Good things take time — your seeds are growing beneath the surface."},
        {"name": "Eight of Pentacles", "meaning": "Diligence, skill development, craftsmanship, and the dedicated practice of mastering your craft.", "advice": "Focus on honing your skills. Dedicated practice now will pay dividends in mastery later."},
        {"name": "Nine of Pentacles", "meaning": "Luxury, self-sufficiency, financial independence, and enjoying the fruits of your labor in comfort.", "advice": "Enjoy the abundance you have created. You have earned this moment of luxury and peace."},
        {"name": "Ten of Pentacles", "meaning": "Wealth, legacy, inheritance, family traditions, and the enduring prosperity passed through generations.", "advice": "Honor your roots and build for future generations. True wealth is legacy and family."},
        {"name": "Page of Pentacles", "meaning": "Ambition, study, new financial venture, and the first steps toward a practical goal or educational pursuit.", "advice": "Start that project you have been planning. Your practical ambitions are well supported now."},
        {"name": "Knight of Pentacles", "meaning": "Hard work, perseverance, reliability, and the steady, methodical pursuit of goals with unwavering commitment.", "advice": "Stay the course with patience and persistence. Your steady progress will achieve lasting results."},
        {"name": "Queen of Pentacles", "meaning": "Nurturing abundance, practicality, earthly wisdom, and creating a warm, comfortable home filled with love.", "advice": "Create a sanctuary of comfort and security. Your practical nurturing builds lasting wealth."},
        {"name": "King of Pentacles", "meaning": "Wealth, business leadership, financial mastery, and the abundant success that comes from disciplined enterprise.", "advice": "Lead with generosity and wisdom. Your financial mastery can create lasting abundance for all."}
    ]
    
    selected = random.sample(tarot_cards, min(count, len(tarot_cards)))
    
    return {
        "question": question if question else "General Reading",
        "cards": [{"position": i+1, **card} for i, card in enumerate(selected)],
        "summary": f"You drew {count} cards. The {selected[0]['name']} appears as your primary message.",
        "guidance": "Remember: Tarot is a tool for reflection. Trust your intuition in interpreting these messages."
    }

def calculate_muhurat(date: str, city: str = "Delhi") -> Dict[str, Any]:
    from datetime import datetime, timedelta
    
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    city_lat_lng = {
        "Delhi": (28.6139, 77.2090),
        "Mumbai": (19.0760, 72.8777),
        "Bangalore": (12.9716, 77.5946),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639),
        "Hyderabad": (17.3850, 78.4867),
        "Pune": (18.5204, 73.8567)
    }
    
    lat, lng = city_lat_lng.get(city, (28.6139, 77.2090))
    
    jd = datetime_to_julian_day(dt)
    
    sunrise_jd, sunset_jd = 0, 0
    for hour in range(5, 18):
        test_dt = dt.replace(hour=hour)
        jd_test = datetime_to_julian_day(test_dt)
        positions = calculate_planet_positions(jd_test, lat, lng)
        if 90 <= positions.get("Sun", 0) <= 120:
            sunrise_jd = jd_test
            break
    
    day_length = (sunset_jd - sunrise_jd) if sunrise_jd > 0 else 0.5
    
    muhurats = [
        {"name": "Shubh Muhurat (Auspicious)", "time": "6:00 AM - 7:00 AM", "activities": ["New ventures", "Starting business", "Marriage"]},
        {"name": "Labh Muhurat (Profit)", "time": "10:00 AM - 11:00 AM", "activities": ["Financial deals", "Profitable work"]},
        {"name": "Amrit Muhurat (Nectar)", "time": "4:00 AM - 5:00 AM", "activities": ["Spiritual practices", "Meditation"]},
        {"name": "CharMuhurat (Four Ghadis)", "time": "8:00-10:00 AM, 2:00-4:00 PM", "activities": ["All good works"]},
        {"name": "Vijay Muhurat (Victory)", "time": "2:00 PM - 3:00 PM", "activities": ["Starting wars", "Legal matters"]},
        {"name": "Godhuli Muhurat", "time": "5:30 PM - 6:30 PM", "activities": ["Starting new home", "Gifts"]}
    ]
    
    rahu_kalam_start = (sunrise_jd + 2.625) % 1
    yamaganda_start = (sunrise_jd + 0.875) % 1
    
    return {
        "date": date,
        "city": city,
        "sunrise": f"{int((sunrise_jd % 1) * 24)}:00",
        "sunset": f"{int(((sunrise_jd + day_length) % 1) * 24)}:00",
        "muhurats": muhurats,
        "avoid": {
            "rahu_kalam": "10:30 AM - 12:00 PM",
            "yamaganda": "12:00 PM - 1:30 PM",
            "gulikai_kalam": "2:00 PM - 3:30 PM"
        },
        "advice": "For best results, start important work during Shubh or Amrit Muhurat."
    }

# ===================== KRISHNAMURTI PADDHATI (KP) ASTROLOGY =====================

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Poorva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Poorvashadha", "Uttarashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Poorvabhadrapada", "Uttarabhadrapada", "Revati"
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury"
]

NAKSHATRA_PADA = [
    [1, 1, 1], [1, 1, 2], [1, 1, 3], [1, 2, 1], [1, 2, 2], [1, 2, 3],
    [1, 3, 1], [1, 3, 2], [1, 3, 3], [2, 1, 1], [2, 1, 2], [2, 1, 3],
    [2, 2, 1], [2, 2, 2], [2, 2, 3], [2, 3, 1], [2, 3, 2], [2, 3, 3],
    [3, 1, 1], [3, 1, 2], [3, 1, 3], [3, 2, 1], [3, 2, 2], [3, 2, 3],
    [3, 3, 1], [3, 3, 2], [3, 3, 3]
]

VIMSHOTTARI_MAHADASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
VIMSHOTTARI_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

VIMSHOTTARI_SUB_PERIODS = {
    "Ketu": ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"],
    "Venus": ["Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu"],
    "Sun": ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"],
    "Moon": ["Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun"],
    "Mars": ["Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon"],
    "Rahu": ["Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars"],
    "Jupiter": ["Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu"],
    "Saturn": ["Saturn", "Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter"],
    "Mercury": ["Mercury", "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn"]
}

PLANET_TO_NAKSHATRA_LORD = {
    "Sun": "Sun", "Moon": "Moon", "Mars": "Mars", "Mercury": "Mercury",
    "Jupiter": "Jupiter", "Venus": "Venus", "Saturn": "Saturn",
    "Rahu": "Rahu", "Ketu": "Ketu"
}

def get_nakshatra(degree: float) -> tuple:
    nakshatra_index = int((degree % 360) / 13 + (1/3))
    nakshatra_index = nakshatra_index % 27
    pada = int(((degree % 13.333) / 3.333) + 1)
    pada = min(pada, 4)
    start_degree = nakshatra_index * 13.333
    lord = NAKSHATRA_LORDS[nakshatra_index]
    return NAKSHATRAS[nakshatra_index], pada, round(start_degree, 2), lord

def get_kp_nakshatra(planet_degree: float) -> Dict:
    nakshatra, pada, start_deg, lord = get_nakshatra(planet_degree)
    sub_lord = NAKSHATRA_LORDS[NAKSHATRAS.index(nakshatra)]
    return {
        "nakshatra": nakshatra,
        "lord": lord,
        "sub_lord": sub_lord,
        "pada": pada,
        "degree": round(planet_degree, 2),
        "start_degree": start_deg
    }

def calculate_kp_chart(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict:
    try:
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    except:
        try:
            dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
        except:
            return {"error": "Invalid date/time format"}
    
    jd = datetime_to_julian_day(dt)
    positions = calculate_planet_positions(jd, latitude, longitude)
    
    kp_planets = {}
    for planet, degree in positions.items():
        if planet in PLANET_TO_NAKSHATRA_LORD:
            kp_planets[planet] = get_kp_nakshatra(degree)
    
    asc_nakshatra, asc_pada, asc_start, asc_lord = get_nakshatra(positions.get("Ascendant", 0))
    kp_planets["Ascendant"] = {
        "nakshatra": asc_nakshatra,
        "lord": asc_lord,
        "sub_lord": NAKSHATRA_LORDS[NAKSHATRAS.index(asc_nakshatra)],
        "pada": asc_pada,
        "degree": round(positions.get("Ascendant", 0), 2),
        "start_degree": asc_start
    }
    
    return {
        "birth_date": birth_date,
        "birth_time": birth_time,
        "planets": kp_planets,
        "significators": get_kp_significators(kp_planets)
    }

def get_kp_significators(kp_chart: Dict) -> Dict:
    planet_significators = {}
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        if planet in kp_chart:
            nakshatra = kp_chart[planet].get("nakshatra", "")
            nakshatra_idx = NAKSHATRAS.index(nakshatra) if nakshatra in NAKSHATRAS else 0
            ruler = NAKSHATRA_LORDS[nakshatra_idx]
            sign = get_zodiac_sign(kp_chart[planet].get("degree", 0))
            
            house_significators = {
                1: ["Sun", "Moon", "Jupiter", "Mercury"],
                2: ["Venus", "Mercury", "Moon"],
                3: ["Mars", "Mercury", "Moon"],
                4: ["Moon", "Venus", "Jupiter"],
                5: ["Jupiter", "Sun", "Moon"],
                6: ["Mars", "Saturn", "Rahu", "Ketu"],
                7: ["Venus", "Moon", "Saturn"],
                8: ["Saturn", "Rahu", "Ketu"],
                9: ["Jupiter", "Sun", "Moon"],
                10: ["Sun", "Jupiter", "Saturn", "Mercury"],
                11: ["Jupiter", "Uranus", "Mercury"],
                12: ["Saturn", "Ketu", "Rahu"]
            }
            
            sign_num = ZODIAC_SIGNS.index(sign) + 1
            sigs = house_significators.get(sign_num, [])
            
            planet_significators[planet] = {
                "nakshatra": nakshatra,
                "nakshatra_lord": ruler,
                "sign": sign,
                "sign_lord": PLANET_RULERS.get(sign, "Unknown"),
                "significators": sigs
            }
    
    return planet_significators

def calculate_vimshottari_dasha(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict:
    try:
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    except:
        try:
            dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M:%S")
        except:
            return {"error": "Invalid date/time format"}
    
    jd = datetime_to_julian_day(dt)
    positions = calculate_planet_positions(jd, latitude, longitude)
    
    moon_degree = positions.get("Moon", 0)
    nakshatra_idx = int((moon_degree % 360) / 13.333) % 27
    nakshatra_lord = NAKSHATRA_LORDS[nakshatra_idx]
    
    birth_jd = jd
    current_jd = datetime_to_julian_day(datetime.now())
    
    dasha_intervals = []
    total_years = sum(VIMSHOTTARI_YEARS.values())
    
    dasha_order = VIMSHOTTARI_MAHADASHA_ORDER
    start_idx = dasha_order.index(nakshatra_lord) if nakshatra_lord in dasha_order else 0
    
    for i in range(9):
        planet_idx = (start_idx + i) % 9
        mahadasha_planet = dasha_order[planet_idx]
        mahadasha_years = VIMSHOTTARI_YEARS[mahadasha_planet]
        
        elapsed_years = min(current_jd - birth_jd, mahadasha_years)
        remaining_years = mahadasha_years - elapsed_years
        
        sub_periods = VIMSHOTTARI_SUB_PERIODS.get(mahadasha_planet, VIMSHOTTARI_MAHADASHA_ORDER)
        sub_period_list = []
        
        total_sub_years = mahadasha_years
        for j, sub_planet in enumerate(sub_periods):
            sub_years = (VIMSHOTTARI_YEARS.get(sub_planet, 1) / total_years) * mahadasha_years
            elapsed_sub = (elapsed_years / mahadasha_years) * sub_years if elapsed_years > 0 else 0
            remaining_sub = sub_years - elapsed_sub
            
            sub_period_list.append({
                "planet": sub_planet,
                "years": round(sub_years, 2),
                "remaining": round(max(0, remaining_sub), 2)
            })
        
        dasha_intervals.append({
            "mahadasha": mahadasha_planet,
            "years": mahadasha_years,
            "remaining": round(max(0, remaining_years), 2),
            "sub_periods": sub_period_list
        })
    
    current_dasha = dasha_intervals[0]["mahadasha"] if dasha_intervals else None
    
    return {
        "birth_date": birth_date,
        "moon_nakshatra": NAKSHATRAS[nakshatra_idx],
        "moon_nakshatra_lord": nakshatra_lord,
        "current_dasha": current_dasha,
        "dasha_sequence": dasha_intervals,
        "message": f"Moon is in {NAKSHATRAS[nakshatra_idx]} nakshatra, ruled by {nakshatra_lord}. Currently running {current_dasha} Mahadasha."
    }

def generate_yearly_predictions(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC", years: int = 10) -> Dict[str, Any]:
    try:
        dt = datetime.fromisoformat(f"{birth_date}T{birth_time}")
    except:
        return {"error": "Invalid date/time format. Use ISO format: YYYY-MM-DD HH:MM"}

    try:
        tz = pytz.timezone(timezone)
        dt = tz.localize(dt) if dt.tzinfo is None else dt
    except:
        dt = pytz.utc.localize(dt)

    chart = calculate_natal_chart(birth_date, birth_time, latitude, longitude, timezone)
    if "error" in chart:
        return chart

    birth_jd = datetime_to_julian_day(dt)
    positions = calculate_planet_positions(birth_jd, latitude, longitude)

    moon_degree = positions.get("Moon", 0)
    nakshatra_idx = int((moon_degree % 360) / 13.333) % 27
    nakshatra_lord = NAKSHATRA_LORDS[nakshatra_idx]

    dasha_order = VIMSHOTTARI_MAHADASHA_ORDER
    start_idx = dasha_order.index(nakshatra_lord) if nakshatra_lord in dasha_order else 0

    md_timeline = []
    cum = 0.0
    for i in range(9):
        pi = (start_idx + i) % 9
        planet = dasha_order[pi]
        d_years = VIMSHOTTARI_YEARS[planet]
        md_timeline.append({"planet": planet, "start": cum, "end": cum + d_years, "total": d_years})
        cum += d_years

    now = datetime.now(tz)
    current_jd = datetime_to_julian_day(now)
    elapsed = (current_jd - birth_jd) / 365.25

    total_vim_years = sum(VIMSHOTTARI_YEARS.values())
    current_year = now.year
    predictions = []

    _md_career = {
        "Sun": [
            "Career advancement and recognition take center stage as the Sun's radiant energy propels you into the professional spotlight. Leadership opportunities emerge naturally, and your confidence inspires trust in colleagues and superiors. This is your time to step into positions of authority and showcase your unique capabilities.",
            "Your professional authority grows significantly during this Sun-ruled period. Recognition from superiors and peers is likely, and opportunities to lead important projects or mentor others will present themselves. Assert your expertise boldly, as the cosmos supports your rise in stature."
        ],
        "Moon": [
            "Your career path benefits from emotional intelligence and intuitive decision-making during this Moon-ruled period. You find greater satisfaction in roles that allow you to nurture and support others. Trust your instincts when evaluating professional opportunities, as your emotional radar is exceptionally accurate.",
            "Professional growth comes through enhanced emotional connections with colleagues and clients. Your ability to read people and situations gives you a subtle but powerful advantage in negotiations and teamwork. Consider roles in counseling, hospitality, or caregiving that align with your nurturing energy."
        ],
        "Mars": [
            "Dynamic energy and competitive drive define your career landscape under Mars influence. You are naturally drawn to ambitious projects and may feel compelled to take bold risks. Channel this fiery energy strategically to achieve breakthroughs, but be mindful of impulsive decisions that could create unnecessary conflicts.",
            "Your professional ambition burns brightly as Mars fuels your desire for achievement. This is an excellent period for launching new initiatives, pursuing athletic or physically demanding careers, or taking on leadership roles that require decisive action. Your courage inspires others to follow your lead."
        ],
        "Mercury": [
            "Your communication skills and intellectual agility are your greatest professional assets during this Mercury-ruled period. Writing, speaking, negotiating, and problem-solving come naturally, making this an ideal time for roles in media, technology, or consulting. Your ability to adapt quickly gives you a competitive edge.",
            "Mercury's influence sharpens your mind and enhances your professional versatility. Networking proves exceptionally fruitful, and a conversation or idea exchange could lead to a significant career opportunity. Focus on clear communication and lifelong learning to maximize this period's potential."
        ],
        "Jupiter": [
            "Expansion and good fortune characterize your career path during Jupiter's benevolent influence. Opportunities for growth through higher education, international connections, or philosophical pursuits are strongly favored. Your optimism and generosity attract mentors and allies who help you reach new heights.",
            "Jupiter blesses your professional life with abundance and meaningful growth. Teaching, publishing, legal work, or any career that involves sharing wisdom aligns perfectly with this energy. Your reputation for integrity and vision positions you for significant advancement."
        ],
        "Venus": [
            "Venus graces your professional life with creativity, diplomacy, and opportunities in fields related to beauty, art, finance, or relationships. Your natural charm and ability to create harmony make you invaluable in collaborative environments. This is a favorable period for career advancement through social connections and negotiation.",
            "Your professional appeal is heightened under Venus's influence as your diplomatic skills and artistic sensibilities come to the forefront. Careers in design, fashion, beauty, finance, or the arts are especially favored. Your ability to build rapport and create win-win outcomes opens important doors."
        ],
        "Saturn": [
            "Saturn's disciplined energy brings a period of hard work, responsibility, and karmic lessons in your career. Progress may feel slow, but the foundations you build now are solid and enduring. Patience, persistence, and a methodical approach are rewarded with long-term success and earned authority.",
            "Your career demands discipline and perseverance during this Saturn-ruled period. Challenges and delays test your commitment, but each obstacle is a lesson that prepares you for greater responsibility. Structure, planning, and consistent effort are the keys to professional advancement now."
        ],
        "Rahu": [
            "Rahu's influence brings sudden changes, worldly ambitions, and foreign connections into your career sphere. You may feel drawn to unconventional paths, technology, or opportunities abroad. Your ambition intensifies, driving you toward material success through innovative or nontraditional means.",
            "Professional life takes unexpected turns under Rahu's unpredictable energy. Foreign travel, international business, technology, or research fields may play a significant role. Your hunger for advancement is strong, but stay rooted in ethics to ensure that rapid success is built on a solid foundation."
        ],
        "Ketu": [
            "Ketu's spiritual energy turns your focus inward, making this a period of introspection and detachment in your career. Material ambitions may feel less important as you seek deeper meaning in your work. This is an excellent time for research, spiritual pursuits, or completing unfinished business before a new beginning.",
            "Your career path takes a contemplative turn under Ketu's influence as you question the purpose behind your professional efforts. Roles in research, spirituality, healing, or academia align with this energy. Embracing simplicity and letting go of ego-driven ambitions brings unexpected clarity."
        ]
    }

    _md_love = {
        "Sun": [
            "Your warmth and charisma make you magnetic in love during this Sun-ruled period. Confidence and generosity in romance attract admirers, but true intimacy requires vulnerability beneath the shining exterior. Existing relationships are revitalized as your partner basks in your radiant attention and loyalty.",
            "Love takes on a passionate, confident tone as the Sun empowers your romantic life. Your natural leadership in relationships creates a dynamic where your partner feels both inspired and cherished. Single natives may meet someone through creative or professional settings who admires your strength and vitality."
        ],
        "Moon": [
            "Emotional depth and nurturing define your love life during this Moon-ruled period. Your sensitivity allows you to connect with your partner on a profound emotional level, creating an atmosphere of trust and understanding. Family matters and home life take on greater significance in your romantic landscape.",
            "Your intuitive understanding of your partner's needs deepens as the Moon heightens your emotional perception. This is a powerful time for healing old relationship wounds through honest communication and gentle care. Single natives are drawn to partners who offer emotional security and genuine tenderness."
        ],
        "Mars": [
            "Passion and intensity characterize your romantic life under Mars influence. Your desire nature is heightened, and you pursue what you want with bold determination. While this creates exciting chemistry, be mindful of conflicts arising from impulsiveness or a competitive dynamic with your partner.",
            "Mars ignites your romantic drive with fiery passion and irresistible confidence. Existing relationships experience a renewed spark of excitement and physical connection. Single natives may encounter a dynamic, compelling person who challenges and excites them in equal measure."
        ],
        "Mercury": [
            "Intellectual connection takes priority in love during Mercury's influence. Stimulating conversations and shared ideas form the foundation of romantic attraction. Your wit and charm make you captivating, but remember that emotional expression matters as much as clever words in matters of the heart.",
            "Communication is the key to romantic fulfillment under Mercury's rule. Your ability to express your feelings articulately strengthens your bond with your partner. Single natives are most likely to connect with someone who engages their mind first and captures their heart through meaningful dialogue."
        ],
        "Jupiter": [
            "Love expands in beautiful ways during Jupiter's benefic influence. Existing relationships grow through shared adventures, travel, or educational pursuits that bring you closer together. Your optimism and generosity create a harmonious atmosphere where love can flourish abundantly.",
            "Jupiter blesses your romantic life with joy, expansion, and meaningful growth. This is a favorable period for marriage proposals, deepening commitments, or meeting someone through spiritual or educational settings. Your generous heart attracts partners who appreciate your warmth and wisdom."
        ],
        "Venus": [
            "Venus, the planet of love, blesses your romantic life with harmony, pleasure, and deep affection. Your sensual nature is heightened, and you attract love effortlessly through your grace and charm. This is one of the most favorable periods for romance, creativity, and strengthening intimate bonds.",
            "Love flows with grace and beauty during Venus's direct influence on your relationship sector. Existing partnerships are bathed in harmony and mutual appreciation, while single natives have exceptional chances of meeting someone truly compatible. Indulge in romance, art, and the pleasures of shared intimacy."
        ],
        "Saturn": [
            "Saturn's influence in love brings seriousness, commitment, and karmic relationship lessons. Existing bonds are tested and strengthened through challenges that reveal their true foundation. This is not a time for casual romance but for building lasting, mature partnerships based on mutual respect and responsibility.",
            "Relationships take on a mature, committed tone under Saturn's disciplined energy. You may feel the weight of relationship responsibilities or face delays in romantic matters. These challenges serve to strengthen your foundation — partnerships that endure this period are built to last a lifetime."
        ],
        "Rahu": [
            "Rahu brings intensity and unexpected developments to your love life. You may be drawn to unconventional relationships, cross-cultural connections, or partners from foreign lands. Your desires intensify, creating a magnetic attraction to the mysterious or forbidden, but discernment is needed to distinguish genuine connection from illusion.",
            "Love takes unpredictable turns under Rahu's influence as you find yourself attracted to people who are very different from your usual type. Foreign connections, online relationships, or unusual circumstances bring romantic opportunities. Stay grounded in your values to navigate this exciting but potentially destabilizing energy."
        ],
        "Ketu": [
            "Ketu's spiritual energy brings a period of detachment and reflection in romantic matters. You may feel less interested in conventional relationships and more drawn to solitude or spiritual connection. This is a powerful time for releasing old relationship patterns that no longer serve your highest good.",
            "Your approach to love becomes more philosophical under Ketu's influence as you seek soul-level connections rather than superficial romance. Past-life patterns in relationships may surface for healing. Embracing periods of solitude allows you to clarify what your heart truly desires."
        ]
    }

    _md_finance = {
        "Sun": [
            "Financial prosperity comes through leadership and career advancement during this Sun-ruled period. Your earning potential brightens as your professional reputation grows. Avoid ostentatious spending to maintain an image — invest in assets that appreciate and reflect your true worth.",
            "Your financial sector is illuminated by the Sun, bringing opportunities for income growth through recognition and advancement. This is a favorable time to negotiate salary increases or pursue monetization of your creative talents. Generosity flows abundantly, but balance it with prudent saving."
        ],
        "Moon": [
            "Financial stability is tied to emotional security during this Moon-ruled period. Your spending may be influenced by moods, so practice mindful financial habits. Real estate, home-related investments, and ventures related to food, hospitality, or caregiving are financially favorable.",
            "Your financial intuition is strong under the Moon's influence, making this a good period for trusting your gut feelings about investments. Income may come through nurturing professions or home-based businesses. Creating a budget that honors your need for emotional and material security brings peace of mind."
        ],
        "Mars": [
            "Mars drives your financial ambition with bold energy and a willingness to take calculated risks. This is a favorable period for launching new ventures, pursuing competitive opportunities, or increasing your income through assertive action. Avoid impulsive spending driven by impatience or ego.",
            "Your earning power is energized by Mars as you pursue financial goals with determination and courage. Entrepreneurial ventures, commission-based work, or performance-based bonuses are particularly lucrative. Channel your competitive spirit into wealth-building rather than unnecessary material competition."
        ],
        "Mercury": [
            "Financial opportunities multiply through your communication skills and intellectual agility during Mercury's influence. Side hustles, freelance work, consulting, or ventures involving writing, teaching, or technology prove profitable. Your ability to spot market trends and negotiate favorable terms is enhanced.",
            "Mercury sharpens your financial acumen, making this an ideal period for reviewing budgets, optimizing investments, and seeking new income streams. Your versatility opens doors to multiple revenue sources. Stay organized and avoid scattering your resources across too many ventures at once."
        ],
        "Jupiter": [
            "Jupiter brings expansion and abundance to your financial life, making this one of the most favorable periods for wealth accumulation. Educational investments, international ventures, and opportunities in teaching, publishing, or law are particularly lucrative. Your optimism attracts prosperity, but maintain practical oversight.",
            "Financial growth accelerates under Jupiter's beneficent gaze as your wise decisions and generous spirit attract abundance. This is an excellent time for long-term investments, especially in education, travel, or ventures that expand your horizons. Your prosperity serves a higher purpose — use it to create value for others."
        ],
        "Venus": [
            "Venus blesses your financial life with comfort and material pleasures during its influence. Income from creative arts, beauty, fashion, design, or relationship-oriented professions flourishes. Your appreciation for quality and beauty can be monetized, but be mindful of overspending on luxury and indulgence.",
            "Financial harmony prevails under Venus as your ability to create value through aesthetic and social channels is enhanced. Partnerships and collaborations prove financially rewarding. This is a favorable period for investments in art, beauty, or luxury goods, but balance enjoyment with practical savings."
        ],
        "Saturn": [
            "Saturn brings a period of financial discipline, where patience and careful planning are essential. Progress may feel slow, but the wealth you build now is solid and enduring. Avoid risky investments and focus on long-term assets, retirement planning, and debt reduction. Your hard work in this period yields lasting financial security.",
            "Your financial life requires discipline and strategic planning under Saturn's influence. Delays in expected income or increased responsibilities may create temporary pressure, but these challenges teach valuable lessons in resource management. Building wealth slowly through consistent effort and prudent investments is the path to lasting prosperity."
        ],
        "Rahu": [
            "Rahu brings sudden financial opportunities and a strong desire for material advancement. Foreign investments, technology ventures, or unconventional income streams may prove surprisingly profitable. Your ambition for wealth intensifies, but due diligence is essential to distinguish genuine opportunities from enticing illusions.",
            "Financial surprises unfold under Rahu's unpredictable energy as unexpected windfalls or opportunities from foreign sources may arise. Your appetite for risk increases, and speculative ventures could bring rapid gains if approached with careful research. Ground your ambitions in reality to avoid overextension."
        ],
        "Ketu": [
            "Ketu's influence brings a period of financial detachment where material concerns take a back seat to spiritual priorities. This is a time for simplifying your finances, releasing attachment to possessions, and clearing debts. Unexpected expenses related to closure or completion may arise, making way for a fresh start.",
            "Your relationship with money undergoes a spiritual recalibration under Ketu's energy. You may feel less driven to accumulate wealth and more interested in financial freedom through minimalism. Completing old financial obligations and letting go of material attachments creates space for new abundance in the next cycle."
        ]
    }

    _md_health = {
        "Sun": [
            "Your vitality and overall health are strong during this Sun-ruled period, with abundant energy for pursuing your goals. The heart and spine are your focal areas — regular cardiovascular exercise and good posture are essential. Your natural radiance serves you well, but avoid burnout from overwork and remember that rest fuels sustainable energy.",
            "The Sun bestows vibrant health and a strong constitution during this period. Your life force is high, making this an excellent time for beginning new fitness regimens or outdoor activities. Pay attention to your heart health and practice stress management to maintain your radiant vitality."
        ],
        "Moon": [
            "Your emotional and physical health are deeply connected during this Moon-ruled period. Stress or emotional turmoil can manifest as digestive issues or water retention. Prioritize emotional wellbeing through journaling, therapy, or time in nature. Water-based activities like swimming provide healing and balance.",
            "The Moon's influence makes your health sensitive to your emotional state. Nurturing routines that include adequate sleep, proper hydration, and a balanced diet are essential. Your body responds well to gentle, consistent care rather than intense or extreme regimens. Prioritize rest and emotional nourishment."
        ],
        "Mars": [
            "Mars fills you with dynamic energy and physical drive during its influence, making this an excellent period for vigorous exercise and athletic pursuits. However, your tendency to push too hard can lead to injuries, inflammation, or accidents. Headaches, fevers, or inflammatory conditions may arise if stress is not managed properly.",
            "Your physical energy is high under Mars, channel it into structured physical activity like martial arts, HIIT, or competitive sports. Your immune system is active, but your propensity for accidents increases when you rush. Practice patience and warm up properly before physical exertion to prevent injuries."
        ],
        "Mercury": [
            "Your health is closely tied to your nervous system during Mercury's influence. Anxiety, restlessness, or overthinking can manifest as digestive issues, sleep problems, or tension headaches. Mental stimulation is essential, but balance it with calming practices like meditation or breathwork to keep your nervous system regulated.",
            "Mercury's energy keeps your mind active and your body on the move, but your nervous system needs conscious care. Respiratory health, hands, and digestion are areas to watch. Practices that calm the mind, such as yoga or tai chi, combined with adequate rest, will keep your system balanced and resilient."
        ],
        "Jupiter": [
            "Jupiter blesses you with robust health and a strong constitution during its benefic influence. Your natural optimism supports healing and recovery. However, Jupiter's expansive energy can lead to overindulgence in food, drink, or pleasure, potentially causing weight gain or liver issues. Moderation is the key to maintaining your wellbeing.",
            "Your overall health outlook is positive under Jupiter's influence as your body responds well to holistic healing approaches. The liver, hips, and thighs are areas to monitor. This is an excellent period for adopting a more generous approach to self-care — prioritize whole foods, joyful movement, and practices that nurture both body and spirit."
        ],
        "Venus": [
            "Venus brings harmony to your health sector, encouraging gentle, pleasurable approaches to wellbeing. Your body responds beautifully to activities that combine movement with beauty, such as dance, yoga, or nature walks. The throat, kidneys, and skin are sensitive areas that require attention and gentle care.",
            "Your health thrives on pleasure and harmony under Venus's influence. Indulging in life's luxuries in moderation supports your wellbeing — think nourishing meals, gentle movement, and adequate rest. Your body's natural balance is strong, making this a good period for beauty treatments, massage, and other rejuvenating practices."
        ],
        "Saturn": [
            "Saturn's influence demands discipline and attention to your physical structure. Bones, joints, teeth, and knees require extra care during this period. Chronic conditions may need ongoing management, and the pace of life slows, requiring you to honor your need for adequate rest and recovery. Consistency in health routines is your greatest ally.",
            "Your health requires a disciplined, structured approach under Saturn's energy. Long-term wellness depends on the habits you establish now — prioritize bone health through weight-bearing exercise, adequate calcium, and vitamin D. Patience with your body's limitations and consistent self-care build a foundation for lasting vitality."
        ],
        "Rahu": [
            "Rahu brings unusual or stress-related health conditions that may be difficult to diagnose through conventional means. Your immune system needs support, and stress-related disorders, skin issues, or mysterious symptoms may arise. Alternative healing modalities and a holistic approach to health are particularly effective during this period.",
            "Your health requires vigilant attention under Rahu's unpredictable influence as stress and lifestyle factors may manifest in unexpected ways. Sleep disorders, anxiety, or unusual symptoms should not be ignored. Prioritize detoxification, regular health checkups, and grounding practices that connect you to your body's wisdom."
        ],
        "Ketu": [
            "Ketu's energy turns your attention to spiritual and mental health during its influence. Physical vitality may feel diminished as your energy is directed inward. This is a powerful period for healing through meditation, energy work, or spiritual practices. Mysterious or psychosomatic conditions may surface for resolution — trust your intuition about the root causes.",
            "Your health takes on a spiritual dimension under Ketu as you become more attuned to subtle energies within your body. This is a favorable time for detoxification, fasting, or cleanses that release accumulated toxins. Chronic or recurring health issues may reach a point of resolution as you release old patterns stored in your body."
        ]
    }

    _md_theme = {
        "Sun": "A period of radiant self-expression and empowered leadership. The universe calls you to step into the spotlight, own your authority, and let your authentic light shine without apology.",
        "Moon": "A season of emotional nurturing and intuitive growth. The cosmos encourages you to tend to your emotional foundations, deepen your relationships, and trust the wisdom of your heart.",
        "Mars": "A dynamic phase of courageous action and passionate pursuit. The universe supports bold moves and assertive energy, channeling your drive toward meaningful achievements.",
        "Mercury": "A time of intellectual expansion and vibrant communication. The stars align to enhance your mental agility, social connections, and ability to adapt and thrive through the power of your words.",
        "Jupiter": "A fortunate cycle of expansion, wisdom, and abundant growth. The cosmos showers you with opportunities to broaden your horizons through learning, travel, and meaningful connections.",
        "Venus": "A harmonious period of love, beauty, and creative fulfillment. The universe invites you to indulge in life's pleasures, deepen your relationships, and surround yourself with grace and elegance.",
        "Saturn": "A karmic phase of discipline, responsibility, and enduring achievement. The stars ask you to build patiently, honor your commitments, and trust that hard work now creates unshakable foundations.",
        "Rahu": "An unpredictable cycle of ambition, innovation, and worldly desires. The cosmos propels you toward unconventional paths, foreign connections, and material pursuits that expand your experience of reality.",
        "Ketu": "A spiritual season of detachment, introspection, and profound release. The universe guides you to let go of what no longer serves you and discover freedom through inner wisdom and surrender."
    }

    _ad_blends = {
        "Sun": "The Sun's confident energy amplifies your self-expression and leadership qualities, giving you the courage to pursue your ambitions with clarity and purpose.",
        "Moon": "The Moon's nurturing influence adds emotional depth and intuitive sensitivity, encouraging you to trust your feelings and seek comfort in meaningful connections.",
        "Mars": "Mars brings dynamic energy and assertive drive, pushing you to take decisive action and pursue your goals with passionate determination.",
        "Mercury": "Mercury enhances your communication skills and mental agility, making this an ideal time for learning, networking, and expressing your ideas with clarity.",
        "Jupiter": "Jupiter's expansive presence brings optimism, wisdom, and good fortune, encouraging growth through generosity, education, and a broader perspective on life.",
        "Venus": "Venus adds harmony, beauty, and a touch of grace, softening challenges with charm and reminding you to find pleasure and connection in everyday moments.",
        "Saturn": "Saturn's disciplined influence brings structure and responsibility, teaching patience and perseverance while building foundations that will stand the test of time.",
        "Rahu": "Rahu introduces ambition, innovation, and a hunger for new experiences, pushing you beyond your comfort zone into uncharted territory.",
        "Ketu": "Ketu's spiritual energy encourages introspection and release, helping you detach from material concerns and connect with deeper truths."
    }

    _md_rating_base = {
        "Sun": 8, "Moon": 7, "Mars": 6, "Mercury": 7,
        "Jupiter": 9, "Venus": 8, "Saturn": 5, "Rahu": 5, "Ketu": 4
    }

    _ad_rating_mod = {
        "Sun": 0, "Moon": 1, "Mars": -1, "Mercury": 1,
        "Jupiter": 1, "Venus": 1, "Saturn": -1, "Rahu": -1,         "Ketu": -1
    }

    _reasoning_md_career = {
        "Sun": "Sun (Mahadasha lord) illuminates your career sector, bringing recognition and leadership opportunities",
        "Moon": "Moon (Mahadasha lord) nurtures your professional environment through emotional intelligence and public appeal",
        "Mars": "Mars (Mahadasha lord) drives your professional ambition with dynamic energy and competitive spirit",
        "Mercury": "Mercury (Mahadasha lord) enhances your communication skills and intellectual agility at work",
        "Jupiter": "Jupiter (Mahadasha lord) expands your career through wisdom, higher learning, and fortunate opportunities",
        "Venus": "Venus (Mahadasha lord) brings creativity, diplomacy, and harmonious professional relationships to your career",
        "Saturn": "Saturn (Mahadasha lord) brings discipline and karmic lessons to your career, rewarding patience and persistence",
        "Rahu": "Rahu (Mahadasha lord) propels your career toward innovation, foreign connections, and unconventional paths",
        "Ketu": "Ketu (Mahadasha lord) turns your career focus toward research, spirituality, and meaningful detachment from material ambition"
    }
    _reasoning_ad_career = {
        "Sun": "while the Sun (Antardasha lord) adds confidence and professional visibility to your efforts",
        "Moon": "while the Moon (Antardasha lord) adds emotional depth and public appeal to your professional life",
        "Mars": "while Mars (Antardasha lord) adds competitive drive and bold initiative to your career pursuits",
        "Mercury": "while Mercury (Antardasha lord) enhances your networking and communication abilities",
        "Jupiter": "while Jupiter (Antardasha lord) brings expansion and good fortune to your career path",
        "Venus": "while Venus (Antardasha lord) adds creative flair and diplomatic skills to your professional interactions",
        "Saturn": "while Saturn (Antardasha lord) ensures steady, sustainable growth through disciplined effort",
        "Rahu": "while Rahu (Antardasha lord) brings unexpected breakthroughs and innovative approaches",
        "Ketu": "while Ketu (Antardasha lord) brings spiritual depth and intuitive wisdom to your decision-making"
    }
    _reasoning_md_love = {
        "Sun": "Sun (Mahadasha lord) radiates warmth and confidence in your romantic life, making you more attractive and charismatic",
        "Moon": "Moon (Mahadasha lord) deepens emotional sensitivity and nurtures your capacity for intimate connection",
        "Mars": "Mars (Mahadasha lord) ignites passion and romantic drive, bringing intensity and excitement to relationships",
        "Mercury": "Mercury (Mahadasha lord) emphasizes intellectual rapport and lively communication in your love life",
        "Jupiter": "Jupiter (Mahadasha lord) brings expansion and generosity to your relationships, fostering growth and commitment",
        "Venus": "Venus (Mahadasha lord) blesses your love life with harmony, beauty, and deep romantic fulfillment",
        "Saturn": "Saturn (Mahadasha lord) brings commitment, maturity, and karmic relationship lessons to your love life",
        "Rahu": "Rahu (Mahadasha lord) creates magnetic attraction and unexpected romantic opportunities with foreign or unconventional partners",
        "Ketu": "Ketu (Mahadasha lord) brings spiritual evolution through love, encouraging soul-level connections and releasing past patterns"
    }
    _reasoning_ad_love = {
        "Sun": "while the Sun (Antardasha lord) adds passionate warmth and confident self-expression to your relationships",
        "Moon": "while the Moon (Antardasha lord) adds emotional depth and nurturing care to your romantic bond",
        "Mars": "while Mars (Antardasha lord) adds passionate intensity and bold romantic gestures",
        "Mercury": "while Mercury (Antardasha lord) encourages open communication and intellectual connection in love",
        "Jupiter": "while Jupiter (Antardasha lord) brings joy, expansion, and a spirit of generosity to your relationship",
        "Venus": "while Venus (Antardasha lord) enhances romance, sensuality, and affectionate harmony between partners",
        "Saturn": "while Saturn (Antardasha lord) strengthens commitment and encourages mature, lasting partnership",
        "Rahu": "while Rahu (Antardasha lord) brings excitement, novelty, and unexpected romantic encounters",
        "Ketu": "while Ketu (Antardasha lord) fosters spiritual connection and helps release old emotional patterns"
    }
    _reasoning_md_finance = {
        "Sun": "Sun (Mahadasha lord) illuminates your financial potential through career advancement and recognized authority",
        "Moon": "Moon (Mahadasha lord) links your financial wellbeing to emotional security and intuitive investment decisions",
        "Mars": "Mars (Mahadasha lord) energizes your earning potential through bold initiatives and competitive drive",
        "Mercury": "Mercury (Mahadasha lord) sharpens your financial acumen, creating opportunities through communication and intellect",
        "Jupiter": "Jupiter (Mahadasha lord) expands your wealth through wise investments, education, and generous abundance",
        "Venus": "Venus (Mahadasha lord) blesses your finances through creative pursuits, social connections, and material comforts",
        "Saturn": "Saturn (Mahadasha lord) demands financial discipline and patience, building lasting wealth through consistent effort",
        "Rahu": "Rahu (Mahadasha lord) brings unconventional financial opportunities and sudden gains through innovation",
        "Ketu": "Ketu (Mahadasha lord) encourages financial detachment and simplifying your relationship with material wealth"
    }
    _reasoning_ad_finance = {
        "Sun": "while the Sun (Antardasha lord) boosts your earning capacity through increased confidence and visibility",
        "Moon": "while the Moon (Antardasha lord) adds intuitive guidance and emotional balance to your financial decisions",
        "Mars": "while Mars (Antardasha lord) drives assertive wealth-building actions and calculated financial risks",
        "Mercury": "while Mercury (Antardasha lord) enhances your ability to negotiate and spot profitable opportunities",
        "Jupiter": "while Jupiter (Antardasha lord) brings financial expansion through wise investments and fortunate timing",
        "Venus": "while Venus (Antardasha lord) brings financial gains through social connections and creative ventures",
        "Saturn": "while Saturn (Antardasha lord) encourages prudent saving and long-term financial planning",
        "Rahu": "while Rahu (Antardasha lord) brings unexpected income through unconventional or foreign sources",
        "Ketu": "while Ketu (Antardasha lord) encourages simplifying finances and releasing attachment to material wealth"
    }
    _reasoning_md_health = {
        "Sun": "Sun (Mahadasha lord) governs your vitality and overall life force, strengthening your constitution and immune system",
        "Moon": "Moon (Mahadasha lord) influences your emotional wellbeing and digestive health through its connection to body rhythms",
        "Mars": "Mars (Mahadasha lord) governs your physical energy and immune response but can increase inflammation and injury risk",
        "Mercury": "Mercury (Mahadasha lord) rules your nervous system and communication between body and mind",
        "Jupiter": "Jupiter (Mahadasha lord) blesses you with robust health but warns against overindulgence affecting the liver",
        "Venus": "Venus (Mahadasha lord) governs your reproductive system, skin, and overall sense of physical harmony",
        "Saturn": "Saturn (Mahadasha lord) governs bones, joints, and chronic conditions, demanding disciplined health routines",
        "Rahu": "Rahu (Mahadasha lord) brings stress-related and hard-to-diagnose health conditions requiring holistic care",
        "Ketu": "Ketu (Mahadasha lord) turns your attention to spiritual healing and releasing deep-seated health patterns"
    }
    _reasoning_ad_health = {
        "Sun": "while the Sun (Antardasha lord) boosts your vitality and supports cardiovascular health",
        "Moon": "while the Moon (Antardasha lord) encourages emotional balance and proper rest for overall wellbeing",
        "Mars": "while Mars (Antardasha lord) energizes your physical fitness but requires caution against accidents",
        "Mercury": "while Mercury (Antardasha lord) supports nervous system health and mental clarity",
        "Jupiter": "while Jupiter (Antardasha lord) promotes healing through optimism and holistic health practices",
        "Venus": "while Venus (Antardasha lord) supports hormonal balance and gentle, pleasurable approaches to health",
        "Saturn": "while Saturn (Antardasha lord) encourages structural health through consistent routines and bone care",
        "Rahu": "while Rahu (Antardasha lord) requires vigilance against stress-related and unusual health symptoms",
        "Ketu": "while Ketu (Antardasha lord) supports deep healing through spiritual practices and detoxification"
    }

    _career_prep = {
        "Sun": "Build your public profile and take on leadership roles in the coming months",
        "Moon": "Trust your intuition in professional matters and nurture your workplace relationships",
        "Mars": "Channel your competitive drive into strategic career moves and bold initiatives",
        "Mercury": "Invest in learning new skills and expanding your professional network",
        "Jupiter": "Pursue educational opportunities and seek mentors who can expand your horizons",
        "Venus": "Leverage your diplomatic skills and creative talents for career advancement",
        "Saturn": "Focus on consistent daily discipline and long-term career planning",
        "Rahu": "Embrace innovation and explore unconventional career paths or foreign opportunities",
        "Ketu": "Take time for introspection about your true career calling and release ego-driven ambitions"
    }
    _love_prep = {
        "Sun": "Show up with confidence and generosity in your relationships \u2014 your warmth is your greatest asset",
        "Moon": "Prioritize emotional honesty and create a safe space for vulnerability with your partner",
        "Mars": "Balance passion with patience \u2014 your drive to connect is powerful, but let love unfold naturally",
        "Mercury": "Communicate openly and listen deeply \u2014 meaningful conversations are the foundation of love now",
        "Jupiter": "Plan romantic adventures and shared growth experiences to deepen your bond",
        "Venus": "Create romantic moments filled with beauty and affection — your natural charm attracts love effortlessly",
        "Saturn": "Demonstrate your commitment through reliable actions and build trust steadily over time",
        "Rahu": "Stay grounded in your values while exploring exciting new dimensions of your relationship",
        "Ketu": "Release old relationship patterns and trust that solitude can be deeply clarifying for your heart"
    }
    _finance_prep = {
        "Sun": "Invest in your professional brand and negotiate your worth \u2014 recognition leads to raises",
        "Moon": "Create a budget that honors your emotional needs while building a secure financial foundation",
        "Mars": "Take calculated risks in investments and pursue aggressive savings goals",
        "Mercury": "Research multiple income streams and consult experts before making financial decisions",
        "Jupiter": "Invest in education and long-term assets that grow in value over time",
        "Venus": "Monetize your creative talents and build partnerships that generate shared wealth",
        "Saturn": "Create a strict savings plan and focus on debt reduction for long-term stability",
        "Rahu": "Explore innovative investment opportunities but conduct thorough due diligence",
        "Ketu": "Simplify your finances and clear outstanding debts before making new commitments"
    }
    _health_prep = {
        "Sun": "Prioritize cardiovascular exercise and maintain a consistent sleep schedule for optimal vitality",
        "Moon": "Focus on emotional wellness through journaling, therapy, or time in nature",
        "Mars": "Channel excess energy into structured physical activities and warm up properly before exercise",
        "Mercury": "Practice stress management techniques like meditation and ensure adequate mental rest",
        "Jupiter": "Adopt a balanced approach to diet and exercise \u2014 moderation is key to sustaining good health",
        "Venus": "Incorporate gentle movement like yoga or dance and prioritize relaxation and self-care",
        "Saturn": "Establish consistent health routines with emphasis on bone health and joint care",
        "Rahu": "Schedule regular health checkups and explore holistic or alternative healing modalities",
        "Ketu": "Embrace detoxification practices and spiritual healing to release deep-seated imbalances"
    }

    import random as _r

    def _pick(lst, seed_val):
        idx = hash(str(seed_val)) % len(lst)
        return lst[idx]

    for y in range(years):
        year_num = current_year + y
        year_mid_elapsed = elapsed + y + 0.5

        md_entry = None
        for m in md_timeline:
            if m["start"] <= year_mid_elapsed < m["end"]:
                md_entry = m
                break

        if md_entry is None:
            md_entry = md_timeline[-1]

        md_planet = md_entry["planet"]
        md_relative = year_mid_elapsed - md_entry["start"]
        sub_periods = VIMSHOTTARI_SUB_PERIODS[md_planet]
        ad_planet = sub_periods[-1]
        sub_cum = 0.0
        for sp in sub_periods:
            sp_years = (VIMSHOTTARI_YEARS[sp] / total_vim_years) * md_entry["total"]
            if sub_cum <= md_relative < sub_cum + sp_years:
                ad_planet = sp
                break
            sub_cum += sp_years

        age = year_num - dt.year
        if (dt.month, dt.day) > (7, 1):
            age -= 1
        age = max(0, age)

        care = _pick(_md_career[md_planet], f"{md_planet}{ad_planet}{year_num}career")
        love = _pick(_md_love[md_planet], f"{md_planet}{ad_planet}{year_num}love")
        fin = _pick(_md_finance[md_planet], f"{md_planet}{ad_planet}{year_num}fin")
        heal = _pick(_md_health[md_planet], f"{md_planet}{ad_planet}{year_num}health")
        theme = _md_theme[md_planet]
        ad_blend = _ad_blends[ad_planet]

        care += f" On the sub-period level, {ad_blend}"
        love += f" With {ad_planet} as your sub-period ruler, {ad_blend[0].lower() + ad_blend[1:]}"
        fin += f" The {ad_planet} sub-period adds the following nuance: {ad_blend}"
        heal += f" Under the {ad_planet} sub-influence, {ad_blend[0].lower() + ad_blend[1:]}"

        rating = _md_rating_base[md_planet] + _ad_rating_mod[ad_planet]
        rating = max(1, min(10, rating))

        conf_base = 50 + _md_rating_base[md_planet] * 5 + _ad_rating_mod[ad_planet] * 2
        career_conf = max(10, min(99, conf_base))
        love_conf = max(10, min(99, conf_base - 2))
        finance_conf = max(10, min(99, conf_base + 1))
        health_conf = max(10, min(99, conf_base - 1))

        career_reasoning = _reasoning_md_career[md_planet] + ", while " + _reasoning_ad_career[ad_planet]
        love_reasoning = _reasoning_md_love[md_planet] + ", while " + _reasoning_ad_love[ad_planet]
        finance_reasoning = _reasoning_md_finance[md_planet] + ", while " + _reasoning_ad_finance[ad_planet]
        health_reasoning = _reasoning_md_health[md_planet] + ", while " + _reasoning_ad_health[ad_planet]

        ad_start_abs = md_entry["start"] + sub_cum
        ad_end_abs = ad_start_abs + sp_years
        year_start_abs = elapsed + y
        year_end_abs = year_start_abs + 1
        window_start = max(ad_start_abs, year_start_abs)
        window_end = min(ad_end_abs, year_end_abs)
        start_month = max(1, min(12, int((window_start - year_start_abs) * 12) + 1))
        end_month = max(1, min(12, int((window_end - year_start_abs) * 12) + 1))
        _mn = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        best_window = f"Peak period: {_mn[start_month]}-{_mn[end_month]} {year_num}"

        predictions.append({
            "year": year_num,
            "age": age,
            "mahadasha": md_planet,
            "antardasha": ad_planet,
            "career": {
                "prediction": care,
                "confidence": career_conf,
                "reasoning": career_reasoning,
                "best_window": best_window,
                "preparation": _career_prep[md_planet]
            },
            "love": {
                "prediction": love,
                "confidence": love_conf,
                "reasoning": love_reasoning,
                "best_window": best_window,
                "preparation": _love_prep[md_planet]
            },
            "finance": {
                "prediction": fin,
                "confidence": finance_conf,
                "reasoning": finance_reasoning,
                "best_window": best_window,
                "preparation": _finance_prep[md_planet]
            },
            "health": {
                "prediction": heal,
                "confidence": health_conf,
                "reasoning": health_reasoning,
                "best_window": best_window,
                "preparation": _health_prep[md_planet]
            },
            "overall_theme": theme,
            "rating": rating
        })

    return {
        "predictions": predictions,
        "moon_nakshatra": NAKSHATRAS[nakshatra_idx],
        "moon_nakshatra_lord": nakshatra_lord,
        "chart_summary": {
            "sun_sign": chart.get("sun_sign"),
            "moon_sign": chart.get("moon_sign"),
            "rising_sign": chart.get("rising_sign")
        }
    }


def calculate_horary_kp(question: str, question_date: str, question_time: str, latitude: float, longitude: float) -> Dict:
    try:
        dt = datetime.strptime(f"{question_date} {question_time}", "%Y-%m-%d %H:%M")
    except:
        try:
            dt = datetime.strptime(f"{question_date} {question_time}", "%Y-%m-%d %H:%M:%S")
        except:
            return {"error": "Invalid date/time format"}
    
    jd = datetime_to_julian_day(dt)
    positions = calculate_planet_positions(jd, latitude, longitude)
    
    asc_degree = positions.get("Ascendant", 0)
    asc_sign = get_zodiac_sign(asc_degree)
    
    asc_nakshatra, asc_pada, asc_start, asc_lord = get_nakshatra(asc_degree)
    asc_sub_lord = NAKSHATRA_LORDS[NAKSHATRAS.index(asc_nakshatra)]
    
    horary_chart = {}
    for planet, degree in positions.items():
        if planet in PLANET_TO_NAKSHATRA_LORD:
            kp_info = get_kp_nakshatra(degree)
            horary_chart[planet] = kp_info
    
    horary_chart["Ascendant"] = {
        "nakshatra": asc_nakshatra,
        "lord": asc_lord,
        "sub_lord": asc_sub_lord,
        "pada": asc_pada,
        "degree": round(asc_degree, 2)
    }
    
    significator_planets = {
        "1": "Ascendant lord",
        "2": "Moon, Mercury",
        "3": "Mars, Mercury",
        "4": "Moon, Venus, Jupiter",
        "5": "Jupiter, Sun, Moon",
        "6": "Mars, Saturn, Rahu, Ketu",
        "7": "Venus, Moon, Saturn",
        "8": "Saturn, Rahu, Ketu",
        "9": "Jupiter, Sun, Moon",
        "10": "Sun, Jupiter, Saturn, Mercury",
        "11": "Jupiter, Uranus, Mercury",
        "12": "Saturn, Rahu, Ketu"
    }
    
    answer = determine_horary_answer(horary_chart, question)
    
    return {
        "question": question,
        "question_time": f"{question_date} {question_time}",
        "ascendant_sign": asc_sign,
        "ascendant_nakshatra": asc_nakshatra,
        "lord": asc_lord,
        "sub_lord": asc_sub_lord,
        "chart": horary_chart,
        "significators": significator_planets,
        "answer": answer
    }

def determine_horary_answer(chart: Dict, question: str) -> Dict:
    question_lower = question.lower()
    
    asc_lord = chart.get("Ascendant", {}).get("lord", "")
    moon = chart.get("Moon", {})
    moon_nakshatra = moon.get("nakshatra", "")
    moon_lord = moon.get("lord", "")
    
    if any(word in question_lower for word in ["marriage", "love", "partner", "relationship", "wedding"]):
        sign = "7th"
        significator = "Venus, Moon"
        desc = "Look at 7th house and Venus for relationship matters."
    elif any(word in question_lower for word in ["job", "career", "work", "promotion"]):
        sign = "10th"
        significator = "Sun, Saturn, Jupiter"
        desc = "10th house and Saturn indicate career matters."
    elif any(word in question_lower for word in ["money", "wealth", "finance", "income"]):
        sign = "2nd"
        significator = "Venus, Mercury, Moon"
        desc = "2nd house indicates wealth and finances."
    elif any(word in question_lower for word in ["health", "disease", "illness"]):
        sign = "6th"
        significator = "Mars, Saturn, Rahu"
        desc = "6th house and Mars indicate health matters."
    elif any(word in question_lower for word in ["child", "pregnancy", "birth"]):
        sign = "5th"
        significator = "Jupiter, Sun"
        desc = "5th house and Jupiter indicate children."
    elif any(word in question_lower for word in ["education", "study", "exam"]):
        sign = "4th"
        significator = "Moon, Jupiter, Mercury"
        desc = "4th house and Mercury indicate education."
    elif any(word in question_lower for word in ["travel", "journey", "trip"]):
        sign = "9th"
        significator = "Jupiter, Sun"
        desc = "9th house indicates travel and journeys."
    else:
        sign = "1st"
        significator = "Ascendant Lord"
        desc = "Look at Ascendant and its lord for general matters."
    
    return {
        "topic": "General Horary Analysis",
        "key_house": sign,
        "significators": significator,
        "analysis": desc,
        "ascendant_lord": asc_lord,
        "moon_nakshatra": moon_nakshatra,
        "verdict": f"Based on KP System: The {sign} house and {significator} are important. {desc} Moon is in {moon_nakshatra} ({moon_lord})."
    }

def calculate_panchang(date_str: str, latitude: float, longitude: float) -> Dict[str, Any]:
    try:
        dt = datetime.fromisoformat(date_str)
    except:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    jd = datetime_to_julian_day(dt)
    positions = calculate_planet_positions(jd, latitude, longitude)
    sun_deg = positions.get("Sun", 0)
    moon_deg = positions.get("Moon", 0)

    tithi_index = int(((moon_deg - sun_deg) % 360) // 12)
    tithi_names = [
        "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
        "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
        "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
    ]
    tithi_name = tithi_names[tithi_index] if tithi_index < len(tithi_names) else "Unknown"

    yoga_index = int(((moon_deg + sun_deg) % 360) // 13.333) % 27
    yoga_names = [
        "Vishkumbha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
        "Atiganda", "Sukarman", "Dhriti", "Shula", "Ganda",
        "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
        "Siddhi", "Vyatipata", "Variyana", "Parigha", "Shiva",
        "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
        "Indra", "Vaidhriti"
    ]
    yoga_name = yoga_names[yoga_index]

    karana_index = int(((moon_deg - sun_deg) % 360) // 6) % 11
    karana_names = ["Bava", "Balava", "Kaulava", "Taitila", "Garija", "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna"]
    karana_name = karana_names[karana_index]

    sunrise_hour = 6.0 + (longitude / 15.0) * 0.5
    solar_noon_hour = 12.0
    abhijit_start = solar_noon_hour - 0.4
    abhijit_end = solar_noon_hour + 0.4

    sunrise_str = f"{int(sunrise_hour):02d}:{int((sunrise_hour % 1) * 60):02d}"
    sunset_str = f"{int(18.0):02d}:{int(0):02d}"

    rahu_start_hour = (sunrise_hour + 8.0) % 24
    rahu_end_hour = (rahu_start_hour + 1.5) % 24

    tithi_start_hour = (sunrise_hour + tithi_index * 0.8) % 24
    tithi_end_hour = (tithi_start_hour + 0.8) % 24

    return {
        "tithi": {"name": tithi_name, "index": tithi_index + 1, "description": f"Tithi is {tithi_name} - the {tithi_index + 1}{'st' if tithi_index == 0 else 'nd' if tithi_index == 1 else 'rd' if tithi_index == 2 else 'th'} lunar phase", "start_time": f"{int(tithi_start_hour):02d}:{int((tithi_start_hour % 1) * 60):02d}", "end_time": f"{int(tithi_end_hour):02d}:{int((tithi_end_hour % 1) * 60):02d}"},
        "yoga": {"name": yoga_name, "index": yoga_index + 1, "description": f"Yoga is {yoga_name} - the {yoga_index + 1}{'st' if yoga_index == 0 else 'nd' if yoga_index == 1 else 'rd' if yoga_index == 2 else 'th'} of 27 yogas"},
        "karana": {"name": karana_name, "index": karana_index + 1, "description": f"Karana is {karana_name}"},
        "abhijit_muhurat": f"{int(abhijit_start):02d}:{int((abhijit_start % 1) * 60):02d} - {int(abhijit_end):02d}:{int((abhijit_end % 1) * 60):02d}",
        "sunrise": sunrise_str,
        "sunset": sunset_str,
        "rahu_kaal": f"{int(rahu_start_hour):02d}:{int((rahu_start_hour % 1) * 60):02d} - {int(rahu_end_hour):02d}:{int((rahu_end_hour % 1) * 60):02d}",
        "date": date_str,
        "city": "Custom Location"
    }

def calculate_wealth_prediction(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict[str, Any]:
    chart = calculate_natal_chart(birth_date, birth_time, latitude, longitude, timezone)
    if "error" in chart:
        return chart
    planets = chart.get("planets", {})
    houses = chart.get("houses", {})

    wealth_potential = "medium"
    investment_periods = []
    loss_periods = []
    lucky_years = []
    property_buying_periods = []

    venus = planets.get("Venus", {})
    jupiter = planets.get("Jupiter", {})
    mars = planets.get("Mars", {})
    saturn = planets.get("Saturn", {})
    sun = planets.get("Sun", {})

    venus_sign = venus.get("sign", "")
    jup_sign = jupiter.get("sign", "")
    mars_sign = mars.get("sign", "")
    sat_sign = saturn.get("sign", "")
    sun_sign_val = sun.get("sign", "")

    house_2 = houses.get("2", {}).get("sign", "")
    house_11 = houses.get("11", {}).get("sign", "")
    house_5 = houses.get("5", {}).get("sign", "")
    house_8 = houses.get("8", {}).get("sign", "")

    wealth_score = 0
    if venus_sign in ["Taurus", "Libra", "Pisces"]:
        wealth_score += 2
    if jup_sign in ["Sagittarius", "Pisces"]:
        wealth_score += 2
    if house_2 in ["Taurus", "Capricorn", "Virgo"]:
        wealth_score += 2
    if house_11 in ["Sagittarius", "Pisces", "Aries"]:
        wealth_score += 1
    if mars_sign in ["Capricorn", "Aries"]:
        wealth_score += 1
    if sun_sign_val in ["Leo"]:
        wealth_score += 1

    if wealth_score >= 6:
        wealth_potential = "high"
    elif wealth_score >= 3:
        wealth_potential = "medium"
    else:
        wealth_potential = "low"

    desc_parts = []
    if house_2:
        desc_parts.append(f"2nd house (accumulated wealth) is in {house_2}")
    if house_11:
        desc_parts.append(f"11th house (gains) is in {house_11}")
    if venus_sign:
        desc_parts.append(f"Venus (luxury) is placed in {venus_sign}")
    if jup_sign:
        desc_parts.append(f"Jupiter (expansion) is in {jup_sign}")

    import random as _rw
    seed = f"{birth_date}{birth_time}{latitude}{longitude}"
    rng = _rw.Random(seed)
    base_year = datetime.fromisoformat(f"{birth_date}T{birth_time}").year if "T" in birth_date else datetime.strptime(birth_date, "%Y-%m-%d").year
    for i in range(3):
        investment_periods.append(base_year + rng.randint(25 + i * 5, 35 + i * 5))
    for i in range(2):
        loss_periods.append(base_year + rng.randint(40 + i * 3, 50 + i * 3))
    for i in range(3):
        lucky_years.append(base_year + rng.randint(20 + i * 7, 30 + i * 7))
    for i in range(2):
        property_buying_periods.append(base_year + rng.randint(30 + i * 5, 45 + i * 5))

    confidence_score = max(50, min(wealth_score * 10 + 50, 99))

    venus_contribution = 2 if venus_sign in ["Taurus", "Libra", "Pisces"] else 0
    jupiter_contribution = 2 if jup_sign in ["Sagittarius", "Pisces"] else 0
    house_2_contribution = 2 if house_2 in ["Taurus", "Capricorn", "Virgo"] else 0
    house_11_contribution = 1 if house_11 in ["Sagittarius", "Pisces", "Aries"] else 0
    mars_contribution = 1 if mars_sign in ["Capricorn", "Aries"] else 0
    sun_contribution = 1 if sun_sign_val in ["Leo"] else 0

    wealth_reasoning_parts = []
    if venus_sign:
        wealth_reasoning_parts.append(f"Venus in {venus_sign}")
    if jup_sign:
        wealth_reasoning_parts.append(f"Jupiter in {jup_sign}")
    if house_2:
        wealth_reasoning_parts.append(f"2nd house in {house_2}")
    if house_11:
        wealth_reasoning_parts.append(f"11th house in {house_11}")
    reasoning = " + ".join(wealth_reasoning_parts) + f" = {wealth_potential} wealth indicators"

    best_inv = investment_periods[:2]
    best_investment_window = f"Best investment years: {best_inv[0]}-{best_inv[1]}" if len(best_inv) == 2 else ""

    prep_best = f"ages {best_inv[0]}-{best_inv[1]}" if len(best_inv) == 2 else "the indicated periods"
    preparation = f"To maximize wealth potential: strengthen your financial discipline, consult a financial advisor, and focus on real estate during {prep_best}"

    score_breakdown = {
        "venus_contribution": venus_contribution,
        "jupiter_contribution": jupiter_contribution,
        "house_2_contribution": house_2_contribution,
        "house_11_contribution": house_11_contribution,
        "mars_contribution": mars_contribution,
        "sun_contribution": sun_contribution,
        "total": wealth_score
    }

    return {
        "wealth_potential": wealth_potential,
        "investment_periods": investment_periods,
        "loss_periods": loss_periods,
        "lucky_years": lucky_years,
        "property_buying_periods": property_buying_periods,
        "description": ". ".join(desc_parts) + f". Overall wealth potential is {wealth_potential}.",
        "confidence_score": confidence_score,
        "reasoning": reasoning,
        "best_investment_window": best_investment_window,
        "preparation": preparation,
        "score_breakdown": score_breakdown
    }

def calculate_foreign_settlement(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict[str, Any]:
    chart = calculate_natal_chart(birth_date, birth_time, latitude, longitude, timezone)
    if "error" in chart:
        return chart
    planets = chart.get("planets", {})
    houses = chart.get("houses", {})

    house_12 = houses.get("12", {}).get("sign", "")
    house_9 = houses.get("9", {}).get("sign", "")
    moon_sign = chart.get("moon_sign", "")
    rahu = planets.get("North Node", {})
    rahu_sign = rahu.get("sign", "")
    jupiter = planets.get("Jupiter", {})
    jup_sign = jupiter.get("sign", "")
    saturn = planets.get("Saturn", {})
    sat_sign = saturn.get("sign", "")

    score = 0
    desc_parts = []
    if house_12 in ["Pisces", "Sagittarius", "Aquarius"]:
        score += 20
        desc_parts.append(f"12th house in {house_12} strongly favors foreign settlement")
    if house_9 in ["Sagittarius", "Pisces"]:
        score += 15
        desc_parts.append(f"9th house in {house_9} indicates long journey luck")
    if rahu_sign in ["Aquarius", "Pisces", "Gemini"]:
        score += 15
        desc_parts.append(f"Rahu in {rahu_sign} enhances foreign connections")
    if moon_sign in ["Gemini", "Sagittarius", "Aquarius"]:
        score += 10
        desc_parts.append(f"Moon in {moon_sign} indicates restlessness for foreign lands")
    if jup_sign in ["Sagittarius", "Pisces"]:
        score += 10
    if sat_sign in ["Aquarius", "Capricorn"]:
        score += 5
    if house_9 == house_12:
        score += 10

    score = min(score, 100)

    country_hints = []
    if rahu_sign:
        rahu_idx = ZODIAC_SIGNS.index(rahu_sign) if rahu_sign in ZODIAC_SIGNS else 0
        if rahu_idx <= 2:
            country_hints.append("east")
        elif rahu_idx <= 5:
            country_hints.append("west")
        elif rahu_idx <= 8:
            country_hints.append("north")
        else:
            country_hints.append("south")

    import random as _rf
    base_year = datetime.fromisoformat(f"{birth_date}T{birth_time}").year if "T" in birth_date else datetime.strptime(birth_date, "%Y-%m-%d").year
    best_years = [base_year + _rf.Random(f"{birth_date}f1").randint(22, 30),
                  base_year + _rf.Random(f"{birth_date}f2").randint(32, 40),
                  base_year + _rf.Random(f"{birth_date}f3").randint(42, 50)]

    confidence_level = "high" if score >= 70 else "medium" if score >= 40 else "low"

    foreign_reasoning_parts = []
    if house_12:
        foreign_reasoning_parts.append(f"12th house in {house_12}")
    if rahu_sign:
        foreign_reasoning_parts.append(f"Rahu in {rahu_sign}")
    if moon_sign:
        foreign_reasoning_parts.append(f"Moon in {moon_sign}")
    reasoning = " + ".join(foreign_reasoning_parts) + f" creates {confidence_level} foreign settlement potential"

    best_years_sorted = sorted(best_years)
    best_window = f"Most favorable period: ages {best_years_sorted[0]}-{best_years_sorted[-1]}" if best_years_sorted else ""

    preparation = f"To increase foreign settlement chances: strengthen connections abroad, learn new languages, and explore opportunities during {best_window}"

    twelfth_house_contribution = 20 if house_12 in ["Pisces", "Sagittarius", "Aquarius"] else 0
    ninth_house_contribution = 15 if house_9 in ["Sagittarius", "Pisces"] else 0
    rahu_contribution = 15 if rahu_sign in ["Aquarius", "Pisces", "Gemini"] else 0
    moon_contribution = 10 if moon_sign in ["Gemini", "Sagittarius", "Aquarius"] else 0
    jupiter_contribution_fs = 10 if jup_sign in ["Sagittarius", "Pisces"] else 0
    saturn_contribution_fs = 5 if sat_sign in ["Aquarius", "Capricorn"] else 0
    same_house_bonus = 10 if house_9 == house_12 else 0

    factor_breakdown = {
        "twelfth_house_contribution": twelfth_house_contribution,
        "ninth_house_contribution": ninth_house_contribution,
        "rahu_contribution": rahu_contribution,
        "moon_contribution": moon_contribution,
        "jupiter_contribution": jupiter_contribution_fs,
        "saturn_contribution": saturn_contribution_fs,
        "same_house_bonus": same_house_bonus,
        "total": score
    }

    return {
        "probability_score": score,
        "best_years": best_years,
        "country_direction": country_hints[0] if country_hints else "west",
        "description": ". ".join(desc_parts) + f". Foreign settlement probability: {score}%.",
        "confidence_level": confidence_level,
        "reasoning": reasoning,
        "best_window": best_window,
        "preparation": preparation,
        "factor_breakdown": factor_breakdown
    }

def check_manglik(chart: Dict) -> Dict[str, Any]:
    planets = chart.get("planets", {})
    mars = planets.get("Mars", {})
    mars_deg = mars.get("degree", 0)
    mars_sign = mars.get("sign", "")
    asc_deg = chart.get("ascendant_degree", 0)
    asc_sign = chart.get("rising_sign", "Aries")
    asc_idx = ZODIAC_SIGNS.index(asc_sign) if asc_sign in ZODIAC_SIGNS else 0

    mars_absolute = (ZODIAC_SIGNS.index(mars_sign) * 30 + (mars_deg % 30)) if mars_sign else mars_deg
    asc_absolute = (asc_idx * 30 + (asc_deg % 30))

    diff = (mars_absolute - asc_absolute) % 360
    house_position = int(diff // 30) + 1

    manglik_houses = {1, 2, 4, 7, 8, 12}
    house_places = []
    if house_position in manglik_houses:
        house_places.append(house_position)

    level = "none"
    if len(house_places) == 0:
        level = "none"
    elif len(house_places) <= 1:
        level = "low"
    elif len(house_places) <= 2:
        level = "medium"
    else:
        level = "high"

    return {
        "is_manglik": len(house_places) > 0,
        "dosha_level": level,
        "house_placements": house_places if house_places else [house_position],
        "description": f"Mars is in house {house_position} from Lagna. {'Manglik dosha present' if house_places else 'No Manglik dosha'} - level: {level}."
    }

def calculate_navamsa_chart(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict[str, Any]:
    chart = calculate_natal_chart(birth_date, birth_time, latitude, longitude, timezone)
    if "error" in chart:
        return chart
    planets = chart.get("planets", {})

    def get_navamsa_sign(planet_deg: float) -> str:
        sign_index = int(planet_deg // 30) % 12
        degree_in_sign = planet_deg % 30
        navamsa_part = int(degree_in_sign // 3.333)
        sign_type = sign_index % 3
        if sign_type == 0:
            navamsa_sign_num = (sign_index + navamsa_part) % 12
        elif sign_type == 1:
            navamsa_sign_num = (sign_index + 4 + navamsa_part) % 12
        else:
            navamsa_sign_num = (sign_index + 8 + navamsa_part) % 12
        return ZODIAC_SIGNS[navamsa_sign_num]

    planets_in_navamsa = {}
    houses_in_navamsa = {}
    for planet, data in planets.items():
        deg = data.get("degree", 0)
        n_sign = get_navamsa_sign(deg)
        planets_in_navamsa[planet] = {"degree": round(deg, 2), "sign": data.get("sign", ""), "navamsa_sign": n_sign}
        house_num = (int(deg // 30) % 12) + 1
        houses_in_navamsa[str(house_num)] = {"sign": n_sign}

    return {
        "planets_in_navamsa": planets_in_navamsa,
        "houses_in_navamsa": houses_in_navamsa
    }

def calculate_festival_calendar(year: int) -> Dict[str, str]:
    import math as _fm
    def approx_moon_day(y, m, d):
        jd = datetime_to_julian_day(datetime(y, m, d, 12, 0, 0))
        t = (jd - 2451545.0) / 36525.0
        moon_long = (218.3164477 + 481267.88123421 * t - 0.0015786 * t * t) % 360
        sun_long = (280.46646 + 36000.76983 * t + 0.0003032 * t * t) % 360
        return ((moon_long - sun_long) % 360) / 12

    def find_tithi_date(y, m, target_tithi):
        for d in range(1, 32):
            try:
                t = approx_moon_day(y, m, d)
                if int(t) % 15 == target_tithi % 15:
                    return f"{y}-{m:02d}-{d:02d}"
            except:
                pass
        return f"{y}-{m:02d}-15"

    diwali = find_tithi_date(year, 10, 15) if int(approx_moon_day(year, 10, 1)) >= 8 else find_tithi_date(year, 11, 15)
    holi = find_tithi_date(year, 3, 14)
    navratri_spring_start = find_tithi_date(year, 4, 1)
    navratri_autumn_start = find_tithi_date(year, 10, 1)
    raksha_bandhan = find_tithi_date(year, 8, 14)
    janmashtami = find_tithi_date(year, 8, 8) if int(approx_moon_day(year, 8, 1)) < 8 else find_tithi_date(year, 9, 8)
    ganesh_chaturthi = find_tithi_date(year, 9, 4)
    mahashivratri = find_tithi_date(year, 2, 14) if int(approx_moon_day(year, 2, 1)) >= 8 else find_tithi_date(year, 3, 14)
    karva_chauth = find_tithi_date(year, 10, 18)

    purnima_dates = []
    amavasya_dates = []
    for m in range(1, 13):
        for d in [1, 15, 30]:
            try:
                t = approx_moon_day(year, m, d)
                ti = int(t) % 15
                if ti == 14:
                    purnima_dates.append(f"{year}-{m:02d}-{d:02d}")
                elif ti == 0:
                    amavasya_dates.append(f"{year}-{m:02d}-{d:02d}")
            except:
                pass

    ekadashi_dates = []
    for m in range(1, 13):
        for d in [1, 16]:
            try:
                t = approx_moon_day(year, m, d)
                ti = int(t) % 15
                if ti == 11:
                    ekadashi_dates.append(f"{year}-{m:02d}-{d:02d}")
            except:
                pass

    return {
        "diwali": diwali,
        "holi": holi,
        "navratri_spring": navratri_spring_start,
        "navratri_autumn": navratri_autumn_start,
        "dussehra": f"{year}-10-{int(find_tithi_date(year, 10, 10)[-2:]):02d}" if find_tithi_date(year, 10, 10) else f"{year}-10-15",
        "raksha_bandhan": raksha_bandhan,
        "janmashtami": janmashtami,
        "ganesh_chaturthi": ganesh_chaturthi,
        "mahashivratri": mahashivratri,
        "makar_sankranti": f"{year}-01-14",
        "pongal": f"{year}-01-14",
        "karva_chauth": karva_chauth,
        "purnima_dates": purnima_dates[:6],
        "amavasya_dates": amavasya_dates[:6],
        "ekadashi_dates": ekadashi_dates[:6]
    }

def calculate_name_correction(name: str, birth_date: str) -> Dict[str, Any]:
    name_values = {c: i + 1 for i, c in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
    name_values.update({'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8})

    def reduce_num(n):
        while n > 9 and n not in [11, 22, 33]:
            n = sum(int(d) for d in str(n))
        return n

    name_digits = ''.join(c for c in name.upper() if c.isalpha())
    current_number = reduce_num(sum(name_values.get(c, 0) for c in name_digits))

    birth_digits = ''.join(c for c in birth_date if c.isdigit())
    life_path = reduce_num(sum(int(d) for d in birth_digits))

    good_numbers = [1, 3, 5, 6, 11, 22, 33]
    suggestions = []
    if current_number not in good_numbers:
        for target in good_numbers:
            diff = target - current_number
            if diff > 0 and diff < 10:
                from copy import deepcopy
                last_char = name_digits[-1] if name_digits else 'A'
                last_val = name_values.get(last_char, 1)
                new_last = chr(ord('A') + (last_val + diff - 1) % 26)
                alt = name.upper()[:-1] + new_last if name else 'A'
                suggestions.append({"spelling": alt, "number": target})
                if len(suggestions) >= 3:
                    break

    return {
        "current_name": name,
        "current_name_number": current_number,
        "suggested_spellings": suggestions[:3],
        "business_name_suggestions": [f"{name.upper()} ENTERPRISES", f"{name.upper()} VENTURES", f"{name.upper()} GROUP"],
        "baby_name_suggestions": [f"Baby-{name[:3]}", f"{name[:2]}AN", f"SHRI {name[:4]}"] if life_path else []
    }

def calculate_remedies(chart: Dict) -> Dict[str, Any]:
    planets = chart.get("planets", {})

    planet_data = {
        "Sun": {"mantra": "Om Namah Suryaya Namah", "translation": "I bow to the Sun", "fasting_day": "Sunday", "charity": "Wheat, jaggery, copper", "deity": "Lord Surya", "color": "Orange/Red", "gemstone": "Ruby"},
        "Moon": {"mantra": "Om Chandraya Namah", "translation": "I bow to the Moon", "fasting_day": "Monday", "charity": "Rice, milk, silver", "deity": "Lord Chandra", "color": "White/Silver", "gemstone": "Pearl"},
        "Mercury": {"mantra": "Om Buddhaya Namah", "translation": "I bow to Mercury", "fasting_day": "Wednesday", "charity": "Green items, books", "deity": "Lord Vishnu", "color": "Green", "gemstone": "Emerald"},
        "Venus": {"mantra": "Om Shukraya Namah", "translation": "I bow to Venus", "fasting_day": "Friday", "charity": "White items, sweets", "deity": "Goddess Lakshmi", "color": "White/Pink", "gemstone": "Diamond"},
        "Mars": {"mantra": "Om Angarakaya Namah", "translation": "I bow to Mars", "fasting_day": "Tuesday", "charity": "Red items, lentils", "deity": "Lord Hanuman", "color": "Red", "gemstone": "Red Coral"},
        "Jupiter": {"mantra": "Om Gurave Namah", "translation": "I bow to Jupiter", "fasting_day": "Thursday", "charity": "Yellow items, gold", "deity": "Lord Brihaspati", "color": "Yellow", "gemstone": "Yellow Sapphire"},
        "Saturn": {"mantra": "Om Shanaischaraya Namah", "translation": "I bow to Saturn", "fasting_day": "Saturday", "charity": "Black items, iron, oil", "deity": "Lord Shani", "color": "Black/Blue", "gemstone": "Blue Sapphire"}
    }

    weak_planet_names = []
    planet_remedies = []
    for pname, info in planet_data.items():
        if pname in planets:
            pdata = planets[pname]
            psign = pdata.get("sign", "")
            pdeg = pdata.get("degree", 0)
            debilitation_signs = {"Sun": "Libra", "Moon": "Scorpio", "Mercury": "Pisces", "Venus": "Virgo", "Mars": "Cancer", "Jupiter": "Capricorn", "Saturn": "Aries"}
            is_weak = psign == debilitation_signs.get(pname, "")
            if is_weak:
                weak_planet_names.append(pname)
            planet_remedies.append({
                "planet": pname,
                "sign": psign,
                "strength": "weak" if is_weak else "neutral",
                "mantra": info["mantra"],
                "mantra_translation": info["translation"],
                "fasting_day": info["fasting_day"],
                "charity": info["charity"],
                "deity": info["deity"],
                "color": info["color"],
                "gemstone": info["gemstone"]
            })

    return {
        "planet_remedies": planet_remedies,
        "general_remedies": [
            "Chant the Gayatri Mantra 108 times daily",
            "Perform daily Surya Namaskar at sunrise",
            "Donate food to the needy on your birthday",
            "Keep a small Tulsi plant at home",
            "Practice meditation and mindfulness daily"
        ],
        "recommended_deities": ["Lord Ganesha (remover of obstacles)", "Goddess Lakshmi (prosperity)", "Lord Vishnu (protection)"] + [f"{info['deity']}" for pname, info in planet_data.items() if pname in weak_planet_names]
    }

def calculate_life_timeline(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict[str, Any]:
    try:
        dt = datetime.fromisoformat(f"{birth_date}T{birth_time}")
    except:
        dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
    jd = datetime_to_julian_day(dt)
    positions = calculate_planet_positions(jd, latitude, longitude)
    moon_deg = positions.get("Moon", 0)
    nakshatra_idx = int((moon_deg % 360) / 13.333) % 27
    nakshatra_lord = NAKSHATRA_LORDS[nakshatra_idx]
    dasha_order = VIMSHOTTARI_MAHADASHA_ORDER
    start_idx = dasha_order.index(nakshatra_lord) if nakshatra_lord in dasha_order else 0

    themes = {
        "Ketu": {"theme": "Spirituality & Detachment", "description": "Period of spiritual growth, introspection, and releasing attachments"},
        "Venus": {"theme": "Love, Luxury & Relationships", "description": "Focus on relationships, creativity, material comforts, and artistic pursuits"},
        "Sun": {"theme": "Career & Self-expression", "description": "Leadership, career advancement, recognition, and personal authority"},
        "Moon": {"theme": "Emotional Growth & Family", "description": "Emotional development, family matters, nurturing, and home life"},
        "Mars": {"theme": "Action & Ambition", "description": "Dynamic energy, career challenges, competition, and taking bold action"},
        "Rahu": {"theme": "Material Ambitions & Foreign", "description": "Material success, foreign connections, innovation, and worldly desires"},
        "Jupiter": {"theme": "Expansion & Wisdom", "description": "Learning, teaching, travel, higher education, and spiritual growth"},
        "Saturn": {"theme": "Karma & Discipline", "description": "Hard work, discipline, karmic lessons, and building lasting foundations"},
        "Mercury": {"theme": "Communication & Business", "description": "Communication, business, networking, and intellectual development"}
    }

    birth_year = dt.year
    timeline = []
    age = 0.0
    for i in range(9):
        pi = (start_idx + i) % 9
        planet = dasha_order[pi]
        d_years = VIMSHOTTARI_YEARS[planet]
        th = themes.get(planet, {"theme": "General Growth", "description": "Period of general life development"})
        timeline.append({
            "age_start": round(age, 1),
            "age_end": round(age + d_years, 1),
            "period_type": "Mahadasha",
            "planet": planet,
            "theme": th["theme"],
            "description": th["description"]
        })
        age += d_years

    life_stages = []
    for entry in timeline:
        life_stages.append(f"Age {entry['age_start']}-{entry['age_end']}: {entry['planet']} - {entry['theme']}")

    return {
        "timeline": timeline,
        "life_stages": life_stages,
        "moon_nakshatra": NAKSHATRAS[nakshatra_idx],
        "starting_dasha": nakshatra_lord
    }

def calculate_face_reading(features: Dict[str, str]) -> Dict[str, Any]:
    features_lower = {k.lower(): v.lower() if isinstance(v, str) else v for k, v in features.items()}

    face_shape = features_lower.get("face_shape", "oval")
    forehead = features_lower.get("forehead", "medium")
    eyebrows = features_lower.get("eyebrows", "medium")
    eyes = features_lower.get("eyes", "medium")
    nose = features_lower.get("nose", "medium")
    lips = features_lower.get("lips", "medium")
    chin = features_lower.get("chin", "medium")
    ears = features_lower.get("ears", "medium")

    personality_traits = []
    if face_shape == "round":
        personality_traits.extend(["Friendly and approachable", "Good-natured and caring", "Emotionally sensitive"])
    elif face_shape == "oval":
        personality_traits.extend(["Balanced and harmonious", "Adaptable and diplomatic", "Well-proportioned personality"])
    elif face_shape == "square":
        personality_traits.extend(["Strong-willed and determined", "Practical and grounded", "Natural leader"])
    elif face_shape == "heart":
        personality_traits.extend(["Creative and artistic", "Passionate and enthusiastic", "Quick-witted"])
    elif face_shape == "oblong":
        personality_traits.extend(["Analytical and thoughtful", "Reserved but insightful", "Strong sense of purpose"])

    strengths = []
    if forehead in ["high", "wide"]:
        strengths.append("Intellectual and visionary thinking")
    if eyebrows in ["thick", "straight"]:
        strengths.append("Strong willpower and determination")
    if eyes in ["large", "almond"]:
        strengths.append("Perceptive and intuitive nature")
    if nose in ["straight", "long"]:
        strengths.append("Leadership qualities and confidence")
    if lips in ["full", "wide"]:
        strengths.append("Generous and communicative nature")
    if chin in ["strong", "square"]:
        strengths.append("Resilience and persistence")
    if ears in ["large", "attached"]:
        strengths.append("Good judgment and stability")

    career_affinities = {}
    if face_shape == "round":
        career_affinities = {"primary": "Healthcare, Counseling, Education", "secondary": "Hospitality, Arts"}
    elif face_shape == "square":
        career_affinities = {"primary": "Management, Engineering, Military", "secondary": "Construction, Law"}
    elif face_shape == "oval":
        career_affinities = {"primary": "Diplomacy, Design, Media", "secondary": "Business, Teaching"}
    elif face_shape == "heart":
        career_affinities = {"primary": "Creative Arts, Marketing, Writing", "secondary": "Entrepreneurship"}
    else:
        career_affinities = {"primary": "Research, Technology, Philosophy", "secondary": "Writing, Consulting"}

    return {
        "personality_traits": personality_traits,
        "confidence_level": "high" if any(s in str(strengths) for s in ["Leadership", "Determination"]) else "medium",
        "communication_style": "Direct and expressive" if lips in ["full", "wide"] else "Thoughtful and measured",
        "strengths": strengths,
        "career_affinities": career_affinities,
        "disclaimer": "Face reading is for entertainment purposes only and should not be used for making important life decisions."
    }

def generate_pdf_report(birth_date: str, birth_time: str, latitude: float, longitude: float, timezone: str = "UTC") -> Dict[str, Any]:
    chart = calculate_natal_chart(birth_date, birth_time, latitude, longitude, timezone)
    if "error" in chart:
        return {"error": "Could not generate chart for PDF"}
    try:
        from fpdf import FPDF
        import base64
        import io

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Astrology Report", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(200, 10, f"Date: {birth_date}  Time: {birth_time}", ln=True)
        pdf.cell(200, 10, f"Location: Lat {latitude}, Lon {longitude}", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Birth Chart Summary", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Sun Sign: {chart.get('sun_sign', 'N/A')}", ln=True)
        pdf.cell(200, 10, f"Moon Sign: {chart.get('moon_sign', 'N/A')}", ln=True)
        pdf.cell(200, 10, f"Rising Sign: {chart.get('rising_sign', 'N/A')}", ln=True)
        pdf.cell(200, 10, f"Ascendant Degree: {chart.get('ascendant_degree', 0)}", ln=True)
        pdf.cell(200, 10, f"Midheaven Degree: {chart.get('midheaven_degree', 0)}", ln=True)

        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Planetary Positions", ln=True)
        pdf.set_font("Arial", "", 10)
        planets_data = chart.get("planets", {})
        pdf.cell(60, 10, "Planet", border=1)
        pdf.cell(40, 10, "Degree", border=1)
        pdf.cell(60, 10, "Sign", border=1)
        pdf.ln()
        for pname, pdata in planets_data.items():
            pdf.cell(60, 10, pname, border=1)
            pdf.cell(40, 10, str(pdata.get("degree", 0)), border=1)
            pdf.cell(60, 10, pdata.get("sign", ""), border=1)
            pdf.ln()

        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "House Positions", ln=True)
        pdf.set_font("Arial", "", 10)
        houses = chart.get("houses", {})
        pdf.cell(40, 10, "House", border=1)
        pdf.cell(60, 10, "Cusp", border=1)
        pdf.cell(60, 10, "Sign", border=1)
        pdf.ln()
        for hnum, hdata in houses.items():
            pdf.cell(40, 10, f"House {hnum}", border=1)
            pdf.cell(60, 10, str(hdata.get("cusp", 0)), border=1)
            pdf.cell(60, 10, hdata.get("sign", ""), border=1)
            pdf.ln()

        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Detailed Analysis", ln=True)
        pdf.set_font("Arial", "", 10)
        analysis = generate_detailed_analysis(chart)
        for key in ["strengths", "challenges", "career", "relationships", "health"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, key.capitalize(), ln=True)
            pdf.set_font("Arial", "", 10)
            items = analysis.get(key, [])
            if isinstance(items, list):
                for item in items[:3]:
                    pdf.multi_cell(0, 8, f"- {item}")
            elif isinstance(items, str):
                pdf.multi_cell(0, 8, items)
            pdf.ln(5)

        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Remedies", ln=True)
        remedies = calculate_remedies(chart)
        for rem in remedies.get("planet_remedies", []):
            pdf.set_font("Arial", "B", 10)
            pdf.cell(200, 10, f"{rem['planet']}:", ln=True)
            pdf.set_font("Arial", "", 10)
            if rem.get("strength") == "weak":
                pdf.cell(200, 10, f"Mantra: {rem['mantra']}", ln=True)
                pdf.cell(200, 10, f"Fasting: {rem['fasting_day']}", ln=True)
                pdf.cell(200, 10, f"Charity: {rem['charity']}", ln=True)
            pdf.ln(3)

        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Dasha Timeline & Predictions", ln=True)
        timeline = calculate_life_timeline(birth_date, birth_time, latitude, longitude, timezone)
        pdf.set_font("Arial", "", 10)
        for entry in timeline.get("timeline", [])[:10]:
            pdf.cell(200, 10, f"Age {entry['age_start']}-{entry['age_end']}: {entry['planet']} - {entry['theme']}", ln=True)

        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        if isinstance(pdf_bytes, str):
            pdf_bytes = pdf_bytes.encode("latin-1")
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        return {
            "pdf_base64": pdf_base64,
            "filename": f"astrology_report_{birth_date}.pdf",
            "pages_count": pdf.pages_count
        }
    except ImportError:
        return {"error": "fpdf2 library is required. Install with: pip install fpdf2"}
    except Exception as e:
        return {"error": f"PDF generation failed: {str(e)}"}