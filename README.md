# Credit Card Fraud Detection

This is a machine learning project I built to detect fraudulent credit card transactions in real-time. It uses a Random Forest model hooked up to a Flask API, and includes a web interface where you can test out transactions to see if the model flags them as fraud.

## How it works
The system is pretty straightforward:
- I trained a few machine learning models (using GridSearchCV for tuning) and saved the best one.
- There's a local MySQL database setup to store the prediction logs for analytics.
- The backend is a Flask app (`app.py`) that handles incoming transaction data and runs it through the model.
- The frontend (`templates/index.html`) is a simple UI for submitting transaction data manually.

## Project Structure
- `app.py`: Main Flask application and prediction logic
- `sql/`: SQL scripts to create the database tables
- `models/`: Where the trained `.pkl` models are stored
- `notebooks/`: Jupyter notebooks I used for EDA and model training
- `templates/`: HTML files for the web interface
- `render.yaml`: Configuration for easy deployment on Render

## Setup

1. **Clone the repo**
```bash
git clone https://github.com/avyasaini/Credit-Card-Fraud-Detection.git
cd Credit-Card-Fraud-Detection
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app locally**
```bash
python app.py
```
The app will run on `http://127.0.0.1:5000`.

## API Usage
You can also test the `/predict` endpoint directly using Postman or curl. Send a POST request with JSON data like this:

```json
{
  "amt": 281.06,
  "city_pop": 885,
  "lat": 35.9946,
  "long": -81.7266,
  "merch_lat": 36.430124,
  "merch_long": -81.179483,
  "unix_time": 1325466397,
  "category": "grocery_pos"
}
```

## Performance
The Random Forest model performed really well on the validation set, achieving an F1-Score of around 0.99. I used balanced class weights to deal with the heavily imbalanced dataset (since most transactions aren't fraud).

## Contact
If you have any questions or feedback about this project, feel free to open an issue in the repository!

