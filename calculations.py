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
            accrual_rate = (1 / 20) * 1  # 1 hour for each 20 hours in a pay status
        elif 3 <= years_of_service < 15:
            accrual_rate = (1 / 13) * 1  # 1 hour for each 13 hours in a pay status
        else:
            accrual_rate = (1 / 10) * 1  # 1 hour for each 10 hours in a pay status
    elif employee_type == "Uncommon Tours of Duty":
        if years_of_service < 3:
            accrual_rate = (4 * (pay_periods * 40 / 80))  # 4 hours times average # of hours per pay period divided by 80
        elif 3 <= years_of_service < 15:
            accrual_rate = (6 * (pay_periods * 40 / 80))  # 6 hours times average # of hours per pay period divided by 80
        else:
            accrual_rate = (8 * (pay_periods * 40 / 80))  # 8 hours times average # of hours per pay period divided by 80
    elif employee_type == "SES, Senior Level, Scientific/Professional Positions":
        accrual_rate = 8  # 8 hours for each pay period, regardless of years of service

    # Calculate total leave accrual
    total_accrued_leave = accrual_rate * pay_periods
    return total_accrued_leave

def calculate_severance_pay(annual_salary, years_of_service, age_years, age_months):
    """Calculate Severance Pay based on annual salary, years of service, and age at separation."""

    # Basic severance pay calculation
    if years_of_service < 10:
        basic_severance = years_of_service * (annual_salary / 52)  # one week per year
    else:
        basic_severance = (10 * (annual_salary / 52)) + ((years_of_service - 10) * 2 * (annual_salary / 52))  # first 10 years + 2 weeks per year after 10

    # Age adjustment calculation
    if age_years < 40:
        age_factor = 1.0
    elif 40 <= age_years < 50:
        # For ages 40-49, apply a slight increment for months
        age_factor = 1.0 + (age_months * 0.025)
    elif 50 <= age_years < 65:
        age_factor = 2.0  # Example, can increase based on exact age range
    else:
        age_factor = 3.5  # For age 65 and above

    # Adjusted severance pay (applying age factor)
    adjusted_severance = basic_severance * age_factor
    
    # Total severance pay (no cap unless explicitly needed)
    total_severance = adjusted_severance

    # Biweekly and weeks of severance pay
    biweekly_severance = total_severance / 26  # Biweekly payments (26 pay periods in a year)
    weeks_of_severance = total_severance / (annual_salary / 52)  # Total weeks of severance pay

    return total_severance, basic_severance, adjusted_severance - basic_severance, biweekly_severance, weeks_of_severance
