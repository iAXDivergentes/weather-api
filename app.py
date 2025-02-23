import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Chaves da API (Variáveis de Ambiente)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "93febb167dc2456eb2b16a97178fb847")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "AIzaSyCE91wNkbAeihp0djs_-qEQfTtLwfOsiTU")

# URLs para cotações
DOLLAR_API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
EURO_API_URL = "https://economia.awesomeapi.com.br/json/last/EUR-BRL"
BITCOIN_API_URL = "https://economia.awesomeapi.com.br/json/last/BTC-BRL"

def get_commodities():
    """ Simulação para commodities agropecuárias """
    return {
        "algodão": "R$ 180,00/ha",
        "milho": "R$ 60,00/saca",
        "soja": "R$ 130,00/saca"
    }

def get_weather(city):
    """ Obtém os dados climáticos """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BR&appid={WEATHER_API_KEY}&units=metric&lang=pt"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "cidade": data["name"],
            "condição": data["weather"][0]["description"].capitalize(),
            "temperatura": f"{data['main']['temp']}°C",
            "sensação térmica": f"{data['main']['feels_like']}°C",
            "mínima": f"{data['main']['temp_min']}°C",
            "máxima": f"{data['main']['temp_max']}°C",
            "umidade": f"{data['main']['humidity']}%",
            "vento": f"{data['wind']['speed']} m/s"
        }
    else:
        return {"erro": "Não foi possível obter os dados meteorológicos"}

def get_currency_price(api_url, currency_name):
    """ Obtém a cotação da moeda ou Bitcoin """
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        valor = float(data[list(data.keys())[0]]['bid'])
        return {currency_name: f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")}
    else:
        return {currency_name: "Erro ao obter cotação"}

@app.route('/', methods=['GET'])
def home():
    """ Verifica se a API está ativa """
    return jsonify({"mensagem": "API AgroVix está ativa! Use o endpoint /weather para previsão do tempo e /cotacoes para ver as cotações."})

@app.route('/weather', methods=['GET'])
def weather_info():
    """ Obtém previsão do tempo + cotações """
    city = request.args.get('cidade')
    if not city:
        return jsonify({"erro": "Cidade não informada"}), 400

    weather = get_weather(city)
    dollar = get_currency_price(DOLLAR_API_URL, "cotação_dólar")
    euro = get_currency_price(EURO_API_URL, "cotação_euro")
    bitcoin = get_currency_price(BITCOIN_API_URL, "cotação_bitcoin")
    commodities = get_commodities()

    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={city.replace(' ', '+')},Brasil"

    return jsonify({
        "previsão_tempo": weather,
        "cotação_dólar": dollar,
        "cotação_euro": euro,
        "cotação_bitcoin": bitcoin,
        "commodities": commodities,
        "mapa_google": google_maps_link
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
