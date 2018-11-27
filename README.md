# Objectives

## Back-end developer assignment:
Implement an online currency converter, providing a Web API endpoint called convert.

The endpoint must accept HTTP GET requests.

You’re free to design the endpoint structure as you like, as long it accepts the following
parameters:
*  amount: the amount to convert (e.g. 12.35)
* src_currency: ISO currency code for the source currency to convert (e.g. EUR,
USD, GBP)
* dest_currency: ISO currency code for the destination currency to convert (e.g. EUR,
USD, GBP)
* reference_date: reference date for the exchange rate, in YYYY-MM-DD format
Your program must convert the provided amount from src_currency to dest_currency,
given the exchange rate at the reference_date.

The response should be a JSON object like this:
```json
{
  "amount": 20.23,
  "currency": "EUR"
}
```

You can find an xml file with the last 90 days exchange rates at this [link](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml)

## Constraints:
* Node.js version >=7 or Python language, version >=3.4
* Publish your project to an accessible git source code repository
* Provide clear instructions on how to run your project through a README file

## Notes:
* You are free to use any framework you want

## Bonus points
* Containerization with Docker
* Write automated tests for your project.
* Dynamically retrieve the latest XML file at project startup time and somehow store it for the converter usage

# Implementation

## Python Version
The library is compatible with python version `>= 3.6`, since it uses the f-string introduced by that version on.  

## Footprint
There is a minimal external dependencies footprint, but for `gunicorn` and `meinheld`, which are used to speed up HTTP server.

## Design
The code design follows the single responsibility principle by using a dedicated class for any specific task.

## Installation
Install the dependencies via `pip`:

```shell
pip install -r requirements.txt
```

## Usage

### API
The library exposes a single HTTP API at `0.0.0.0:8888/convert` (or at the port you bound at server start). 

### Parameters
The query parameters described by the objectives have some defaults:
* query = parse_qs(environ.get('QUERY_STRING')) or {}
* amount: 9.99
* src_currency: EUR
* dest_currency: USD
* reference_date: the most recent specified on fetched exchange rates document

#### Refresh XML
There is an additional parameter, `fresh`, that force to fetch a fresh copy of the exchange rates HTML form remote source:
* fresh: False

### Start Server
To start the server use the `gunicorn` executable by spawning as many workers as you need:
```shell
gunicorn -w 4 -k meinheld.gmeinheld.MeinheldWorker -b :8888 app:convert
```

### Examples
Convert 99.99 EUR to USD by 29 of August rate:
http://127.0.0.1:8888/convert?amount=99.99&src_currency=EUR&dest_currency=USD&reference_date=2018-08-29
```json
{"amount": 116.59, "currency": "USD"}
```

Convert 9.99 USD to PLN (last available rate):
http://127.0.0.1:8888/convert?amount=9.99&src_currency=USD&dest_currency=PLN
```json
{"amount": 37.73, "currency": "PLN"}
```

## Errors
Some basic errors management is done via exceptions.

### Wrong Date
http://127.0.0.1:8888/convert?amount=99.99&src_currency=EUR&dest_currency=USD&reference_date=2018-11-31
```
'unavailable reference date, use one of these: 2018-11-26, 2018-11-23, 2018-11-22, 2018-11-21, 2018-11-20, 2018-11-19, 2018-11-16, 2018-11-15, 2018-11-14, 2018-11-13, 2018-11-12, 2018-11-09, 2018-11-08, 2018-11-07, 2018-11-06, 2018-11-05, 2018-11-02, 2018-11-01, 2018-10-31, 2018-10-30, 2018-10-29, 2018-10-26, 2018-10-25, 2018-10-24, 2018-10-23, 2018-10-22, 2018-10-19, 2018-10-18, 2018-10-17, 2018-10-16, 2018-10-15, 2018-10-12, 2018-10-11, 2018-10-10, 2018-10-09, 2018-10-08, 2018-10-05, 2018-10-04, 2018-10-03, 2018-10-02, 2018-10-01, 2018-09-28, 2018-09-27, 2018-09-26, 2018-09-25, 2018-09-24, 2018-09-21, 2018-09-20, 2018-09-19, 2018-09-18, 2018-09-17, 2018-09-14, 2018-09-13, 2018-09-12, 2018-09-11, 2018-09-10, 2018-09-07, 2018-09-06, 2018-09-05, 2018-09-04, 2018-09-03, 2018-08-31, 2018-08-30, 2018-08-29'
```

### Wrong Currency
http://127.0.0.1:8888/convert?amount=99.99&src_currency=EUR&dest_currency=XXX
```
'unavailable currency, use one of these: EUR, USD, JPY, BGN, CZK, DKK, GBP, HUF, PLN, RON, SEK, CHF, ISK, NOK, HRK, RUB, TRY, AUD, BRL, CAD, CNY, HKD, IDR, ILS, INR, KRW, MXN, MYR, NZD, PHP, SGD, THB, ZAR'
```

## Tests
The library is covered, by fast, isolated unit and docs testing (to grant reliable documentation):
```shell
./run_test
..............
----------------------------------------------------------------------
Ran 14 tests in 0.007s

OK
```
