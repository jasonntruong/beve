import requests

URL = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=7"
page = requests.get(URL)

words = page.text.split("</strong>")
te = words[1].split("</p>")
print(te[0][3:])