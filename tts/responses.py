import random
import threading
import time
import subprocess
import psutil
from datetime import datetime
from nlp.intent_parser import extract_timer_duration



active_timers = []

def start_timer(seconds, speak_function):

    def timer_thread():
        time.sleep(seconds)
        speak_function.speak("टाइमर पूरा हुआ")

    t = threading.Thread(target=timer_thread, daemon=True)
    active_timers.append(t)
    t.start()

def generate_response(intent, original_text=None, tts=None):

    #  WAKE 
    if intent == "WAKE":
        return random.choice([
            "नमस्ते, मैं सुन रही हूँ",
            "जी, बताइए",
            "हाँ, आदेश दीजिए"
        ])

    #  GREETING 
    elif intent == "GREETING":
        return random.choice([
            "मैं ठीक हूँ, धन्यवाद",
            "सब बढ़िया है",
            "मैं आपकी मदद के लिए तैयार हूँ"
        ])

    #  THANK YOU 
    elif intent == "THANK_YOU":
        return random.choice([
            "आपका स्वागत है",
            "कोई बात नहीं",
            "खुशी हुई मदद करके"
        ])

    #  TURN ON 
    elif intent == "TURN_ON":
        if original_text and "लाइट" in original_text:
            return "लाइट चालू कर दी गई है"
        return random.choice([
            "चालू कर दिया गया है",
            "सिस्टम ऑन कर दिया गया है"
        ])

    #  TURN OFF 
    elif intent == "TURN_OFF":
        if original_text and "लाइट" in original_text:
            return "लाइट बंद कर दी गई है"
        return random.choice([
            "बंद कर दिया गया है",
            "सिस्टम बंद कर दिया गया है"
        ])

    #  TIME 
    elif intent == "TIME":
        now = datetime.now().strftime("%H:%M")
        return f"अभी समय है {now}"

    #  DATE 
    elif intent == "DATE":
        today = datetime.now().strftime("%d %B %Y")
        return f"आज की तारीख है {today}"

    #  DAY 
    elif intent == "DAY":
        day = datetime.now().strftime("%A")
        return f"आज {day} है"

    #  WEATHER (Offline Placeholder) 
    elif intent == "WEATHER":
        return random.choice([
            "मौसम सामान्य है",
            "आज मौसम साफ है",
            "तापमान सामान्य स्तर पर है"
        ])

    #  CPU STATUS 
    elif intent == "CPU_STATUS":
        cpu = psutil.cpu_percent(interval=0.5)
        return f"सी पी यू उपयोग {cpu} प्रतिशत है"

    #  MEMORY STATUS 
    elif intent == "MEMORY_STATUS":
        mem = psutil.virtual_memory().percent
        return f"मेमोरी उपयोग {mem} प्रतिशत है"

    #  DISK STATUS 
    elif intent == "DISK_STATUS":
        disk = psutil.disk_usage('/').percent
        return f"डिस्क उपयोग {disk} प्रतिशत है"

    #  VOLUME UP 
    elif intent == "VOLUME_UP":
        try:
            subprocess.run(
                ["amixer", "set", "Master", "unmute"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            subprocess.run(
                ["amixer", "set", "Master", "10%+"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return "आवाज़ बढ़ा दी गई है"
        except Exception:
            return "आवाज़ बढ़ाने में समस्या आई"

    #  VOLUME DOWN 
    elif intent == "VOLUME_DOWN":
        try:
            subprocess.run(
                ["amixer", "set", "Master", "10%-"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return "आवाज़ कम कर दी गई है"
        except Exception:
            return "आवाज़ कम करने में समस्या आई"

    #  MUTE 
    elif intent == "MUTE":
        try:
            subprocess.run(
                ["amixer", "set", "Master", "mute"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return "सिस्टम म्यूट कर दिया गया है"
        except Exception:
            return "म्यूट करने में समस्या आई"

    #  TIMER 
    elif intent == "TIMER":

        seconds = extract_timer_duration(original_text or "")

        if seconds:
            from timer_manager import start_timer
            start_timer(seconds,tts)   
            return f"{seconds} सेकंड का टाइमर लगा दिया गया है"

        return "कृपया समय बताएं, जैसे 5 मिनट या 10 सेकंड"

    #  EXIT 
    elif intent == "EXIT":
        return "ठीक है, स्लीप मोड में जा रही हूँ"

    #  UNKNOWN 
    else:
        return random.choice([
            "मुझे समझ नहीं आया",
            "कृपया फिर से कहें",
            "मैं समझ नहीं पाई"
        ])
