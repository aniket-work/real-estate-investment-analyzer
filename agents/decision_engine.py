"""
Decision Engine - Synthesizes all agent outputs into investment recommendation
"""
from models.property import (Property, MarketAnalysis, PropertyEvaluation, 
                             FinancialMetrics, InvestmentRecommendation)


class DecisionEngine:
    """Makes final investment decisions based on all agent analyses"""
    
    def __init__(self):
        self.role = "Investment Decision Engine"
        # Weighting for overall score calculation
        self.weights = {
            "financial": 0.40,  # 40% weight on financial metrics
            "market": 0.30,     # 30% weight on market conditions
            "property": 0.30    # 30% weight on property quality
        }
    
    def make_decision(self, property: Property, market_analysis: MarketAnalysis,
                     property_eval: PropertyEvaluation, 
                     financial_metrics: FinancialMetrics) -> InvestmentRecommendation:
        """
        Synthesizes all analyses into a final investment recommendation
        
        Scoring methodology:
        - Financial Score: Based on cap rate, cash flow, and ROI
        - Market Score: Based on location quality and appreciation potential
        - Property Score: Based on condition and value rating
        """
        
        # Calculate individual component scores (0-100)
        financial_score = self._calculate_financial_score(financial_metrics)
        market_score = market_analysis.location_score
        property_score = property_eval.condition_score
        
        # Calculate weighted overall score
        overall_score = (
            financial_score * self.weights["financial"] +
            market_score * self.weights["market"] +
            property_score * self.weights["property"]
        )
        
        # Determine investment grade
        investment_grade = self._assign_grade(overall_score)
        
        # Determine recommendation
        recommendation = self._determine_recommendation(overall_score, financial_metrics)
        
        # Calculate confidence based on score consistency
        confidence = self._calculate_confidence(financial_score, market_score, property_score)
        
        # Determine risk level
        risk_level = self._assess_risk(market_analysis, property_eval, financial_metrics)
        
        # Identify key strengths and concerns
        strengths = self._identify_strengths(market_analysis, property_eval, financial_metrics)
        concerns = self._identify_concerns(market_analysis, property_eval, financial_metrics)
        
        # Generate rationale
        rationale = self._generate_rationale(overall_score, investment_grade, 
                                             financial_metrics, market_analysis)
        
        decision = InvestmentRecommendation(
            property_id=property.property_id,
            investment_grade=investment_grade,
            overall_score=round(overall_score, 1),
            confidence=round(confidence, 1),
            recommendation=recommendation,
            rationale=rationale,
            risk_level=risk_level,
            key_strengths=strengths,
            key_concerns=concerns
        )
        
        return decision
    
    def _calculate_financial_score(self, metrics: FinancialMetrics) -> float:
        """Calculates financial component score (0-100)"""
        
        # Cap rate scoring (0-40 points)
        cap_rate_score = min(metrics.cap_rate * 4, 40)
        
        # Cash flow scoring (0-30 points)
        if metrics.monthly_cash_flow >= 500:
            cash_flow_score = 30
        elif metrics.monthly_cash_flow >= 300:
            cash_flow_score = 25
        elif metrics.monthly_cash_flow >= 100:
            cash_flow_score = 20
        elif metrics.monthly_cash_flow > 0:
            cash_flow_score = 15
        else:
            cash_flow_score = 0
        
        # ROI scoring (0-30 points)
        roi_score = min(metrics.roi_5_year / 3, 30)
        
        total_score = cap_rate_score + cash_flow_score + roi_score
        return min(total_score, 100)
    
    def _assign_grade(self, score: float) -> str:
        """Assigns letter grade based on overall score"""
        
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        else:
            return "D"
    
    def _determine_recommendation(self, score: float, metrics: FinancialMetrics) -> str:
        """Determines buy/hold/pass recommendation"""
        
        # Must have positive cash flow for any buy recommendation
        if metrics.monthly_cash_flow <= 0:
            return "Pass"
        
        if score >= 80:
            return "Strong Buy"
        elif score >= 70:
            return "Buy"
        elif score >= 60:
            return "Consider"
        else:
            return "Pass"
    
    def _calculate_confidence(self, financial_score: float, 
                             market_score: float, property_score: float) -> float:
        """Calculates confidence based on score consistency"""
        
        scores = [financial_score, market_score, property_score]
        avg_score = sum(scores) / len(scores)
        
        # Calculate variance
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Lower variance = higher confidence
        # Max std_dev of ~30 = 0% confidence, 0 std_dev = 100% confidence
        confidence = max(100 - (std_dev * 3), 50)
        
        return confidence
    
    def _assess_risk(self, market: MarketAnalysis, prop_eval: PropertyEvaluation,
                    metrics: FinancialMetrics) -> str:
        """Assesses overall investment risk level"""
        
        risk_factors = 0
        
        # Market risk factors
        if market.market_heat == "Cool":
            risk_factors += 1
        if market.crime_index > 50:
            risk_factors += 1
        if market.appreciation_rate < 4:
            risk_factors += 1
        
        # Property risk factors
        if prop_eval.condition_score < 60:
            risk_factors += 1
        if len(prop_eval.issues_flagged) > 2:
            risk_factors += 1
        
        # Financial risk factors
        if metrics.monthly_cash_flow < 200:
            risk_factors += 1
        if metrics.cap_rate < 5:
            risk_factors += 1
        
        if risk_factors >= 4:
            return "High"
        elif risk_factors >= 2:
            return "Medium"
        else:
            return "Low"
    
    def _identify_strengths(self, market: MarketAnalysis, 
                           prop_eval: PropertyEvaluation,
                           metrics: FinancialMetrics) -> list:
        """Identifies key investment strengths"""
        
        strengths = []
        
        if metrics.cap_rate > 8:
            strengths.append(f"Excellent cap rate ({metrics.cap_rate}%)")
        if metrics.monthly_cash_flow > 500:
            strengths.append(f"Strong cash flow (${metrics.monthly_cash_flow}/month)")
        if market.appreciation_rate > 7:
            strengths.append(f"High appreciation market ({market.appreciation_rate}%/year)")
        if market.location_score > 80:
            strengths.append(f"Premium location (score: {market.location_score})")
        if prop_eval.value_rating == "Undervalued":
            strengths.append("Property priced below market")
        if market.school_rating >= 8:
            strengths.append(f"Excellent schools (rating: {market.school_rating})")
        
        return strengths if strengths else ["Meets basic investment criteria"]
    
    def _identify_concerns(self, market: MarketAnalysis,
                          prop_eval: PropertyEvaluation,
                          metrics: FinancialMetrics) -> list:
        """Identifies key investment concerns"""
        
        concerns = []
        
        if metrics.monthly_cash_flow < 100:
            concerns.append("Minimal cash flow cushion")
        if metrics.cap_rate < 5:
            concerns.append(f"Low cap rate ({metrics.cap_rate}%)")
        if market.competition_level == "High":
            concerns.append("High buyer competition in market")
        if prop_eval.condition_score < 70:
            concerns.append("Property may need significant repairs")
        if prop_eval.value_rating == "Overvalued":
            concerns.append("Property priced above market average")
        if market.crime_index > 45:
            concerns.append("Above-average crime in area")
        if len(prop_eval.issues_flagged) > 1 and "No major concerns" not in prop_eval.issues_flagged[0]:
            concerns.append(f"{len(prop_eval.issues_flagged)} potential property issues")
        
        return concerns if concerns else ["No significant concerns identified"]
    
    def _generate_rationale(self, score: float, grade: str,
                           metrics: FinancialMetrics,
                           market: MarketAnalysis) -> str:
        """Generates human-readable investment rationale"""
        
        if score >= 80:
            return (f"This property scores {grade} with strong fundamentals across all metrics. "
                   f"The {metrics.cap_rate}% cap rate combined with {market.market_heat.lower()} "
                   f"market conditions creates an excellent investment opportunity.")
        elif score >= 70:
            return (f"This property earns a {grade} rating with solid investment potential. "
                   f"Financial metrics are sound with {metrics.cap_rate}% cap rate, though "
                   f"some areas could be stronger.")
        elif score >= 60:
            return (f"This property receives a {grade} grade. While it meets basic criteria, "
                   f"the investment case is moderate with a {metrics.cap_rate}% cap rate.")
        else:
            return (f"This property scores {grade} and presents challenges. "
                   f"The {metrics.cap_rate}% cap rate and other factors suggest caution.")
