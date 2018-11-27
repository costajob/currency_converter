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
