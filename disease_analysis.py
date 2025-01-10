import logging
from typing import Dict, List, Optional
from species_config import SPECIES_CONFIG, get_species_category

logger = logging.getLogger(__name__)

class DiseaseAnalyzer:
    """Analyzes disease risks and provides health recommendations for different species"""

    def __init__(self):
        self.disease_database = {
            'Mammals': {
                'common_diseases': {
                    'Heart Disease': {
                        'risk_factors': ['age', 'weight', 'activity_level'],
                        'symptoms': ['lethargy', 'coughing', 'difficulty_breathing'],
                        'severity': 'High',
                        'preventive_measures': ['regular exercise', 'weight management']
                    }
                },
                'species_specific': {
                    'Elephant': {
                        'Foot Problems': {
                            'risk_factors': ['weight', 'environment', 'activity_level'],
                            'severity': 'High',
                            'preventive_measures': ['Regular foot care', 'Proper substrate', 'Exercise']
                        },
                        'Arthritis': {
                            'risk_factors': ['age', 'weight'],
                            'severity': 'Moderate',
                            'preventive_measures': ['Joint supplements', 'Weight management']
                        }
                    },
                    'Tiger': {
                        'Dental Disease': {
                            'risk_factors': ['age', 'diet'],
                            'severity': 'High',
                            'preventive_measures': ['Dental checks', 'Proper diet']
                        }
                    },
                    'Lion': {
                        'Joint Problems': {
                            'risk_factors': ['age', 'weight'],
                            'severity': 'Moderate',
                            'preventive_measures': ['Exercise', 'Joint supplements']
                        }
                    },
                    'Cheetah': {
                        'Stress-related Issues': {
                            'risk_factors': ['environment', 'social_factors'],
                            'severity': 'High',
                            'preventive_measures': ['Stress reduction', 'Environmental enrichment']
                        }
                    }
                }
            },
            'Birds': {
                'common_diseases': {
                    'Respiratory Infection': {
                        'risk_factors': ['environment', 'ventilation'],
                        'severity': 'High',
                        'preventive_measures': ['Good ventilation', 'Clean environment']
                    }
                },
                'species_specific': {
                    'Eagle': {
                        'Lead Poisoning': {
                            'risk_factors': ['environment', 'diet'],
                            'severity': 'Critical',
                            'preventive_measures': ['Proper diet', 'Environmental monitoring']
                        }
                    }
                }
            },
            'Reptiles': {
                'common_diseases': {
                    'Metabolic Bone Disease': {
                        'risk_factors': ['diet', 'uvb_exposure'],
                        'severity': 'High',
                        'preventive_measures': ['UVB lighting', 'Calcium supplementation']
                    }
                }
            },
            'Aquatic': {
                'common_diseases': {
                    'Water Quality Issues': {
                        'risk_factors': ['environment', 'water_parameters'],
                        'severity': 'High',
                        'preventive_measures': ['Regular water testing', 'Proper filtration']
                    }
                }
            }
        }

    def analyze_health_risks(self, animal_data: Dict) -> Dict:
        """Analyze health risks and provide recommendations"""
        try:
            species = animal_data.get('Species')
            category = get_species_category(species)
            
            if not category:
                raise ValueError(f"Unknown species category for: {species}")

            risks = {
                'disease_risks': [],
                'preventive_measures': [],
                'immediate_concerns': [],
                'long_term_monitoring': []
            }

            # Get category-specific diseases
            category_diseases = self.disease_database.get(category, {})
            
            # Analyze common diseases for the category
            common_diseases = category_diseases.get('common_diseases', {})
            for disease, info in common_diseases.items():
                risk_level = self._calculate_risk_level(animal_data, info['risk_factors'])
                if risk_level > 0.5:
                    risks['disease_risks'].append({
                        'disease': disease,
                        'risk_level': risk_level,
                        'severity': info['severity'],
                        'preventive_measures': info['preventive_measures']
                    })

            # Analyze species-specific diseases
            species_diseases = category_diseases.get('species_specific', {}).get(species, {})
            for disease, info in species_diseases.items():
                risk_level = self._calculate_risk_level(animal_data, info['risk_factors'])
                if risk_level > 0.5:
                    risks['disease_risks'].append({
                        'disease': disease,
                        'risk_level': risk_level,
                        'severity': info['severity'],
                        'preventive_measures': info['preventive_measures']
                    })

            # Add general preventive measures
            risks['preventive_measures'].extend([
                'Regular health check-ups',
                'Proper nutrition',
                'Adequate exercise',
                'Clean environment'
            ])

            return risks

        except Exception as e:
            logger.error(f"Error in health risk analysis: {str(e)}")
            return {
                'disease_risks': [],
                'preventive_measures': ['Consult with veterinarian'],
                'immediate_concerns': [],
                'long_term_monitoring': []
            }

    def _calculate_risk_level(self, data: Dict, risk_factors: List[str]) -> float:
        """Calculate risk level based on risk factors"""
        try:
            risk_score = 0.0
            applicable_factors = 0

            for factor in risk_factors:
                if factor == 'age':
                    age = float(data.get('Age', 0))
                    species_lifespan = self._get_species_lifespan(data['Species'])
                    if age > species_lifespan * 0.75:
                        risk_score += 1.0
                    elif age > species_lifespan * 0.5:
                        risk_score += 0.5
                    applicable_factors += 1

                elif factor == 'weight':
                    if 'Weight' in data:
                        weight = float(data['Weight'])
                        weight_range = self._get_weight_range(data['Species'])
                        if weight > weight_range[1] or weight < weight_range[0]:
                            risk_score += 1.0
                        applicable_factors += 1

                elif factor == 'environment':
                    env = data.get('Living_Environment')
                    if env == 'Outdoor Only':
                        risk_score += 0.8
                    elif env == 'Mixed':
                        risk_score += 0.4
                    applicable_factors += 1

                elif factor == 'activity_level':
                    activity = data.get('Activity_Level')
                    if activity == 'Sedentary':
                        risk_score += 1.0
                    elif activity == 'Moderate':
                        risk_score += 0.5
                    applicable_factors += 1

            return risk_score / max(applicable_factors, 1)

        except Exception as e:
            logger.error(f"Error calculating risk level: {str(e)}")
            return 0.0
    def _get_species_lifespan(self, species: str) -> float:
        """Get species lifespan from config"""
        species_config = get_species_config(species)
        return species_config.get('lifespan', 15) if species_config else 15

    def _get_weight_range(self, species: str) -> tuple:
        """Get species weight range from config"""
        species_config = get_species_config(species)
        return species_config.get('weight_range', (0, 1000)) if species_config else (0, 1000)
