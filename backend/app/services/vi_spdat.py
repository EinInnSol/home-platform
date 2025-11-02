"""
VI-SPDAT Scoring Service
Vulnerability Index - Service Prioritization Decision Assistance Tool

This implements the standardized vulnerability assessment used in homeless services.
The scoring determines housing priority and program eligibility.

Score ranges:
- 0-3: Low acuity → Prevention/diversion services
- 4-7: Medium acuity → Rapid re-housing
- 8-17: High acuity → Permanent supportive housing
"""

from typing import Dict, Any
from app.models.client import VISPDATScore, HousingType, IntakeData
import logging

logger = logging.getLogger(__name__)


class VISPDATService:
    """
    VI-SPDAT scoring logic
    This is the deterministic rules engine - no AI, just HUD-compliant scoring
    """
    
    def calculate_score(self, intake_data: IntakeData) -> VISPDATScore:
        """
        Calculate VI-SPDAT score from intake data
        Returns score object with recommendations
        """
        
        housing_history = self._score_housing_history(intake_data)
        wellness = self._score_wellness(intake_data)
        risk = self._score_risk(intake_data)
        
        total = housing_history + wellness + risk
        
        # Determine acuity level
        if total >= 8:
            acuity = "high"
            recommended_housing = HousingType.PERMANENT_SUPPORTIVE
        elif total >= 4:
            acuity = "medium"
            recommended_housing = HousingType.RAPID_REHOUSING
        else:
            acuity = "low"
            recommended_housing = HousingType.EMERGENCY_SHELTER
        
        logger.info(
            f"VI-SPDAT calculated: total={total}, "
            f"acuity={acuity}, housing={recommended_housing}"
        )
        
        return VISPDATScore(
            total_score=total,
            housing_history_score=housing_history,
            wellness_score=wellness,
            risk_score=risk,
            acuity_level=acuity,
            recommended_housing_type=recommended_housing
        )
    
    def _score_housing_history(self, data: IntakeData) -> int:
        """
        Score housing history (0-6 points)
        - Length of homelessness
        - Frequency of homelessness
        - Housing barriers
        """
        score = 0
        
        # Currently homeless
        if data.currently_homeless:
            score += 1
        
        # Nights homeless in past 3 years
        if data.nights_homeless_past_3_years:
            if data.nights_homeless_past_3_years >= 365:
                score += 2  # Chronically homeless
            elif data.nights_homeless_past_3_years >= 90:
                score += 1
        
        # Barriers to housing
        if data.transportation_barriers:
            score += 1
        if data.childcare_barriers:
            score += 1
        if data.employment_barriers:
            score += 1
        
        return min(score, 6)  # Cap at 6
    
    def _score_wellness(self, data: IntakeData) -> int:
        """
        Score health and wellness (0-6 points)
        - Physical health
        - Substance use
        - Mental health
        - Medications
        """
        score = 0
        
        # Health conditions
        if data.chronic_health:
            score += 2  # Chronic health is higher priority
        if data.substance_use:
            score += 2
        if data.mental_health:
            score += 2
        
        return min(score, 6)  # Cap at 6
    
    def _score_risk(self, data: IntakeData) -> int:
        """
        Score risk factors (0-5 points)
        - History of trauma
        - Institutional history
        - Resources and support
        """
        score = 0
        
        # Institutional history
        if data.history_foster_care:
            score += 1
        if data.history_incarceration:
            score += 1
        if data.history_victimization:
            score += 1
        
        # Lack of resources
        if not data.has_income:
            score += 1
        if not data.has_id or not data.has_social_security_card:
            score += 1
        
        # Lack of support network
        if not data.has_family_support and not data.has_friends_support:
            score += 1
        
        return min(score, 5)  # Cap at 5
    
    def get_intervention_recommendations(
        self, 
        score: VISPDATScore
    ) -> Dict[str, Any]:
        """
        Generate intervention recommendations based on score
        This is deterministic logic that will be enhanced by AI in Phase 1
        """
        
        recommendations = {
            'housing_type': score.recommended_housing_type,
            'acuity_level': score.acuity_level,
            'immediate_actions': [],
            'support_services': [],
            'timeline': ''
        }
        
        if score.acuity_level == 'high':
            recommendations['immediate_actions'] = [
                'Contact emergency shelter for immediate placement',
                'Connect with healthcare services within 48 hours',
                'Begin permanent supportive housing application',
                'Schedule comprehensive needs assessment'
            ]
            recommendations['support_services'] = [
                'Case management',
                'Mental health services',
                'Substance abuse treatment',
                'Medical care coordination',
                'Benefits enrollment'
            ]
            recommendations['timeline'] = 'Immediate priority - contact within 24 hours'
            
        elif score.acuity_level == 'medium':
            recommendations['immediate_actions'] = [
                'Schedule rapid re-housing assessment',
                'Connect with job training resources',
                'Identify temporary housing options',
                'Begin document collection process'
            ]
            recommendations['support_services'] = [
                'Employment assistance',
                'Financial literacy training',
                'Life skills coaching',
                'Healthcare navigation'
            ]
            recommendations['timeline'] = 'High priority - contact within 72 hours'
            
        else:  # low acuity
            recommendations['immediate_actions'] = [
                'Assess for diversion opportunities',
                'Connect with prevention services',
                'Provide resource navigation',
                'Schedule follow-up check-in'
            ]
            recommendations['support_services'] = [
                'Financial assistance',
                'Mediation services',
                'Resource referrals',
                'Community support groups'
            ]
            recommendations['timeline'] = 'Standard priority - contact within 1 week'
        
        return recommendations


# Global VI-SPDAT service instance
vi_spdat_service = VISPDATService()
