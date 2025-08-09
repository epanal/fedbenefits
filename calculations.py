from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN

def calculate_lump_sum_payment(hourly_rate: float, leave_balance_hours: float) -> float:
    """Calculate lump sum payment for unused annual leave."""
    return hourly_rate * leave_balance_hours  # Use leave hours directly

def calculate_annual_leave_accrual(employee_type, years_of_service, pay_periods, hours_in_pay_status=None, avg_hours_per_pay_period=None):
    """Calculate annual leave accrual based on employee type, years of service, and pay periods."""
    if employee_type == "Full-time Employee":
        if years_of_service < 3:
            accrual_rate = 4  # ½ day (4 hours) per pay period
        elif 3 <= years_of_service < 15:
            accrual_rate = 6  # ¾ day (6 hours) per pay period, except for 1¼ day (10 hours) in the last pay period
        else:
            accrual_rate = 8  # 1 day (8 hours) per pay period
    elif employee_type == "Part-time Employee":
        if hours_in_pay_status is None:
            raise ValueError("Please enter the number of hours in pay status for part-time employees.")
        if years_of_service < 3:
            accrual_rate = hours_in_pay_status / 20  # 1 hour for each 20 hours in a pay status
        elif 3 <= years_of_service < 15:
            accrual_rate = hours_in_pay_status / 13  # 1 hour for each 13 hours in a pay status
        else:
            accrual_rate = hours_in_pay_status / 10  # 1 hour for each 10 hours in a pay status
    elif employee_type == "Uncommon Tours of Duty":
        if avg_hours_per_pay_period is None:
            raise ValueError("Please enter the average number of hours per biweekly pay period for uncommon tours of duty.")
        if years_of_service < 3:
            accrual_rate = 4 * (avg_hours_per_pay_period / 80)
        elif 3 <= years_of_service < 15:
            accrual_rate = 6 * (avg_hours_per_pay_period / 80)
        else:
            accrual_rate = 8 * (avg_hours_per_pay_period / 80)
    elif employee_type == "SES, Senior Level, Scientific/Professional Positions":
        accrual_rate = 8  # 8 hours for each pay period, regardless of years of service

    total_accrued_leave = accrual_rate * pay_periods
    return total_accrued_leave

