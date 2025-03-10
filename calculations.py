def calculate_lump_sum_payment(hourly_rate, leave_balance_hours):
    """Calculate lump sum payment for unused annual leave."""
    return hourly_rate * leave_balance_hours  # Use leave hours directly

def calculate_annual_leave_accrual(employee_type, years_of_service, pay_periods):
    """Calculate annual leave accrual based on employee type, years of service, and pay periods."""
    if employee_type == "Full-time Employee":
        if years_of_service < 3:
            accrual_rate = 4  # ½ day (4 hours) per pay period
        elif 3 <= years_of_service < 15:
            accrual_rate = 6  # ¾ day (6 hours) per pay period, except for 1¼ day (10 hours) in the last pay period
        else:
            accrual_rate = 8  # 1 day (8 hours) per pay period
    elif employee_type == "Part-time Employee":
        if years_of_service < 3:
            accrual_rate = (1 / 20)  # 1 hour for each 20 hours in a pay status
        elif 3 <= years_of_service < 15:
            accrual_rate = (1 / 13)  # 1 hour for each 13 hours in a pay status
        else:
            accrual_rate = (1 / 10)  # 1 hour for each 10 hours in a pay status
    elif employee_type == "Uncommon Tours of Duty":
        if years_of_service < 3:
            accrual_rate = (4 * (pay_periods * 40 / 80))
        elif 3 <= years_of_service < 15:
            accrual_rate = (6 * (pay_periods * 40 / 80))
        else:
            accrual_rate = (8 * (pay_periods * 40 / 80))
    elif employee_type == "SES, Senior Level, Scientific/Professional Positions":
        accrual_rate = 8  # 8 hours for each pay period, regardless of years of service

    total_accrued_leave = accrual_rate * pay_periods
    return total_accrued_leave

def calculate_severance_pay(annual_salary, years_of_service, age_years, age_months):
    """Calculate severance pay based on annual salary, years of service, and age.
    
    - Basic Severance Pay: 1 week of pay per year for the first 10 years, then 2 weeks per year thereafter.
    - Age Factor: For ages 40 to 65, linearly interpolate from 1.0 at age 40 to 3.5 at age 65. For ages under 40, factor = 1.0; for 65 and older, factor = 3.5.
    - Biweekly Severance Pay: Defined as 2 times the weekly pay.
    - Weeks of Severance Pay: Total severance divided by weekly pay.
    """
    # Weekly pay calculation
    weekly_pay = annual_salary / 52.0

    # Basic Severance Pay calculation
    if years_of_service < 10:
        basic_severance = years_of_service * weekly_pay
    else:
        basic_severance = (10 * weekly_pay) + ((years_of_service - 10) * 2 * weekly_pay)

    # Age factor calculation using linear interpolation between age 40 and 65
    age = age_years + age_months / 12.0
    if age < 40:
        age_factor = 1.0
    elif age < 65:
        age_factor = 1.0 + ((age - 40) / (65 - 40)) * (3.5 - 1.0)
    else:
        age_factor = 3.5

    # Adjusted Severance Pay calculation
    adjusted_severance = basic_severance * age_factor

    # Total Severance Pay (no cap applied)
    total_severance = adjusted_severance

    # Weeks of Severance Pay calculation
    weeks_of_severance = total_severance / weekly_pay

    # Biweekly Severance Pay: expected to be 2 * weekly pay
    biweekly_severance = 2 * weekly_pay

    return total_severance, basic_severance, adjusted_severance - basic_severance, biweekly_severance, weeks_of_severance
