from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from models.model import WeatherPredictor
import uvicorn
import numpy as np
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.post("/weather")
async def predict(request: Request):

    body = await request.json()
    x = [[body['app_temp'],body['hum'],body['wsp'],body['wdir'],body['nua'],body['prec'],body['vis']]]
    model = WeatherPredictor()
    result = model.predict_next_15(x)[0]
    infos = dict()
    for i in range(len(result)):
        infos[f"t{str(i+1)}"] = float(result[i])

    return {
        "status": "OK",
        "temps": infos
    }

if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=4555)