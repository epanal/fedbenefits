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
