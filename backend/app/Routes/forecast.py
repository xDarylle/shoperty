from app import app
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Order, Shop, Product, OrderStatus
from datetime import datetime
import pandas as pd 
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

@login_required
@app.route('/api/v1/admin/forecast', methods=['GET'])
def forecast():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'GET':
        # query data (orders) from database
        shop = Shop.query.filter_by(user=current_user.id).first()
        orders = Order.query.order_by(Order.dateCreated.desc()).join(Product.query.filter_by(shop=shop.id)).all()

        # get sales
        data=[]
        for order in orders:
            if order.status == OrderStatus.query.filter_by(name='COMPLETE').first().id:
                product = Product.query.get(order.product)
                converted_date = order.dateCreated.strftime('%x')
                data.append([converted_date, order.quantity * product.price])

        if not data:
            return Response(
                status=200,
            )

        # get start and end dates
        start = data[-1][0]
        end = data[0][0]

        # create base data for dates between the start and end dates
        base = createBaseData(start, end)

        # convert data list to DataFrame
        base_df = pd.DataFrame(base, columns=['Date', 'Sales'])
        sales_df = pd.DataFrame(data, columns=['Date', 'Sales'])

        # concatinate base and sales dataframes
        df = pd.concat([base_df, sales_df])

        # get the means of sales by date
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.groupby(df.Date.dt.date)['Sales'].mean()
        df = pd.DataFrame({'Date': df.index, 'Sales': df.values})

        # get range of dates from start to current date
        now = datetime.now()
        dates_len = len(pd.date_range(start, now))

        # get data from past 30 days
        if dates_len > 30:
            s = len(df) - 30
            df = df.iloc[s:len(df)]
        else:
            s = len(df) - dates_len
            df = df.iloc[s:len(df)]

        y = df['Sales']

        # if data from database is less than 30
        # skip forecasting
        if len(df) < 30:
            data = []
            for i, date in enumerate(df['Date']):
                index = df['Date'].index.start + i
                d = date.strftime("%b %d")
                if i == len(df['Date']) - 1:
                    data.append({'date': "Today", 'sales': y.loc[index]})
                else:
                    data.append({'date': d, 'sales': y.loc[index]})

            return Response(
                status=200,
                data=data
            )

        # forecast using ARIMA 
        model = ARIMA(y, order=(0, 0, 1))
        model_fit = model.fit()
        predicted = model_fit.predict(len(y), len(y))
        y_pred = model_fit.predict(0, len(y)-1)
        rmse = mean_squared_error(y_true=y, y_pred=y_pred, squared=False)

        # prepare response data
        sales = []
        for i, date in enumerate(df['Date']):
            index = df['Date'].index.start + i
            d = date.strftime("%b %d")
            
            sales.append({'date': d, 'sales': y.loc[index], 'predicted': y_pred.loc[index]})

        predicted = {'predicted': round(predicted.values[0], 2), 'date': "Tomorrow"}
        sales.append(predicted)

        return Response(
            status=200,
            data=sales,
            message=rmse
        )

# create datas with dates and 0 sales
def createBaseData(start, end):
    start = start
    dates = pd.date_range(start, end)
    
    data = []
    for date in dates:
        data.append([date, 0])

    return data