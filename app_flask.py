from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date, datetime, timedelta
from calculations import (
    calculate_severance_pay,
    calculate_lump_sum_payment,
    calculate_annual_leave_accrual,
    calculate_scd,
    calculate_tsp_growth,
    calculate_tsp_loan,
    calculate_tsp_frontload
)

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_secure_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/severance', methods=['GET'])
def show_severance_form():
    values = session.get('severance_inputs', {
        'annual_salary': 0,
        'years': 0,
        'months': 0,
        'age_years': 0,
        'age_months': 0
    })
    return render_template('severance.html', values=values)

@app.route('/lump_sum', methods=['GET'])
def show_lump_sum_form():
    values = session.get('lump_sum_inputs', {
        'hourly_rate': 0,
        'leave_hours': 0
    })
    return render_template('lump_sum.html', values=values)

@app.route('/leave_accrual', methods=['GET'])
def show_leave_accrual_form():
    values = session.get('leave_accrual_inputs', {
        'employee_type': 'Full-time Employee',
        'years': 0,
        'pay_periods': 1,
        'hours_in_pay_status': '',
        'avg_hours_per_period': ''
    })
    return render_template('leave_accrual.html', values=values)

@app.route('/drp_comparison', methods=['GET'])
def show_drp_comparison_form():
    today = date.today()
    values = session.get('drp_comparison_inputs', {
        'biweekly_salary': 0,
        'drp_start_date': today.isoformat(),
        'severance_estimate': 0,
        'rif_pay_periods': 0
    })

    try:
        drp_start = datetime.fromisoformat(values['drp_start_date']).date()
    except Exception:
        drp_start = today

    # Static cutoff for FY2025
    sep_30 = date(2025, 9, 30)
    remaining = max(0, (sep_30 - drp_start).days // 14)

    return render_template(
        'drp_comparison.html',
        values=values,
        remaining_periods=remaining,
        current_date=today.isoformat()
    )

@app.route("/tsp-growth", methods=["GET", "POST"])
def tsp_growth():
    if request.method == "POST":
        current_balance = float(request.form["current_balance"])
        annual_contribution = float(request.form["annual_contribution"])
        years = int(request.form["years"])
        annual_rate = float(request.form["annual_rate"])

        # Save inputs in session for displaying later
        session["tsp_inputs"] = {
            "current_balance": current_balance,
            "annual_contribution": annual_contribution,
            "years": years,
            "annual_rate": annual_rate
        }

        result = calculate_tsp_growth(current_balance, annual_contribution, years, annual_rate)
        return render_template("tsp_growth.html", result=result,
                               current_balance=current_balance,
                               annual_contribution=annual_contribution,
                               years=years,
                               annual_rate=annual_rate)

    return render_template("tsp_growth.html", result=None)

@app.route("/tsp-loan", methods=["GET", "POST"])
def tsp_loan():
    if request.method == "POST":
        form = request.form

        try:
            loan_type = form["loan_type"]
            tsp_balance = float(form["tsp_balance"])
            loan_amount = float(form["loan_amount"])
            loan_interest_rate = float(form["loan_interest_rate"])
            expected_annual_growth = float(form["expected_annual_growth"])
            num_pay_periods = int(form["num_pay_periods"])
            biweekly_contribution_no_loan = float(form["biweekly_contribution_no_loan"])
            biweekly_contribution_during_loan = float(form["biweekly_contribution_during_loan"])
        except (ValueError, KeyError):
            return render_template("tsp_loan.html", error="Please enter valid numeric values.", values=form)

        # Validations
        if loan_amount < 1000:
            return render_template("tsp_loan.html", error="Loan must be at least $1,000.", values=form)
        if loan_amount > tsp_balance:
            return render_template("tsp_loan.html", error="Loan cannot exceed current TSP balance.", values=form)
        if num_pay_periods < 26 or num_pay_periods > 390:
            return render_template("tsp_loan.html", error="Loan length must be between 26 and 390 pay periods.", values=form)
        if loan_amount > 50000:
            return render_template("tsp_loan.html", error="Loan cannot exceed $50,000.", values=form)
        
        # Loan-type-specific validation
        loan_range = {
            "general": (26, 130),
            "residential": (131, 390)
        }
        min_pp, max_pp = loan_range[loan_type]
        if not (min_pp <= num_pay_periods <= max_pp):
            return render_template("tsp_loan.html", error=f"{loan_type.capitalize()} loans must be between {min_pp} and {max_pp} payments (pay periods).", values=form)

        session["tsp_loan_inputs"] = dict(form)

        result = calculate_tsp_loan(
            loan_type,
            tsp_balance,
            loan_amount,
            loan_interest_rate,
            expected_annual_growth,
            num_pay_periods,
            biweekly_contribution_no_loan,
            biweekly_contribution_during_loan
        )

        return render_template("tsp_loan.html", result=result, values=form)

    # GET request
    saved_values = session.get("tsp_loan_inputs", {})
    return render_template("tsp_loan.html", result=None, values=saved_values)

@app.route('/severance', methods=['POST'])
def process_severance():
    annual_salary = float(request.form['annual_salary'])
    years = int(request.form['years'])
    months = int(request.form['months'])
    age_years = int(request.form['age_years'])
    age_months = int(request.form['age_months'])

    session['severance_inputs'] = {
        'annual_salary': annual_salary,
        'years': years,
        'months': months,
        'age_years': age_years,
        'age_months': age_months
    }

    if annual_salary == 0 or (years == 0 and months == 0) or age_years == 0:
        return render_template('result_severance.html', result={
            "error": "Please enter valid input values greater than zero for calculation."
        })

    total, basic, age_adj, biweekly, weeks = calculate_severance_pay(
        annual_salary, years, months, age_years, age_months
    )

    return render_template('result_severance.html', result={
        "annual_salary": round(annual_salary, 2),
        "years": years,
        "months": months,
        "age_years": age_years,
        "age_months": age_months,
        "basic": round(basic, 2),
        "age_adj": round(age_adj, 2),
        "total": round(total, 2),
        "weeks": round(weeks, 2)
    })

@app.route('/lump_sum', methods=['POST'])
def process_lump_sum():
    hourly_rate = float(request.form['hourly_rate'])
    leave_hours = float(request.form['leave_hours'])

    session['lump_sum_inputs'] = {
        'hourly_rate': hourly_rate,
        'leave_hours': leave_hours
    }

    lump_sum = calculate_lump_sum_payment(hourly_rate, leave_hours)
    return render_template('result_lump_sum.html', result=round(lump_sum, 2))

@app.route('/leave_accrual', methods=['POST'])
def process_leave_accrual():
    emp_type = request.form['employee_type']
    years = int(request.form['years'])
    periods = int(request.form['pay_periods'])

    hrs_status = request.form.get('hours_in_pay_status')
    hrs_status = int(hrs_status) if hrs_status else None

    avg_hrs = request.form.get('avg_hours_per_period')
    avg_hrs = int(avg_hrs) if avg_hrs else None

    session['leave_accrual_inputs'] = {
        'employee_type': emp_type,
        'years': years,
        'pay_periods': periods,
        'hours_in_pay_status': hrs_status if hrs_status is not None else '',
        'avg_hours_per_period': avg_hrs if avg_hrs is not None else ''
    }

    try:
        leave = calculate_annual_leave_accrual(emp_type, years, periods, hrs_status, avg_hrs)
        return render_template('result_leave_accrual.html', result=round(leave, 2))
    except ValueError as e:
        return render_template('result_leave_accrual.html', error=str(e))

@app.route('/drp_comparison', methods=['POST'])
def process_drp_comparison():
    biweekly_salary = float(request.form['biweekly_salary'])
    severance_est = float(request.form['severance_estimate'])
    rif_periods = int(request.form['rif_pay_periods'])
    drp_start_date = request.form['drp_start_date']
    drp_start = date.fromisoformat(drp_start_date)

    session['drp_comparison_inputs'] = {
        'biweekly_salary': biweekly_salary,
        'drp_start_date': drp_start_date,
        'severance_estimate': severance_est,
        'rif_pay_periods': rif_periods
    }

    today = date.today()
    sep_30 = date(today.year, 9, 30)
    remaining_periods = max(0, (sep_30 - drp_start).days // 14)
    total_drp = biweekly_salary * remaining_periods
    total_rif = biweekly_salary * rif_periods
    adjusted_severance = severance_est + total_rif

    return render_template('result_drp_comparison.html', result={
        "total_drp": round(total_drp, 2),
        "severance_est": round(severance_est, 2),
        "total_rif": round(total_rif, 2),
        "adjusted_severance": round(adjusted_severance, 2),
        "remaining_periods": remaining_periods,
        "better": "DRP" if total_drp > adjusted_severance else "Severance" if adjusted_severance > total_drp else "Equal"
    })

@app.route('/scd', methods=['GET', 'POST'])
def scd_calculator():
    scd = None
    error = None
    prior_starts = []
    prior_ends = []

    if request.method == "POST":
        try:
            current_start = request.form['current_start']
            prior_starts = request.form.getlist("prior_start[]")
            prior_ends = request.form.getlist("prior_end[]")
            prior_periods = list(zip(prior_starts, prior_ends))

            current_start_dt = datetime.strptime(current_start, "%Y-%m-%d")
            today_dt = datetime.today()
            today_str = date.today().isoformat()
            current_days = (today_dt - current_start_dt).days + 1
            current_period = (current_start, today_str, current_days)

            if not prior_periods or all(not s.strip() or not e.strip() for s, e in prior_periods):
                # No prior periods entered — SCD is just the current start
                scd = current_start_dt.date()
                total_days = current_days
                period_breakdown = [current_period]
            else:
                # Calculate SCD using prior periods
                scd, total_days, period_breakdown = calculate_scd(current_start, prior_periods)

                total_service_days = total_days + current_days

                # Add current service block for display only (not counted in SCD shift)
                period_breakdown.append(current_period)

            return render_template(
                "result_scd.html",
                scd=scd,
                error=error,
                current_start=current_start,
                total_days=total_days,
                total_service_days=total_service_days,
                periods=period_breakdown,
                current_date=today_str
            )

        except Exception as ex:
            error = f"Error calculating SCD: {ex}"

    return render_template("scd.html", scd=scd, error=error)

@app.route("/tsp-frontload", methods=["GET", "POST"])
def tsp_frontload():
    if request.method == "POST":
        form = request.form
        try:
            annual_salary = float(form["annual_salary"])
            target_investment = float(form["target_investment"])
            max_biweekly = float(form["max_biweekly"])
            match_percent = float(form["match_percent"])
            growth_rate = float(form["growth_rate"])
            include_match = "include_match" in form
        except (ValueError, KeyError):
            values = {
                "annual_salary": form.get("annual_salary", ""),
                "target_investment": form.get("target_investment", ""),
                "max_biweekly": form.get("max_biweekly", ""),
                "match_percent": form.get("match_percent", ""),
                "growth_rate": form.get("growth_rate", ""),
                "include_match": "include_match" in form
            }
            return render_template("tsp_frontload.html", result=None, values=values, error="Invalid input")

        values = {
            "annual_salary": annual_salary,
            "target_investment": target_investment,
            "max_biweekly": max_biweekly,
            "match_percent": match_percent,
            "growth_rate": growth_rate,
            "include_match": include_match
        }

        try:
            result, table, chart_data = calculate_tsp_frontload(
                annual_salary=annual_salary,
                target_investment=target_investment,
                max_biweekly=max_biweekly,
                match_percent=match_percent,
                annual_growth_percent=growth_rate,
                include_match_in_growth=include_match  # ✅ NEW ARG
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render_template("tsp_frontload.html", result=None, values=values, error=str(e))

        return render_template("tsp_frontload.html", result=result, values=values, table=table, chart_data=chart_data)

    # GET request
    return render_template("tsp_frontload.html", result=None, values={})

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('index'))  # or render_template('404.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)