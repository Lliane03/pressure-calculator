import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('pressure_calculator.html')

@app.route('/clear', methods=['POST'])
def clear():
    return flask.redirect('/')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        force = float(flask.request.form['force']) # The Force value is set to a floating-point number (float) to allow the calculator to accept  whole and decimal values as input.
        area = float(flask.request.form['area']) # The Area value is set to a floating-point number (float) to allow the calculator to accept whole and decimal values as input.
        unit = flask.request.form['unit']
        
        # Both Force and Area should not be negative and <=0. This is required to solve for the Pressure.
        if force <= 0 or area <= 0:
            return flask.render_template('pressure_calculator.html', error_message="The Force and Area should be positive and greater than 0 in order to have pressure.")
        
        pressure = calculate_pressure(force, area)
        
        if unit == "pa": # Result to Pascals; SI unit, equal to one newton per square meter.
            result = round(pressure, 3) # Rounded to three decimal places.
            selected_unit = "Pa"

        elif unit == "psi": # Convert Pascals to PSI; 1 psi ≈ 6895 Pa.
            result = round(pressure / 6895, 7) # Rounded to seven decimal places.
            selected_unit = "psi"

        elif unit == "bar": # Convert Pascals to Bars; equal to 100,000 Pa.
            result = round(pressure / 100000, 6) # Rounded to six decimal places.
            selected_unit = "bar"

        elif unit == "atm": # Convert Pascals to Atmospheres; 1 atm = 101,325 Pa.
            result = round(pressure / 101325, 6) # Rounded to six decimal places.
            selected_unit = "atm"

        elif unit == "torr": # Convert Pascals to Torr or mmHg; 1 mmHg ≈ 133 Pa.
            result = round(pressure / 133, 5) # Rounded to five decimal places.
            selected_unit = "mmHg (Torr)"

        elif unit == "kPa": # Convert Pascals to Kilopascals; 1 kPa = 1,000 Pa.
            result = round(pressure / 1000, 6) # Rounded to six decimal places.
            selected_unit = "kPa"

        elif unit == "at": # Convert Pascals to Technical Atmospheres; 1 at ≈ 98066.5 Pa.
            result = round(pressure / 98066.5, 8) # Rounded to eight decimal places.
            selected_unit = "at"

        elif unit == "hPa": # Convert Pascals to Hectopascals; 1 hPa = 100 Pa.
            result = round(pressure / 100, 5) # Rounded to five decimal places.
            selected_unit = "hPa"

        elif unit == "MPa": # Convert Pascals to Megapascals; 1 MPa = 1,000,000 Pa.
            result = round(pressure / 1000000, 10) # Rounded to ten decimal places.
            selected_unit = "MPa"
            
        elif unit == "inHg": # Convert Pascals to Inches of Mercury; 1 inHg = 3,386 Pa  approximately.
            result = round(pressure * 0.00029529980165, 7) # Rounded to seven decimal places.
            selected_unit = "inHg"
        
        return flask.render_template('pressure_calculator.html', pressure=result, selected_unit=selected_unit, force=force, area=area)
    except ValueError:
        return flask.render_template('pressure_calculator.html', error_message="Please enter valid numerical values.")

def calculate_pressure(force, area):
    return force / area

if __name__ == '__main__':
    app.run(debug=True)