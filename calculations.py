def calculate_lump_sum_payment(hourly_rate, leave_balance_hours):
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

def calculate_severance_pay(annual_salary, years_of_service, age_years, age_months):
    """
    Calculate Severance Pay using:
      - Basic Severance Pay: 1 week per year for first 10 years; 2 weeks per year thereafter.
      - Age Factor: Linear interpolation from 1.0 at age 40 to 3.5 at age 65.
        For age < 40, factor = 1.0; for age >= 65, factor = 3.5.
      - Biweekly Severance Pay is defined as 2 * weekly pay.
      - Weeks of Severance Pay = total severance / weekly pay.
    """
    # Use 52.175 as divisor to compute weekly pay (per OPM convention)
    weekly_pay = annual_salary / 52.175

    # Basic severance pay calculation
    if years_of_service < 10:
        basic_severance = years_of_service * weekly_pay
    else:
        basic_severance = (10 * weekly_pay) + ((years_of_service - 10) * 2 * weekly_pay)

    # Combine years and months into a decimal age
    age = age_years + age_months / 12.0

    # Linear interpolation for age factor between 40 and 65:
    if age < 40:
        age_factor = 1.0
    elif age < 65:
        age_factor = 1.0 + ((age - 40) / (65 - 40)) * (3.5 - 1.0)
    else:
        age_factor = 3.5

    # Adjusted severance pay using age factor
    adjusted_severance = basic_severance * age_factor

    # Total severance pay (no cap applied here)
    total_severance = adjusted_severance

    # **NEW: Apply the salary cap of 1 year's salary**
    salary_cap = annual_salary
    total_severance = min(total_severance, salary_cap)

    # Biweekly Severance Pay: Defined as 2 * weekly pay per the worksheet
    biweekly_severance = 2 * weekly_pay

    # **NEW: Cap the weeks of severance to a maximum of 52 weeks**
    weeks_of_severance = min(52, basic_severance / weekly_pay)

    # Age adjustment amount (difference between adjusted and basic)
    age_adjustment = adjusted_severance - basic_severance

    return total_severance, basic_severance, age_adjustment, biweekly_severance, weeks_of_severance
