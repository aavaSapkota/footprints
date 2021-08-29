# FoodPrints
![license](https://img.shields.io/badge/license-BSD--3--Clause-green?style=flat-square)

**Created for [Technova 2021](https://technova2021.devpost.com/)**

FoodPrints is a web app for the everyday user looking to better understand their impact on the planet. The app provides a quick and easy way for users to check their climate footprint on a day-to-day basis by parsing their grocery receipts to provide valuable insights about purchased items.

## Installation
Clone the repository
```
git clone https://github.com/aavaSapkota/footprints.git
cd carbon-footprint-tracker
```
Install requirements
```
pip install -r requirements.txt
```
Setup Google Cloud Vision API by following this [tutorial](https://cloud.google.com/vision/docs/before-you-begin)

Write Cloud Vision API key to environment variables by copying `cfTracker/.env.example` to `cfTracker/.env` and supplying path to key file

Run Django migrations
```
python3 manage.py migrate
```
Finally, run the server
```
python3 manage.py runserver
```
