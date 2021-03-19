import pandas as pd 
import pandas_datareader as pdr
import matplotlib.pyplot as mpl

from fbprophet import Prophet
from datetime import datetime, timedelta, date

koreaStock = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
koreaStock = koreaStock.rename(columns={'회사명':'name','종목코드':'stockCode','상장일':'stockBirth'})
koreaStock = koreaStock[['name', 'stockCode','stockBirth']]

today = [datetime.today().year, datetime.today().month, datetime.today().day]
yesterday = (date.today() - timedelta(1)).strftime('%Y-%m-%d')

def searchStockCode():
    try :
        userSerchingStock = input()
        stockCode = koreaStock[koreaStock['name'].isin([userSerchingStock])].iloc[0,1]
        stockCode = str(stockCode).zfill(6) + '.KS'
        stockBirth = koreaStock[koreaStock['name'].isin([userSerchingStock])].iloc[0,2]
        stockBirth = str(stockBirth).split('-')
        return stockCode,stockBirth
    except:
        return searchStockCode()
    
stockCode,stockBirth = searchStockCode()

start = datetime(int(stockBirth[0]), int(stockBirth[1]), int(stockBirth[2]))
done = datetime(today[0],today[1],today[2])

searchStock = pdr.DataReader(stockCode, "yahoo", start, done)
realityDF = pd.DataFrame({'ds': searchStock.index, 'y' : searchStock['Close']})

model = Prophet()
model.fit(realityDF)

future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

futureData = forecast[forecast['ds'].isin([yesterday])]
futureData = int(futureData.iloc[0,18])

todayData = realityDF.loc[yesterday : yesterday]
todayData = int(todayData.iloc[0,1])

errorValue = todayData - futureData
dataSet = str(yesterday) + '  ' + str(errorValue) 

print(dataSet + '\n')
print("nowData", todayData,'won', ' | ', 'futureData', futureData, 'won', ' | ', 'errorValue', errorValue, 'won') 

result = pd.DataFrame(
    {
        'nowData': [todayData],
        'futureData': [futureData],
        'errorValue': [errorValue]
    }
)

#model.plot(forecast) 
#model.plot_components(forecast)
#mpl.show()
#result.to_excel('StockDataFrame')
print(result)

