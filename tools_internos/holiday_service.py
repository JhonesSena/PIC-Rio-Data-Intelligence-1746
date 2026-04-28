import requests
import pandas as pd

class HolidayService:
    """
    Serviço para extração de feriados da Public Holiday API (Nager.Date).
    """
    BASE_URL = "https://date.nager.at/api/v3/PublicHolidays"

    def get_holidays(self, year, country_code="BR"):
        """
        Busca feriados para um determinado ano e país.
        """
        url = f"{self.BASE_URL}/{year}/{country_code}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        return df

    def get_long_weekends(self, year, country_code="BR"):
        """
        Busca feriados prolongados (Long Weekends).
        Diferencial: Fins de semana prolongados impactam a demanda de forma distinta.
        """
        url = f"https://date.nager.at/api/v3/LongWeekend/{year}/{country_code}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data)
        df['startDate'] = pd.to_datetime(df['startDate'])
        df['endDate'] = pd.to_datetime(df['endDate'])
        
        return df

if __name__ == "__main__":
    # Teste simples
    service = HolidayService()
    try:
        df = service.get_holidays(2023)
        print("Feriados de 2023 obtidos com sucesso:")
        print(df[['date', 'localName', 'name']].head())
    except Exception as e:
        print(f"Erro ao obter feriados: {e}")
