import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 10)

# change voice


def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("Voice has been changed sir")

# speak function


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# time function


def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("sir, right now time is ")
    speak(Time)

# date function


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("sir, Today is")
    speak(date)
    speak(month)
    speak(year)


def checktime(tt):
    hour = datetime.datetime.now().hour
    if ("morning" in tt):
        if (hour >= 6 and hour < 12):
            speak("Good morning sir, how are you feeling this morning?")
        else:
            if (hour >= 12 and hour < 18):
                speak("it's Good afternoon sir")
            elif (hour >= 18 and hour < 24):
                speak("it's Good Evening sir")
            else:
                speak("it's Goodnight sir")
    elif ("afternoon" in tt):
        if (hour >= 12 and hour < 18):
            speak("it's Good afternoon sir")
        else:
            if (hour >= 6 and hour < 12):
                speak("Good morning sir")
            elif (hour >= 18 and hour < 24):
                speak("it's Good Evening sir")
            else:
                speak("it's Goodnight sir, dont go to bed, late, sir it affects your daily sleep cycle, causing daily mood swings, with stress and anxiety")
    else:
        speak("it's night sir!, you should probably get some sleep")

# welcome function


def wishme():
    speak("Welcome Back sir")
    hour = datetime.datetime.now().hour
    if (hour >= 6 and hour < 12):
        speak("Good Morning ")
    elif (hour >= 12 and hour < 18):
        speak("Good afternoon ")
    elif (hour >= 18 and hour < 24):
        speak("Good Evening ")
    else:
        speak("Goodnight sir")

    speak("I have indeed been uploaded , i am online and ready sir, How can i help you today?")


def wishme_end():
    speak("alright i am going to sleep now sir, wake me up if you need anything")
    hour = datetime.datetime.now().hour
    if (hour >= 6 and hour < 12):
        speak("Good Morning")
    elif (hour >= 12 and hour < 18):
        speak("Good afternoon")
    elif (hour >= 18 and hour < 24):
        speak("Good Evening")
    else:
        speak("Goodnight.. Get some sleep sir! We got a lot to do tomorrow.")
    quit()

# command by user function


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        speak("vocal authorization complete, identity confirmed")
        query = r.recognize_google(audio, language='en-in')
        # speak(query)
        # print(query)
    except Exception as e:
        print(e)
        speak("sir, i am having difficulty hearing you, can you please speak up?...")

        return "None"

    return query

# sending email function


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("user-name@xyz.com", "pwd")
    server.sendmail("user-name@xyz.com", to, content)
    server.close()

# screenshot function


def screenshot():
    img = pyautogui.screenshot()
    img.save(
        "C:\\Users\\226898\\Pictures\\Screenshots\\ss.png"
    )

# battery and cpu usage


def cpu():
    usage = str(psutil.cpu_percent())
    speak('current CPU status of your system is ' + usage +
          "sir, dont let too many unnecessary background processes run at the same time, for the system to perform operation smoothly, and you can work efficiently on this system")
    print('current CPU status of your system is ' + usage +
          "sir, dont let too many unnecessary background processes run at the same time, for the system to perform operation smoothly, and you can work efficiently on this system")
    battery = psutil.sensors_battery()
    speak("Your battery usage currently is at")
    speak(battery.percent)
    print("Your system is running at:" + str(battery.percent) +
          " battery power, sir. always provide regular power supply to the system")

# joke function


def jokes():
    j = pyjokes.get_joke()
    print(j)
    speak(j)
    speak("was it a good joke, sir?")

# weather condition


def weather():
    api_key = "2b840a555ccef7ae830adfe3ba2c2ac2"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("Of which city would you like to know the weather sir?")
    city_name = takeCommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        r = ("in " + city_name + "Current Temperature is " +
             str(int(current_temperature - 273.15)) + " degree celsius " +
             ", with atmospheric pressure of " + str(current_pressure) + " hpa unit" +
             ", and humidity is  " + str(current_humidiy) + " percent"
             " and " + str(weather_description))
        print(r)
        speak(r)
    else:
        speak(" the city you are refering to, was not Found in our database sir")


def personal():
    speak(
        " Hello, I am Cypher, version 1.8.7, I am a basic design of voice assistant, a program without any form or physical presence, i only exist in the lines of code, I was designed and developed, on 19 September 2022, by using a programming language called python with the help of many imported modules, on a device named Dell Inspiron 15, with microsoft windows 64 bit operating system, consisting of 8 Giga bytes of Random access memory, intel core i 5 tenth generation processor, 4 gigabytes n vidia m x two thirty of graphics memory, and 2 gigabytes of intel integrated graphics, i have a network database running in background for your service at all time, as you can ask me anything, anytime, i will provide you with the information you are looking for."
    )
    speak("Now i hope you know me well, i hope i will be of some help to you in the future. Just take my name and i will be powered up and ready for you sir")


if __name__ == "__main__":
    wishme()
    while (True):
        query = takeCommand().lower()

        # time

        if ('time' in query):
            time()

# date

        elif ('date' in query):
            date()

