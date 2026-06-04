"""
Flask web application for Cessna-172 Weight & Balance calculation.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from .item import WeightItem
from .calculator import WeightAndBalance

# Typical arm positions for Cessna-172 (from POH)
ARM_VALUES = {
    "Pilot": 36.0,
    "Copilot": 36.0,
    "Front Passenger": 73.0,
    "Rear Passenger": 84.0,
    "Baggage Area 1": 95.0,
    "Baggage Area 2": 115.0,
    "Fuel": 48.0,
}

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)
app.secret_key = 'your-secret-key-here'  # In production, use a proper secret key


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        items = []
        for name, default_arm in ARM_VALUES.items():
            weight_str = request.form.get(name.lower().replace(' ', '_').replace('-', '_'), '0')
            try:
                weight = float(weight_str)
                if weight < 0:
                    flash(f"Weight for {name} cannot be negative.", "error")
                    return redirect(url_for('index'))
                if weight > 0:
                    items.append(WeightItem(name, weight, default_arm))
            except ValueError:
                flash(f"Please enter a valid number for {name}.", "error")
                return redirect(url_for('index'))

        if not items:
            flash("Please enter at least one weight.", "warning")
            return redirect(url_for('index'))

        try:
            wb = WeightAndBalance(items)
            report = wb.report()
            ok, note = wb.is_within_limits()
            return render_template('result.html', report=report, ok=ok, note=note)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('index'))

    # GET request: show the form
    return render_template('index.html', arm_values=ARM_VALUES)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)