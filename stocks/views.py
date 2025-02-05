import yfinance as yf
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse
import requests
import yfinance as yf
from forex_python.converter import CurrencyRates
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates

@api_view(['GET'])
def test_req(request):
    return Response("Testres")

# Method to get mutual fund NAV
@api_view(['GET'])
def get_mf_price(request, symbol):
    try:
        # Construct the full mutual fund symbol (e.g., HDFC00000001.BO for an Indian MF on BSE)
        mf_symbol = f"{symbol}.BO"  # Using .BO for BSE-listed mutual funds
        
        # Fetch the mutual fund data from Yahoo Finance
        mf = yf.Ticker(mf_symbol)
        price_data = mf.history(period="1d")
        
        # If no data is found, return a meaningful error message
        if price_data.empty:
            return Response({"error": f"No data found for mutual fund {symbol}. Possibly delisted or incorrect symbol."}, status=404)
        
        # Get the most recent NAV and round it to 2 decimal places
        nav = price_data['Close'].iloc[-1]
        rounded_nav = round(nav, 2)
        
        return Response({"symbol": symbol, "nav": rounded_nav})
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)


# View to get stock price with stock exchange as parameter
@api_view(['GET'])
def get_stock_price(request, exchange, symbol):
    try:
        # Map exchange to correct Yahoo Finance suffix
        exchange_suffix = {
            "nse": ".NS",  # For NSE stocks
            "nasdaq": "",  # For NASDAQ stocks (e.g., Google: GOOGL.O)
            "nyse": ".N"  # For NYSE stocks
        }
        
        # Check if the provided exchange is valid
        if exchange.lower() not in exchange_suffix:
            return Response({"error": "Invalid stock exchange. Supported exchanges: NSE, NASDAQ, NYSE."}, status=400)

        # Construct the full stock symbol (e.g., GOOGL.O for Google on NASDAQ, RELIANCE.NS for Reliance on NSE)
        stock_symbol = f"{symbol}{exchange_suffix[exchange.lower()]}"
        
        # Fetch the stock data
        stock = yf.Ticker(stock_symbol)
        price_data = stock.history(period="1d")
        
        # If no data is found, return a meaningful error message
        if price_data.empty:
            return Response({"error": f"No data found for {symbol} on {exchange.upper()}. Possibly delisted or incorrect symbol."}, status=404)
        
        # Get the most recent stock price and round to 2 decimal places
        price = price_data['Close'].iloc[-1]
        rounded_price = round(price, 2)
        
        return Response({"symbol": symbol, "exchange": exchange.upper(), "price": rounded_price})
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
# View to get currency exchange rate
@api_view(['GET'])
def get_currency_exchange(request, symbol):
    try:
        # Yahoo Finance ticker for currency exchange
        exchange_rate = yf.Ticker(f"{symbol}=X")
        
        # Get the most recent exchange rate
        price = exchange_rate.history(period="1d")['Close'].iloc[-1]
        
        # Round to 2 decimal places
        rounded_exchange_rate = round(price, 2)
        
        return Response({"symbol": symbol, "exchange_rate": rounded_exchange_rate})
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
# Method to get mutual fund NAV
@api_view(['GET'])
def get_mf_price(request, symbol):
    try:
        # Construct the full mutual fund symbol (e.g., HDFC00000001.BO for an Indian MF on BSE)
        mf_symbol = f"{symbol}.BO"  # Using .BO for BSE-listed mutual funds
        
        # Fetch the mutual fund data from Yahoo Finance
        mf = yf.Ticker(mf_symbol)
        price_data = mf.history(period="1d")
        
        # If no data is found, return a meaningful error message
        if price_data.empty:
            return Response({"error": f"No data found for mutual fund {symbol}. Possibly delisted or incorrect symbol."}, status=404)
        
        # Get the most recent NAV and round it to 2 decimal places
        nav = price_data['Close'].iloc[-1]
        rounded_nav = round(nav, 2)
        
        return Response({"symbol": symbol, "nav": rounded_nav})
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    

    # Method to get currency exchange rate


@api_view(['GET'])
def get_currency_rate(request, from_currency, to_currency):
    """
    This method scrapes Google search to fetch the exchange rate from one currency to another.
    """
    # Construct the Google search URL
    url = f"https://www.google.com/search?q={from_currency}+to+{to_currency}+exchange+rate"
    
    try:
        # Send a GET request to Google
        response = requests.get(url)
        
        # Check if the response status is OK (200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for the exchange rate in the page content (Google search result)
            rate = None
            try:
                # Google's exchange rate is usually in a span tag with this class
                # rate = soup.find("span", class_="DFlfde SwHCTb").text
                # return JsonResponse({
                #     "from_currency": from_currency,
                #     "to_currency": to_currency,
                #     "rate": rate
                # })
                exchange_rate = soup.find("div", {"class": "YMlKec fxKbKc"}).text
                response_data = {
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'exchange_rate': float(exchange_rate),
                }
                return Response(response_data)
            except AttributeError:
                return JsonResponse({"error": "Could not find the exchange rate on the page."}, status=404)
        else:
            return JsonResponse({"error": f"Failed to retrieve data. Status code: {response.status_code}"}, status=500)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

@api_view(['GET'])
def get_exchange_rate(request):
    # Get query parameters for 'from_currency' and 'to_currency'
    from_currency = request.query_params.get('from', 'USD').upper()
    to_currency = request.query_params.get('to', 'EUR').upper()

    # Fetch the exchange rate
    c = CurrencyRates()
    try:
        exchange_rate = c.get_rate(from_currency, to_currency)
        response_data = {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'exchange_rate': exchange_rate,
        }
        return Response(response_data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

#https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/AED/INR.json
#https://v6.exchangerate-api.com/v6/{api_key}/pair/AED/INR
#http://127.0.0.1:8000/api/currency_rate/AED/INR/ 