def calculate_severance_pay(annual_salary, years_of_service, months_of_service, age_years, age_months):
    """
    Calculate Severance Pay considering additional months of service.
    
    - Basic Severance: 1 week per year for first 10 years; 2 weeks per year thereafter.
    - Partial Months: Each full 3 months beyond the final full year contributes 25%.
    - Age Adjustment: 2.5% of total severance for each full 3 months of age over 40.
    - Biweekly Severance: 2 * weekly pay.
    - Caps: Max severance is 1 year's salary; max weeks is 52.
    """

    # Step 1: Calculate weekly pay
    weekly_pay = annual_salary / 52.175  

    # Step 2: Determine years of service adjustment (full years only)
    if years_of_service < 10:
        adj_years_of_service = years_of_service
    else:
        adj_years_of_service = ((years_of_service - 10) * 2 ) + 10

    # Step 3: Calculate basic severance (full years)
    basic_severance = weekly_pay * adj_years_of_service    

    # Step 4: Calculate partial severance for months (before applying age factor)
    full_periods_of_3_months = months_of_service // 3
    partial_severance = (weekly_pay * 2) * full_periods_of_3_months * 0.25

    # Step 5: Compute total severance BEFORE age factor
    total_severance_before_age_factor = basic_severance + partial_severance

    # Step 6: Calculate age factor (only for full 3-month increments over 40)
    age = age_years + age_months / 12.0
    full_3_months_over_40 = max(0, int((age - 40) * 12 // 3))

    # Step 7: Apply age factor to total severance before cap
    age_adjustment = total_severance_before_age_factor * (0.025 * full_3_months_over_40)
    total_severance = total_severance_before_age_factor + age_adjustment

    # Step 8: Apply salary cap (max severance = 1 year of salary)
    total_severance = min(total_severance, weekly_pay * 52)

    # Step 9: Calculate biweekly severance
    biweekly_severance = 2 * weekly_pay

    # Step 10: Calculate weeks of severance (max 52)
    weeks_of_severance = min(52, (total_severance / biweekly_severance) * 2)

    return total_severance, total_severance_before_age_factor, age_adjustment, biweekly_severance, weeks_of_severance

def calculate_scd(current_start_str, prior_periods):
    """
    Calculates the adjusted Service Computation Date (SCD).

    Parameters:
    - current_start_str: ISO-format string of current start date (YYYY-MM-DD)
    - prior_periods: list of (start_str, end_str) tuples

    Returns:
    - adjusted_scd (date)
    - total_creditable_days (int)
    - period_breakdown (list of (start, end, days))
    """
    current_start = datetime.strptime(current_start_str, "%Y-%m-%d")
    total_days = 0
    period_breakdown = []

    for start_str, end_str in prior_periods:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
        delta = (end - start).days + 1
        days = max(delta, 0)
        total_days += days
        period_breakdown.append((start_str, end_str, days))

    adjusted_scd = (current_start - timedelta(days=total_days)).date()
    return adjusted_scd, total_days, period_breakdown

def calculate_tsp_growth(current_balance, annual_contribution, years, annual_rate):
    r = annual_rate / 100
    P = current_balance
    PMT = annual_contribution
    yearly_data = []

    balance = P
    for year in range(1, years + 1):
        balance = balance * (1 + r) + PMT
        contributions = PMT * year
        growth = balance - contributions - P
        yearly_data.append({
            "year": year,
            "balance": round(balance, 2),
            "contributions": round(contributions, 2),
            "growth": round(growth, 2)
        })

    future_value = balance
    total_contributions = PMT * years
    growth_total = future_value - total_contributions - P

    return {
        "future_value": round(future_value, 2),
        "total_contributions": round(total_contributions, 2),
        "growth": round(growth_total, 2),
        "yearly_data": yearly_data
    }

def calculate_tsp_loan(
    loan_type: str,
    tsp_balance: float,
    loan_amount: float,
    loan_interest_rate: float,
    expected_annual_growth: float,
    num_pay_periods: int,
    biweekly_contribution_no_loan: float,
    biweekly_contribution_during_loan: float
):
    annual_growth_rate = expected_annual_growth / 100
    loan_rate = loan_interest_rate / 100
    r = loan_rate / 26
    g = annual_growth_rate / 26
    years = num_pay_periods / 26

    processing_fee = 100 if loan_type == "residential" else 50

    # Loan payment
    if r > 0:
        payment = loan_amount * r / (1 - (1 + r) ** -num_pay_periods)
    else:
        payment = loan_amount / num_pay_periods
    total_repaid = payment * num_pay_periods

    # No loan growth
    no_loan_bal = tsp_balance
    no_loan_periods = []
    for p in range(1, num_pay_periods + 1):
        no_loan_bal += biweekly_contribution_no_loan
        no_loan_bal *= (1 + g)
        no_loan_periods.append(round(no_loan_bal, 2))

    # With loan
    with_loan_bal = tsp_balance - loan_amount - processing_fee
    loan_balance = loan_amount
    with_loan_periods = []
    payperiod_data = []

    for p in range(1, num_pay_periods + 1):
        interest = loan_balance * r
        principal = payment - interest
        loan_balance = max(0, loan_balance - principal)

        with_loan_bal += biweekly_contribution_during_loan
        with_loan_bal += principal  # Credit the repaid principal
        with_loan_bal *= (1 + g)    # Apply growth AFTER contributions + repayment

        payperiod_data.append({
            "period": p,
            "no_loan": round(no_loan_periods[p - 1], 2),
            "with_loan": round(with_loan_bal, 2),
            "diff": round(no_loan_periods[p - 1] - with_loan_bal, 2),
            "loan_balance": round(loan_balance, 2),
            "interest": round(interest, 2),
            "principal": round(principal, 2),
            "contribution_with_loan": round(biweekly_contribution_during_loan, 2),
            "contribution_no_loan": round(biweekly_contribution_no_loan, 2),
            "remaining_loan_payments": num_pay_periods - p
        })

        if p % 26 == 0:
            with_loan_periods.append(round(with_loan_bal, 2))

    # Continue growing balance after loan is paid
    total_periods = int(years * 26)
    for p in range(num_pay_periods + 1, total_periods + 1):
        no_loan_bal += biweekly_contribution_no_loan
        no_loan_bal *= (1 + g)

        with_loan_bal += biweekly_contribution_no_loan
        with_loan_bal *= (1 + g)

        payperiod_data.append({
            "period": p,
            "no_loan": round(no_loan_bal, 2),
            "with_loan": round(with_loan_bal, 2),
            "diff": round(no_loan_bal - with_loan_bal, 2),
            "loan_balance": None,
            "remaining_loan_payments": None
        })

        if p % 26 == 0:
            no_loan_periods.append(round(no_loan_bal, 2))
            with_loan_periods.append(round(with_loan_bal, 2))

    delta = no_loan_bal - with_loan_bal

    return {
        "balance_no_loan": round(no_loan_bal, 2),
        "balance_with_loan": round(with_loan_bal, 2),
        "delta": round(delta, 2),
        "loan_payment": round(payment, 2),
        "total_repaid": round(total_repaid, 2),
        "processing_fee": processing_fee,
        "yearly_data": {
            "labels": [p["period"] for p in payperiod_data],
            "no_loan": [p["no_loan"] for p in payperiod_data],
            "with_loan": [p["with_loan"] for p in payperiod_data]
        },
        "payperiod_data": payperiod_data
    }

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN

def calculate_lump_sum_payment(hourly_rate: float, leave_balance_hours: float) -> float:
    """Calculate lump sum payment for unused annual leave."""
    return hourly_rate * leave_balance_hours  # Use leave hours directly

def calculate_annual_leave_accrual(employee_type, years_of_service, pay_periods, hours_in_pay_status=None, avg_hours_per_pay_period=None):
    """Calculate annual leave accrual based on employee type, years of service, and pay periods."""
    if employee_type == "Full-time Employee":
        if years_of_service < 3:
            accrual_rate = 4  # ½ day (4 hours) per pay period
        elif 3 <= years_of_service < 15:
            accrual_rate = 6  # ¾ day (6 hours) per pay period, except for 1¼ day (10 hours) in the last pay period
        else:
            accrual_rate = 8  # 1 day (8 hours) per pay period
    elif employee_type == "Part-time Employee":
        if hours_in_pay_status is None:
            raise ValueError("Please enter the number of hours in pay status for part-time employees.")
        if years_of_service < 3:
            accrual_rate = hours_in_pay_status / 20  # 1 hour for each 20 hours in a pay status
        elif 3 <= years_of_service < 15:
            accrual_rate = hours_in_pay_status / 13  # 1 hour for each 13 hours in a pay status
        else:
            accrual_rate = hours_in_pay_status / 10  # 1 hour for each 10 hours in a pay status
    elif employee_type == "Uncommon Tours of Duty":
        if avg_hours_per_pay_period is None:
            raise ValueError("Please enter the average number of hours per biweekly pay period for uncommon tours of duty.")
        if years_of_service < 3:
            accrual_rate = 4 * (avg_hours_per_pay_period / 80)
        elif 3 <= years_of_service < 15:
            accrual_rate = 6 * (avg_hours_per_pay_period / 80)
        else:
            accrual_rate = 8 * (avg_hours_per_pay_period / 80)
    elif employee_type == "SES, Senior Level, Scientific/Professional Positions":
        accrual_rate = 8  # 8 hours for each pay period, regardless of years of service

    total_accrued_leave = accrual_rate * pay_periods
    return total_accrued_leave

def calculate_severance_pay(annual_salary, years_of_service, months_of_service, age_years, age_months):
    """
    Calculate Severance Pay considering additional months of service.
    
    - Basic Severance: 1 week per year for first 10 years; 2 weeks per year thereafter.
    - Partial Months: Each full 3 months beyond the final full year contributes 25%.
    - Age Adjustment: 2.5% of total severance for each full 3 months of age over 40.
    - Biweekly Severance: 2 * weekly pay.
    - Caps: Max severance is 1 year's salary; max weeks is 52.
    """

    # Step 1: Calculate weekly pay
    weekly_pay = annual_salary / 52.175  

    # Step 2: Determine years of service adjustment (full years only)
    if years_of_service < 10:
        adj_years_of_service = years_of_service
    else:
        adj_years_of_service = ((years_of_service - 10) * 2 ) + 10

    # Step 3: Calculate basic severance (full years)
    basic_severance = weekly_pay * adj_years_of_service    

    # Step 4: Calculate partial severance for months (before applying age factor)
    full_periods_of_3_months = months_of_service // 3
    partial_severance = (weekly_pay * 2) * full_periods_of_3_months * 0.25

    # Step 5: Compute total severance BEFORE age factor
    total_severance_before_age_factor = basic_severance + partial_severance

    # Step 6: Calculate age factor (only for full 3-month increments over 40)
    age = age_years + age_months / 12.0
    full_3_months_over_40 = max(0, int((age - 40) * 12 // 3))

    # Step 7: Apply age factor to total severance before cap
    age_adjustment = total_severance_before_age_factor * (0.025 * full_3_months_over_40)
    total_severance = total_severance_before_age_factor + age_adjustment

    # Step 8: Apply salary cap (max severance = 1 year of salary)
    total_severance = min(total_severance, weekly_pay * 52)

    # Step 9: Calculate biweekly severance
    biweekly_severance = 2 * weekly_pay

    # Step 10: Calculate weeks of severance (max 52)
    weeks_of_severance = min(52, (total_severance / biweekly_severance) * 2)

    return total_severance, total_severance_before_age_factor, age_adjustment, biweekly_severance, weeks_of_severance

def calculate_scd(current_start_str, prior_periods):
    """
    Calculates the adjusted Service Computation Date (SCD).

    Parameters:
    - current_start_str: ISO-format string of current start date (YYYY-MM-DD)
    - prior_periods: list of (start_str, end_str) tuples

    Returns:
    - adjusted_scd (date)
    - total_creditable_days (int)
    - period_breakdown (list of (start, end, days))
    """
    current_start = datetime.strptime(current_start_str, "%Y-%m-%d")
    total_days = 0
    period_breakdown = []

    for start_str, end_str in prior_periods:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
        delta = (end - start).days + 1
        days = max(delta, 0)
        total_days += days
        period_breakdown.append((start_str, end_str, days))

    adjusted_scd = (current_start - timedelta(days=total_days)).date()
    return adjusted_scd, total_days, period_breakdown

def calculate_tsp_growth(current_balance, annual_salary, employee_percent,
                         employer_percent, years, annual_rate, inflation_rate):
    """
    Calculates TSP growth with separate salary, employee %, employer %, 
    and inflation adjustment.

    Returns:
        dict with:
        - future_value_nominal
        - future_value_real
        - total_contributions
        - growth
        - yearly_data (list of dicts)
    """

    # Calculate annual contribution from employee + employer
    annual_contribution = annual_salary * (employee_percent + employer_percent) / 100

    balance = current_balance
    yearly_data = []
    total_contributions = 0

    for year in range(1, years + 1):
        # Add contributions for the year
        balance += annual_contribution
        total_contributions += annual_contribution

        # Apply growth
        balance *= (1 + annual_rate / 100)

        # Track breakdown for chart
        yearly_data.append({
            "year": year,
            "contributions": round(total_contributions, 2),
            "growth": round(balance - total_contributions - current_balance, 2)
        })

    future_value_nominal = balance
    future_value_real = balance / ((1 + inflation_rate / 100) ** years)

    return {
        "future_value_nominal": round(future_value_nominal, 2),
        "future_value_real": round(future_value_real, 2),
        "total_contributions": round(total_contributions, 2),
        "growth": round(future_value_nominal - current_balance - total_contributions, 2),
        "yearly_data": yearly_data
    }

def calculate_tsp_loan(
    loan_type: str,
    tsp_balance: float,
    loan_amount: float,
    loan_interest_rate: float,
    expected_annual_growth: float,
    num_pay_periods: int,
    biweekly_contribution_no_loan: float,
    biweekly_contribution_during_loan: float
):
    annual_growth_rate = expected_annual_growth / 100
    loan_rate = loan_interest_rate / 100
    r = loan_rate / 26
    g = annual_growth_rate / 26
    years = num_pay_periods / 26

    processing_fee = 100 if loan_type == "residential" else 50

    # Loan payment
    if r > 0:
        payment = loan_amount * r / (1 - (1 + r) ** -num_pay_periods)
    else:
        payment = loan_amount / num_pay_periods
    total_repaid = payment * num_pay_periods

    # No loan growth
    no_loan_bal = tsp_balance
    no_loan_periods = []
    for p in range(1, num_pay_periods + 1):
        no_loan_bal += biweekly_contribution_no_loan
        no_loan_bal *= (1 + g)
        no_loan_periods.append(round(no_loan_bal, 2))

    # With loan
    with_loan_bal = tsp_balance - loan_amount - processing_fee
    loan_balance = loan_amount
    with_loan_periods = []
    payperiod_data = []

    for p in range(1, num_pay_periods + 1):
        interest = loan_balance * r
        principal = payment - interest
        loan_balance = max(0, loan_balance - principal)

        with_loan_bal += biweekly_contribution_during_loan
        with_loan_bal += principal  # Credit the repaid principal
        with_loan_bal *= (1 + g)    # Apply growth AFTER contributions + repayment

        payperiod_data.append({
            "period": p,
            "no_loan": round(no_loan_periods[p - 1], 2),
            "with_loan": round(with_loan_bal, 2),
            "diff": round(no_loan_periods[p - 1] - with_loan_bal, 2),
            "loan_balance": round(loan_balance, 2),
            "interest": round(interest, 2),
            "principal": round(principal, 2),
            "contribution_with_loan": round(biweekly_contribution_during_loan, 2),
            "contribution_no_loan": round(biweekly_contribution_no_loan, 2),
            "remaining_loan_payments": num_pay_periods - p
        })

        if p % 26 == 0:
            with_loan_periods.append(round(with_loan_bal, 2))

    # Continue growing balance after loan is paid
    total_periods = int(years * 26)
    for p in range(num_pay_periods + 1, total_periods + 1):
        no_loan_bal += biweekly_contribution_no_loan
        no_loan_bal *= (1 + g)

        with_loan_bal += biweekly_contribution_no_loan
        with_loan_bal *= (1 + g)

        payperiod_data.append({
            "period": p,
            "no_loan": round(no_loan_bal, 2),
            "with_loan": round(with_loan_bal, 2),
            "diff": round(no_loan_bal - with_loan_bal, 2),
            "loan_balance": None,
            "remaining_loan_payments": None
        })

        if p % 26 == 0:
            no_loan_periods.append(round(no_loan_bal, 2))
            with_loan_periods.append(round(with_loan_bal, 2))

    delta = no_loan_bal - with_loan_bal

    return {
        "balance_no_loan": round(no_loan_bal, 2),
        "balance_with_loan": round(with_loan_bal, 2),
        "delta": round(delta, 2),
        "loan_payment": round(payment, 2),
        "total_repaid": round(total_repaid, 2),
        "processing_fee": processing_fee,
        "yearly_data": {
            "labels": [p["period"] for p in payperiod_data],
            "no_loan": [p["no_loan"] for p in payperiod_data],
            "with_loan": [p["with_loan"] for p in payperiod_data]
        },
        "payperiod_data": payperiod_data
    }

def calculate_tsp_frontload(
    annual_salary,
    target_investment,
    max_biweekly,
    match_percent,
    annual_growth_percent,
    include_match_in_growth=False
):
    # --- constants / base values ---
    num_periods = 26
    # Employee minimum needed each PP to qualify for match (employee-only dollars)
    base = round(annual_salary * (match_percent / 100) / num_periods, 2)

    # Require enough target to fund the base all year (otherwise you can't earn full match)
    min_year_employee = round(base * num_periods, 2)
    if target_investment < min_year_employee:
        raise ValueError(
            f"Target investment (${target_investment:,.2f}) must be at least "
            f"the yearly minimum to receive full match (${min_year_employee:,.2f})."
        )

    # Extra dollars you can front-load beyond the reserved base in every period
    extra_front_budget = round(target_investment - min_year_employee, 2)

    # The most EXTRA you can add in any front-load period (employee-only)
    per_period_extra_cap = max(0.0, round(max_biweekly - base, 2))

    # How many full "max" periods fit, then a one-off remainder (employee-only extras)
    if per_period_extra_cap > 0:
        full_max_periods = int(extra_front_budget // per_period_extra_cap)
        extra_remainder = round(extra_front_budget - full_max_periods * per_period_extra_cap, 2)
    else:
        full_max_periods = 0
        extra_remainder = 0.0

    # --- build schedules (employee-only amounts) ---
    # Front plan: base in all 26 periods, plus extras up front
    front_emp = []
    for i in range(1, num_periods + 1):
        if i <= full_max_periods:
            # base + full extra -> equals max_biweekly (employee-only)
            emp = round(base + per_period_extra_cap, 2)
            label = "Front-Load (Max)"
        elif i == full_max_periods + 1 and extra_remainder > 0:
            emp = round(base + extra_remainder, 2)
            label = "One-Off Remainder"
        else:
            emp = round(base, 2)
            label = "Match Only"
        front_emp.append((emp, label))

    # Even plan: distribute employee-only dollars in cents, put remainder in LAST period
    tgt_cents = int(round(target_investment * 100))          # total employee cents
    base_even_cents = tgt_cents // num_periods               # floor per period
    leftover_cents = tgt_cents - base_even_cents * num_periods
    even_emp = []
    for i in range(1, num_periods + 1):
        cents = base_even_cents + (leftover_cents if i == num_periods else 0)
        even_emp.append(round(cents / 100.0, 2))

    # --- growth calculation (optionally include employer match in the account growth) ---
    growth_rate = (1 + annual_growth_percent / 100) ** (1 / num_periods)
    match_per_period = base  # employer contribution per period (not shown in table, used for growth if flagged)

    front_balance = 0.0
    even_balance = 0.0
    cumulative_front = 0.0
    cumulative_even = 0.0
    table = []
    labels = []

    for i in range(1, num_periods + 1):
        f_emp, f_label = front_emp[i - 1]
        e_emp = even_emp[i - 1]

        # cumulative (employee-only)
        cumulative_front = round(cumulative_front + f_emp, 2)
        cumulative_even = round(cumulative_even + e_emp, 2)

        # growth step
        f_begin = front_balance
        e_begin = even_balance

        # front account
        add_front = f_emp + (match_per_period if include_match_in_growth else 0.0)
        front_balance = (front_balance + add_front) * growth_rate

        # even account
        add_even = e_emp + (match_per_period if include_match_in_growth else 0.0)
        even_balance = (even_balance + add_even) * growth_rate

        table.append({
            "PP": i,
            "Front Contribution": round(f_emp, 2),     # employee-only
            "Even Contribution": round(e_emp, 2),      # employee-only
            "Type": f_label,
            "Cumulative Front": round(cumulative_front, 2),
            "Cumulative Even": round(cumulative_even, 2),
            "Front Begin": round(f_begin, 2),
            "Front End": round(front_balance, 2),
            "Even Begin": round(e_begin, 2),
            "Even End": round(even_balance, 2),
        })
        labels.append(i)

    # --- derive summary from actual schedule (not assumptions) ---
    front_max_count = sum(1 for emp, _lbl in front_emp if emp == round(max_biweekly, 2))
    # a one-off is any period strictly between base and max (employee-only)
    one_off_emp = next((emp for emp, _ in front_emp if base < emp < round(max_biweekly, 2)), 0.0)
    match_only_count = sum(1 for emp, _ in front_emp if emp == base)

    if front_max_count > 0 and one_off_emp > 0:
        summary_lines = [
            f"Always contribute at least ${base} per pay period to receive the full agency match.",
            f"First, contribute ${round(max_biweekly,2)} for {front_max_count} pay periods.",
            f"Then contribute ${round(one_off_emp,2)} for 1 pay period.",
            f"Finally, continue contributing ${base} for the remaining {match_only_count} pay periods."
        ]
    elif front_max_count > 0 and one_off_emp == 0:
        summary_lines = [
            f"Always contribute at least ${base} per pay period to receive the full agency match.",
            f"First, contribute ${round(max_biweekly,2)} for {front_max_count} pay periods.",
            f"Finally, continue contributing ${base} for the remaining {match_only_count} pay periods."
        ]
    elif front_max_count == 0 and one_off_emp > 0:
        # Edge case: only a one-off (includes the base that period)
        # Compute “remaining” match-only periods correctly
        remaining = match_only_count - 1 if match_only_count > 0 else 0
        summary_lines = [
            f"Always contribute at least ${base} per pay period to receive the full agency match.",
            f"Make a one-off of ${round(one_off_emp,2)} in the first pay period,",
            f"then contribute ${base} for the remaining {remaining} pay periods."
        ]
    else:
        summary_lines = [
            f"Contribute ${base} in each pay period to receive the full agency match."
        ]

    result = {
        "match_per_period": round(base, 2),
        "front_load_periods": front_max_count,
        "one_off_amount": round(one_off_emp, 2),
        "match_only_periods": match_only_count,
        "max_biweekly": round(max_biweekly, 2),  # employee-only max per PP
        "front_ending_balance": round(front_balance, 2),
        "even_ending_balance": round(even_balance, 2),
        "advantage": round(front_balance - even_balance, 2),
        "summary_lines": summary_lines,
    }

    chart_data = {
        "labels": labels,
        "front": [row["Front End"] for row in table],
        "even": [row["Even End"] for row in table],
    }

    return result, table, chart_data
