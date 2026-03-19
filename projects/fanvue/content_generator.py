"""
Yuki Mori - Content Generator
Generiert täglich Captions, Hashtags und Posting-Pläne
"""
import random
from datetime import datetime, timedelta

CAPTIONS = {
    "morning": [
        "good morning 🌸 took me a while to get up today",
        "soft mornings are my favorite ☁️",
        "woke up thinking about matcha... as always 🍵",
        "monday? already? 🥺",
        "good morning from my cozy corner 🤍",
    ],
    "cafe": [
        "matcha date with myself ☕ no better company honestly",
        "found my new favorite spot 🌿",
        "some days you just need a good café and silence ☁️",
        "this matcha > everything today 🍵✨",
    ],
    "gaming": [
        "who wants to play? 🎮 i never say no to a good game night",
        "lost again... but make it cute 🎮💀",
        "gaming hours > everything else tonight",
        "i may be bad at this but i look cute doing it 🎮🌸",
    ],
    "outfit": [
        "felt cute, might delete later... actually no i look good 😌",
        "this fit has been living in my head rent free 🤍",
        "soft day, soft fit ☁️",
        "pastel is a lifestyle not just a color 🌸",
    ],
    "cozy": [
        "sunday reset mode activated 🕯️",
        "candles, blanket, no plans. perfect evening 🤍",
        "the week can wait, im cozy 🌙",
        "if you need me ill be here doing absolutely nothing 🕯️✨",
    ],
    "engagement": [
        "matcha or coffee? very important question ☕🍵",
        "what are you doing this weekend? 🌸",
        "show me your current wallpaper 📱",
        "night owl or early bird? 🌙☀️",
        "what song is stuck in your head right now? 🎵",
    ],
}

HASHTAGS = {
    "core": ["#AIModel", "#VirtualModel", "#AIGirl", "#DigitalModel", "#AIInfluencer"],
    "kawaii": ["#KawaiiGirl", "#KawaiiAesthetic", "#KawaiiStyle", "#kawaii", "#kawaiilife"],
    "japanese": ["#JapaneseAesthetic", "#JapanStyle", "#TokyoGirl", "#JapaneseGirl", "#jpop"],
    "lifestyle": ["#SoftGirl", "#CosyVibes", "#SoftAesthetic", "#PastelAesthetic", "#cottagecore"],
    "gaming": ["#GamingGirl", "#GamerGirl", "#GamersOfInstagram", "#GamingLife"],
    "general": ["#instadaily", "#photooftheday", "#instagood", "#beautiful", "#aesthetic"],
}

WEEKLY_PLAN = {
    0: ("morning", "Morning selfie im Bett"),      # Montag
    1: ("cafe", "Café-Shot mit Matcha"),            # Dienstag
    2: ("gaming", "Gaming-Setup Selfie"),           # Mittwoch
    3: ("outfit", "Close-up Portrait"),             # Donnerstag
    4: ("outfit", "Freitags-Outfit"),               # Freitag
    5: ("cozy", "Outdoor/Natur"),                   # Samstag
    6: ("cozy", "Cozy Home Sunday"),                # Sonntag
}

def get_todays_plan():
    today = datetime.now()
    weekday = today.weekday()
    category, scene = WEEKLY_PLAN[weekday]

    caption = random.choice(CAPTIONS[category])

    # Mix hashtags
    tags = (
        HASHTAGS["core"] +
        random.sample(HASHTAGS["kawaii"], 3) +
        random.sample(HASHTAGS["japanese"], 2) +
        random.sample(HASHTAGS["lifestyle"], 3) +
        random.sample(HASHTAGS["general"], 3)
    )
    random.shuffle(tags)
    hashtag_string = " ".join(tags[:20])

    # Occasionally add engagement question
    if random.random() < 0.3:
        caption += "\n\n" + random.choice(CAPTIONS["engagement"])

    # Fanvue promo (every 3rd post)
    if today.day % 3 == 0:
        caption += "\n\nexclusive content on fanvue 💌 link in bio"

    return {
        "date": today.strftime("%Y-%m-%d"),
        "weekday": today.strftime("%A"),
        "posting_time": "18:00",
        "scene": scene,
        "category": category,
        "caption": caption,
        "hashtags": hashtag_string,
        "image_prompt": get_image_prompt(category),
    }

def get_image_prompt(category):
    base = "portrait photo of Yuki, a beautiful 22 year old Japanese woman, long straight black hair, large expressive brown eyes, soft skin, natural makeup, warm gentle smile, photorealistic, 8k, professional photography"
    
    additions = {
        "morning": ", laying in bed, morning light, white sheets, sleepy smile, cozy bedroom, soft natural light",
        "cafe": ", sitting in cozy café, holding matcha latte, pastel outfit, warm lighting, bokeh background",
        "gaming": ", sitting at gaming setup, RGB lights, headphones, casual streetwear, happy expression",
        "outfit": ", standing, full body, kawaii fashion, pastel colors, natural daylight, Harajuku street",
        "cozy": ", sitting on couch, cozy knit sweater, candles, warm home lighting, relaxed",
    }
    
    negative = "ugly, deformed, blurry, low quality, watermark, text, extra limbs, bad anatomy, cartoon"
    
    return {
        "positive": base + additions.get(category, ""),
        "negative": negative,
    }

if __name__ == "__main__":
    plan = get_todays_plan()
    print(f"📅 Content Plan für {plan['weekday']}, {plan['date']}")
    print(f"⏰ Posting-Zeit: {plan['posting_time']} Uhr")
    print(f"🎬 Szene: {plan['scene']}")
    print(f"\n📝 Caption:\n{plan['caption']}")
    print(f"\n#️⃣ Hashtags:\n{plan['hashtags']}")
    print(f"\n🎨 Image Prompt:\n{plan['image_prompt']['positive']}")
    print(f"\n❌ Negative:\n{plan['image_prompt']['negative']}")
