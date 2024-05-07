# FinTech-Innovation-Lab-Project

## Visit the website
We have successfully deployed our code to https://fintech-innov-lab-74182ead78a6.herokuapp.com/. You can see the deployed code in `heroku` branch. However, since activating server will cost a lot of money along the time goes by, we ultimately decided not to keep the deployment active. Please reach out to me if you need to see the website, I will switch it to active for you.

## How to run the application locally
You can see the recorded video [here](https://drive.google.com/file/d/1XXvjewyD0U7tzUtiR6-kZxJCggFKo7pK/view?usp=drive_link). Downloading data and cleaning data takes a while in the backend.

To run the application locally,
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

## Why the insights generated useful?
In choosing to focus on insights from the Management’s Discussion and Analysis (MDA), Quantitative Risk, and Risk Factor sections of 10-K filings, we target the most informative areas for stakeholders to evaluate a company's overall health and strategic positioning. Here’s why these aspects are particularly chosen:

1. MDA (Management’s Discussion and Analysis) - This section is chosen because it provides a narrative explanation of the financial and operational results provided in the financial statements. The MDA gives context to the numbers, offering insights into the company's performance trends, underlying business drivers, and management's strategy for future growth. This narrative helps stakeholders understand beyond raw financial data, providing a deeper look at the company’s operations from the management’s viewpoint.
2. Quantitative Risk - Focusing on this aspect is crucial because it quantifies risk exposures in financial terms, offering a clearer picture of potential financial impacts. This section helps in identifying the specific areas where financial risks are most pronounced, such as market risk, credit risk, or liquidity risk. These insights are vital for investors and financial analysts who need to assess risk management effectiveness and the potential for unexpected financial setbacks.
3. Risk Factor Summary - This is highlighted due to its comprehensive detailing of potential risks that could adversely affect the company. It encompasses a wide range of risks including economic, environmental, regulatory, and operational risks. Highlighting these risks provides a precautionary insight for stakeholders, allowing them to consider external and internal factors that could derail the company's strategies and impact its financial health.
By choosing these aspects for insight generation, we provide users with a holistic understanding of both the operational and financial standing of the company, combined with a strategic view of potential risks and management’s expectations for the future. This comprehensive approach aids stakeholders in making more informed decisions regarding their engagement or investment in the company, aligning their strategies and expectations with the company’s projected path.
