import streamlit as st
from calculations import calculate_lump_sum_payment, calculate_pension

st.title("Federal Benefits Calculator")

# Create custom "button-like" tabs with icons
tab1 = st.button("🏖️ Annual Leave Lump Sum")
tab2 = st.button("💰 Pension Estimator")

# Conditional content based on which "button" is clicked
if tab1:
    st.header("Annual Leave Lump Sum Calculator 📝", help="Learn more about lump sum payments: https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/")
    hourly_rate = st.number_input("Hourly Pay Rate ($)", min_value=0.0, step=0.01, key="hourly_rate")
    leave_balance_hours = st.number_input("Unused Annual Leave Balance (hours)", min_value=0.0, step=0.1, key="leave_balance")
    
    if hourly_rate > 0 and leave_balance_hours > 0:
        lump_sum_payment = calculate_lump_sum_payment(hourly_rate, leave_balance_hours)
        st.subheader("Lump Sum Payment Calculation")
        st.write(f"**Estimated Lump Sum Payment:** ${lump_sum_payment:,.2f}")
    
    # Adding the source link at the bottom of the section
    st.markdown("[Source: OPM Lump Sum Payments for Annual Leave](https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/)")

elif tab2:
    st.header("Pension Estimator")
    high_3_salary = st.number_input("High-3 Average Salary ($)", min_value=0.0, step=1000.0, key="high_3_salary")
    years_of_service = st.number_input("Years of Federal Service", min_value=0.0, step=0.1, key="years_of_service")
    
    if high_3_salary > 0 and years_of_service > 0:
        pension = calculate_pension(high_3_salary, years_of_service)
        st.subheader("Pension Calculation")
        st.write(f"**Estimated Annual Pension:** ${pension:,.2f}")
