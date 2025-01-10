import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DiseasePredictor:
    """Handles disease prediction and risk analysis"""

    def __init__(self):
        self.disease_database = {
            'Mammals': {
                'common_diseases': {
                    'Heart Disease': {
                        'risk_factors': ['age', 'weight', 'activity_level'],
                        'symptoms': ['lethargy', 'coughing', 'difficulty_breathing'],
                        'genetic_predisposition': True,
                        'preventive_measures': ['regular exercise', 'weight management']
                    },
                    'Diabetes': {
                        'risk_factors': ['obesity', 'age', 'diet'],
                        'symptoms': ['increased_thirst', 'frequent_urination'],
                        'genetic_predisposition': True,
                        'preventive_measures': ['diet control', 'regular monitoring']
                    }
                },
                'breed_specific_diseases': {
                    'Dog': {
                        'German Shepherd': ['Hip Dysplasia', 'Degenerative Myelopathy'],
                        'Labrador': ['Progressive Retinal Atrophy', 'Joint Problems']
                    },
                    'Cat': {
                        'Persian': ['Polycystic Kidney Disease', 'Respiratory Issues'],
                        'Siamese': ['Amyloidosis', 'Progressive Retinal Atrophy']
                    }
                }
            },
            'Birds': {
                'common_diseases': {
                    'Respiratory Infection': {
                        'risk_factors': ['environment', 'stress'],
                        'symptoms': ['wheezing', 'nasal_discharge'],
                        'preventive_measures': ['clean environment', 'stress reduction']
                    }
                }
            },
            'Reptiles': {
                'common_diseases': {
                    'Metabolic Bone Disease': {
                        'risk_factors': ['diet', 'uvb_exposure'],
                        'symptoms': ['weak_bones', 'lethargy'],
                        'preventive_measures': ['proper UVB lighting', 'calcium supplementation']
                    }
                }
            }
        }

    def analyze_health_risks(self, animal_data: Dict) -> Dict:
        """Analyze health risks based on comprehensive factors"""
        try:
            risks = {
                'high_risk_factors': [],
                'moderate_risk_factors': [],
                'potential_diseases': [],
                'preventive_recommendations': []
            }

            # Analyze basic health metrics
            self._analyze_vital_signs(animal_data, risks)
            self._analyze_age_related_risks(animal_data, risks)
            self._analyze_weight_related_risks(animal_data, risks)
            self._analyze_genetic_risks(animal_data, risks)
            self._analyze_environmental_risks(animal_data, risks)
            self._analyze_behavioral_risks(animal_data, risks)

            # Get breed-specific risks
            if animal_data.get('Breed'):
                self._analyze_breed_specific_risks(animal_data, risks)

            return risks

        except Exception as e:
            logger.error(f"Error in health risk analysis: {str(e)}")
            return {
                'error': 'Failed to analyze health risks',
                'message': str(e)
            }

    def _analyze_vital_signs(self, data: Dict, risks: Dict) -> None:
        """Analyze vital signs for health risks"""
        if data.get('Heart_Rate'):
            hr = float(data['Heart_Rate'])
            species_range = self._get_vital_range(data['Species'], 'heart_rate')
            if species_range:
                if hr < species_range[0] or hr > species_range[1]:
                    risks['high_risk_factors'].append({
                        'factor': 'Heart Rate',
                        'value': hr,
                        'normal_range': species_range,
                        'recommendation': 'Immediate veterinary consultation recommended'
                    })

    def _analyze_age_related_risks(self, data: Dict, risks: Dict) -> None:
        """Analyze age-related health risks"""
        if data.get('Age'):
            age = float(data['Age'])
            species_lifespan = self._get_species_lifespan(data['Species'])
            
            if age > species_lifespan * 0.75:
                risks['moderate_risk_factors'].append({
                    'factor': 'Age',
                    'category': 'Senior',
                    'recommendations': [
                        'Regular health checkups',
                        'Age-appropriate diet',
                        'Modified exercise routine'
                    ]
                })

    def _analyze_genetic_risks(self, data: Dict, risks: Dict) -> None:
        """Analyze genetic and breed-specific health risks"""
        if data.get('Genetic_Predisposition') == 'High':
            risks['high_risk_factors'].append({
                'factor': 'Genetic Predisposition',
                'recommendations': [
                    'Regular screening for hereditary conditions',
                    'Preventive care measures',
                    'Genetic counseling'
                ]
            })

    def _get_vital_range(self, species: str, vital_sign: str) -> Optional[tuple]:
        """Get normal vital sign range for species"""
        # Implementation depends on species_config.py ranges
        pass

    def _get_species_lifespan(self, species: str) -> float:
        """Get average lifespan for species"""
        # Implementation depends on species_config.py data
        pass 