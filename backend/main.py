from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from pathlib import Path

app = FastAPI()

BASE = Path(__file__).parent
pipeline = joblib.load(BASE / "models/preprocessing_pipeline.pkl")
model    = joblib.load(BASE / "models/xgboost_model.pkl")


class StoreData(BaseModel):
    Store: int
    DayOfWeek: int
    Date: str
    Open: int
    Promo: int
    StateHoliday: str
    SchoolHoliday: int
    StoreType: str
    Assortment: str
    CompetitionDistance: float | None = None
    CompetitionOpenSinceMonth: float | None = None
    CompetitionOpenSinceYear: float | None = None
    Promo2: int
    Promo2SinceWeek: float | None = None
    Promo2SinceYear: float | None = None
    PromoInterval: str | None = None


@app.get("/")
def home():
    return {"message": "Sales Forecast API Running"}


@app.post("/predict")
def predict(data: StoreData):

    df = pd.DataFrame([data.model_dump()])

    df["Date"] = pd.to_datetime(df["Date"])

    processed = pipeline.transform(df)

    prediction = model.predict(processed)

    return {
        "predicted_sales": float(prediction[0])
    }