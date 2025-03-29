import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
from calculations import (
    calculate_severance_pay, 
    calculate_lump_sum_payment, 
    calculate_annual_leave_accrual
)

# Title
st.title("Fed Benefits Calculators")

# Add spacing after the title
st.markdown("<br>", unsafe_allow_html=True)

# Function to add general disclaimer
def add_general_disclaimer():
    st.markdown("""
        <p style="color:gray; font-size: 12px; text-align:center;">
        *Note: These calculations are estimates based on available data and may not account for all variables. Please refer to the official OPM and agency policies for precise guidelines and calculations.*
        </p>
    """, unsafe_allow_html=True)

# Tab-like behavior with selectbox
tab = st.selectbox("Select a Calculator", ["💼 Severance Pay Estimation","⚖️ Severance vs. DRP Comparison","🏖️ Annual Leave Lump Sum", "📅 Annual Leave Accrual"])

# Functions for calculators
def annual_leave_lump_sum():
    st.header("Annual Leave Lump Sum Calculator 📝", help="Learn more about lump sum payments: https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/")
    hourly_rate = st.number_input("Hourly Pay Rate ($)", min_value=0.0, step=0.01, key="hourly_rate")
    leave_balance_hours = st.number_input("Unused Annual Leave Balance (hours)", min_value=0.0, step=0.1, key="leave_balance")
    
    if hourly_rate > 0 and leave_balance_hours > 0:
        lump_sum_payment = calculate_lump_sum_payment(hourly_rate, leave_balance_hours)
        st.subheader("Lump Sum Payment Calculation")
        st.write(f"**Estimated Lump Sum Payment:** ${lump_sum_payment:,.2f}")
    else:
        st.write("Please enter valid values for both fields.")
    # General disclaimer
    add_general_disclaimer()
    st.markdown("[Source: OPM Annual Leave Lump Sum Payment](https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/lump-sum-payments-for-annual-leave/)")

def annual_leave_accrual():
    st.header("Annual Leave Accrual Calculator 📅")
    employee_type = st.selectbox("Select Employee Type", [
        "Full-time Employee",
        "Part-time Employee",
        "Uncommon Tours of Duty",
        "SES, Senior Level, Scientific/Professional Positions"
    ])
    years_of_service = st.number_input("Years of Federal Service", min_value=0, step=1, key="years_of_service")
    pay_periods = st.number_input("Number of Pay Periods", min_value=1, step=1, key="pay_periods")
    
    hours_in_pay_status = None
    avg_hours_per_pay_period = None

    if employee_type == "Part-time Employee":
        hours_in_pay_status = st.number_input("Enter Hours in Pay Status per Pay Period", min_value=0, step=1, key="hours_in_pay_status")
    
    if employee_type == "Uncommon Tours of Duty":
        avg_hours_per_pay_period = st.number_input("Enter Average Hours per Biweekly Pay Period", min_value=0, step=1, key="avg_hours_per_pay_period")
    
    if years_of_service > 0 and pay_periods > 0:
        try:
            accrued_leave = calculate_annual_leave_accrual(employee_type, years_of_service, pay_periods, hours_in_pay_status, avg_hours_per_pay_period)
            st.subheader("Annual Leave Accrued")
            st.write(f"**Annual Leave Accrued:** {accrued_leave:,.2f} hours")
        except ValueError as e:
            st.error(str(e))
        
        # Footnote for special case
        if employee_type == "Full-time Employee" and 3 <= years_of_service < 15:
            st.markdown("""
                <p style="color:gray; font-size: 12px;">
                *Note: For full-time employees with 3 years but less than 15 years of service, the last pay period accrual may be adjusted to 1¼ days (10 hours) instead of ¾ day (6 hours). This is an estimate and does not reflect this adjustment.*
                </p>
            """, unsafe_allow_html=True)
        
    else:
        st.write("Please enter valid values for both fields.")
    # General disclaimer
    add_general_disclaimer()
    st.markdown("[Source: OPM Annual Leave Fact Sheet](https://www.opm.gov/policy-data-oversight/pay-leave/leave-administration/fact-sheets/annual-leave/)")

def severance_pay_estimation():
    st.header("Severance Pay Estimator 💼", help="Learn more about severance pay: https://www.opm.gov/policy-data-oversight/pay-leave/pay-administration/fact-sheets/severance-pay-estimation-worksheet/")
    
    # Input fields for the calculator
    annual_salary = st.number_input("Annual Basic Pay ($)", min_value=0, step=1000, key="annual_salary")
    years_of_service = st.number_input("Full Years of Creditable Federal Service", min_value=0, step=1, key="years_of_service")
    months_of_service = st.number_input("Additional Months of Service (0 to 11)", min_value=0, max_value=11, step=1, key="months_of_service",
                                        help="Enter the remaining months of service beyond the full years. For example, if you worked for 5 years and 6 months, input 6.")

    st.write("Enter your age in full years (e.g., 43 years) and the remaining months (e.g., 5 months).")
    age_years = st.number_input("Age at Separation (Years)", min_value=0, step=1, key="age_years")
    age_months = st.number_input("Additional Months (0 to 11)", min_value=0, max_value=11, step=1, key="age_months", 
                                 help="Enter the remaining months of your age beyond the full years. For example, if you are 43 years and 5 months old, input 5.")

    if annual_salary > 0 and (years_of_service > 0 or months_of_service > 0) and age_years > 0:
        total_severance, basic_severance, age_adjustment, biweekly_severance, weeks_of_severance = calculate_severance_pay(
            annual_salary, years_of_service, months_of_service, age_years, age_months
        )
        st.subheader("Severance Pay Calculation")
        st.write(f"**Basic Severance Pay:** ${basic_severance:,.2f}")
        st.write(f"**Age Adjustment Allowance:** ${age_adjustment:,.2f}")
        st.write(f"**Adjusted Severance Pay:** ${basic_severance + age_adjustment:,.2f}")
        st.info(f"### 💰 Total Severance Pay: **${total_severance:,.2f}**")
        #st.write(f"**Biweekly Severance Pay:** ${biweekly_severance:,.2f}")
        st.write(f"**Weeks of Severance Pay:** {weeks_of_severance:.2f} weeks")
    else:
        st.write("Please enter valid values for all fields.")
    
    # General disclaimer
    add_general_disclaimer()
    st.markdown("[Source: OPM Severance Pay Estimation Worksheet](https://www.opm.gov/policy-data-oversight/pay-leave/pay-administration/fact-sheets/severance-pay-estimation-worksheet/)")

