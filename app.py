import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔑 CHAVES DAS APIS
WEATHER_API_KEY = "93febb167dc2456eb2b16a97178fb847"  # OpenWeatherMap
GOOGLE_MAPS_API_KEY = "AIzaSyCE91wNkbAeihp0djs_-qEQfTtLwfOsiTU"  # Google Maps

# 🌎 URLs PARA COTAÇÕES EM TEMPO REAL
DOLLAR_API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
EURO_API_URL = "https://economia.awesomeapi.com.br/json/last/EUR-BRL"
BITCOIN_API_URL = "https://economia.awesomeapi.com.br/json/last/BTC-BRL"

# 🌱 SIMULAÇÃO DE PREÇOS DE COMMODITIES AGRÍCOLAS
def get_commodities():
    return {
        "algodão": "R$ 180,00/ha",
        "milho": "R$ 60,00/saca",
        "soja": "R$ 130,00/saca"
    }

# 🌦️ FUNÇÃO PARA PEGAR O CLIMA
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city},BR&appid={WEATHER_API_KEY}&units=metric&lang=pt"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast = data['list'][0]  # Previsão mais recente

        # Pegando as temperaturas máxima e mínima do dia
        max_temp = max([item['main']['temp_max'] for item in data['list'][:8]])
        min_temp = min([item['main']['temp_min'] for item in data['list'][:8]])

        return {
            "cidade": data["city"]["name"],
            "condição": forecast["weather"][0]["description"].capitalize(),
            "máxima": f"{max_temp:.1f}°C",
            "mínima": f"{min_temp:.1f}°C",
            "sensação térmica": f"{forecast['main']['feels_like']:.1f}°C",
            "temperatura": f"{forecast['main']['temp']:.1f}°C",
            "umidade": f"{forecast['main']['humidity']}%",
            "vento": f"{forecast['wind']['speed']} m/s"
        }
    else:
        return {"erro": "Não foi possível obter os dados meteorológicos"}

# 💰 FUNÇÃO PARA PEGAR A COTAÇÃO DE MOEDAS E BITCOIN
def get_currency_price(api_url, currency_name):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        valor = float(data[list(data.keys())[0]]['bid'])
        return {currency_name: f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}
    else:
        return {currency_name: "Erro ao obter cotação"}

# 🔥 ENDPOINT PRINCIPAL
@app.route('/')
def home():
    return jsonify({
        "mensagem": "API AgroVix está ativa! Use o endpoint /weather para previsão do tempo e /cotacoes para ver as cotações."
    })

# 🌤️ ENDPOINT PARA CLIMA
@app.route('/weather', methods=['GET'])
def weather_info():
    city = request.args.get('cidade')
    if not city:
        return jsonify({"erro": "Cidade não informada"}), 400

    weather = get_weather(city)
    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={city.replace(' ', '+')},Brasil"

    return jsonify({
        "previsão_tempo": weather,
        "mapa_google": google_maps_link
    })

# 💲 ENDPOINT PARA COTAÇÕES
@app.route('/cotacoes', methods=['GET'])
def cotacoes():
    dollar = get_currency_price(DOLLAR_API_URL, "cotação_dólar")
    euro = get_currency_price(EURO_API_URL, "cotação_euro")
    bitcoin = get_currency_price(BITCOIN_API_URL, "cotação_bitcoin")
    commodities = get_commodities()

    return jsonify({
        "cotação_dólar": dollar,
        "cotação_euro": euro,
        "cotação_bitcoin": bitcoin,
        "commodities": commodities
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
