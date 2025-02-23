import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Chaves da API
WEATHER_API_KEY = "93febb167dc2456eb2b16a97178fb847"  # OpenWeatherMap
GOOGLE_MAPS_API_KEY = "AIzaSyCE91wNkbAeihp0djs_-qEQfTtLwfOsiTU"  # Google Maps

# URLs para as cotações de moedas e Bitcoin
DOLLAR_API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
EURO_API_URL = "https://economia.awesomeapi.com.br/json/last/EUR-BRL"
BITCOIN_API_URL = "https://economia.awesomeapi.com.br/json/last/BTC-BRL"

# URLs das commodities agrícolas
SOJA_URL = "https://www.noticiasagricolas.com.br/cotacoes/soja"
MILHO_URL = "https://www.noticiasagricolas.com.br/cotacoes/milho"
ALGODAO_URL = "https://www.noticiasagricolas.com.br/cotacoes/algodao"

def get_weather(city):
    """ Obtém os dados climáticos de uma cidade específica no Brasil """
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

def get_currency_price(api_url, currency_name):
    """ Obtém a cotação da moeda ou Bitcoin em tempo real """
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return {currency_name: f"R$ {data[list(data.keys())[0]]['bid']}"}
    else:
        return {currency_name: "Erro ao obter cotação"}

def get_commodities_price():
    """ Obtém os preços das commodities agrícolas """
    try:
        response_soja = requests.get(SOJA_URL)
        response_milho = requests.get(MILHO_URL)
        response_algodao = requests.get(ALGODAO_URL)

        # Simulação de extração dos preços (deve ser ajustado com BeautifulSoup para raspagem de dados)
        preco_soja = "R$ 130,00"  # Simulação
        preco_milho = "R$ 60,00"   # Simulação
        preco_algodao = "R$ 180,00/ha"  # Simulação

        return {
            "soja": preco_soja,
            "milho": preco_milho,
            "algodao": preco_algodao
        }
    except Exception as e:
        return {"erro": f"Erro ao obter preços das commodities: {str(e)}"}

@app.route('/')
def home():
    """ Endpoint para verificar se a API está ativa """
    return jsonify({"mensagem": "API AgroVix está ativa! Use o endpoint /weather para previsão do tempo e /cotacoes para ver as cotações."})

@app.route('/weather', methods=['GET'])
def weather_info():
    """ Endpoint para obter os dados do clima + cotação do dólar e Google Maps """
    city = request.args.get('cidade')
    if not city:
        return jsonify({"erro": "Cidade não informada"}), 400

    weather = get_weather(city)
    dollar = get_currency_price(DOLLAR_API_URL, "cotacao_dolar")
    euro = get_currency_price(EURO_API_URL, "cotacao_euro")
    bitcoin = get_currency_price(BITCOIN_API_URL, "cotacao_bitcoin")
    commodities = get_commodities_price()

    # Link para o Google Maps da cidade
    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={city.replace(' ', '+')},Brasil"

    return jsonify({
        "previsao_tempo": weather,
        "cotacao_dolar": dollar,
        "cotacao_euro": euro,
        "cotacao_bitcoin": bitcoin,
        "commodities": commodities,
        "mapa_google": google_maps_link
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
