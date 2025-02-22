from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Chave da API OpenWeather
WEATHER_API_KEY = "93febb167dc2456eb2b16a97178fb847"

def get_weather(city):
    """ Obtém os dados climáticos de uma cidade específica """
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

@app.route('/')
def home():
    """ Endpoint para a raiz da API """
    return jsonify({"mensagem": "API de previsão do tempo está ativa! Use o endpoint /weather para consultar."}, ensure_ascii=False)

@app.route('/weather', methods=['GET'])
def weather_info():
    """ Endpoint para obter os dados do clima """
    city = request.args.get('cidade')

    if not city:
        return jsonify({"erro": "Cidade não informada"}, ensure_ascii=False), 400

    weather = get_weather(city)
    return jsonify(weather, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
