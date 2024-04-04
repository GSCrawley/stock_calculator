from flask import Flask, render_template, request, jsonify
from utils import get_stock_data, calculate_metrics
from charts import generate_scatterplot
from sas_code_generator import generate_sas_code

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Renders the home page with the form to input stock ticker.
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    # Endpoint to handle form submission and perform analysis.
    ticker = request.form['ticker']
    metrics_requested = request.form.getlist('metrics')
    
    # Retrieve and process stock data
    stock_data = get_stock_data(ticker)
    
    # Calculate requested metrics
    results = calculate_metrics(stock_data, metrics_requested)
    
    # Generate scatterplot chart if requested
    if 'scatterplot' in metrics_requested:
        scatterplot_img = generate_scatterplot(stock_data)
        results['scatterplot_img'] = scatterplot_img
    
    # Generate SAS code if requested
    if 'sas_code' in metrics_requested:
        sas_code = generate_sas_code(stock_data)
        results['sas_code'] = sas_code
    
    # Return the results to a new result page or as JSON
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