# DRP vs Severance Comparison Function
def compare_severance_vs_drp():
    st.header("Severance Pay vs. DRP ⚖️")

    # Add disclaimer
    st.markdown("""
    <p style="font-size: 14px; color: gray;">
    **Disclaimer:** This tool compares the estimated severance pay, including the period when the RIF notice is served, with the actual severance, and compares that with the length of the DRP and estimated pay during that period. 
    It does not account for a wide range of personal factors or other benefits, such as lump sum leave payouts, TSP matching, or tax implications. 
    </p>
    """, unsafe_allow_html=True)
    
    # Inputs for Severance Pay
    severance_estimate = st.number_input("Total Estimated Severance Pay ($)", min_value=0.0, step=1000.0, key="severance_estimate")
    
    # Inputs for DRP Calculation
    biweekly_salary = st.number_input("Biweekly Salary ($)", min_value=0.0, step=100.0, key="biweekly_salary")
    
    # Pay periods remaining until September 30
    today = date.today()
    sep_30 = date(today.year, 9, 30)
    
    # DRP start date input
    drp_start_date = st.date_input("Select DRP Start Date", min_value=today, max_value=sep_30, value=today)
    
    # Calculate pay periods remaining based on DRP start date
    pay_periods_remaining = max(0, (sep_30 - drp_start_date).days // 14)
    st.write(f"**Pay Periods Remaining Until Sep 30, 2025:** {pay_periods_remaining}")
    
    # New input: Pay periods between RIF notice and RIF severance
    rif_pay_periods = st.number_input("Pay Periods Between RIF Notice and Actual RIF", min_value=0, step=1, key="rif_pay_periods")
    
    if severance_estimate > 0 and biweekly_salary > 0:
        total_drp_earnings = biweekly_salary * pay_periods_remaining
        total_rif_earnings = biweekly_salary * rif_pay_periods
        adjusted_severance = severance_estimate + total_rif_earnings
        
        # Display Results
        st.subheader("Comparison Results")
        st.markdown(f"**Total Severance Pay Estimate:** ${severance_estimate:,.2f}", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'><strong>Earnings Under DRP Until Sep 30, 2025:</strong> ${total_drp_earnings:,.2f} ({pay_periods_remaining} pay periods * ${biweekly_salary:,.2f})</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 16px;'><strong>Earnings During RIF Notice Period to Actual RIF:</strong> ${total_rif_earnings:,.2f} ({rif_pay_periods} pay periods * ${biweekly_salary:,.2f})</p>", unsafe_allow_html=True)
        st.markdown(f"**Total Adjusted RIF Severance (Severance Estimate + RIF notice period earnings):** ${adjusted_severance:,.2f}", unsafe_allow_html=True)

        # Highlight which option is better
        if total_drp_earnings > adjusted_severance:
            st.info(f"✅ **Delayed Resignated Program from DRP start date until September 30, 2025 provides an estimate of ${total_drp_earnings - adjusted_severance:,.2f} more than taking severance.**")
        elif adjusted_severance > total_drp_earnings:
            st.info(f"⚠️ **Taking severance provides ${adjusted_severance - total_drp_earnings:,.2f} more than the DRP from its start date until September 30, 2025.**")
        else:
            st.warning("💰 **Both options provide the same total payout. Consider other benefits such as retirement service credit, health insurance, and tax implications.**")

    else:
        st.write("Please enter valid values for all fields.")
    
    # General disclaimer
    add_general_disclaimer()

# Display the selected tab's content
if tab == "🏖️ Annual Leave Lump Sum":
    annual_leave_lump_sum()

elif tab == "⚖️ Severance vs. DRP Comparison":
    compare_severance_vs_drp()

elif tab == "📅 Annual Leave Accrual":
    annual_leave_accrual()

elif tab == "💼 Severance Pay Estimation":
    severance_pay_estimation()

# Add spacing after the content
st.markdown("<br>", unsafe_allow_html=True)

# Add donation button
st.markdown("""
<a href="https://buymeacoffee.com/vetfed" target="_blank">
    <button style="background-color: #FF5F5F; color: white; padding: 10px 20px; font-size: 16px; border-radius: 5px; margin-bottom: 20px;">
        ☕ Buy Me a Coffee
    </button>
</a>
""", unsafe_allow_html=True)
