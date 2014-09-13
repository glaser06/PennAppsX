import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
	audio = r.listen(source)

try:
    list = r.recognize(audio,True)
    for prediction in list:
        print(prediction["text"])
except LookupError:
	print("Could not understand!")
