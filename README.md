# beve
Discord bot built in Python for my friend group's server. Beve is deployed on a Rasp Pi and thus online 24/7.
Below are Beve's notable commands/events

# Facial Detection
Using "beve sees" followed by an attached image, beve will reply with who in the friend group it sees. This uses the open-cv and face_recognition library, and a dataset of my friend's faces.

# Speak
Using "beve say" followed by a message, beve will speak that message in the voice chat. It makes beve feel "alive" and is pretty funny to use. This uses gTTS library

# Anime Notifications
Whenever an episode of an anime we are tracking comes out (i.e Attack on Titan or Demon Slayer), beve will ping the watchers.

# Horoscope
Entering "beve horoscope your_horoscope" will scrape your horoscope from https://www.horoscope.com/us/index.aspx , a horoscope website which is updated daily
