"""
Property Evaluator Agent - Assesses property condition and value
"""
from models.property import Property, PropertyEvaluation
from data.mock_properties import get_market_data
from datetime import datetime


class PropertyEvaluator:
    """Evaluates individual property characteristics and value"""
    
    def __init__(self):
        self.role = "Property Evaluator"
    
    def evaluate_property(self, property: Property) -> PropertyEvaluation:
        """
        Evaluates property condition, pricing, and value potential
        
        In production, this would:
        - Integrate with property inspection APIs
        - Analyze comparable sales (comps)
        - Check building permits and renovation history
        - Assess structural integrity via ML models
        """
        
        # Calculate price per sqft
        price_per_sqft = property.price / property.sqft
        
        # Get market average for comparison
        market_data = get_market_data(property.city)
        market_avg_price_per_sqft = market_data["avg_price_per_sqft"]
        
        # Determine value rating
        price_ratio = price_per_sqft / market_avg_price_per_sqft
        if price_ratio < 0.90:
            value_rating = "Undervalued"
        elif price_ratio > 1.10:
            value_rating = "Overvalued"
        else:
            value_rating = "Fair"
        
        # Calculate condition score based on age and type
        current_year = datetime.now().year
        property_age = current_year - property.year_built
        
        base_condition = 100
        age_penalty = min(property_age * 1.5, 30)  # Max 30 point penalty
        condition_score = max(base_condition - age_penalty, 50)
        
        # Assess renovation potential
        if property_age > 20:
            renovation_potential = "High"
        elif property_age > 10:
            renovation_potential = "Medium"
        else:
            renovation_potential = "Low"
        
        # Flag potential issues based on age
        issues_flagged = []
        if property_age > 25:
            issues_flagged.append("Roof may need replacement soon")
            issues_flagged.append("HVAC system likely aging")
        if property_age > 40:
            issues_flagged.append("Foundation inspection recommended")
            issues_flagged.append("Electrical system may need upgrade")
        if property.property_type == "Condo" and property.hoa_fees > 400:
            issues_flagged.append("High HOA fees impact cash flow")
        
        evaluation = PropertyEvaluation(
            condition_score=round(condition_score, 1),
            price_per_sqft=round(price_per_sqft, 2),
            market_avg_price_per_sqft=market_avg_price_per_sqft,
            value_rating=value_rating,
            renovation_potential=renovation_potential,
            issues_flagged=issues_flagged if issues_flagged else ["No major concerns identified"]
        )
        
        return evaluation
    
    def get_value_insights(self, evaluation: PropertyEvaluation) -> dict:
        """Generates actionable insights from property evaluation"""
        
        price_variance = ((evaluation.price_per_sqft - evaluation.market_avg_price_per_sqft) 
                         / evaluation.market_avg_price_per_sqft * 100)
        
        insights = {
            "condition_rating": "Excellent" if evaluation.condition_score >= 85 else
                               "Good" if evaluation.condition_score >= 70 else
                               "Fair" if evaluation.condition_score >= 55 else "Poor",
            "pricing_vs_market": f"{price_variance:+.1f}% vs market average",
            "value_opportunity": evaluation.value_rating,
            "improvement_potential": evaluation.renovation_potential
        }
        
        return insights
