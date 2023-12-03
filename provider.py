import json
from flask import Flask, jsonify, request
import requests 

class Provider:

    def serviceInfoRequest(serviceName):
        port = 0
        containerName = ""

        if serviceName == "pastyields":
            port = 4000
            containerName = "pastyields"

        elif serviceName == "datadisplay":
            port = 4001
            containerName = "datadisplayer"

        elif serviceName == "rankbysector":
            port = 4002
            containerName = "ranker"
        
        endpoint = f"http://{containerName}:{port}/info"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error calling container1 endpoint: {response.status_code}")
            return {"message": f"Error calling container2 endpoint: {response.status_code}"}



app = Flask(__name__)


#Manual Register
@app.route('/getinfo', methods=['GET'])
def manualRegister():
    #get service information 
    serviceName = request.args.get('serviceName')
    serviceInfo = Provider.serviceInfoRequest(serviceName)
    #send request to register into registry 
    registerURL = "http://registry:4004//register-service"
    response = requests.post(registerURL, json=serviceInfo)
    response_data = {
        "status_code": response.status_code,
        "content": response.text  # You can adjust this based on the content type of the response
    }
    return {"mes": response_data}

#Manual Deregister
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4003)