from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID=2dea9c200c1d79c4faae7b49a845e5fa"


NEWS_API_URL = 'https://newsapi.org/v2/everything?q={0}&apiKey=e749302c7a7944289c2d80437a1c7ed1'


@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    
    weather = get_weather(city)
    news = 'covid'
    news = get_news(news)
    return render_template("home.html", weather=weather, news=news)

@app.route('/news')
def searchnews():
    news = request.args.get('news')
    if not news:
        news = 'covid'
    
    news = get_news(news)

    return render_template("news.html", news=news)

def get_weather(city):
    try:
        query = quote(city)
        url = OPEN_WEATHER_URL.format(query)
        data = urlopen(url).read()
        parsed = json.loads(data)
        weather = None

        if parsed.get('weather'):
    
            description = parsed['weather'][0]['description']
            temperature = parsed['main']['temp']
            pressure = parsed['main']['pressure']
            humidity = parsed['main']['humidity']

            wind = parsed['wind']['speed']
        
            icon =  parsed['weather'][0]['icon']
            url_icon = f"http://openweathermap.org/img/wn/{icon}@2x.png"

            city = parsed['name']
            country = parsed['sys']['country']

            weather = {'description': description,
                    'temperature': temperature,
                    'pressure': pressure,
                    'humidity': humidity,
                    'wind': wind,
                    'city': city,
                    'country': country,
                    'url_icon': url_icon,
                    }
        return weather

    except:
        weather = {'description': "city not found",
                    }
    return weather


def get_news(news):
    try:
        query = quote(news)
        url = NEWS_API_URL.format(query)
        data = urlopen(url).read()
        parsed = json.loads(data)
        news = None

        if parsed.get('articles'):
            countNews = len(parsed['articles'])

            titleList = []
            descriptionList = []
            urlList = []
            urlToImageList = []
            for i in range(countNews):
                title = parsed['articles'][i]['title']
                titleList.append(title)

                description = parsed['articles'][i]['description']
                descriptionList.append(description)

                url = parsed['articles'][i]['url']
                urlList.append(url)

                urlToImage = parsed['articles'][i]['urlToImage']
                urlToImageList.append(urlToImage)

            news = {'countNews': countNews,
                    'titleList': titleList,
                    'descriptionList': descriptionList,
                    'urlList': urlList,
                    'urlToImageList': urlToImageList,
                    }
        return news
    except:
        news = None
        return news
