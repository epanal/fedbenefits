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
    # Convert age into total years including fractional months
    age_in_years = age_years + (age_months / 12)

    # Determine the age adjustment factor based on the age (capped at 65)
    if age_years >= 65:
        age_adjustment_factor = 3.5
    else:
        # Lookup the age adjustment factor based on the age
        # (This is your existing logic for age adjustment based on the age_in_years, for example)
        if age_in_years > 40:
            age_adjustment_factor = ((age_in_years - 40) // 0.25) * 0.025  # 2.5% for each full 3 months over 40
        else:
            age_adjustment_factor = 0

    # Basic Severance Pay calculation (assuming 2 weeks per year of service)
    basic_severance = (annual_salary / 26) * years_of_service
    
    # Age Adjustment
    age_adjustment = basic_severance * age_adjustment_factor
    
    # Total Severance Pay is the sum of basic severance and age adjustment
    total_severance = basic_severance + age_adjustment
    
    # Biweekly Severance Pay
    biweekly_severance = total_severance / 26  # Divide by 26 pay periods per year
    
    # Calculate the weeks of severance pay
    weeks_of_severance = total_severance / (annual_salary / 52) 
