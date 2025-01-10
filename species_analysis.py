import logging
from typing import Dict, List, Optional
from species_config import SPECIES_CONFIG, get_species_category, get_species_config
import numpy as np

logger = logging.getLogger(__name__)

class SpeciesHealthAnalyzer:
    """Handles species-specific health analysis and predictions"""

    def __init__(self):
        self.species_ranges = SPECIES_CONFIG
        self.vital_signs_weights = {
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
                'temperature': 0.50  # Temperature more critical for reptiles
            },
            'Aquatic': {
                'heart_rate': 0.30,
                'respiratory_rate': 0.40,
                'temperature': 0.30
            }
        }

    def analyze_health(self, data: Dict) -> Dict:
        """Perform species-specific health analysis"""
        try:
            species = data.get('Species')
            category = get_species_category(species)
            
            if not category or not species:
                raise ValueError(f"Invalid species: {species}")

            species_config = get_species_config(species)
            
            analysis = {
                'vital_signs': self._analyze_vital_signs(data, species_config, category),
                'physical_condition': self._analyze_physical_condition(data, species_config),
                'environmental_factors': self._analyze_environmental_factors(data, category),
                'age_assessment': self._analyze_age(data, species_config),
                'risk_factors': self._identify_risk_factors(data, species_config, category)
            }

            # Calculate overall health score
            analysis['health_score'] = self._calculate_species_health_score(analysis)
            
            return analysis

        except Exception as e:
            logger.error(f"Error in species health analysis: {str(e)}")
            return {'error': str(e)}

    def _analyze_vital_signs(self, data: Dict, species_config: Dict, category: str) -> Dict:
        """Analyze vital signs based on species-specific ranges"""
        vital_signs = {}
        weights = self.vital_signs_weights.get(category, {})
        
        for sign, (min_val, max_val) in species_config['vital_signs'].items():
            if sign in data and data[sign]:
                value = float(data[sign])
                deviation = 0
                
                if value < min_val:
                    deviation = (min_val - value) / min_val
                elif value > max_val:
                    deviation = (value - max_val) / max_val
                
                status = 'Normal' if deviation == 0 else 'Abnormal'
                severity = self._calculate_severity(deviation)
                
                vital_signs[sign] = {
                    'value': value,
                    'range': (min_val, max_val),
                    'status': status,
                    'severity': severity,
                    'weight': weights.get(sign, 0.33),
                    'deviation': deviation
                }
        
        return vital_signs

    def _analyze_physical_condition(self, data: Dict, species_config: Dict) -> Dict:
        """Analyze physical condition based on species characteristics"""
        weight = float(data.get('Weight', 0))
        weight_range = species_config.get('weight_range', (0, 0))
        
        condition = {
            'weight_status': 'Normal',
            'severity': 'Low',
            'recommendations': []
        }
        
        if weight < weight_range[0]:
            condition.update({
                'weight_status': 'Underweight',
                'severity': 'High',
                'recommendations': [
                    'Increase caloric intake',
                    'Check for underlying conditions',
                    'Monitor weight gain progress'
                ]
            })
        elif weight > weight_range[1]:
            condition.update({
                'weight_status': 'Overweight',
                'severity': 'High',
                'recommendations': [
                    'Implement weight management plan',
                    'Increase exercise frequency',
                    'Adjust diet portions'
                ]
            })
        
        return condition

    def _analyze_environmental_factors(self, data: Dict, category: str) -> Dict:
        """Analyze environmental factors based on species category"""
        env_factors = {
            'Mammals': {
                'Indoor Only': {'risk': 'Low', 'concerns': ['Limited exercise']},
                'Outdoor Only': {'risk': 'High', 'concerns': ['Weather exposure', 'Parasites']},
                'Mixed': {'risk': 'Moderate', 'concerns': ['Temperature changes']}
            },
            'Birds': {
                'Indoor Only': {'risk': 'Low', 'concerns': ['Air quality']},
                'Outdoor Only': {'risk': 'High', 'concerns': ['Predators', 'Weather']},
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
        
        environment = data.get('Living_Environment')
        category_env = env_factors.get(category, {})
        
        return category_env.get(environment, {'risk': 'Unknown', 'concerns': []})

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
                'specific_concerns': ['Growth monitoring', 'Vaccination schedule']
            }
        elif age_ratio < 0.75:
            return {
                'status': 'Adult',
                'life_stage': 'Mature',
                'specific_concerns': ['Regular health maintenance']
            }
        else:
            return {
                'status': 'Senior',
                'life_stage': 'Geriatric',
                'specific_concerns': ['Age-related conditions', 'Mobility issues']
            }

    def _identify_risk_factors(self, data: Dict, species_config: Dict, category: str) -> List[Dict]:
        """Identify species-specific risk factors"""
        risk_factors = []
        
        # Age-related risks
        age_analysis = self._analyze_age(data, species_config)
        if age_analysis['status'] == 'Senior':
            risk_factors.append({
                'factor': 'Age',
                'risk_level': 'High',
                'concerns': age_analysis['specific_concerns']
            })
        
        # Environment risks
        env_analysis = self._analyze_environmental_factors(data, category)
        if env_analysis['risk'] in ['High', 'Moderate']:
            risk_factors.append({
                'factor': 'Environment',
                'risk_level': env_analysis['risk'],
                'concerns': env_analysis['concerns']
            })
        
        # Weight risks
        weight_analysis = self._analyze_physical_condition(data, species_config)
        if weight_analysis['weight_status'] != 'Normal':
            risk_factors.append({
                'factor': 'Weight',
                'risk_level': weight_analysis['severity'],
                'concerns': weight_analysis['recommendations']
            })
        
        return risk_factors

    def _calculate_severity(self, deviation: float) -> str:
        """Calculate severity level based on deviation from normal range"""
        if deviation == 0:
            return 'Normal'
        elif deviation < 0.1:
            return 'Mild'
        elif deviation < 0.2:
            return 'Moderate'
        else:
            return 'Severe'

    def _calculate_species_health_score(self, analysis: Dict) -> float:
        """Calculate overall health score based on species-specific analysis"""
        try:
            base_score = 100
            deductions = 0
            
            # Vital signs deductions
            vital_signs = analysis.get('vital_signs', {})
            for sign, data in vital_signs.items():
                if data['status'] == 'Abnormal':
                    deduction = data['deviation'] * 100 * data['weight']
                    deductions += deduction
            
            # Physical condition deductions
            condition = analysis.get('physical_condition', {})
            if condition.get('weight_status') != 'Normal':
                deductions += 15 if condition.get('severity') == 'High' else 8
            
            # Risk factor deductions
            risk_factors = analysis.get('risk_factors', [])
            for risk in risk_factors:
                if risk['risk_level'] == 'High':
                    deductions += 10
                elif risk['risk_level'] == 'Moderate':
                    deductions += 5
            
            return max(0, min(100, base_score - deductions))
            
        except Exception as e:
            logger.error(f"Error calculating health score: {str(e)}")
            return 0 