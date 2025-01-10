from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
from species_config import (
    get_species_config, get_species_category, get_all_species,
    get_species_vital_ranges, get_species_care_recommendations,
    get_critical_signs, get_environmental_factors
)
from species_metrics import SpeciesMetricsAnalyzer
from disease_analysis import DiseaseAnalyzer

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize analyzers
metrics_analyzer = SpeciesMetricsAnalyzer()
disease_analyzer = DiseaseAnalyzer()

@app.route('/')
def landing():
    """Display landing page"""
    return render_template('landing.html')

@app.route('/main')
def main():
    """Display main application page"""
    return render_template('index.html')

@app.route('/api/species-info', methods=['GET'])
def get_species_info():
    """Get information about all supported species"""
    try:
        return jsonify({
            'species_list': get_all_species(),
            'categories': {
                'Mammals': 'Warm-blooded vertebrates with fur/hair',
                'Birds': 'Feathered, winged vertebrates',
                'Reptiles': 'Cold-blooded vertebrates with scales',
                'Aquatic': 'Water-dwelling vertebrates'
            }
        })
    except Exception as e:
        logger.error(f"Error getting species info: {str(e)}")
        return jsonify({'error': 'Failed to get species information'}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No data provided")

        species = data.get('Species')
        if not species:
            raise ValueError("Species is required")

        # Get species configuration
        species_config = get_species_config(species)
        if not species_config:
            raise ValueError(f"Unsupported species: {species}")

        # Get species category
        category = get_species_category(species)

        # Perform species-specific metrics analysis
        metrics_analysis = metrics_analyzer.analyze_metrics(data)
        
        # Analyze disease risks
        disease_risks = disease_analyzer.analyze_health_risks(data)

        # Get species-specific care recommendations
        care_recommendations = get_species_care_recommendations(species)

        # Generate comprehensive response
        response = {
            'prediction': determine_health_status(metrics_analysis['health_score']),
            'diagnostic_insights': {
                'health_score': metrics_analysis['health_score'],
                'species_category': category,
                'vital_signs': metrics_analysis['vital_signs'],
                'weight_analysis': metrics_analysis['weight_analysis'],
                'age_analysis': metrics_analysis['age_analysis'],
                'environmental_analysis': metrics_analysis['environmental_analysis'],
                'diet_analysis': metrics_analysis['diet_analysis'],
                'activity_analysis': metrics_analysis['activity_analysis'],
                'risk_level': metrics_analysis['risk_level']
            },
            'disease_risks': disease_risks,
            'recommendations': generate_recommendations(
                data, 
                metrics_analysis,
                disease_risks,
                species_config,
                care_recommendations
            )
        }

        logger.info(f"Generated prediction for {species}")
        return jsonify(response)

    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def determine_health_status(health_score):
    """Determine health status based on score"""
    if health_score >= 90:
        return {
            'status': 'Healthy',
            'description': 'Overall health is excellent',
            'confidence': 'High'
        }
    elif health_score >= 75:
        return {
            'status': 'Minor Issue',
            'description': 'Minor health concerns present',
            'confidence': 'Medium'
        }
    elif health_score >= 60:
        return {
            'status': 'Requires Treatment',
            'description': 'Medical attention recommended',
            'confidence': 'Medium'
        }
    return {
        'status': 'Critical',
        'description': 'Immediate veterinary care needed',
        'confidence': 'High'
    }

def generate_recommendations(data, metrics_analysis, disease_risks, species_config, care_recommendations):
    """Generate comprehensive recommendations"""
    try:
        recommendations = {
            'immediate_actions': [],
            'lifestyle_changes': [],
            'monitoring_plan': [],
            'veterinary_care': []
        }

        # Add recommendations based on metrics analysis
        if metrics_analysis['risk_level'] == 'High':
            recommendations['immediate_actions'].extend([
                {
                    'recommendation': "Schedule immediate veterinary consultation",
                    'urgency': 'High'
                },
                {
                    'recommendation': "Monitor vital signs closely",
                    'urgency': 'High'
                }
            ])

        # Add weight-related recommendations
        weight_analysis = metrics_analysis.get('weight_analysis', {})
        if weight_analysis.get('status') != 'Normal':
            recommendations['lifestyle_changes'].extend([
                {
                    'recommendation': rec,
                    'urgency': weight_analysis.get('severity', 'Medium')
                } for rec in weight_analysis.get('recommendations', [])
            ])

        # Add age-specific recommendations
        age_analysis = metrics_analysis.get('age_analysis', {})
        if age_analysis.get('specific_concerns'):
            recommendations['monitoring_plan'].extend([
                {
                    'recommendation': concern,
                    'urgency': age_analysis.get('risk_level', 'Medium')
                } for concern in age_analysis['specific_concerns']
            ])

        # Add environmental recommendations
        env_analysis = metrics_analysis.get('environmental_analysis', {})
        if env_analysis.get('risk_level') in ['High', 'Moderate']:
            recommendations['lifestyle_changes'].extend([
                {
                    'recommendation': concern,
                    'urgency': env_analysis['risk_level']
                } for concern in env_analysis.get('concerns', [])
            ])

        # Add species-specific care recommendations
        for care in care_recommendations:
            recommendations['veterinary_care'].append({
                'recommendation': care,
                'urgency': 'Medium'
            })

        return recommendations

    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        return {
            'immediate_actions': [{'recommendation': "Contact veterinarian", 'urgency': 'High'}],
            'lifestyle_changes': [],
            'monitoring_plan': [],
            'veterinary_care': []
        }

if __name__ == '__main__':
    app.run(debug=True) 