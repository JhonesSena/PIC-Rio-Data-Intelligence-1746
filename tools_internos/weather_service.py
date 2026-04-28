import requests
import pandas as pd
from datetime import datetime

class WeatherService:
    """
    Serviço para extração de dados climáticos da Open-Meteo API.
    """
    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
    
    def __init__(self, lat=-22.9064, lon=-43.1729):
        self.lat = lat
        self.lon = lon

    def get_historical_weather(self, start_date, end_date):
        """
        Busca dados históricos de temperatura e precipitação em lote (batch).
        Minimiza o número de requisições à API para otimizar performance e custo.
        Formato das datas: 'YYYY-MM-DD'
        """
        print(f"Buscando dados climáticos de {start_date} até {end_date}...")
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "weather_code"],
            "timezone": "America/Sao_Paulo"
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        daily_data = data.get("daily", {})
        
        df = pd.DataFrame(daily_data)
        df['time'] = pd.to_datetime(df['time'])
        
        # Otimização: Renomear para facilitar o merge posterior
        df.rename(columns={'time': 'data'}, inplace=True)
        
        return df

if __name__ == "__main__":
    # Teste simples
    service = WeatherService()
    try:
        df = service.get_historical_weather("2023-01-01", "2023-01-07")
        print("Dados climáticos obtidos com sucesso:")
        print(df.head())
    except Exception as e:
        print(f"Erro ao obter dados: {e}")
