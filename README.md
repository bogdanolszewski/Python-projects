# Stock Watcher

This is an app i built using a popular web visualization library Plotly, and dash - a library which allows the developer to skip the boring part of deploying the actual Flask app itself.

The app can be used to access stock data from the Yfinance library, which is responsible for making the http requests.
Once loaded (the page is hosted on http://127.0.0.1:8050/ ), the user can select a stock from the dropdown list and input the date range he/she desires. Processing takes a few seconds, the callbacks must return the charts and short analytical description below.
