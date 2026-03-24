import speech_recognition as sr
from deep_translator import GoogleTranslator

LANGUAGES = {
    "Kannada": "kn-IN",
    "Hindi":   "hi-IN",
    "Tamil":   "ta-IN",
    "Telugu":  "te-IN",
    "English": "en-IN"
}

LANG_CODES = {
    "Kannada": "kn",
    "Hindi":   "hi",
    "Tamil":   "ta",
    "Telugu":  "te",
    "English": "en"
}

SYMPTOM_KEYWORDS = {
    "blurred vision":    "Blurred Vision",
    "blurry":            "Blurred Vision",
    "blur":              "Blurred Vision",
    "cannot see":        "Blurred Vision",
    "cant see":          "Blurred Vision",
    "poor vision":       "Blurred Vision",
    "weak vision":       "Blurred Vision",
    "pain":              "Eye Pain",
    "ache":              "Eye Pain",
    "hurts":             "Eye Pain",
    "hurting":           "Eye Pain",
    "sore":              "Eye Pain",
    "burning":           "Eye Pain",
    "redness":           "Redness",
    "red":               "Redness",
    "pink":              "Redness",
    "irritation":        "Redness",
    "watering":          "Watering",
    "tears":             "Watering",
    "discharge":         "Watering",
    "wet":               "Watering",
    "light sensitivity": "Light Sensitivity",
    "sensitive to light":"Light Sensitivity",
    "brightness":        "Light Sensitivity",
    "bright light":      "Light Sensitivity",
    "double vision":     "Double Vision",
    "double":            "Double Vision",
    "two images":        "Double Vision",
    "floaters":          "Floaters",
    "spots":             "Dark Spots",
    "dark spots":        "Dark Spots",
    "black spots":       "Dark Spots",
    "shadow":            "Dark Spots",
    "headache":          "Headache",
    "head pain":         "Headache",
    "itching":           "Itching",
    "itchy":             "Itching",
    "scratch":           "Itching",
    "swelling":          "Swelling",
    "swollen":           "Swelling",
    "puffiness":         "Swelling",
    "dryness":           "Dryness",
    "dry":               "Dryness",
    "tired":             "Eye Fatigue",
    "fatigue":           "Eye Fatigue",
    "strain":            "Eye Fatigue",
    "night blindness":   "Night Blindness",
    "night":             "Night Blindness",
    "dark":              "Night Blindness",
    "tunnel":            "Tunnel Vision",
    "peripheral":        "Tunnel Vision",
    "halo":              "Halos",
    "halos":             "Halos",
    "glare":             "Halos",
}

def extract_symptoms(text):
    text_lower = text.lower()
    found = []
    for keyword, symptom in SYMPTOM_KEYWORDS.items():
        if keyword in text_lower and symptom not in found:
            found.append(symptom)
    # Fallback: return the actual spoken description so doctor sees it
    return found if found else [text.strip()]

def translate_to_english(text, source_language):
    if source_language == "English":
        return text
    try:
        src_code = LANG_CODES.get(source_language, "auto")
        translated = GoogleTranslator(
            source=src_code, target='en'
        ).translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # fallback to original if translation fails

def record_voice(language_name, timeout=8):
    lang_code = LANGUAGES.get(language_name, "en-IN")
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold  = 1.2

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=timeout,
                             phrase_time_limit=15)

        # Convert speech to text in native language
        original_text = r.recognize_google(audio, language=lang_code)

        # Translate to English for symptom extraction
        english_text = translate_to_english(original_text, language_name)

        # Extract symptoms from English text
        symptoms = extract_symptoms(english_text)

        return {
            "success":          True,
            "text":             original_text,
            "english_text":     english_text,
            "symptoms":         symptoms,
            "language":         language_name
        }

    except sr.WaitTimeoutError:
        return {"success": False,
                "error": "No speech detected — please try again"}
    except sr.UnknownValueError:
        return {"success": False,
                "error": "Could not understand speech — speak clearly and try again"}
    except sr.RequestError:
        return {"success": False,
                "error": "Could not connect to speech service — check internet connection"}
    except Exception as e:
        return {"success": False, "error": f"Microphone error: {str(e)}"}