import streamlit as st
from calculations import calculate_lump_sum_payment, calculate_annual_leave_accrual

st.title("Federal Benefits Calculator")

# Add your donation button using Buy Me a Coffee link
st.markdown("""
<a href="https://buymeacoffee.com/vetfed" target="_blank">
    <button style="background-color: #FF5F5F; color: white; padding: 10px 20px; font-size: 16px; border-radius: 5px;">Support Me on Buy Me a Coffee</button>
</a>
""", unsafe_allow_html=True)

# Create a radio button to switch between the tabs (Annual Leave Lump Sum, Annual Leave Accrual)
option = st.radio("Select a Calculator", ["🏖️ Annual Leave Lump Sum", "📅 Annual Leave Accrual"])

# Conditional content based on the radio button selection
if option == "🏖️ Annual Leave Lump Sum":
    st.header("Annual Leave Lump Sum Calculator 📝", help="Learn more about lump sum payments: https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/")
    
    hourly_rate = st.number_input("Hourly Pay Rate ($)", min_value=0.0, step=0.01, key="hourly_rate")
    leave_balance_hours = st.number_input("Unused Annual Leave Balance (hours)", min_value=0.0, step=0.1, key="leave_balance")
    
    if hourly_rate > 0 and leave_balance_hours > 0:
        lump_sum_payment = calculate_lump_sum_payment(hourly_rate, leave_balance_hours)
        st.subheader("Lump Sum Payment Calculation")
        st.write(f"**Estimated Lump Sum Payment:** ${lump_sum_payment:,.2f}")
    else:
        st.write("Please enter valid values for both fields.")
    
    st.markdown("[Source: OPM Lump Sum Payments for Annual Leave](https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/)")

elif option == "📅 Annual Leave Accrual":
    st.header("Annual Leave Accrual Calculator 📅")
    
    # User selects employee type
    employee_type = st.selectbox("Select Employee Type", [
        "Full-time Employee",
        "Part-time Employee",
        "Uncommon Tours of Duty",
        "SES, Senior Level, Scientific/Professional Positions"
    ])
    
    # Input for years of service and pay periods
    years_of_service = st.number_input("Years of Federal Service", min_value=0, step=1, key="years_of_service")
    pay_periods = st.number_input("Number of Pay Periods", min_value=1, step=1, key="pay_periods")
    
    if years_of_service > 0 and pay_periods > 0:
        accrued_leave = calculate_annual_leave_accrual(employee_type, years_of_service, pay_periods)
        st.subheader("Annual Leave Accrued")
        st.write(f"**Annual Leave Accrued:** {accrued_leave:,.2f} hours")
    else:
        st.write("Please enter valid values for both fields.")
    
    # Add reference link for Annual Leave Accrual
    st.markdown("[Source: OPM Annual Leave Information](https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/annual-leave/)")