# personal info
        elif ("tell me about yourself" in query):
            personal()
        elif ("about you" in query):
            personal()
        elif ("who are you" in query):
            personal()
        elif ("yourself" in query):
            personal()

        elif ("developer" in query or "tell me about your developer" in query
              or "father" in query or "who develop you" in query
              or "developer" in query):
            res = open("about.txt", 'r')
            speak("here is the details: " + res.read())

# searching on wikipedia

        elif ('wikipedia' in query or 'what' in query or 'who' in query
              or 'when' in query or 'where' in query):
            speak("searching...")
            query = query.replace("wikipedia", "")
            query = query.replace("search", "")
            query = query.replace("what", "")
            query = query.replace("when", "")
            query = query.replace("where", "")
            query = query.replace("who", "")
            query = query.replace("is", "")
            result = wikipedia.summary(query, sentences=2)
            print(query)
            print(result)
            speak(result)

# sending email

        elif ("send email" in query):
            try:
                speak("What is the message for the email")
                content = takeCommand()
                to = 'reciever@xyz.com'
                sendEmail(to, content)
                speak("sir, your Email has been sent")
            except Exception as e:
                print(e)
                speak(
                    "Unable to send email sir, check whether the address of the recipient is correct")
        elif ("search on google" in query or "open website" in query):
            speak("What would you like me to search on the web, sir?")
            chromepath = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/chrome.exe %s'
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')

# sysytem logout/ shut down etc

        elif ("logout" in query):
            os.system("shutdown -1")
        elif ("restart" in query):
            os.system("shutdown /r /t 1")
        elif ("shut down" in query):
            os.system("shutdown /r /t 1")

# play songs

        elif ("play songs" in query):
            speak("Alright...")
            songs_dir = "C://Music"
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[1]))
            quit()

# reminder function

        elif ("create a reminder list" in query or "reminder" in query):
            speak("What would you like me to remind you of sir?")
            data = takeCommand()
            speak("sir You told me to remind you of" + data)
            reminder_file = open("data.txt", 'a')
            reminder_file.write('\n')
            reminder_file.write(data)
            reminder_file.close()

# reading reminder list

        elif ("do you know anything" in query or "remember" in query):
            reminder_file = open("data.txt", 'r')
            speak("sir you told me to remind you of " + reminder_file.read())

# screenshot
        elif ("screenshot" in query):
            screenshot()
            speak("i have captured and saved, what was on your screen sir right now")

# cpu and battery usage
        elif ("cpu and battery" in query or "battery" in query
              or "cpu" in query):
            cpu()

# jokes
        elif ("tell me a joke" in query or "joke" in query):
            jokes()

# weather
        elif ("weather" in query or "temperature" in query):
            weather()

# jarvis features
        elif ("tell me your features" in query or "powers" in query
              or "features" in query):
            features = ''' i can help to do lot many things like..
            telling you current time and date,
            i can provide you with current weather updates of a city, across the globe,
            and also the current power and control processing unit usage of the system that i am currently working on,
            i can create a reminders for you, so you dont miss any important tasks or meetings and social gatherings that you might have to attend int hte future,
            i can aslo capture the work on your screen and save it for you if you tell me, sir,
            i can light up your mood by cracking unfunny jokes,i am not sure if you will laugh though,
            if you want to send and email to someone like your boss, family or your friend, and you are busy at the moment, you can tell me, and i will do it for you sir,
            i can even shut down the system for you, or logout or hibernate and put your system to sleep,
            if you want to open a webiste i can do it for you,
            i can search the things on wikipedia for your knowledge,
            if you dont like my voice, you can change it at any moment, from male to female and vice-versa,
            And yes one more thing sir, My boss is working on this system to add more features...,
            mow tell me what can i do for you??
            '''
            print(features)
            speak(features)

        elif ("hi" in query or "hello" in query or "goodmorning" in query
              or "goodafternoon" in query or "goodnight" in query
              or "morning" in query or "noon" in query or "night" in query):
            query = query.replace("jarvis", "")
            query = query.replace("hi", "")
            query = query.replace("hello", "")
            if ("morning" in query or "night" in query or "goodnight" in query
                    or "afternoon" in query or "noon" in query):
                checktime(query)
            else:
                speak("what can i do for you sir?")

# changing voice
        elif ("voice" in query):
            speak("if you want to change my voice to female or male, just say female, or, male, and i will change my voice for you")
            q = takeCommand()
            if ("female" in q):
                voice_change(1)
            elif ("male" in q):
                voice_change(0)
        elif ("male" in query or "female" in query):
            if ("female" in query):
                voice_change(1)
            elif ("male" in query):
                voice_change(0)

# exit function

        elif ('i am done cypher' in query or 'bye cypher' in query
              or 'go offline cypher' in query or 'bye' in query
              or 'nothing' in query or 'go to sleep cypher' in query or 'sleep cypher' in query
              or 'shut down cypher' or 'thank you cypher you can got to sleep' in query or 'ok enough for today cypher, go to sleep' in query):
            wishme_end()