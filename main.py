from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id_other = os.environ["USER_ID_OTHER"]
template_id = os.environ["TEMPLATE_ID"]
love_heart = os.environ["LOVE_HEART"]

def get_current_date():
  current_date = today.strftime("%m-%d").replace("-","月") + "日"
  return current_date

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  temp_day = str(weather['low']) +"° ~"+ str(weather['high']) +"° "
  return weather['weather'], str(math.floor(weather['temp'])) + "°", temp_day, weather['wind']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d") 
  return delta.days + 1

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, temperature_day, wind = get_weather()
data = {"date":{"value":get_current_date(),"color":"#808080"},"weather":{"value":wea,"color":get_random_color()},"temperature":{"value":temperature,"color":get_random_color()},"temperature_day":{"value":temperature_day,"color":get_random_color()},"wind":{"value":wind,"color":get_random_color()},"love_heart":{"value":love_heart,"color":get_random_color()},"love_days":{"value":get_count(),"color":"#CC00FF"},"birthday_left":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
res2 = wm.send_template(user_id_other, template_id, data)
print(res2)

