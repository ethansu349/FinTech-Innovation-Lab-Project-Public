# FinTech-Innovation-Lab-Project

## Visit the website
We have deployed our app to heroku. Visit [website](https://fintech-innov-lab-74182ead78a6.herokuapp.com/) for more details. However, there is a hard time limit of response time to be under 30s in heroku. Our API would take more than 30s to download data, so the website cannot get response from backend now. We will resolve this issue as soon as possible.

## How to run the project locally
```bash
# run the backend
cd backend
# create a new virtual environment (make sure your python version is >= 3.9)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Flask server will run on port 5000
python app.py

# run the frontend
cd ../frontend
npm install
# React will run on port 3000
npm start
```

## OpenAPI API Key
We hide our API key in `backend/app.py/#114` for safety concern. In order to get the key, please reach out to me.
