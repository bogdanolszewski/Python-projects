#from pickle import NONE
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import time
import plotly.express as px
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from datetime import timedelta

from StocksList import return_stock_list
app = Dash(__name__, use_pages=False, prevent_initial_callbacks=True)

#RZECZY DO ZROBIENIA:

# see https://plotly.com/python/px-arguments/ for more options

#stocksList = return_stock_list()
stocksList = ['AAPL','AMZN','TSLA','GOOGL','GOOG','BRK.B','META','MA','KO','XOM','PG','PFE','DIS','ADBE','MCD','CSCO','INTC',
                'AMD','ORCL','NFLX','BLK','GE','IVR','MRNA','GM','MET','NDAQ','STX']

stocksList.sort()

#print(help(dcc.DatePickerSingle))

app.layout = html.Div(id="page",
            children=[
                html.Div(id="UserInputs",children=[
                            dcc.Dropdown(stocksList, id="StockDrpdn"), #stocks dropdown
                            #dcc.Input(id="StockDrpdn", type="text", placeholder="IVR", debounce=True), #replaced by dropdown above
                            #dcc.DatePickerSingle(id='startdate', placeholder = (date.today()-timedelta(days=31)).strftime('%Y-%m-%d'),min_date_allowed=date(2020, 1, 1), display_format='YYYY-MM-DD'),
                            #dcc.DatePickerSingle(id='enddate', placeholder = (date.today()).strftime('%Y-%m-%d'), min_date_allowed=date(2020, 1, 1), display_format='YYYY-MM-DD'),
                            dcc.Input(id="startdate", type="text", placeholder="from (yyyy-mm-dd)"),
                            dcc.Input(id="enddate", type="text", placeholder="until (yyyy-mm-dd)"),
                            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),#inputs for stock and start and end dates
                        ]),
                html.Div(id="Popularstocks", children=["Please input a stock ticker, a start date and an end date."],
                        style={"color": "aqua", "display": "flex", "padding-top": "20px"}),

                html.H1(children=[html.Div(id="StockName")]),

                html.Div(id="description"),

                html.Div(id="Wrapper1",
                children=[

                    dcc.Loading(
                    id="ls-loading-2",
                    children=[html.Div([html.Div(id="ls-loading-output-2")])],
                    type="circle",),

                    html.Div(id="charts1",
                    children=[html.Div(id="StockOpenClosePrices"),html.Div(id="StockHighLowPrices")])
                        ]
                        ),

                html.Div(id="Wrapper2",
                children=[
                    html.Div(id="Measures"),
                        ]
                        ),
        #dash.page_container
                    ])

@app.callback(Output('StockOpenClosePrices', 'children'),
              Output('StockHighLowPrices', 'children'),
              Output('Measures', 'children'),
              Output('StockName','children'),
              #Output("ls-loading-output-2", "children"),
              Input('submit-button-state', 'n_clicks'),
              State('StockDrpdn', 'value'),
              State('startdate', 'value'),
              State('enddate', 'value'))

