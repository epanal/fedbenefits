import streamlit as st
from calculations import calculate_lump_sum_payment, calculate_annual_leave_accrual

st.title("Federal Benefits Calculator")

# Create button-like tabs for Lump Sum and Annual Leave Accrual
tab1 = st.button("🏖️ Annual Leave Lump Sum")
tab2 = st.button("📅 Annual Leave Accrual")

# Debugging: Check which tab was clicked
st.write(f"Tab1 clicked: {tab1}, Tab2 clicked: {tab2}")

# Conditional content based on button click
if tab1:
    st.header("Annual Leave Lump Sum Calculator 📝", help="Learn more about lump sum payments: https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/")
    
    hourly_rate = st.number_input("Hourly Pay Rate ($)", min_value=0.0, step=0.01, key="hourly_rate")
    leave_balance_hours = st.number_input("Unused Annual Leave Balance (hours)", min_value=0.0, step=0.1, key="leave_balance")
    
    # Debugging: Print the inputs
    st.write(f"Hourly rate: {hourly_rate}, Leave balance hours: {leave_balance_hours}")
    
    if hourly_rate > 0 and leave_balance_hours > 0:
        lump_sum_payment = calculate_lump_sum_payment(hourly_rate, leave_balance_hours)
        st.subheader("Lump Sum Payment Calculation")
        st.write(f"**Estimated Lump Sum Payment:** ${lump_sum_payment:,.2f}")
    else:
        st.write("Please enter valid values for both fields.")
    
    st.markdown("[Source: OPM Lump Sum Payments for Annual Leave](https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/)")

elif tab2:
    st.header("Annual Leave Accrual Calculator 📅")
    
    years_of_service = st.number_input("Years of Federal Service", min_value=0.0, step=0.1, key="years_of_service")
    pay_periods = st.number_input("Number of Pay Periods", min_value=1, step=1, key="pay_periods")
    
    # Debugging: Print the inputs
    st.write(f"Years of service: {years_of_service}, Pay periods: {pay_periods}")
    
    if years_of_service > 0 and pay_periods > 0:
        accrued_leave = calculate_annual_leave_accrual(years_of_service, pay_periods)
        st.subheader("Annual Leave Accrued")
        st.write(f"**Annual Leave Accrued:** {accrued_leave:,.2f} hours")
    else:
        st.write("Please enter valid values for both fields.")
