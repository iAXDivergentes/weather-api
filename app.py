from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Chave da API OpenWeather (substitua pela sua)
WEATHER_API_KEY = "93febb167dc2456eb2b16a97178fb847"

def get_weather(city):
    """ Obtém os dados climáticos de uma cidade específica """

    if not WEATHER_API_KEY:
        return jsonify({"erro": "Chave da API não configurada corretamente"}), 500

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},BR&appid={WEATHER_API_KEY}&units=metric&lang=pt"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança um erro caso a resposta não seja 200

        data = response.json()

        if "main" not in data or "weather" not in data:
            return jsonify({"erro": "Resposta inesperada da API OpenWeather", "detalhes": data}), 500

        return jsonify({
            "cidade": data.get("name", "Desconhecida"),
            "temperatura": f"{data['main']['temp']}°C",
            "sensação térmica": f"{data['main']['feels_like']}°C",
            "mínima": f"{data['main']['temp_min']}°C",
            "máxima": f"{data['main']['temp_max']}°C",
            "umidade": f"{data['main']['humidity']}%",
            "vento": f"{data['wind']['speed']} m/s",
            "condição": data["weather"][0]["description"].capitalize()
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Erro na requisição à API OpenWeather", "detalhes": str(e)}), 500

@app.route('/')
def home():
    """ Endpoint para a raiz da API """
    return jsonify({"mensagem": "API de previsão do tempo está ativa! Use o endpoint /weather para consultar."})

@app.route('/weather', methods=['GET'])
def weather_info():
    """ Endpoint para obter os dados do clima """
    city = request.args.get('cidade')

    if not city:
        return jsonify({"erro": "Cidade não informada"}), 400

    return get_weather(city)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
