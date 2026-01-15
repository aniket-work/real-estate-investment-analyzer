"""
Financial Calculator Agent - Computes investment metrics
"""
from models.property import Property, FinancialMetrics


class FinancialCalculator:
    """Calculates investment returns and financial metrics"""
    
    def __init__(self):
        self.role = "Financial Analyst"
        # Standard assumptions for calculations
        self.down_payment_pct = 0.20  # 20% down
        self.interest_rate = 0.07  # 7% mortgage rate
        self.loan_term_years = 30
        self.vacancy_rate = 0.05  # 5% vacancy
        self.maintenance_rate = 0.10  # 10% of rent for maintenance
        self.property_mgmt_rate = 0.08  # 8% of rent for property management
    
    def calculate_metrics(self, property: Property, appreciation_rate: float) -> FinancialMetrics:
        """
        Calculates comprehensive financial metrics for investment analysis
        
        Formulas used:
        - Cap Rate = (NOI / Property Price) × 100
        - Cash-on-Cash = (Annual Cash Flow / Total Cash Invested) × 100
        - ROI = ((Future Value - Initial Investment) / Initial Investment) × 100
        """
        
        # Calculate down payment and loan amount
        down_payment = property.price * self.down_payment_pct
        loan_amount = property.price - down_payment
        
        # Calculate monthly mortgage payment (P&I)
        monthly_rate = self.interest_rate / 12
        num_payments = self.loan_term_years * 12
        monthly_mortgage = (loan_amount * monthly_rate * (1 + monthly_rate)**num_payments) / \
                          ((1 + monthly_rate)**num_payments - 1)
        
        # Calculate monthly operating expenses
        monthly_property_tax = property.property_tax_annual / 12
        monthly_insurance = property.insurance_annual / 12
        monthly_hoa = property.hoa_fees
        
        # Calculate effective monthly rent (accounting for vacancy)
        effective_monthly_rent = property.estimated_rent * (1 - self.vacancy_rate)
        
        # Calculate monthly expenses
        monthly_maintenance = property.estimated_rent * self.maintenance_rate
        monthly_mgmt = property.estimated_rent * self.property_mgmt_rate
        
        total_monthly_expenses = (monthly_mortgage + monthly_property_tax + 
                                 monthly_insurance + monthly_hoa + 
                                 monthly_maintenance + monthly_mgmt)
        
        # Calculate monthly and annual cash flow
        monthly_cash_flow = effective_monthly_rent - total_monthly_expenses
        annual_cash_flow = monthly_cash_flow * 12
        
        # Calculate Net Operating Income (NOI) - excludes mortgage
        annual_noi = (effective_monthly_rent * 12) - \
                    ((monthly_property_tax + monthly_insurance + monthly_hoa + 
                      monthly_maintenance + monthly_mgmt) * 12)
        
        # Calculate Cap Rate
        cap_rate = (annual_noi / property.price) * 100
        
        # Calculate total initial investment (down payment + closing costs)
        closing_costs = property.price * 0.03  # Assume 3% closing costs
        total_investment = down_payment + closing_costs
        
        # Calculate Cash-on-Cash Return
        cash_on_cash = (annual_cash_flow / total_investment) * 100
        
        # Calculate 5-year ROI (including appreciation)
        future_value = property.price * ((1 + appreciation_rate/100) ** 5)
        equity_buildup = self._calculate_equity_buildup(loan_amount, monthly_rate, num_payments, 60)
        total_cash_flow_5yr = annual_cash_flow * 5
        total_gain = (future_value - property.price) + equity_buildup + total_cash_flow_5yr
        roi_5_year = (total_gain / total_investment) * 100
        
        # Calculate break-even point
        if monthly_cash_flow > 0:
            break_even_months = int(total_investment / monthly_cash_flow)
        else:
            break_even_months = 999  # Never breaks even
        
        metrics = FinancialMetrics(
            cap_rate=round(cap_rate, 2),
            cash_on_cash_return=round(cash_on_cash, 2),
            monthly_cash_flow=int(monthly_cash_flow),
            annual_cash_flow=int(annual_cash_flow),
            roi_5_year=round(roi_5_year, 2),
            break_even_months=break_even_months,
            total_investment=int(total_investment),
            net_operating_income=int(annual_noi)
        )
        
        return metrics
    
    def _calculate_equity_buildup(self, loan_amount: float, monthly_rate: float, 
                                  total_payments: int, months_paid: int) -> float:
        """Calculates equity built up through principal payments"""
        
        monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate)**total_payments) / \
                         ((1 + monthly_rate)**total_payments - 1)
        
        balance = loan_amount
        total_principal_paid = 0
        
        for month in range(months_paid):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            total_principal_paid += principal_payment
            balance -= principal_payment
        
        return total_principal_paid
    
    def get_financial_insights(self, metrics: FinancialMetrics) -> dict:
        """Generates investment quality insights from financial metrics"""
        
        insights = {
            "cash_flow_quality": "Excellent" if metrics.monthly_cash_flow > 500 else
                                "Good" if metrics.monthly_cash_flow > 200 else
                                "Break-even" if metrics.monthly_cash_flow > 0 else "Negative",
            "cap_rate_rating": "Strong" if metrics.cap_rate > 8 else
                              "Good" if metrics.cap_rate > 6 else
                              "Average" if metrics.cap_rate > 4 else "Weak",
            "roi_outlook": "Excellent" if metrics.roi_5_year > 80 else
                          "Good" if metrics.roi_5_year > 50 else
                          "Moderate" if metrics.roi_5_year > 30 else "Poor",
            "payback_timeline": f"{metrics.break_even_months} months" if metrics.break_even_months < 999 
                               else "Does not break even"
        }
        
        return insights
