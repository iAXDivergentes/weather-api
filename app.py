import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Definição das chaves da API
WEATHER_API_KEY = "93febb167dc2456eb2b16a97178fb847"  # Chave da OpenWeatherMap
GOOGLE_MAPS_API_KEY = "AIzaSyCE91wNkbAeihp0djs_-qEQfTtLwfOsiTU"  # Chave da Google Maps API

# URL da API do Banco Central para obter a cotação do dólar
DOLLAR_API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"


def get_weather(city):
    """ Obtém os dados climáticos de uma cidade específica no Brasil """
    if not WEATHER_API_KEY:
        return {"erro": "Chave da API não configurada corretamente"}

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BR&appid={WEATHER_API_KEY}&units=metric&lang=pt"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "cidade": data.get("name", "Desconhecida"),
            "temperatura": f"{data['main']['temp']}°C",
            "sensação térmica": f"{data['main']['feels_like']}°C",
            "mínima": f"{data['main']['temp_min']}°C",
            "máxima": f"{data['main']['temp_max']}°C",
            "umidade": f"{data['main']['humidity']}%",
            "vento": f"{data['wind']['speed']} m/s",
            "condição": data["weather"][0]["description"].capitalize()
        }
    else:
        return {"erro": "Não foi possível obter os dados meteorológicos"}


def get_dollar_price():
    """ Obtém a cotação atual do dólar """
    response = requests.get(DOLLAR_API_URL)
    if response.status_code == 200:
        data = response.json()
        return {"cotacao_dolar": f"R$ {data['USDBRL']['bid']}"}
    else:
        return {"erro": "Não foi possível obter a cotação do dólar"}


@app.route('/')
def home():
    """ Endpoint para verificar se a API está ativa """
    return jsonify({"mensagem": "API AgroVix está ativa! Use o endpoint /weather para previsão do tempo."})


@app.route('/weather', methods=['GET'])
def weather_info():
    """ Endpoint para obter os dados do clima + cotação do dólar e Google Maps """
    city = request.args.get('cidade')
    if not city:
        return jsonify({"erro": "Cidade não informada"}), 400

    weather = get_weather(city)
    dollar = get_dollar_price()

    # Link para o Google Maps da cidade
    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={city.replace(' ', '+')},Brasil"

    return jsonify({
        "previsao_tempo": weather,
        "cotacao_dolar": dollar,
        "mapa_google": google_maps_link
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
