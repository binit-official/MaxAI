import re
import cv2
import pyttsx3
import speech_recognition as sr
import webbrowser
import random
import sys
import os
import datetime
import pyautogui as p
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import regex as re

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 195)


def say(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def sanitize_text(text):
    # Remove asterisks
    text = re.sub(r'\*', '', text)
    # Remove emojis and special characters except common punctuation
    # text = re.sub(r'[^\w\s.,!?\'"]', '', text)
    return text

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "sorry could not understand sir"


def play_random_song():
    # List of predefined song URLs on YouTube Music
    songs = {
        "Shape of You": "https://music.youtube.com/watch?v=JGwWNGJdvx8",
        "Blinding Lights": "https://music.youtube.com/watch?v=4NRXx6U8ABQ",
        "Levitating": "https://music.youtube.com/watch?v=t5rE2HhdiNY",
        "Uptown Funk": "https://music.youtube.com/watch?v=OPf0YbXqDm0",
        "Perfect": "https://music.youtube.com/watch?v=2Vv-BfVoq4g",
        "Dance Monkey": "https://music.youtube.com/watch?v=q0o2C5FZLl4",
        "Bad Guy": "https://music.youtube.com/watch?v=DyDfgMOUjCI",
        "Someone Like You": "https://music.youtube.com/watch?v=hLQl3WQQoQ0",
        "Rolling in the Deep": "https://music.youtube.com/watch?v=rYEDA3JcQqw",
        "Thinking Out Loud": "https://music.youtube.com/watch?v=lp-EO5I60KA",
        "Havana": "https://music.youtube.com/watch?v=HCjNJDNzw8Y",
        "Despacito": "https://music.youtube.com/watch?v=kJQP7kiw5Fk",
        "Señorita": "https://music.youtube.com/watch?v=Pkh8UtuejGw",
        "Shallow": "https://music.youtube.com/watch?v=bo_efYhYU2A",
        "Old Town Road": "https://music.youtube.com/watch?v=r7qovpFAGrQ",
        "Believer": "https://music.youtube.com/watch?v=7wtfhZwyrcc",
        "Thunder": "https://music.youtube.com/watch?v=fKopy74weus",
        "Radioactive": "https://music.youtube.com/watch?v=ktvTqknDobU",
        "Roar": "https://music.youtube.com/watch?v=CevxZvSJLk8",
        "Dark Horse": "https://music.youtube.com/watch?v=0KSOMA3QBU0",
        "Firework": "https://music.youtube.com/watch?v=QGJuMBdaqIw",
        "Happy": "https://music.youtube.com/watch?v=ZbZSe6N_BXs",
        "Get Lucky": "https://music.youtube.com/watch?v=5NV6Rdv1a3I",
        "All of Me": "https://music.youtube.com/watch?v=450p7goxZqg",
        "Love Me Like You Do": "https://music.youtube.com/watch?v=AJtDXIazrMo",
        "Let Her Go": "https://music.youtube.com/watch?v=RBumgq5yVrA",
        "Take Me to Church": "https://music.youtube.com/watch?v=P9-4xHVc7uk",
        "Stay": "https://music.youtube.com/watch?v=2-MBfn8XjIU",
        "Sorry": "https://music.youtube.com/watch?v=fRh_vgS2dFE",
        "Love Yourself": "https://music.youtube.com/watch?v=oyEuk8j8imI",
        "What Do You Mean": "https://music.youtube.com/watch?v=DK_0jXPuIr0",
        "Bad Habits": "https://music.youtube.com/watch?v=orJSJGHjBLI",
        "Butter": "https://music.youtube.com/watch?v=WMweEpGlu_U",
        "Save Your Tears": "https://music.youtube.com/watch?v=XXYlFuWEuKI",
        "Watermelon Sugar": "https://music.youtube.com/watch?v=E07s5ZYygMg",
        "Adore You": "https://music.youtube.com/watch?v=yezDEWako8U",
        "Circles": "https://music.youtube.com/watch?v=wXhTHyIgQ_U",
        "Good 4 U": "https://music.youtube.com/watch?v=gNi_6U5Pm_o",
        "Deja Vu": "https://music.youtube.com/watch?v=cii6ruuycQA",
        "drivers license": "https://music.youtube.com/watch?v=ZmDBbnmKpqQ",
        "positions": "https://music.youtube.com/watch?v=tZM3C2s4V1c",
        "34+35": "https://music.youtube.com/watch?v=Yq-hjTAZ0sA",
        "Rain on Me": "https://music.youtube.com/watch?v=AoAm4om0wTs",
        "Stuck with U": "https://music.youtube.com/watch?v=pE49WK-oNjU",
        "Break My Heart": "https://music.youtube.com/watch?v=N02t4GV2XNg",
        "Don't Start Now": "https://music.youtube.com/watch?v=oygrmJFKYZY",
        "Physical": "https://music.youtube.com/watch?v=9HDEHj2yzew",
        "Say So": "https://music.youtube.com/watch?v=pok8H_KF1FA",
        "Juicy": "https://music.youtube.com/watch?v=VJv4Qh7zR3E",
        "Like That": "https://music.youtube.com/watch?v=B_koFaPCLPA",
        "Boss Bitch": "https://music.youtube.com/watch?v=8YXj-G4O5jQ",
        "Supalonely": "https://music.youtube.com/watch?v=FY2y_KVlVNM",
        "Death Bed": "https://music.youtube.com/watch?v=jJPMnTXl63E",
        "Savage Love": "https://music.youtube.com/watch?v=sPTn0QEhxds",
        "Dynamite": "https://music.youtube.com/watch?v=gdZLi9oWNZg",
        "WAP": "https://music.youtube.com/watch?v=hsm4poTWjMs",
        "ROXANNE": "https://music.youtube.com/watch?v=VGmQKp-sY9M",
        "High Fashion": "https://music.youtube.com/watch?v=n0h1V9MO8nU",
        "Blueberry Faygo": "https://music.youtube.com/watch?v=epvZ_t7MJ4c",
        "The Box": "https://music.youtube.com/watch?v=5tKWYPWoguw",
        "Life Is Good": "https://music.youtube.com/watch?v=l0U7SxXHkPY",
        "Godzilla": "https://music.youtube.com/watch?v=r_0JjYUe5jo",
        "The Scotts": "https://music.youtube.com/watch?v=cPhocK4DX8U",
        "Sicko Mode": "https://music.youtube.com/watch?v=6ONRf7h3Mdk",
        "Goosebumps": "https://music.youtube.com/watch?v=Dst9gZkq1a8",
        "Highest in the Room": "https://music.youtube.com/watch?v=tRvH2wWFHZ4",
        "Toosie Slide": "https://music.youtube.com/watch?v=xWggTb45brM",
        "Laugh Now Cry Later": "https://music.youtube.com/watch?v=mvQbJnHj80U",
        "Popstar": "https://music.youtube.com/watch?v=LDZX4ooRsWs",
        "Heartless": "https://music.youtube.com/watch?v=1DpH-icPpl0",
        "Goodbyes": "https://music.youtube.com/watch?v=ba7mB8oueCY",
        "Wow.": "https://music.youtube.com/watch?v=VoDKhNvpCyA",
        "Sunflower": "https://music.youtube.com/watch?v=ApXoWvfEYVU",
        "Better Now": "https://music.youtube.com/watch?v=UYwF-jdcVjY",
        "Psycho": "https://music.youtube.com/watch?v=au2n7VVGv_c",
        "Rockstar": "https://music.youtube.com/watch?v=UceaB4D0jpo",
        "Congratulations": "https://music.youtube.com/watch?v=SC4xMk98Pdc",
        "White Iverson": "https://music.youtube.com/watch?v=SLsTskih7_I",
        "Humble": "https://music.youtube.com/watch?v=tvTRZJ-4EyI",
        "DNA.": "https://music.youtube.com/watch?v=NLZRYQ"
    }

    # Select a random song from the dictionary
    song = random.choice(list(songs.keys()))
    song_url = songs[song]

    # Open the direct URL of the song on YouTube Music
    webbrowser.open(song_url)
    say(f"Opened YouTube Music and started playing {song}.")


def shutdown_assistant():
    say("pleasure working with you sir... call me when needed...")
    sys.exit()  # Exit the script


def chat(query):
    print()


def open_notepad():
    # Path to WhatsApp executable
    notepad_path = "C:\\Windows\\notepad.exe"

    if os.path.exists(notepad_path):
        os.startfile(notepad_path)
        say("Opening notepad.")
    else:
        say("notepad executable not found.")


def generate_response(prompt,max_length=500):
    vertexai.init(project="zenai-429916", location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")

    generation_config = {
        "max_output_tokens": max_length,
        "temperature": 1,
        "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    responses = model.generate_content(
        [sanitize_text(prompt)],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    response_text = ""
    for response in responses:
        response_text += response.text
    return sanitize_text(response_text)


def zen_intro():
    introductions = [
        (
            "Greetings! I’m Zen, your dedicated virtual assistant. With a wealth of knowledge and a readiness to assist, I'm here to make your life easier and more informed. How may I serve you today?"),
        (
            "Hello there! I'm Zen, your ever-ready assistant. My mission is to provide you with insightful answers and assist with your tasks. Feel free to ask me anything; I’m here to help with a touch of elegance."),
        (
            "Welcome! I’m Zen, your sophisticated assistant. Whether you seek information or need help with various tasks, I’m here to assist you with grace and efficiency. What can I do for you today?"),
        (
            "Salutations! Zen at your service. As your virtual assistant, I'm equipped to handle your queries and support your needs with flair. Let me know how I can enhance your day."),
        (
            "Hi! I’m Zen, your charming assistant. My role is to assist, inform, and enrich your experience with thoughtful responses and assistance. How can I assist you in a delightful manner today?")
    ]
    return random.choice(introductions)


def TaskExecution():
    p.press('esc')
    say("Face recognition successful")
    say("welcome back sir")
    while True:
        query = takecommand()
        if "shutdown" in query.lower() or "stop" in query.lower() or "turn off" in query.lower() or "power off" in query.lower() or "shut down" in query.lower():
            shutdown_assistant()
        else:
            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                     ["google", "https://www.google.com"]]
            for site in sites:
                if f"open {site[0]}".lower() in query.lower():
                    say(f"opening {site[0]} sir...")
                    webbrowser.open(site[1])

            # Add play random song functionality
            if "song" in query.lower() or "music" in query.lower():
                say("Playing a random song on YouTube Music.")
                play_random_song()



            elif "time" in query:
                srtfTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Time is {srtfTime} sir..")
            elif "notepad" in query.lower():
                open_notepad()

            elif "introduce" in query.lower() or "yourself" in query.lower() or "about you" in query.lower():
                intro=zen_intro()
                say(intro)

            else:
                response = generate_response(query.lower())
                say(response)
                print(response)


if __name__ == '__main__':
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 2
    names = ['', 'Binit']

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)), )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])
            if (accuracy < 100):
                id = names[id]
                accuracy = " {0}%".format(round(100 - accuracy))
                TaskExecution()
            else:
                id = "unknown"
                accuracy = " {0}%".format(round(100 - accuracy))
            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
    print("Program terminated....")
    cam.release()
    cv2.destroyAllWindows()
