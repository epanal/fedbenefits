def calculate_lump_sum_payment(hourly_rate, leave_balance_hours):
    """Calculate lump sum payment for unused annual leave."""
    return hourly_rate * leave_balance_hours  # Leave balance is in hours, no conversion needed

def calculate_annual_leave_accrual(years_of_service):
    """Calculate annual leave accrual based on years of service."""
    if years_of_service < 3:
        leave_per_pay_period = 4  # 4 hours per pay period for less than 3 years of service
    elif 3 <= years_of_service <= 15:
        leave_per_pay_period = 6  # 6 hours per pay period for 3-15 years of service
    else:
        leave_per_pay_period = 8  # 8 hours per pay period for more than 15 years of service
    
    # Federal employees accrue leave every two weeks (26 pay periods a year)
    total_accrued_leave = leave_per_pay_period * 26  # 26 pay periods in a year
    
    return total_accrued_leave
