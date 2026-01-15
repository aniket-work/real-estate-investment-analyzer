"""
Data models for Real Estate Investment Analyzer
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Property:
    """Represents a real estate property"""
    property_id: str
    address: str
    city: str
    state: str
    price: int
    bedrooms: int
    bathrooms: float
    sqft: int
    year_built: int
    property_type: str  # "Single Family", "Condo", "Multi-Family"
    estimated_rent: int
    hoa_fees: int = 0
    property_tax_annual: int = 0
    insurance_annual: int = 0


@dataclass
class MarketAnalysis:
    """Market analysis results for a property location"""
    location_score: float  # 0-100
    appreciation_rate: float  # Annual %
    market_heat: str  # "Hot", "Warm", "Cool"
    competition_level: str  # "High", "Medium", "Low"
    neighborhood_rating: float  # 0-10
    school_rating: float  # 0-10
    crime_index: float  # Lower is better, 0-100


@dataclass
class PropertyEvaluation:
    """Property condition and quality assessment"""
    condition_score: float  # 0-100
    price_per_sqft: float
    market_avg_price_per_sqft: float
    value_rating: str  # "Undervalued", "Fair", "Overvalued"
    renovation_potential: str  # "High", "Medium", "Low"
    issues_flagged: list


@dataclass
class FinancialMetrics:
    """Investment financial calculations"""
    cap_rate: float
    cash_on_cash_return: float
    monthly_cash_flow: int
    annual_cash_flow: int
    roi_5_year: float
    break_even_months: int
    total_investment: int
    net_operating_income: int


@dataclass
class InvestmentRecommendation:
    """Final investment decision"""
    property_id: str
    investment_grade: str  # "A+", "A", "B+", "B", "C", "D"
    overall_score: float  # 0-100
    confidence: float  # 0-100
    recommendation: str  # "Strong Buy", "Buy", "Hold", "Pass"
    rationale: str
    risk_level: str  # "Low", "Medium", "High"
    key_strengths: list
    key_concerns: list
