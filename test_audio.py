from gtts import gTTS
from playsound import playsound
import tempfile
import os
import random

def announce_message(message):
    tts = gTTS(text=message, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    tts.save(temp_file.name)
    playsound(temp_file.name)
    os.unlink(temp_file.name)  # Delete the temp file

def motivate():
    messages = [
        "Come on, get your speed back!",
        "You're losing momentum, push through!",
        "That's it, keep moving!",
        "Don't stop now, you've got this!",
        "Almost there, give it all you've got!",
    ]
    announce_message(random.choice(messages))

# Example usage
for count in range(1, 111):  # Simulate counts
    if count % 3 == 0:  # Example condition to motivate
        motivate()
    announce_message(str(count))
