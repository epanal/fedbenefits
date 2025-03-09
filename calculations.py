def calculate_lump_sum_payment(hourly_rate, leave_balance_hours):
    """Calculate lump sum payment for unused annual leave."""
    return hourly_rate * leave_balance_hours  # Leave balance is in hours, no conversion needed

def calculate_annual_leave_accrual(years_of_service, pay_periods):
    """Calculate annual leave accrual based on years of service and pay periods."""
    # Determine the leave accrual rate based on years of service
    if years_of_service < 3:
        leave_per_pay_period = 4  # 4 hours per pay period for less than 3 years of service
    elif 3 <= years_of_service <= 15:
        leave_per_pay_period = 6  # 6 hours per pay period for 3-15 years of service
    else:
        leave_per_pay_period = 8  # 8 hours per pay period for more than 15 years of service
    
    # Calculate the total accrued leave for the entered number of pay periods
    total_accrued_leave = leave_per_pay_period * pay_periods
    
    return total_accrued_leave
