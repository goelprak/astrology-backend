# Hindi translations for astrology app

SIGNS_HI = {
    "Aries": "मेष", "Taurus": "वृषभ", "Gemini": "मिथुन", "Cancer": "कर्क",
    "Leo": "सिंह", "Virgo": "कन्या", "Libra": "तुला", "Scorpio": "वृश्चिक",
    "Sagittarius": "धनु", "Capricorn": "मकर", "Aquarius": "कुंभ", "Pisces": "मीन"
}

PLANETS_HI = {
    "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
    "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि", "Rahu": "राहु",
    "Ketu": "केतु", "Uranus": "अरुण", "Neptune": "वरुण", "Pluto": "प्लूटो"
}

ELEMENTS_HI = {"Fire": "अग्नि", "Earth": "पृथ्वी", "Air": "वायु", "Water": "जल"}

HOUSES_HI = [
    "प्रथम भाव - स्वयं एवं व्यक्तित्व", "द्वितीय भाव - धन एवं मूल्य",
    "तृतीय भाव - संचार", "चतुर्थ भाव - घर एवं परिवार",
    "पंचम भाव - रचनात्मकता", "षष्ठ भाव - कार्य एवं स्वास्थ्य",
    "सप्तम भाव - विवाह एवं साझेदारी", "अष्टम भाव - परिवर्तन",
    "नवम भाव - भाग्य एवं दर्शन", "दशम भाव - करियर एवं प्रतिष्ठा",
    "एकादश भाव - मित्र एवं लाभ", "द्वादश भाव - आध्यात्मिकता"
]

HOUSE_NAMES_HI = [
    "स्वयं एवं पहचान", "धन एवं मूल्य", "संचार", "घर एवं परिवार",
    "रचनात्मकता एवं प्रेम", "कार्य एवं स्वास्थ्य", "विवाह एवं साझेदारी", "परिवर्तन",
    "दर्शन एवं यात्रा", "करियर एवं प्रतिष्ठा", "मित्र एवं आशाएँ", "आध्यात्मिकता"
]

TABS_HI = {
    "Profile": "प्रोफ़ाइल", "Natal Chart": "जन्म कुंडली", "Horoscope": "दैनिक राशिफल",
    "Weekly": "साप्ताहिक", "Monthly": "मासिक", "Yearly": "वार्षिक",
    "Kundli Matching": "कुंडली मिलान", "AI Chat": "AI चैट", "Tarot": "टैरो",
    "Numerology": "अंक ज्योतिष", "Remedies": "उपाय", "Panchang": "पंचांग",
    "K.P. Dasha": "केपी दशा", "Wealth": "धन योग", "Foreign Settlement": "विदेश निवास",
    "Manglik": "मांगलिक", "Navamsa D9": "नवमांश D9", "Name Correction": "नाम सुधार",
    "Life Timeline": "जीवन रेखा", "PDF Report": "PDF रिपोर्ट",
    "Detailed Analysis": "विस्तृत विश्लेषण"
}

# Common AI phrases in Hindi
AI_PREFIX_HI = (
    "नमस्ते! मैं आपका AI ज्योतिष सहायक हूं। "
    "अपने चार्ट, अंक ज्योतिष, KP ज्योतिष या सामान्य ज्योतिष मार्गदर्शन के बारे में मुझसे कुछ भी पूछें।"
)
CHART_ANALYSIS_HI = (
    "{name}, यह रहा आपका जन्म कुंडली विश्लेषण। "
    "आपका सूर्य राशि {sun} है (पहचान, अहंकार, जीवन उद्देश्य)। "
    "आपकी चंद्र राशि {moon} है (भावनाएं, अवचेतन, आंतरिक स्व)। "
    "आपकी लग्न राशि {asc} है (बाहरी व्यक्तित्व, दूसरे आपको कैसे देखते हैं)। "
    "ग्रह स्थितियां: {planets}। {summary}"
)

def confidence_hi(percent):
    if percent >= 85: return "बहुत उच्च"
    if percent >= 70: return "उच्च"
    if percent >= 50: return "मध्यम"
    return "निम्न"

def timing_hi(text):
    """Simple timing translations - returns Hindi timing text if matches patterns"""
    if "month" in text or "months" in text:
        return text.replace("month", "महीने").replace("months", "महीने")
    if "year" in text or "years" in text:
        return text.replace("year", "वर्ष").replace("years", "वर्ष")
    if "week" in text or "weeks" in text:
        return text.replace("week", "सप्ताह").replace("weeks", "सप्ताह")
    if "day" in text or "days" in text:
        return text.replace("day", "दिन").replace("days", "दिन")
    return text

def translate_sign_planet(text, lang):
    """Replace English sign and planet names with Hindi in a string"""
    if lang != "hi":
        return text
    result = text
    for en, hi in {**SIGNS_HI, **PLANETS_HI}.items():
        result = result.replace(en, hi)
    return result

