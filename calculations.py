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
    - Age Factor: 1.0 at age 40 to 3.5 at age 65 (linear interpolation).
    - Biweekly Severance: 2 * weekly pay.
    - Weeks of Severance Pay: Total severance / weekly pay.
    - Caps: Max severance is 1 year's salary; max weeks is 52.
    """

    # Convert total service into fractional years (only full years, excluding months)
    total_years_of_service = years_of_service

    # Use OPM convention of 52.175 weeks in a year
    weekly_pay = annual_salary / 52.175  

    # Adjust years for severance calculation (full years only)
    if total_years_of_service < 10:
        adj_years_of_service = total_years_of_service
    else:
        adj_years_of_service = ((total_years_of_service - 10) * 2 ) + 10

    # Calculate basic severance based on full years
    basic_severance = weekly_pay * adj_years_of_service    

    # Add prorated severance for partial months
    partial_months = months_of_service % 12
    partial_severance = 0
    if partial_months > 0:
        # Calculate additional severance for every 3 months beyond a full year
        partial_severance = (weekly_pay * 2) * (partial_months / 3.0) * 0.25

    # Combine basic severance and partial severance
    total_severance = basic_severance + partial_severance

    # Combine years and months into a decimal age
    age = age_years + age_months / 12.0

    # Linear interpolation for age factor
    if age < 40:
        age_factor = 1.0
    elif age < 65:
        age_factor = 1.0 + ((age - 40) / 25) * 2.5  # (3.5 - 1.0) spread over 25 years
    else:
        age_factor = 3.5

    # Adjust severance with age factor
    adjusted_severance = total_severance * age_factor

    # Apply salary cap (max severance = 1 year of salary)
    total_severance = min(adjusted_severance, weekly_pay * 52)

    # Biweekly Severance Pay
    biweekly_severance = 2 * weekly_pay

    # Cap the weeks of severance to a max of 52
    weeks_of_severance = min(52, (total_severance / biweekly_severance) * 2)

    # Calculate age adjustment amount (how much age factor increases severance)
    age_adjustment = adjusted_severance - total_severance

    return total_severance, basic_severance, partial_severance, age_adjustment, biweekly_severance, weeks_of_severance
