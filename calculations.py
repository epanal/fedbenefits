from datetime import datetime, timedelta

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
    