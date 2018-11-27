# Table of Contents
* [Scope](#scope)
* [Requirements](#requirements)
  * [Version](#version)
  * [Footprint](#footprint)
* [Design](#design)
  * [SRP](#srp)
  * [Rounding](#rounding)
  * [Data](#data)
  * [Tests](#tests)
* [Usage](#usage)
  * [Installation](#installation)
  * [API](#api)
    * [Parameters](#parameters)
  * [Start Server](#start-server)
  * [Examples](#examples)
    * [EUR to USD](#eur-to-usd)
    * [USD to PLN](#usd-to-pln)
  * [Errors](#errors)
    * [Wrong Date](#wrong-date)
    * [Wrong Currency](#wrong-currency)

# Scope
This is the implementation of the python code kata `currency converter`.  
For further instructions please check the `OBJECTIVES.md` file.

# Requirements

## Version
The library is compatible and it has been tested with python versions `3.6.4` and `3.7.1`, since it uses the pretty useful [string literal](https://www.python.org/dev/peps/pep-0498/) interpolation introduced from version `3.6` on.

## Footprint
To grant resiliency (and courtesy of the Python's broad standard library) the external dependencies footprint is kept to a minimum.  
The only external modules are `gunicorn` and `meinheld`, which are used to increase HTTP server throughput.

# Design

## SRP
The code design follows the single responsibility principle by using a dedicated class for any specific task. Each class confined within meaningful modules:
* `currency`: currency related objects, such as `Money` and `EurRates`
* `data`: data related objects, such as `Fetcher` and `Parser`
* `converter`: the conversion core logic within the `Computer` object

## Rounding
The library is relaxed on float arithmetics by rounding final conversion results to *two decimals*.  
This allows to speed up execution by avoiding instantiating `Decimal` objects and is acceptable considering the objectives (granularity of currencies).

## Data
The EUR exchange rates are fetched by a remote [XML document](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml).  
The document is fetched one time only at server start and cached at `./cconv/data/rates.xml` to avoid network latency. Just delete it to fetch a fresh copy.

## Tests
The library is covered, by fast, isolated unit and doc testing (the latter to grant reliable documentation):
```shell
./run_test
..............
----------------------------------------------------------------------
Ran 14 tests in 0.007s

OK
```

# Usage

## Installation
Install the external dependencies via `pip`:
```shell
pip install -r requirements.txt
```

## API
The library exposes a single HTTP API at `0.0.0.0:8888/convert` (or at the port you bound at server start). 

### Parameters
The query parameters described by the objectives have the following defaults:
* amount: 9.99
* src_currency: EUR
* dest_currency: USD
* reference_date: the most recent specified on the XML document

## Start Server
To start the server use the `gunicorn` executable by spawning as many workers as you need and by specifying the HTTP port:
```shell
gunicorn -w 4 -k meinheld.gmeinheld.MeinheldWorker -b :8888 app:convert
```

## Examples

### EUR to USD
http://127.0.0.1:8888/convert?amount=99.99&src_currency=EUR&dest_currency=USD
```json
{"amount": 116.59, "currency": "USD"}
```

### USD to PLN
http://127.0.0.1:8888/convert?amount=9.99&src_currency=USD&dest_currency=PLN
```json
{"amount": 37.73, "currency": "PLN"}
```

## Errors
Some basic errors management is done via exceptions handling.

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
