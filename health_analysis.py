import numpy as np
from typing import Dict, List, Optional
import logging
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class HealthAnalyzer:
    """Advanced health analysis system with enhanced prediction capabilities"""

    def __init__(self):
        self.models = {
            'base': None,
            'species_specific': {},
            'temporal': None
        }
        self.scalers = {}
        self.feature_importances = {}
        self.load_models()

    def load_models(self):
        """Load trained models and scalers"""
        try:
            # Load base model
            self.models['base'] = joblib.load('models/health_analysis_model.pkl')
            self.scalers['base'] = joblib.load('models/scaler.pkl')

            # Load species-specific models if available
            species_models = {
                'Dog': 'models/dog_model.pkl',
                'Cat': 'models/cat_model.pkl',
                'Horse': 'models/horse_model.pkl'
            }
            
            for species, model_path in species_models.items():
                try:
                    self.models['species_specific'][species] = joblib.load(model_path)
                    self.scalers[species] = joblib.load(f'models/{species.lower()}_scaler.pkl')
                except:
                    logger.warning(f"Species-specific model for {species} not found")

        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")

    def analyze_health(self, data: Dict) -> Dict:
        """Perform comprehensive health analysis"""
        try:
            results = {
                'base_prediction': self._get_base_prediction(data),
                'species_prediction': self._get_species_prediction(data),
                'temporal_analysis': self._analyze_temporal_patterns(data),
                'risk_factors': self._analyze_risk_factors(data),
                'interaction_effects': self._analyze_interactions(data),
                'recommendations': self._generate_recommendations(data)
            }

            # Calculate confidence score
            results['confidence_score'] = self._calculate_confidence(results)
            
            return results

        except Exception as e:
            logger.error(f"Error in health analysis: {str(e)}")
            return {'error': str(e)}

    def _get_base_prediction(self, data: Dict) -> Dict:
        """Get prediction from base model"""
        try:
            features = self._prepare_features(data)
            scaled_features = self.scalers['base'].transform([features])
            prediction = self.models['base'].predict_proba([features])[0]
            
            return {
                'prediction': self.models['base'].classes_[prediction.argmax()],
                'probability': float(prediction.max()),
                'feature_importance': self._get_feature_importance(features)
            }
        except Exception as e:
            logger.error(f"Error in base prediction: {str(e)}")
            return {}

    def _get_species_prediction(self, data: Dict) -> Dict:
        """Get species-specific prediction"""
        species = data.get('Species')
        if species in self.models['species_specific']:
            try:
                features = self._prepare_features(data)
                model = self.models['species_specific'][species]
                scaled_features = self.scalers[species].transform([features])
                prediction = model.predict_proba([features])[0]
                
                return {
                    'prediction': model.classes_[prediction.argmax()],
                    'probability': float(prediction.max()),
                    'species_specific_risks': self._get_species_risks(species, data)
                }
            except Exception as e:
                logger.error(f"Error in species prediction: {str(e)}")
        
        return {}

    def _analyze_temporal_patterns(self, data: Dict) -> Dict:
        """Analyze changes over time"""
        try:
            history = data.get('medical_history', [])
            if not history:
                return {}

            trends = {
                'weight': self._analyze_weight_trend(history),
                'activity': self._analyze_activity_trend(history),
                'vital_signs': self._analyze_vital_signs_trend(history)
            }

            return {
                'trends': trends,
                'risk_progression': self._calculate_risk_progression(trends)
            }

        except Exception as e:
            logger.error(f"Error in temporal analysis: {str(e)}")
            return {}

    def _analyze_interactions(self, data: Dict) -> List[Dict]:
        """Analyze interaction effects between different health factors"""
        interactions = []
        
        try:
            # Diet and Activity Level interaction
            if 'Diet_Type' in data and 'Activity_Level' in data:
                diet_activity = self._analyze_diet_activity_interaction(
                    data['Diet_Type'],
                    data['Activity_Level'],
                    data.get('Weight'),
                    data.get('Body_Condition_Score')
                )
                if diet_activity:
                    interactions.append(diet_activity)

            # Environment and Health interaction
            if 'Living_Environment' in data and 'Vaccination_Status' in data:
                env_health = self._analyze_environment_health_interaction(
                    data['Living_Environment'],
                    data['Vaccination_Status'],
                    data.get('Stress_Level')
                )
                if env_health:
                    interactions.append(env_health)

            # Age and Medical History interaction
            if 'Age' in data:
                age_health = self._analyze_age_health_interaction(
                    data['Age'],
                    data.get('Chronic_Conditions', False),
                    data.get('Previous_Surgeries', False)
                )
                if age_health:
                    interactions.append(age_health)

            return interactions

        except Exception as e:
            logger.error(f"Error analyzing interactions: {str(e)}")
            return []

    def _calculate_confidence(self, results: Dict) -> float:
        """Calculate confidence score for predictions"""
        try:
            base_weight = 0.4
            species_weight = 0.3
            temporal_weight = 0.2
            interaction_weight = 0.1

            confidence = 0.0
            
            if 'base_prediction' in results:
                confidence += results['base_prediction'].get('probability', 0) * base_weight
            
            if 'species_prediction' in results:
                confidence += results['species_prediction'].get('probability', 0) * species_weight
            
            # Add temporal and interaction confidences
            # Implementation details...

            return min(1.0, confidence)

        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.0

    def _prepare_features(self, data: Dict) -> List:
        """Prepare feature vector for prediction"""
        try:
            features = []
            feature_order = [
                'Species', 'Age', 'Weight', 'Heart_Rate', 'Respiratory_Rate', 
                'Temperature', 'Body_Condition_Score', 'Diet_Type', 'Activity_Level',
                'Living_Environment', 'Stress_Level', 'Vaccination_Status',
                'Genetic_Predisposition', 'Recent_Behavior_Changes',
                'Chronic_Conditions', 'Previous_Surgeries'
            ]
            
            for feature in feature_order:
                value = data.get(feature)
                
                # Handle missing values
                if value is None:
                    if feature in ['Heart_Rate', 'Respiratory_Rate', 'Temperature']:
                        # Use species-specific averages for vital signs
                        species_config = self._get_species_config(data['Species'])
                        if species_config and feature.lower() in species_config['vital_signs']:
                            min_val, max_val = species_config['vital_signs'][feature.lower()]
                            value = (min_val + max_val) / 2
                        else:
                            value = 0
                    elif feature in ['Body_Condition_Score']:
                        value = 5  # Default to middle score
                    elif feature in ['Stress_Level', 'Genetic_Predisposition']:
                        value = 'Low'  # Default to low risk
                    else:
                        value = 0 if isinstance(value, (int, float)) else 'Unknown'
                
                features.append(value)
                
            return features

        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            return []

    def _get_feature_importance(self, features: List) -> Dict:
        """Get importance of each feature in prediction"""
        try:
            feature_names = [
                'Species', 'Age', 'Weight', 'Heart_Rate', 'Respiratory_Rate',
                'Temperature', 'Body_Condition_Score', 'Diet_Type', 'Activity_Level',
                'Living_Environment', 'Stress_Level', 'Vaccination_Status',
                'Genetic_Predisposition', 'Recent_Behavior_Changes',
                'Chronic_Conditions', 'Previous_Surgeries'
            ]
            
            importances = self.models['base'].feature_importances_
            importance_dict = dict(zip(feature_names, importances))
            
            # Sort by importance
            sorted_importances = {
                k: v for k, v in sorted(
                    importance_dict.items(), 
                    key=lambda item: item[1], 
                    reverse=True
                )
            }
            
            return {
                'feature_importances': sorted_importances,
                'top_factors': list(sorted_importances.keys())[:5]
            }

        except Exception as e:
            logger.error(f"Error calculating feature importance: {str(e)}")
            return {}

    def _analyze_weight_trend(self, history: List) -> Dict:
        """Analyze weight changes over time"""
        try:
            weights = [(entry['date'], entry['weight']) for entry in history]
            weights.sort(key=lambda x: x[0])
            
            if len(weights) < 2:
                return {'trend': 'Insufficient data'}
            
            # Calculate weight change
            total_change = weights[-1][1] - weights[0][1]
            change_rate = total_change / len(weights)
            
            return {
                'trend': 'Increasing' if change_rate > 0.1 else 
                        'Decreasing' if change_rate < -0.1 else 'Stable',
                'change_rate': change_rate,
                'total_change': total_change
            }

        except Exception as e:
            logger.error(f"Error analyzing weight trend: {str(e)}")
            return {'error': str(e)}

    def _analyze_activity_trend(self, history: List) -> Dict:
        """Analyze activity level changes"""
        try:
            activity_levels = [entry['activity_level'] for entry in history]
            
            if not activity_levels:
                return {'trend': 'No data'}
            
            activity_scores = {
                'Very Active': 4,
                'Active': 3,
                'Moderate': 2,
                'Sedentary': 1
            }
            
            scores = [activity_scores.get(level, 0) for level in activity_levels]
            avg_score = sum(scores) / len(scores)
            recent_score = scores[-1] if scores else 0
            
            return {
                'trend': 'Improving' if recent_score > avg_score else
                        'Declining' if recent_score < avg_score else 'Stable',
                'current_level': activity_levels[-1] if activity_levels else 'Unknown',
                'average_score': avg_score
            }

        except Exception as e:
            logger.error(f"Error analyzing activity trend: {str(e)}")
            return {'error': str(e)}

    def _analyze_vital_signs_trend(self, history: List) -> Dict:
        """Analyze trends in vital signs"""
        try:
            vital_signs = {
                'heart_rate': [],
                'respiratory_rate': [],
                'temperature': []
            }
            
            for entry in history:
                for sign in vital_signs:
                    if sign in entry:
                        vital_signs[sign].append(entry[sign])
            
            trends = {}
            for sign, values in vital_signs.items():
                if len(values) >= 2:
                    change = values[-1] - values[0]
                    trends[sign] = {
                        'trend': 'Increasing' if change > 0 else
                                'Decreasing' if change < 0 else 'Stable',
                        'change': change,
                        'current': values[-1],
                        'previous': values[0]
                    }
                else:
                    trends[sign] = {'trend': 'Insufficient data'}
            
            return trends

        except Exception as e:
            logger.error(f"Error analyzing vital signs trend: {str(e)}")
            return {'error': str(e)}

    def _calculate_risk_progression(self, trends: Dict) -> Dict:
        """Calculate risk progression based on trends"""
        try:
            risk_factors = []
            risk_level = 'Low'
            
            # Weight risk
            if 'weight' in trends:
                weight_trend = trends['weight'].get('trend')
                if weight_trend == 'Increasing':
                    risk_factors.append('Rapid weight gain')
                elif weight_trend == 'Decreasing':
                    risk_factors.append('Weight loss')
            
            # Activity risk
            if 'activity' in trends:
                if trends['activity'].get('trend') == 'Declining':
                    risk_factors.append('Decreasing activity level')
            
            # Vital signs risk
            if 'vital_signs' in trends:
                vitals = trends['vital_signs']
                for sign, data in vitals.items():
                    if data.get('trend') in ['Increasing', 'Decreasing']:
                        risk_factors.append(f'Changing {sign}')
            
            # Determine overall risk level
            if len(risk_factors) >= 3:
                risk_level = 'High'
            elif len(risk_factors) >= 1:
                risk_level = 'Moderate'
            
            return {
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendation': self._get_risk_recommendations(risk_level, risk_factors)
            }

        except Exception as e:
            logger.error(f"Error calculating risk progression: {str(e)}")
            return {'error': str(e)}

    def _get_risk_recommendations(self, risk_level: str, risk_factors: List[str]) -> Dict[str, List[str]]:
        """Generate comprehensive health recommendations based on risk assessment"""
        recommendations = {
            'immediate_actions': [],
            'lifestyle_changes': [],
            'monitoring_plan': [],
            'veterinary_care': []
        }
        
        # Immediate Actions based on risk level
        if risk_level == 'High':
            recommendations['immediate_actions'].extend([
                "Schedule immediate veterinary consultation",
                "Monitor vital signs every 2-4 hours",
                "Ensure proper hydration",
                "Restrict physical activity until veterinary assessment"
            ])
            recommendations['veterinary_care'].extend([
                "Request comprehensive blood work",
                "Consider diagnostic imaging",
                "Discuss emergency treatment options"
            ])
        elif risk_level == 'Moderate':
            recommendations['immediate_actions'].extend([
                "Schedule veterinary appointment within 48 hours",
                "Monitor vital signs twice daily",
                "Document any changes in behavior or symptoms"
            ])
        
        # Process specific risk factors
        for factor in risk_factors:
            if 'weight' in factor.lower():
                if 'gain' in factor.lower():
                    recommendations['lifestyle_changes'].extend([
                        "Implement portion control feeding",
                        "Switch to low-calorie diet options",
                        "Increase exercise frequency"
                    ])
                    recommendations['monitoring_plan'].extend([
                        "Weekly weight checks",
                        "Track food intake daily",
                        "Monitor exercise tolerance"
                    ])
                elif 'loss' in factor.lower():
                    recommendations['immediate_actions'].append("Assess food intake and appetite")
                    recommendations['lifestyle_changes'].extend([
                        "Increase meal frequency",
                        "Consider high-calorie supplements"
                    ])
                    recommendations['veterinary_care'].append("Evaluate for underlying conditions")
            
            elif 'activity' in factor.lower():
                recommendations['lifestyle_changes'].extend([
                    "Implement gradual exercise program",
                    "Add environmental enrichment",
                    "Schedule regular play sessions"
                ])
                recommendations['monitoring_plan'].extend([
                    "Track daily activity levels",
                    "Monitor joint mobility",
                    "Assess exercise tolerance"
                ])
            
            elif 'vital' in factor.lower():
                recommendations['immediate_actions'].append("Implement regular vital sign monitoring")
                recommendations['monitoring_plan'].extend([
                    "Create vital signs log",
                    "Track trends and patterns",
                    "Note environmental factors"
                ])
                recommendations['veterinary_care'].append("Share vital signs log with veterinarian")
            
            elif 'hydration' in factor.lower():
                recommendations['immediate_actions'].extend([
                    "Increase water availability",
                    "Monitor water intake",
                    "Check skin elasticity regularly"
                ])
                recommendations['lifestyle_changes'].append("Consider wet food supplementation")
            
            elif 'stress' in factor.lower():
                recommendations['lifestyle_changes'].extend([
                    "Create quiet rest areas",
                    "Maintain consistent daily routine",
                    "Reduce exposure to stressors"
                ])
                recommendations['monitoring_plan'].extend([
                    "Track stress triggers",
                    "Monitor behavioral changes",
                    "Assess sleep patterns"
                ])
            
            elif 'behavior' in factor.lower():
                recommendations['immediate_actions'].append("Document all behavioral changes")
                recommendations['monitoring_plan'].extend([
                    "Keep detailed behavior log",
                    "Note timing of changes",
                    "Track environmental factors"
                ])
                recommendations['veterinary_care'].append("Consider behavioral consultation")
        
        # Add preventive care recommendations
        recommendations['veterinary_care'].extend([
            "Schedule regular health check-ups",
            "Maintain vaccination schedule",
            "Update parasite prevention"
        ])
        
        # Add general lifestyle recommendations
        recommendations['lifestyle_changes'].extend([
            "Maintain consistent feeding schedule",
            "Ensure proper rest periods",
            "Provide mental stimulation"
        ])
        
        # Add general monitoring recommendations
        recommendations['monitoring_plan'].extend([
            "Regular weight checks",
            "Monitor food and water intake",
            "Track energy levels"
        ])
        
        # Deduplicate recommendations
        for category in recommendations:
            recommendations[category] = list(set(recommendations[category]))
        
        return recommendations

    def _get_species_risks(self, species: str, data: Dict) -> List[Dict]:
        """Get species-specific health risks"""
        # Implementation of species-specific risk analysis
        pass 