# Hindi AI response templates
CAREER_HI = (
    "{name}, करियर के बारे में आपके प्रश्न का उत्तर: "
    "आपका दशम भाव (करियर) {element} तत्व से प्रभावित है। "
    "गुरु आपके दशम भाव को मजबूत करता है जबकि शनि दीर्घकालिक विकास में सहायक है। "
    "आपके लिए उपयुक्त करियर: {career}. "
    "विश्वास स्तर: {confidence}% ({conf_label}). "
    "कारण: {reasoning}. "
    "सर्वोत्तम समय: {best_window}. "
    "तैयारी: {preparation}."
)

LOVE_HI = (
    "{name}, प्रेम और संबंधों के बारे में आपके प्रश्न का उत्तर: "
    "आपका सप्तम भाव (विवाह) {sign} राशि में है। "
    "शुक्र आपके प्रेम जीवन को प्रभावित करता है। "
    "विश्वास स्तर: {confidence}% ({conf_label}). "
    "कारण: {reasoning}. "
    "सर्वोत्तम समय: {best_window}. "
    "तैयारी: {preparation}."
)

HEALTH_HI = (
    "{name}, स्वास्थ्य के बारे में आपके प्रश्न का उत्तर: "
    "आपका षष्ठ भाव (स्वास्थ्य) {sign} राशि में है। "
    "चंद्रमा और मंगल आपके स्वास्थ्य को प्रभावित करते हैं। "
    "विश्वास स्तर: {confidence}% ({conf_label}). "
    "कारण: {reasoning}. "
    "सर्वोत्तम समय: {best_window}. "
    "तैयारी: {preparation}."
)

FINANCE_HI = (
    "{name}, वित्त के बारे में आपके प्रश्न का उत्तर: "
    "आपका द्वितीय भाव (धन) {sign} राशि में है। "
    "गुरु और शुक्र आपकी आर्थिक स्थिति को प्रभावित करते हैं। "
    "विश्वास स्तर: {confidence}% ({conf_label}). "
    "कारण: {reasoning}. "
    "सर्वोत्तम समय: {best_window}. "
    "तैयारी: {preparation}."
)

YOUTUBE_HI = (
    "{name}, कंटेंट क्रिएशन करियर के बारे में: "
    "आपका बुध {mer} राशि में है जो आपको {mer_comm} संचार क्षमता देता है। "
    "आपका शुक्र {ven} राशि में है जो {ven_show} रचनात्मकता दर्शाता है। "
    "निर्णय: {yes_no}. "
    "विश्वास स्तर: 78% (उच्च). "
    "सर्वोत्तम समय: अभी अपना चैनल शुरू करें, 6-8 महीनों में विकास दिखेगा। "
    "तैयारी: अपने ज्ञान को अपनी प्राकृतिक {element} ऊर्जा से जोड़ें।"
)

SPORTS_HI = (
    "{name}, खेल करियर के बारे में: "
    "आपका मंगल {mars} राशि में है जो {mars_str} शारीरिक क्षमता देता है। "
    "आपका सूर्य {sun} राशि में है जो {sun_str} नेतृत्व क्षमता दर्शाता है। "
    "निर्णय: {yes_no}. "
    "विश्वास स्तर: 80% (उच्च). "
    "सर्वोत्तम समय: अगले 12-18 महीने गंभीर प्रशिक्षण के लिए अनुकूल हैं। "
    "तैयारी: प्रतिस्पर्धी मैचों से पहले सहनशक्ति और तकनीकी कौशल पर ध्यान दें।"
)

FUTURE_HI = (
    "{name}, आपके भविष्य के बारे में: "
    "आपकी कुंडली के अनुसार, आने वाला समय {element} तत्व से प्रभावित रहेगा। "
    "आपकी वर्तमान महादशा {dasha} की है। "
    "करियर में {career_direction} की ओर बढ़ेंगे। "
    "विश्वास स्तर: 76% (उच्च). "
    "सर्वोत्तम समय: अगले 3-6 महीने महत्वपूर्ण निर्णयों के लिए। "
    "तैयारी: धैर्य रखें और अनुशासित रहें — शनि के प्रभाव में मेहनत रंग लाएगी।"
)

GENERAL_HI = (
    "{name}, आपके प्रश्न का ज्योतिषीय दृष्टिकोण: "
    "आपकी जन्म कुंडली में सूर्य {sun} राशि में, चंद्रमा {moon} राशि में, "
    "और लग्न {asc} राशि में है। "
    "यह संयोजन आपको {element} तत्व प्रधान बनाता है। "
    "आपके जीवन में {house} भाव सबसे अधिक सक्रिय हैं। "
    "विश्वास स्तर: 72% (उच्च). "
    "सर्वोत्तम समय: वर्तमान समय आत्म-चिंतन और योजना बनाने के लिए उपयुक्त है।"
)

def get_greeting(lang, name=""):
    if lang == "hi":
        return f"नमस्ते{', ' + name if name else ''}! मैं आपका AI ज्योतिष सहायक हूं। अपने चार्ट, अंक ज्योतिष, KP ज्योतिष या सामान्य ज्योतिष मार्गदर्शन के बारे में मुझसे कुछ भी पूछें।"
    return f"Hello{', ' + name if name else ''}! I'm your AI Astrology Assistant. Ask me anything about your chart, numerology, KP astrology, or general astrological guidance. For best results, share your birth details in the Profile tab first!"
