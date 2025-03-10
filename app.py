import streamlit as st
from calculations import (
    calculate_severance_pay, 
    calculate_lump_sum_payment, 
    calculate_annual_leave_accrual
)

# Title
st.title("Federal Benefits Calculators")

# Add donation button
st.markdown("""
<a href="https://buymeacoffee.com/vetfed" target="_blank">
    <button style="background-color: #FF5F5F; color: white; padding: 10px 20px; font-size: 16px; border-radius: 5px; margin-bottom: 20px;">Support Me on Buy Me a Coffee</button>
</a>
""", unsafe_allow_html=True)

# Add spacing after the title
st.markdown("<br>", unsafe_allow_html=True)

# Radio button selection
option = st.radio("Select a Calculator", ["🏖️ Annual Leave Lump Sum", "📅 Annual Leave Accrual", "💼 Severance Pay Estimation"])

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

elif option == "📅 Annual Leave Accrual":
    st.header("Annual Leave Accrual Calculator 📅")

    employee_type = st.selectbox("Select Employee Type", [
        "Full-time Employee",
        "Part-time Employee",
        "Uncommon Tours of Duty",
        "SES, Senior Level, Scientific/Professional Positions"
    ])
    
    years_of_service = st.number_input("Years of Federal Service", min_value=0, step=1, key="years_of_service")
    pay_periods = st.number_input("Number of Pay Periods", min_value=1, step=1, key="pay_periods")

    if years_of_service > 0 and pay_periods > 0:
        accrued_leave = calculate_annual_leave_accrual(employee_type, years_of_service, pay_periods)
        st.subheader("Annual Leave Accrued")
        st.write(f"**Annual Leave Accrued:** {accrued_leave:,.2f} hours")
    else:
        st.write("Please enter valid values for both fields.")

elif option == "💼 Severance Pay Estimation":
    st.header("Severance Pay Estimation Calculator 💼", help="Learn more about severance pay: https://www.opm.gov/policy-data-oversight/pay-leave/pay-administration/fact-sheets/severance-pay-estimation-worksheet/")

    # Input fields for the calculator
    annual_salary = st.number_input("Annual Basic Pay ($)", min_value=0.0, step=1000.0, key="annual_salary")
    years_of_service = st.number_input("Years of Creditable Federal Service", min_value=0, step=1, key="years_of_service")
    
    st.write("Enter your age in full years (e.g., 43 years) and the remaining months (e.g., 5 months).")
    age_years = st.number_input("Age at Separation (Years)", min_value=0, step=1, key="age_years")
    
    # More clear prompt for 'Additional Months'
    age_months = st.number_input("Additional Months (0 to 11)", min_value=0, max_value=11, step=1, key="age_months", 
                                 help="Enter the remaining months of your age beyond the full years. For example, if you are 43 years and 5 months old, input 5.")

    if annual_salary > 0 and years_of_service > 0 and age_years > 0:
        total_severance, basic_severance, age_adjustment, biweekly_severance, weeks_of_severance = calculate_severance_pay(
            annual_salary, years_of_service, age_years, age_months
        )

        st.subheader("Severance Pay Calculation")
        st.write(f"**Basic Severance Pay:** ${basic_severance:,.2f}")
        st.write(f"**Adjusted Severance Pay:** ${basic_severance + age_adjustment:,.2f}")
        st.write(f"**Total Severance Pay:** ${total_severance:,.2f}")
        st.write(f"**Biweekly Severance Pay:** ${biweekly_severance:,.2f}")
        st.write(f"**Weeks of Severance Pay:** {weeks_of_severance:.2f} weeks")

    else:
        st.write("Please enter valid values for all fields.")

    st.markdown("[Source: OPM Severance Pay Estimation Worksheet](https://www.opm.gov/policy-data-oversight/pay-leave/pay-administration/fact-sheets/severance-pay-estimation-worksheet/)")

