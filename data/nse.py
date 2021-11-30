import requests
import json


def get_nifty50_tickers():
    return ['NESTLEIND', 'BAJAJFINSV', 'MARUTI', 'HCLTECH', 'RELIANCE', 'TCS', 'BRITANNIA',
            'INDUSINDBK', 'ASIANPAINT', 'KOTAKBANK', 'DRREDDY', 'EICHERMOT', 'BAJFINANCE',
            'TATACONSUM', 'ULTRACEMCO', 'BAJAJ-AUTO', 'NTPC', 'TATAMOTORS', 'JSWSTEEL',
            'WIPRO', 'AXISBANK', 'TATASTEEL', 'UPL', 'HEROMOTOCO', 'CIPLA', 'SUNPHARMA',
            'HINDALCO', 'INFY', 'ADANIPORTS', 'IOC', 'COALINDIA', 'BPCL', 'GRASIM', 'HDFC',
            'POWERGRID', 'HDFCBANK', 'HDFCLIFE', 'ICICIBANK', 'ONGC', 'BHARTIARTL', 'ITC',
            'HINDUNILVR', 'SHREECEM', 'DIVISLAB', 'TITAN', 'SBIN', 'M&M', 'SBILIFE',
            'TECHM', 'LT']


def get_top_stocks_by_market_cap():
    return ["ACC", "ADANIENT", "ADANIGREEN", "ADANIPORTS", "ADANITRANS", "AMBUJACEM", "APOLLOHOSP",
            "ASIANPAINT", "AUROPHARMA", "DMART", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV",
            "BAJAJHLDNG", "BANDHANBNK", "BANKBARODA", "BERGEPAINT", "BPCL", "BHARTIARTL", "BIOCON",
            "BOSCHLTD", "BRITANNIA", "CADILAHC", "CHOLAFIN", "CIPLA", "COALINDIA", "COLPAL", "DLF",
            "DABUR", "DIVISLAB", "DRREDDY", "EICHERMOT", "GAIL", "GLAND", "GODREJCP", "GRASIM",
            "HCLTECH", "HDFCAMC", "HDFCBANK", "HDFCLIFE", "HAVELLS", "HEROMOTOCO", "HINDALCO",
            "HINDPETRO", "HINDUNILVR", "HDFC", "ICICIBANK", "ICICIGI", "ICICIPRULI", "ITC",
            "IOC", "IGL", "INDUSTOWER", "INDUSINDBK", "NAUKRI", "INFY", "INDIGO", "JSWSTEEL",
            "JINDALSTEL", "JUBLFOOD", "KOTAKBANK", "LTI", "LT", "LUPIN", "M&M", "MARICO",
            "MARUTI", "MUTHOOTFIN", "NMDC", "NTPC", "NESTLEIND", "ONGC", "PIIND", "PIDILITIND",
            "PEL", "POWERGRID", "PGHH", "PNB", "RELIANCE", "SBICARD", "SBILIFE", "SHREECEM",
            "SIEMENS", "SBIN", "SAIL", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS",
            "TATASTEEL", "TECHM", "TITAN", "TORNTPHARM", "UPL", "ULTRACEMCO", "MCDOWELL-N",
            "VEDL", "WIPRO"]


def get_nifty50_tickers_from_web():
    url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json'
    headers = {
        "host": "www1.nseindia.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "connection": "keep-alive",
        "cookie": "AKA_A2=A; _ga=GA1.2.667547097.1638103403; _gid=GA1.2.2133656096.1638103403; bm_mi=84A26E4415B8F201BEA8289096174E99~pSINRLYpoPjPrusIXcBYcHdiWDu1S+bcISuvYTIYQbTWWhjUnQtXjYOB9ntpRMW4VWG/OTUxgtL634Apup32gFamOT4WPdbLXgFvSwod9UOijXHfXcfFsGR2yjINbH/qGNMviycDHTif4YCwnu5r4No4Fz3IsWlsOTHmQhcy9yzaIo90LWbLybTRkX/y9t1mE97lyUAVRM0PLbtFHxjQ4aajckCur3Iw0GwH4kj538va8/8jbZP+olbqCRKYJzAUvWKjLP2HYLCBstl01WIAag==; ak_bmsc=0A6A51323C00874C09FBDED6AAF20424~000000000000000000000000000000~YAAQUEo5F4s37DF9AQAAd3CSZg1RJqjsK1XRgMev9Jf+P+r+zErayV+Fmh/DB7StTRor7jkVGGWT664j4njSJWWvYeEPzSpReH4Zcq8MphdxQChyv9CZxZXtzzZeQKexpvsqq31FCdcuC9JLD2db6quZNbW9ZsfOaXrfo14icFVh1oZrFpx0tSHTAe0losJ/+JNo8DEwtdJlM/NTPhKyv+ZJlmGwus6mockiqdsW1ib7JW9aNrsCK3bPHWhTXEOVCke/tX4sTUivuSTofv/T32IFMVPA2Ogqd1wfeZCcEepZA3t+Hp8iZsSa79MtVCTYq4dKfSQYK2HUU+uIelT0FJPJCMhZHDvGeHYslVYDCdWdgPJ/YM+I49lyebR/oP8z5csi+70gviWUNJgN4MA72t5DFzozkbzJeJ2IzRAN; NSE-TEST-1=1927290890.20480.0000; JSESSIONID=97BAE646BA99F4D47F37219362FB2724.tomcat1; bm_sv=332A6A52CF0A5B1CAD2C8E748061AA8A~Ahefp8laVgT5fG1vdtmrHL+eSdGBCBiBnxbjZrAb34Wbt+e8X4Q3JkBFtM33RpNi6fitLnKiLMzm0CzVgMGSUys+BBuh0gG55rfT+wN2Vm9I1JS9OpMVTBtawhxnh1CGlB0q4Qcs9vAsxW1RXleL5JfdaWMJhXw4LnIw8R/vJDE=; RT=\"z=1&dm=nseindia.com&si=c2fa92e0-882d-4113-bda1-f188f99dfa14&ss=kwj8gwhv&sl=4&tt=bg6&bcn=%2F%2F684d0d48.akstat.io%2F&ld=5yhw&ul=684z&hd=6891\"",
        "referer": "https://www1.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm",
        "referrer-policy": "strict-origin-when-cross-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    resp = requests.get(url, headers=headers).content
    resp = json.loads(resp)
    tickers = [x.get("symbol", "") for x in resp.get('data', [])]
    return list(set(tickers))
