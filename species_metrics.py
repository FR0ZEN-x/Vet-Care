import logging
from typing import Dict, List, Optional
from species_config import SPECIES_CONFIG, get_species_category, get_species_config

logger = logging.getLogger(__name__)

class SpeciesMetricsAnalyzer:
    """Handles species-specific health metrics analysis"""

    def __init__(self):
        self.species_config = SPECIES_CONFIG
        self.vital_signs_importance = {
            'Mammals': {
                'heart_rate': 0.35,
                'respiratory_rate': 0.35,
                'temperature': 0.30
            },
            'Birds': {
                'heart_rate': 0.40,
                'respiratory_rate': 0.35,
                'temperature': 0.25
            },
            'Reptiles': {
                'heart_rate': 0.25,
                'respiratory_rate': 0.25,
                'temperature': 0.50
            },
            'Aquatic': {
                'heart_rate': 0.30,
                'respiratory_rate': 0.40,
                'temperature': 0.30
            }
        }

    def analyze_metrics(self, data: Dict) -> Dict:
        """Analyze health metrics based on species"""
        try:
            species = data.get('Species')
            category = get_species_category(species)
            species_config = get_species_config(species)

            if not species_config:
                raise ValueError(f"No configuration found for species: {species}")

            analysis = {
                'vital_signs': self._analyze_vital_signs(data, species_config, category),
                'weight_analysis': self._analyze_weight(data, species_config),
                'age_analysis': self._analyze_age(data, species_config),
                'environmental_analysis': self._analyze_environment(data, category),
                'diet_analysis': self._analyze_diet(data, species),
                'activity_analysis': self._analyze_activity(data, species)
            }

            # Calculate overall health score
            analysis['health_score'] = self._calculate_health_score(analysis, category)
            analysis['risk_level'] = self._determine_risk_level(analysis)

            return analysis

        except Exception as e:
            logger.error(f"Error in species metrics analysis: {str(e)}")
            return {'error': str(e)}

    def _analyze_vital_signs(self, data: Dict, species_config: Dict, category: str) -> Dict:
        """Analyze vital signs based on species-specific ranges"""
        vital_signs = {}
        weights = self.vital_signs_importance.get(category, {})

        for sign, (min_val, max_val) in species_config['vital_signs'].items():
            if sign in data and data[sign]:
                value = float(data[sign])
                deviation = 0

                if value < min_val:
                    deviation = (min_val - value) / min_val
                elif value > max_val:
                    deviation = (value - max_val) / max_val

                vital_signs[sign] = {
                    'value': value,
                    'range': (min_val, max_val),
                    'status': 'Normal' if deviation == 0 else 'Abnormal',
                    'deviation': deviation,
                    'weight': weights.get(sign, 0.33),
                    'severity': self._calculate_severity(deviation)
                }

        return vital_signs

    def _analyze_weight(self, data: Dict, species_config: Dict) -> Dict:
        """Analyze weight based on species-specific ranges"""
        weight = float(data.get('Weight', 0))
        weight_range = species_config.get('weight_range', (0, 0))

        if weight < weight_range[0]:
            status = 'Underweight'
            severity = 'High'
            deviation = (weight_range[0] - weight) / weight_range[0]
        elif weight > weight_range[1]:
            status = 'Overweight'
            severity = 'High'
            deviation = (weight - weight_range[1]) / weight_range[1]
        else:
            status = 'Normal'
            severity = 'Low'
            deviation = 0

        return {
            'value': weight,
            'range': weight_range,
            'status': status,
            'severity': severity,
            'deviation': deviation
        }

    def _analyze_age(self, data: Dict, species_config: Dict) -> Dict:
        """Analyze age relative to species lifespan"""
        age = float(data.get('Age', 0))
        lifespan = species_config.get('lifespan', 0)

        if lifespan == 0:
            return {'status': 'Unknown'}

        age_ratio = age / lifespan
        if age_ratio < 0.25:
            return {
                'status': 'Young',
                'life_stage': 'Juvenile',
                'risk_level': 'Low',
                'concerns': ['Growth monitoring', 'Vaccination schedule']
            }
        elif age_ratio < 0.75:
            return {
                'status': 'Adult',
                'life_stage': 'Mature',
                'risk_level': 'Moderate',
                'concerns': ['Regular health maintenance']
            }
        else:
            return {
                'status': 'Senior',
                'life_stage': 'Geriatric',
                'risk_level': 'High',
                'concerns': ['Age-related conditions', 'Mobility issues']
            }

    def _analyze_environment(self, data: Dict, category: str) -> Dict:
        """Analyze environmental factors based on species category"""
        environment = data.get('Living_Environment')
        
        env_risks = {
            'Mammals': {
                'Indoor Only': {'risk': 'Low', 'concerns': ['Limited exercise']},
                'Outdoor Only': {'risk': 'High', 'concerns': ['Weather exposure', 'Parasites']},
                'Mixed': {'risk': 'Moderate', 'concerns': ['Temperature changes']}
            },
            'Birds': {
                'Indoor Only': {'risk': 'Low', 'concerns': ['Air quality']},
                'Outdoor Only': {'risk': 'High', 'concerns': ['Predators']},
                'Mixed': {'risk': 'Moderate', 'concerns': ['Temperature changes']}
            },
            'Reptiles': {
                'Indoor Only': {'risk': 'Low', 'concerns': ['UV exposure']},
                'Controlled Environment': {'risk': 'Low', 'concerns': ['Temperature regulation']}
            },
            'Aquatic': {
                'Controlled Environment': {'risk': 'Low', 'concerns': ['Water quality']},
                'Mixed': {'risk': 'High', 'concerns': ['Temperature fluctuation']}
            }
        }

        category_risks = env_risks.get(category, {})
        env_assessment = category_risks.get(environment, {'risk': 'Unknown', 'concerns': []})
        
        return {
            'environment': environment,
            'risk_level': env_assessment['risk'],
            'concerns': env_assessment['concerns']
        }

    def _analyze_diet(self, data: Dict, species: str) -> Dict:
        """Analyze diet based on species requirements"""
        diet_type = data.get('Diet_Type')
        
        return {
            'diet_type': diet_type,
            'appropriateness': self._evaluate_diet_appropriateness(diet_type, species),
            'recommendations': self._get_diet_recommendations(species)
        }

    def _analyze_activity(self, data: Dict, species: str) -> Dict:
        """Analyze activity level based on species needs"""
        activity_level = data.get('Activity_Level')
        
        return {
            'activity_level': activity_level,
            'appropriateness': self._evaluate_activity_appropriateness(activity_level, species),
            'recommendations': self._get_activity_recommendations(species)
        }

    def _calculate_severity(self, deviation: float) -> str:
        """Calculate severity level based on deviation"""
        if deviation == 0:
            return 'Normal'
        elif deviation < 0.1:
            return 'Mild'
        elif deviation < 0.2:
            return 'Moderate'
        else:
            return 'Severe'

    def _calculate_health_score(self, analysis: Dict, category: str) -> float:
        """Calculate overall health score based on species-specific metrics"""
        try:
            base_score = 100
            deductions = 0
            
            # Vital signs deductions
            vital_signs = analysis.get('vital_signs', {})
            for sign, data in vital_signs.items():
                if data['status'] == 'Abnormal':
                    deduction = data['deviation'] * 100 * data['weight']
                    deductions += deduction
            
            # Weight deductions
            weight_analysis = analysis.get('weight_analysis', {})
            if weight_analysis.get('status') != 'Normal':
                deductions += 15 if weight_analysis.get('severity') == 'High' else 8
            
            # Age-related deductions
            age_analysis = analysis.get('age_analysis', {})
            if age_analysis.get('risk_level') == 'High':
                deductions += 10
            
            # Environmental deductions
            env_analysis = analysis.get('environmental_analysis', {})
            if env_analysis.get('risk_level') == 'High':
                deductions += 15
            elif env_analysis.get('risk_level') == 'Moderate':
                deductions += 8
            
            return max(0, min(100, base_score - deductions))
            
        except Exception as e:
            logger.error(f"Error calculating health score: {str(e)}")
            return 0

    def _determine_risk_level(self, analysis: Dict) -> str:
        """Determine overall risk level based on analysis"""
        health_score = analysis.get('health_score', 0)
        
        if health_score >= 90:
            return 'Low'
        elif health_score >= 75:
            return 'Moderate'
        else:
            return 'High'

    def _evaluate_diet_appropriateness(self, diet_type: str, species: str) -> Dict:
        """Evaluate appropriateness of diet for species"""
        try:
            diet_recommendations = {
                'Dog': {
                    'Premium Commercial': {'appropriateness': 'High', 'notes': 'Well-balanced nutrition'},
                    'Basic Commercial': {'appropriateness': 'Moderate', 'notes': 'May need supplements'},
                    'Home-Prepared': {'appropriateness': 'Moderate', 'notes': 'Ensure balanced nutrients'},
                    'Raw Diet': {'appropriateness': 'Moderate', 'notes': 'Monitor for pathogens'},
                    'Prescription': {'appropriateness': 'High', 'notes': 'Follow vet recommendations'}
                },
                'Cat': {
                    'Premium Commercial': {'appropriateness': 'High', 'notes': 'Good protein content'},
                    'Basic Commercial': {'appropriateness': 'Moderate', 'notes': 'Check taurine levels'},
                    'Home-Prepared': {'appropriateness': 'Low', 'notes': 'Risk of nutrient deficiency'},
                    'Raw Diet': {'appropriateness': 'Moderate', 'notes': 'Ensure proper handling'},
                    'Prescription': {'appropriateness': 'High', 'notes': 'Follow vet guidelines'}
                }
            }

            species_diet = diet_recommendations.get(species, {})
            diet_eval = species_diet.get(diet_type, {
                'appropriateness': 'Unknown',
                'notes': 'No specific recommendations available'
            })

            return {
                'appropriateness': diet_eval['appropriateness'],
                'notes': diet_eval['notes'],
                'recommendations': self._get_diet_recommendations(species)
            }

        except Exception as e:
            logger.error(f"Error evaluating diet: {str(e)}")
            return {
                'appropriateness': 'Unknown',
                'notes': 'Error evaluating diet',
                'recommendations': []
            }

    def _evaluate_activity_appropriateness(self, activity_level: str, species: str) -> Dict:
        """Evaluate appropriateness of activity level for species"""
        try:
            activity_recommendations = {
                'Dog': {
                    'Very Active': {'appropriateness': 'High', 'notes': 'Excellent for most healthy dogs'},
                    'Active': {'appropriateness': 'High', 'notes': 'Good activity level'},
                    'Moderate': {'appropriateness': 'Moderate', 'notes': 'May need more exercise'},
                    'Sedentary': {'appropriateness': 'Low', 'notes': 'Increase activity if possible'}
                },
                'Cat': {
                    'Very Active': {'appropriateness': 'High', 'notes': 'Great for indoor cats'},
                    'Active': {'appropriateness': 'High', 'notes': 'Good activity level'},
                    'Moderate': {'appropriateness': 'Moderate', 'notes': 'Encourage more play'},
                    'Sedentary': {'appropriateness': 'Low', 'notes': 'Add enrichment activities'}
                }
            }

            species_activity = activity_recommendations.get(species, {})
            activity_eval = species_activity.get(activity_level, {
                'appropriateness': 'Unknown',
                'notes': 'No specific recommendations available'
            })

            return {
                'appropriateness': activity_eval['appropriateness'],
                'notes': activity_eval['notes'],
                'recommendations': self._get_activity_recommendations(species)
            }

        except Exception as e:
            logger.error(f"Error evaluating activity: {str(e)}")
            return {
                'appropriateness': 'Unknown',
                'notes': 'Error evaluating activity',
                'recommendations': []
            }

    def _get_diet_recommendations(self, species: str) -> List[str]:
        """Get diet recommendations for species"""
        recommendations = {
            'Dog': [
                'Feed age-appropriate food',
                'Maintain consistent feeding schedule',
                'Monitor portion sizes',
                'Ensure fresh water available'
            ],
            'Cat': [
                'High protein diet recommended',
                'Multiple small meals daily',
                'Fresh water in multiple locations',
                'Monitor food intake'
            ]
        }
        return recommendations.get(species, ['Consult veterinarian for dietary advice'])

    def _get_activity_recommendations(self, species: str) -> List[str]:
        """Get activity recommendations for species"""
        recommendations = {
            'Dog': [
                'Regular daily walks',
                'Interactive play sessions',
                'Mental stimulation activities',
                'Age-appropriate exercise'
            ],
            'Cat': [
                'Interactive play sessions',
                'Climbing opportunities',
                'Environmental enrichment',
                'Puzzle feeders'
            ]
        }
        return recommendations.get(species, ['Consult veterinarian for activity guidelines'])
  