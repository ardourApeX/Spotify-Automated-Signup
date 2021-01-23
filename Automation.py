import time
import pyautogui as py
import speech_recognition as sr
import pyaudio
import wave
import pyperclip
from tkinter import Tk
import pandas as pd


months_in_year = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "Novemeber": 11,
    "December": 12

}

genders = {
    "Male": 0,
    "Female": 1,
    "Others": 2,
}


def record_audio():
	'''To Record audio from audio captcha as you can not download the captcha'''
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 6
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return

def recog():
	'''Function to convert Output.wav to text'''
    record_audio()
    filename = "output.wav"
    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        print(text)
    return text

def captcha(email, username, password, month, year, gender, day):
	'''Parameter'''
	global count  
	try:
		text = recog()
		time.sleep(4)
		py.press("tab")
		py.write(text)
		time.sleep(1)
		py.press("tab", presses=5, interval=0.3)	
		time.sleep(0.4)
		py.press("enter")
		time.sleep(2.5)
		py.hotkey("ctrl", "a")
		time.sleep(1)
		py.hotkey("ctrl", "c")

		# Only way to check whether attempt was successful or not
		if Tk().clipboard_get() == "\nI'm not a robot\nPrivacy - Terms": 
			print("success")
			return
		else:
			# Pressing Captcha Refresh Button
			py.press("tab")
			time.sleep(0.2)
			py.press("enter")
			captcha()

	except:
		# If speech recognition fail to recognize or detected as bot
		py.hotkey("altleft", "f4")
		automation(email, username, password, month, year, gender, day) 
		


def automation(email, username, password, month, year, gender, day):

	'''All Commands require to navigate through whole page'''
    py.hotkey("ctrl", "shift", "n") # Using Incognito Tab so that there is no need to signout everytime
    time.sleep(1)
    py.hotkey("winleft", "up")
    time.sleep(0.5)
    py.write("https://www.spotify.com/in/signup/")
    time.sleep(0.5)
    py.press("enter")
    time.sleep(4)
    py.press("tab", presses = 3, interval = 0.5)
    py.press("enter")
    time.sleep(0.3)
    py.press("f5")
    time.sleep(3)
    py.press("tab", presses=2, interval = 0.5)
    time.sleep(0.5)
    py.write(email)
    time.sleep(0.5)
    py.press("tab", presses = 2)
    time.sleep(0.5)
    py.write(email)
    time.sleep(0.5)
    py.press("tab")
    time.sleep(0.5)
    py.write(password)
    time.sleep(0.5)
    py.press("tab")
    time.sleep(1)
    py.write(username)
    time.sleep(1)
    py.press("tab")
    py.write(str(year)) #Pyautogui can only write stirng values
    py.press("tab")
    time.sleep(0.5)
    py.press("down", presses = months_in_year[month])
    time.sleep(0.5)
    py.press("tab")
    py.write(str(day)) 
    time.sleep(1)
    py.press(["tab", "space"], interval = 0.5)
    py.press("right", presses = genders[gender])
    time.sleep(0.5)
    py.press(["tab", "space"])
    time.sleep(0.3)
    py.press("tab")
    time.sleep(1)
    py.press("space")
    time.sleep(5)
    py.press("enter")
    time.sleep(1)
    py.press("enter")
    time.sleep(0.2)
    captcha(email, username, password, month, year, gender, day)
    py.press("tab", presses = 5, interval = 0.5)
    py.press("enter")
    time.sleep(10)
    py.hotkey("altleft", "f4")
    return 
    


if __name__ =="__main__":

	df = pd.read_csv("./dataset.csv", dtype="str")
	py.hotkey('winleft', '2') #Place Chrome at second position on taskbar
	time.sleep(3) # Let chrome open
	dfcopy = df.copy()

	# Passing Each row 
	for i in range(df.shape[0]):
	    automation(*list(dfcopy.iloc[i]))
	    dfcopy.drop(i, inplace = True)
	py.hotkey("altleft", "f4")
	dfcopy.to_csv("./updated_data.csv")