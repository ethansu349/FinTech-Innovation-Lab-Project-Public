from flask import Flask, jsonify
import yfinance as yf
from sec_edgar_downloader import Downloader
from flask_cors import CORS
import os
import re
import requests
import html
import pandas as pd

app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)

def download_10k_reports(ticker):
    eaddress = 'lamdapi091@gmail.com'
    # initialize Downloader
    dl = Downloader("GeorgiaTech", eaddress, "./")
    stock = yf.Ticker(ticker)
    # get IPO year
    try:
        hist = stock.history(period="max")  # 'max' retrieves as much history as available
        # Find the IPO date
        ipo_date = (hist.index.min()).strftime('%Y-%m-%d')

    except KeyError:
        print("IPO date not available, defaulting to 1995")
        ipo_date = "1995-01-01"
    
    if ipo_date < "1995-01-01":
        download_date = "1995-01-01"
    else:
        download_date = ipo_date
    dl.get("10-K", ticker, after=download_date)

# Data cleaning and extraction functions
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def clean_html(raw_html):
    # First, we transform the HTML entities
    decoded_html = html.unescape(raw_html)
    # Use regular expressions to remove HTML tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', decoded_html)
    # Replace multiple consecutive newlines with a single newline character
    cleantext = re.sub(r'\n+', '\n', cleantext)
    # Replace multiple consecutive Spaces with a single space
    cleantext = re.sub(r'\s+', ' ', cleantext)
    # Convert the text to lowercase (if needed)
    cleantext = cleantext.lower()
    return cleantext

def extract_section(text, start_phrase, start_phrase2, end_phrase, end_phrase2):
    pattern = re.compile(r'{}\s*(.*?)\s*{}'.format(re.escape(start_phrase.lower()), re.escape(end_phrase.lower())), re.IGNORECASE | re.DOTALL)
    pattern2 = re.compile(r'{}\s*(.*?)\s*{}'.format(re.escape(start_phrase2.lower()), re.escape(end_phrase2.lower())), re.IGNORECASE | re.DOTALL)
    matches = pattern.finditer(text)
    matches2 = pattern2.finditer(text)
    sections = []
    for match in matches:
        sections.append(match.group(1))
    # Combine all the parts found into a single string, separated by a separator
    for match in matches2:
        sections.append(match.group(1))
    return "\n\n---\n\n".join(sections)

def clean_data(root_directory, ticker):
    ticker_directory = os.path.join(root_directory, ticker)
    for subdir, dirs, files in os.walk(ticker_directory):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(subdir, file)
                raw_text = read_text(file_path)
                clean_text = clean_html(raw_text)
                
                # Extract specific parts
                risk_factor_text = extract_section(clean_text, "Item 1A", "Item&#160;1A", "Item 1B", "Item&#160;1B")
                mda_text = extract_section(clean_text, "Item 7", "Item&#160;7", "Item 7A", "Item&#160;7A")
                quant_risk_text = extract_section(clean_text, "Item 7A", "Item&#160;7A", "Item 8", "Item&#160;8")
                
                # save results to txt files
                with open(os.path.join(subdir, 'cleaned_analysis_mda.txt'), 'w', encoding='utf-8') as output_file:
                    output_file.write("MDA: \n" + mda_text + "\n\n\n\n\n")

                with open(os.path.join(subdir, 'cleaned_analysis_quant_risk.txt'), 'w', encoding='utf-8') as output_file:
                    output_file.write("Risk: \n" + quant_risk_text + "\n\n\n\n\n")
                
                with open(os.path.join(subdir, 'cleaned_analysis_risk_factor.txt'), 'w', encoding='utf-8') as output_file:
                    output_file.write("Risk Factor: \n" + risk_factor_text + "\n\n\n\n\n")

def get_files_by_category(base_path, ticker):
    path = os.path.join(base_path, ticker, "10-K")
    for year_dir in os.listdir(path):
        year_path = os.path.join(path, year_dir)
        if os.path.isdir(year_path):
            # extract from each year
            year = year_dir.split('-')[1]
            year = int('19' + year) if int(year) >= 50 else int('20' + year)  

            files = {'MDA': None, 'Risk': None, 'Risk Factor': None}
            for file in os.listdir(year_path):
                if 'mda' in file:
                    files['MDA'] = os.path.join(year_path, file)
                elif 'quant' in file:
                    files['Risk'] = os.path.join(year_path, file)
                elif 'factor' in file:
                    files['Risk Factor'] = os.path.join(year_path, file)
            yield year, year_path, files

# LLM API for Analysis
def call_gpt_api(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def analyze_text(file_path, category):
    with open(file_path, 'r') as file:
        text = file.read()

    # Specialized prompts
    prompts = {
        'MDA': "Provide a summary of the management's discussion and analysis, along with sentiment analysis, in two to three sentences:\n",
        'Risk Factor': "Summarize the key risk factors mentioned in the document, and provide a sentiment analysis in two to three sentences:\n",
        'Risk': "Provide a summary of the risks mentioned in the document, including sentiment analysis, in two to three sentences:\n"
    }
    prompt = prompts[category] + text

    result = call_gpt_api(prompt[0: min(16385, len(prompt))])
    summary = result['choices'][0]['message']['content']  
    sentiment = "Positive" 
    return {"summary": summary, "sentiment": sentiment}

def run_analysis(base_path, ticker):
    all_results = {}
    for year, year_path, files in get_files_by_category(base_path, ticker):
        year_results = {
            "sentimentAnalysis": "",
            "mdaSummary": "",
            "riskSummary": "",
            "riskFactorSummary": ""
        }
        for category, file_path in files.items():
            if file_path:
                analysis_result = analyze_text(file_path, category)
                if category == 'MDA':
                    year_results['mdaSummary'] = analysis_result['summary']
                    year_results['sentimentAnalysis'] = analysis_result['sentiment']
                elif category == 'Risk':
                    year_results['riskSummary'] = analysis_result['summary']
                elif category == 'Risk Factor':
                    year_results['riskFactorSummary'] = analysis_result['summary']
        all_results[str(year)] = year_results
    return all_results

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/getAnalysis/<string:ticker>', methods=['GET'])
def get_ticker_analysis(ticker):
    cur_path = os.path.join('./sec-edgar-filings', ticker)
    if not os.path.isdir(cur_path):
        download_10k_reports(ticker)
        clean_data("./sec-edgar-filings", ticker)
    data = run_analysis("./sec-edgar-filings", ticker)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)