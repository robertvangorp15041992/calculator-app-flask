from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def calculate_airflow(rpm, displacement, turbocharged):
    """
    Calculate the required airflow (m³/min) based on the given formula.
    """
    multiplier = 1.85 if turbocharged else 1
    airflow = (rpm * (displacement * 100) * multiplier) / 2_000_000
    return airflow

# Precleaner models and their airflow ranges
precleaners = [
    {"model": "TA-200", "min_m3": 0.6, "max_m3": 2.8},
    {"model": "TA-225", "min_m3": 2.8, "max_m3": 5.6},
    {"model": "TA-3-300", "min_m3": 3.9, "max_m3": 7.8},
    {"model": "TA-445", "min_m3": 8.5, "max_m3": 16.8},
    {"model": "TA-550", "min_m3": 8.5, "max_m3": 16.8},
    {"model": "TA-660S", "min_m3": 11.0, "max_m3": 23.8},
    {"model": "TA-770L", "min_m3": 18.0, "max_m3": 39.7},
    {"model": "TA-880", "min_m3": 25.2, "max_m3": 56.5}
]

def find_best_precleaner(airflow):
    """
    Find the most suitable precleaner based on calculated airflow.
    """
    suitable_models = [p for p in precleaners if p["min_m3"] <= airflow <= p["max_m3"]]
    return suitable_models if suitable_models else [{"model": "No suitable model found"}]

@app.route('/', methods=['GET'])
def home():
    return '''
    <form action="/calculate" method="get">
        RPM: <input type="number" name="rpm" required><br>
        Displacement (L): <input type="number" step="0.01" name="displacement" required><br>
        Turbocharged: <input type="checkbox" name="turbocharged" value="true"><br>
        <input type="submit" value="Calculate">
    </form>
    '''

@app.route('/calculate', methods=['GET'])
def calculate():
    rpm = float(request.args.get('rpm', 0))
    displacement = float(request.args.get('displacement', 0))
    turbocharged = 'turbocharged' in request.args
    
    airflow = calculate_airflow(rpm, displacement, turbocharged)
    suitable_precleaners = find_best_precleaner(airflow)
    
    result = f"Calculated Airflow: {airflow:.2f} m³/min<br>"
    result += "Recommended Precleaners:<br>" + "<br>".join([p['model'] for p in suitable_precleaners])
    
    return result

if __name__ == '__main__':
    app.run(debug=True)
