"""
Market Analyzer Agent - Evaluates location and market conditions
"""
from models.property import Property, MarketAnalysis
from data.mock_properties import get_market_data


class MarketAnalyzer:
    """Analyzes neighborhood and market conditions for investment potential"""
    
    def __init__(self):
        self.role = "Market Analyst"
    
    def analyze_market(self, property: Property) -> MarketAnalysis:
        """
        Analyzes the market conditions for a given property location
        
        In a production system, this would:
        - Call real estate APIs (Zillow, Redfin, etc.)
        - Fetch crime statistics from government databases
        - Pull school ratings from GreatSchools API
        - Analyze recent sales trends
        
        For this PoC, we use realistic mock data
        """
        
        # Get market data for the city
        market_info = get_market_data(property.city)
        
        # Calculate location score (weighted average)
        location_score = (
            market_info["neighborhood_rating"] * 0.3 +
            market_info["school_rating"] * 0.3 +
            (100 - market_info["crime_index"]) / 10 * 0.4
        ) * 10
        
        analysis = MarketAnalysis(
            location_score=round(location_score, 1),
            appreciation_rate=market_info["appreciation_rate"],
            market_heat=market_info["market_heat"],
            competition_level=market_info["competition_level"],
            neighborhood_rating=market_info["neighborhood_rating"],
            school_rating=market_info["school_rating"],
            crime_index=market_info["crime_index"]
        )
        
        return analysis
    
    def get_market_insights(self, analysis: MarketAnalysis) -> dict:
        """Generates human-readable insights from market analysis"""
        
        insights = {
            "location_quality": "Excellent" if analysis.location_score >= 80 else 
                               "Good" if analysis.location_score >= 65 else
                               "Average" if analysis.location_score >= 50 else "Poor",
            "growth_potential": "High" if analysis.appreciation_rate >= 7 else
                               "Moderate" if analysis.appreciation_rate >= 5 else "Low",
            "buyer_competition": analysis.competition_level,
            "safety_rating": "Safe" if analysis.crime_index < 35 else
                            "Moderate" if analysis.crime_index < 50 else "Concerning"
        }
        
        return insights
