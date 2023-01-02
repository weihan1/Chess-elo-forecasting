from api_access import client
from data import *
from prophet import Prophet

if __name__ == "__main__":
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=365)
    forecast = model.predict(future)
    fig1 = model.plot(forecast)
    plt.show()
    fig = model.plot_components(forecast)
    plt.show()

