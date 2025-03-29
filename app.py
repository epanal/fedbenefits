import streamlit as st
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
        *Note: These calculations are estimates based on available data and may not account for all variables. Please refer to the official OPM policies for precise guidelines and calculations.*
        </p>
    """, unsafe_allow_html=True)

# Tab-like behavior with selectbox
tab = st.selectbox("Select a Calculator", [
    "💼 Severance Pay Estimation",
    "🏖️ Annual Leave Lump Sum",
    "📅 Annual Leave Accrual",
    "⚖️ Severance vs. DRP Comparison"
])

# DRP vs Severance Comparison Function
def compare_severance_vs_drp():
    st.header("Severance Pay vs. Designated Resignation Pay (DRP) ⚖️")
    
    # Inputs for Severance Pay
    severance_estimate = st.number_input("Estimated Severance Pay ($)", min_value=0.0, step=1000.0, key="severance_estimate")

    # Inputs for DRP Calculation
    biweekly_salary = st.number_input("Biweekly Salary ($)", min_value=0.0, step=100.0, key="biweekly_salary")

    # Number of pay periods remaining until Sep 30
    pay_periods_remaining = 14  # Fixed based on our previous count

    if severance_estimate > 0 and biweekly_salary > 0:
        total_drp_earnings = biweekly_salary * pay_periods_remaining
        
        # Display Results
        st.subheader("Comparison Results")
        st.write(f"**Severance Pay Estimate:** ${severance_estimate:,.2f}")
        st.write(f"**Earnings Under DRP (Until Sep 30):** ${total_drp_earnings:,.2f}")

        # Highlight which option is better
        if total_drp_earnings > severance_estimate:
            st.success(f"✅ **Staying until September 30 (DRP) provides ${total_drp_earnings - severance_estimate:,.2f} more than taking severance.**")
        elif severance_estimate > total_drp_earnings:
            st.warning(f"⚠️ **Taking severance provides ${severance_estimate - total_drp_earnings:,.2f} more than staying until September 30.**")
        else:
            st.info("💰 **Both options provide the same total payout. Consider other benefits such as retirement service credit, health insurance, and tax implications.**")

    else:
        st.write("Please enter valid values for both fields.")
    
    # General disclaimer
    add_general_disclaimer()

# Display the selected tab's content
if tab == "🏖️ Annual Leave Lump Sum":
    annual_leave_lump_sum()

elif tab == "📅 Annual Leave Accrual":
    annual_leave_accrual()

elif tab == "💼 Severance Pay Estimation":
    severance_pay_estimation()

elif tab == "⚖️ Severance vs. DRP Comparison":
    compare_severance_vs_drp()

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