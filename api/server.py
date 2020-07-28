from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import json

app = Flask(__name__)

# depois lembrar de substituir o CORS para o frontend do projeto
cors = CORS(app, resources={r"/*": {"origins": "*"}})

serverLog = {
    "temperature": {
        "value": [26.85, 26.78, 26.77, 26.77, 26.75, 26.81, 26.75, 26.77, 26.78, 26.73],
        "time": [
            "26-03-2020 13:32:00",
            "26-03-2020 13:32:30",
            "26-03-2020 13:33:00",
            "26-03-2020 13:33:30",
            "26-03-2020 13:34:00",
            "26-03-2020 13:34:30",
            "26-03-2020 13:35:00",
            "26-03-2020 13:35:30",
            "26-03-2020 13:36:00",
            "26-03-2020 13:36:30",
        ],
        "ledstatus": "off",
        "threshold": {"min": 25, "max": 30},
    },
    "ph": {
        "value": [7.97, 7.96, 7.95, 7.94, 7.92, 7.91, 7.9, 7.89, 7.88, 7.87],
        "time": [
            "26-03-2020 13:32:00",
            "26-03-2020 13:32:30",
            "26-03-2020 13:33:00",
            "26-03-2020 13:33:30",
            "26-03-2020 13:34:00",
            "26-03-2020 13:34:30",
            "26-03-2020 13:35:00",
            "26-03-2020 13:35:30",
            "26-03-2020 13:36:00",
            "26-03-2020 13:36:30",
        ],
        "ledstatus": "off",
        "threshold": {"min": 6, "max": 7},
    },
    "oxygen": {
        "value": [6.71, 6.62, 6.55, 6.45, 6.35, 6.28, 6.22, 6.15, 6.09, 6.05],
        "time": [
            "26-03-2020 13:32:00",
            "26-03-2020 13:32:30",
            "26-03-2020 13:33:00",
            "26-03-2020 13:33:30",
            "26-03-2020 13:34:00",
            "26-03-2020 13:34:30",
            "26-03-2020 13:35:00",
            "26-03-2020 13:35:30",
            "26-03-2020 13:36:00",
            "26-03-2020 13:36:30",
        ],
    }
}

# Recebe as leituras atuais do ph e temperatura Checa se as mesmas estão
# dentro do threshold. Se sim, muda o status do respectivo led para desligado
# Senão, muda o status do respectivo led para ligado


def decisionHandler(tempReading, phReading):
    global serverLog
    phDecision = "L"
    tempDecision = "L"
    serverLog["ph"]["ledstatus"] = "off"
    serverLog["temperature"]["ledstatus"] = "off"

    tempMin = serverLog["temperature"]["threshold"]["min"]
    tempMax = serverLog["temperature"]["threshold"]["max"]

    phMin = serverLog["ph"]["threshold"]["min"]
    phMax = serverLog["ph"]["threshold"]["max"]

    if phReading < phMin or phReading > phMax:
        phDecision = "H"
        serverLog["ph"]["ledstatus"] = "on"

    if tempReading < tempMin or tempReading > tempMax:
        tempDecision = "H"
        serverLog["temperature"]["ledstatus"] = "on"

    return tempDecision, phDecision


# Retorna um html com a explicação dos endpoints da API
@app.route("/")
def teste():
    return app.send_static_file("index.html")

# Retorna o log do servidor, pode receber uma variavel
# amount, que representa a quantidade de dados a serem
# retornados
@app.route("/log")
def log():
    global serverLog
    amount = request.args.get("amount")
    if amount != None and len(serverLog["temperature"]["value"]) > 0:
        amount = int(amount)
        if amount <= 0:
            return jsonify("invalid amount!"), 400
        if len(serverLog["temperature"]["value"]) > amount:
            amount = -amount
            auxLog = {
                "temperature": {
                    "value": serverLog["temperature"]["value"][amount:],
                    "time": serverLog["temperature"]["time"][amount:],
                    "ledstatus": serverLog["temperature"]["ledstatus"],
                    "threshold": serverLog["temperature"]["threshold"]
                },
                "ph": {
                    "value": serverLog["ph"]["value"][amount:],
                    "time": serverLog["ph"]["time"][amount:],
                    "ledstatus": serverLog["ph"]["ledstatus"],
                    "threshold": serverLog["ph"]["threshold"]
                },
                "oxygen": {
                    "value": serverLog["oxygen"]["value"][amount:],
                    "time": serverLog["oxygen"]["time"][amount:],
                }
            }
            return jsonify(auxLog)
    return jsonify(serverLog)

# Retorna a ultima leitura dos sensores, bem
# como os status dos leds e bombas d'água
@app.route("/lastreading")
def reading():
    global serverLog
    if len(serverLog["temperature"]["value"]) > 0:
        auxLog = {
            "temperature": {
                "value": serverLog["temperature"]["value"][-1],
                "time": serverLog["temperature"]["time"][-1],
                "ledstatus": serverLog["temperature"]["ledstatus"],
                "threshold": serverLog["temperature"]["threshold"]
            },
            "ph": {
                "value": serverLog["ph"]["value"][-1],
                "time": serverLog["ph"]["time"][-1],
                "ledstatus": serverLog["ph"]["ledstatus"],
                "threshold": serverLog["ph"]["threshold"]
            },
            "oxygen": {
                "value": serverLog["oxygen"]["value"][-1],
                "time": serverLog["oxygen"]["time"][-1],
            }
        }
        return jsonify(auxLog)

# Configura o threshold de operação das bombas d'água
# Recebe uma variavel que seleciona o sensor a ser configurado
@app.route("/config/<sensor>", methods=["PUT"])
def config(sensor):
    if sensor != "temperature" and sensor != "ph":
        return jsonify("there are only temperature and ph sensor until now!"), 404
    global serverLog
    min = request.args.get("min")
    max = request.args.get("max")
    if min != None and max != None:
        if min < max:
            serverLog[sensor]["threshold"]["min"] = float(min)
            serverLog[sensor]["threshold"]["max"] = float(max)
            return jsonify("threshold updated!")
    return jsonify("threshold values invalid"), 400

# Rota que recebe os dados da camada fisica e os salva no
# database (por hora o database é um dicionario local)
# TODO criar database mysql
@app.route("/save", methods=["POST"])
def save():
    readingTime = datetime.now()
    readingTime = readingTime.strftime("%d-%m-%Y %H:%M:%S")

    content = request.get_json()
    serverLog["temperature"]["value"].append(content["temperature"])
    serverLog["temperature"]["time"].append(readingTime)
    serverLog["ph"]["value"].append(content["ph"])
    serverLog["ph"]["time"].append(readingTime)

    print(
        "\ntemperature = {}°c\nph = {}\ntempo = {}\n".format(
            content["temperature"], content["ph"], readingTime
        )
    )

    tempDecision, phDecision = decisionHandler(
        content["temperature"], content["ph"])
    return jsonify({
        "ledTemp": tempDecision,
        "ledPh": phDecision,
    })

# Limpa todos os dados de leitura dos sensores salvos no database
@app.route("/clear", methods=["DELETE"])
def clear():
    global serverLog
    serverLog["temperature"]["value"].clear()
    serverLog["temperature"]["time"].clear()
    serverLog["ph"]["value"].clear()
    serverLog["ph"]["time"].clear()
    return jsonify("logs cleaned!")


if __name__ == "__main__":
    #app.run(ssl_context=('./ssl/rsa_cert.pem', './ssl/rsa_private.pem'))
    app.run()