def update_charts_and_desc(n_clicks, StockDrpdn, startdate, enddate): #return a graph to the div output1

    if StockDrpdn!='':
        stock = StockDrpdn
        StockData = yf.Ticker(stock)
        #defaultStartDate = (date.today()-timedelta(days=365)).strftime('%Y-%m-%d')
        #if enddate=="until (yyyy-mm-dd)" and startdate=="from (yyyy-mm-dd)":
        #    last_month_history = StockData.history()
            #if enddate and startdate are not given (placeholder values taken), then the yfinance library applies a one month back default
        #else:
        last_month_history = StockData.history(start = startdate, end = enddate )

        last_month_history["Open"] = round(last_month_history["Open"], 2)
        last_month_history["High"] = round(last_month_history["High"], 2)
        last_month_history["Low"] = round(last_month_history["Low"], 2)
        last_month_history["Close"] = round(last_month_history["Close"], 2)
        last_month_history = last_month_history.drop(labels=["Dividends", "Stock Splits"], axis=1)

        OpenClosePrices = px.line(last_month_history, y=["Open", "Close"], x=last_month_history.index, template='plotly_dark',
                        title=f"{stock} Opening and Closing prices")
        open_max = last_month_history["Open"].max()
        close_max = last_month_history["Close"].max()
        open_min = last_month_history["Open"].min()
        close_min = last_month_history["Close"].min()
        OpenClosePrices.update_yaxes(tickprefix="$", showgrid=True)

        #OpenClosePrices.add_hline(y=open_max, line_color='blue', line_dash="dot",annotation_text="highest opening price in period", annotation_position="top right")
        #OpenClosePrices.add_hline(y=open_min, line_color='yellow', line_dash="dot",annotation_text="lowest opening price in period", annotation_position="bottom right")
        OpenClosePrices.add_hline(y=close_max, line_color='green', line_dash="dot",annotation_text="highest closing price", annotation_position="top left")
        OpenClosePrices.add_hline(y=close_min, line_color='gray', line_dash="dot",annotation_text="lowest closing price", annotation_position="bottom left")

        HighLowPrices = px.line(last_month_history, y=["High", "Low"], x=last_month_history.index, template='plotly_dark',
                                title=f"{stock} intraday highest and lowest prices")
        low_max = last_month_history["Low"].max()
        high_max = last_month_history["High"].max()
        low_min = last_month_history["Low"].min()
        high_min = last_month_history["High"].min()
        HighLowPrices.update_yaxes(tickprefix="$", showgrid=True)

        HighLowPrices.add_hline(y=high_max, line_color='blue',  line_dash="dot",annotation_text="all time high", annotation_position="bottom left")
        #HighLowPrices.add_hline(y=high_min, line_color='yellow', line_dash="dot",annotation_text="lowest daily high", annotation_position="bottom left")
        #HighLowPrices.add_hline(y=low_max, line_color='green', line_dash="dot",annotation_text="highest daily low", annotation_position="bottom left")
        HighLowPrices.add_hline(y=low_min, line_color='gray', line_dash="dot",annotation_text="all time low", annotation_position="bottom left")

        #calculating measures
        open_avg = round(last_month_history["Open"].mean(), 2)
        close_avg = round(last_month_history["Close"].mean(), 2)
        low_avg = round(last_month_history["Low"].mean(), 2)
        high_avg = round(last_month_history["High"].mean(), 2)
        ###########
        open_min = last_month_history["Open"].min()
        close_min = last_month_history["Close"].min()
        low_min = last_month_history["Low"].min()
        high_min = last_month_history["High"].min()
        ################
        open_max = last_month_history["Open"].max()
        close_max = last_month_history["Close"].max()
        low_max = last_month_history["Low"].max()
        high_max = last_month_history["High"].max()
        ###################
        high_max_date = last_month_history["High"].idxmax().strftime('%Y-%m-%d')
        close_max_date = last_month_history["Close"].idxmax().strftime('%Y-%m-%d')
        low_max_date = last_month_history["Low"].idxmax().strftime('%Y-%m-%d')
        open_max_date = last_month_history["Open"].idxmax().strftime('%Y-%m-%d')
        #####################
        low_min_date = last_month_history["Low"].idxmin().strftime('%Y-%m-%d')
        high_min_date = last_month_history["High"].idxmin().strftime('%Y-%m-%d')
        close_min_date = last_month_history["Close"].idxmin().strftime('%Y-%m-%d')
        open_min_date = last_month_history["Open"].idxmin().strftime('%Y-%m-%d')
        #how many days where the Opening Price was lower than the closing price?
        last_month_history["positive_close"] = np.where(last_month_history["Close"]>last_month_history["Open"],1,0)
        last_month_history["negative_close"] = np.where(last_month_history["Close"]<last_month_history["Open"],1,0)
        positive_close_days = last_month_history["positive_close"].sum()
        negative_close_days = last_month_history["negative_close"].sum()
        output = f"""{stock} has had a high of {high_max}$ on {high_max_date}, in this time period. The lowest closing price the stock reached was {low_min}$ ({round(high_max-low_min, 2)}$ diff.) on {low_min_date} \n.
        the average opening price was {open_avg}$, compared to the {close_avg}$ closing avg. price. \n
        The average daily high was {high_avg}$ and the average daily low - {low_avg}$. \n
        there were {positive_close_days} days where the closing price was higher than the opening price({negative_close_days} negative days)."""

        return [dcc.Graph(id="StockOpenClosePriceschart",
                figure=OpenClosePrices), dcc.Graph(id="StockHighLowPriceschart", figure=HighLowPrices),
                output,
                stock]

@app.callback(Output("ls-loading-output-2", "children"), Input("submit-button-state", "n_clicks"))
def input_triggers_nested(value):
    time.sleep(3)
    return value


if __name__ == "__main__":
    app.run_server(debug=True)

