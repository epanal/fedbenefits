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

def calculate_severance_pay(annual_pay, years_of_service, age_years, age_months):
    # Step 1: Calculate Weekly Pay
    weekly_pay = annual_pay / 52
    
    # Step 2: Calculate Basic Severance Pay
    if years_of_service <= 10:
        basic_severance_pay = years_of_service * weekly_pay  # 1 week per year
    else:
        basic_severance_pay = (10 * weekly_pay) + ((years_of_service - 10) * 2 * weekly_pay)  # First 10 years, 1 week per year, rest 2 weeks per year
    
    # Step 3: Calculate Age Factor
    if age_years >= 65:
        age_factor = 3.5  # Capped at 3.5 for 65+
    elif age_years >= 50:
        # For ages 50-64, the factor increases progressively from 2.0 to 3.0
        age_factor = 2 + 0.05 * (age_years - 50)
    elif age_years >= 40:
        # For ages 40-49, the factor increases progressively from 1.0 to 1.225
        age_factor = 1 + 0.025 * (age_years - 40)
    else:
        age_factor = 1.0  # Default for under 40
    
    # Step 4: Calculate Adjusted Severance Pay
    adjusted_severance_pay = basic_severance_pay * age_factor
    
    # Step 5: Total Severance Pay (No cap applied, but you can add one if needed)
    total_severance_pay = adjusted_severance_pay  # Assuming no cap

    # Step 6: Biweekly Severance Pay
    biweekly_severance_pay = total_severance_pay / 26
    
    # Step 7: Weeks of Severance Pay
    weeks_of_severance_pay = total_severance_pay / weekly_pay
    
    return total_severance_pay, basic_severance_pay, adjusted_severance_pay, biweekly_severance_pay, weeks_of_severance_pay
