# Species categories and their vital signs ranges
SPECIES_CONFIG = {
    'Mammals': {
        'Dog': {
            'vital_signs': {
                'heart_rate': (60, 140),
                'respiratory_rate': (10, 30),
                'temperature': (37.5, 39.2)
            },
            'weight_range': (2, 90),  # kg
            'lifespan': 12,  # years
            'recommended_care': [
                'Annual dental cleaning',
                'Regular parasite prevention',
                'Core vaccinations'
            ]
        },
        'Cat': {
            'vital_signs': {
                'heart_rate': (120, 140),
                'respiratory_rate': (20, 30),
                'temperature': (38.0, 39.2)
            },
            'weight_range': (2, 10),
            'lifespan': 15,
            'recommended_care': [
                'Indoor lifestyle recommended',
                'Regular dental care',
                'FeLV/FIV testing'
            ]
        },
        'Horse': {
            'vital_signs': {
                'heart_rate': (28, 44),
                'respiratory_rate': (8, 16),
                'temperature': (37.5, 38.5)
            },
            'weight_range': (300, 1000),
            'lifespan': 25
        },
        'Tiger': {
            'vital_signs': {
                'heart_rate': (60, 100),
                'respiratory_rate': (15, 30),
                'temperature': (37.5, 39.0)
            },
            'weight_range': (65, 300),
            'lifespan': 20
        },
        'Lion': {
            'vital_signs': {
                'heart_rate': (60, 100),
                'respiratory_rate': (15, 30),
                'temperature': (37.5, 39.0)
            },
            'weight_range': (120, 250),
            'lifespan': 15
        },
        'Cheetah': {
            'vital_signs': {
                'heart_rate': (120, 170),
                'respiratory_rate': (20, 30),
                'temperature': (37.5, 39.0)
            },
            'weight_range': (35, 65),
            'lifespan': 12,
            'recommended_care': [
                'Regular cardiovascular assessment',
                'High-protein diet management',
                'Exercise space requirements'
            ]
        },
        'Elephant': {
            'vital_signs': {
                'heart_rate': (25, 35),
                'respiratory_rate': (4, 8),
                'temperature': (36.0, 37.5)
            },
            'weight_range': (2000, 6000),
            'lifespan': 60
        }
        # Add more mammals...
    },
    'Birds': {
        'Parrot': {
            'vital_signs': {
                'heart_rate': (340, 600),
                'respiratory_rate': (25, 45),
                'temperature': (39.5, 42.5)
            },
            'weight_range': (0.3, 1.5),
            'lifespan': 50,
            'recommended_care': [
                'Annual avian vet check',
                'Beak and nail trimming',
                'Environmental enrichment'
            ]
        },
        'Eagle': {
            'vital_signs': {
                'heart_rate': (300, 400),
                'respiratory_rate': (20, 30),
                'temperature': (39.0, 41.0)
            },
            'weight_range': (3, 6),
            'lifespan': 20
        }
        # Add more birds...
    },
    'Reptiles': {
        'Snake': {
            'vital_signs': {
                'heart_rate': (30, 80),
                'respiratory_rate': (4, 8),
                'temperature': (28.0, 32.0)
            },
            'weight_range': (0.5, 10),
            'lifespan': 20,
            'recommended_care': [
                'UVB lighting maintenance',
                'Regular substrate changes',
                'Temperature gradient monitoring'
            ]
        },
        'Turtle': {
            'vital_signs': {
                'heart_rate': (40, 90),
                'respiratory_rate': (2, 4),
                'temperature': (26.0, 30.0)
            },
            'weight_range': (1, 150),
            'lifespan': 50
        }
        # Add more reptiles...
    },
    'Aquatic': {
        'Goldfish': {
            'vital_signs': {
                'heart_rate': (60, 120),
                'respiratory_rate': (50, 85),
                'temperature': (18.0, 22.0)
            },
            'weight_range': (0.1, 0.3),
            'lifespan': 10,
            'recommended_care': [
                'Water quality testing',
                'Regular filter maintenance',
                'Temperature stability'
            ]
        },
        'Shark': {
            'vital_signs': {
                'heart_rate': (40, 80),
                'respiratory_rate': (20, 30),
                'temperature': (20.0, 26.0)
            },
            'weight_range': (50, 1000),
            'lifespan': 20
        }
        # Add more aquatic species...
    }
}

# Species-specific health considerations
SPECIES_HEALTH_FACTORS = {
    'Mammals': {
        'activity_importance': 1.2,
        'diet_importance': 1.0,
        'temperature_sensitivity': 1.0,
        'environmental_factors': ['Indoor/Outdoor access', 'Exercise space', 'Social interaction'],
        'critical_signs': ['Respiratory distress', 'Severe lethargy', 'Loss of appetite'],
        'species_specific': {
            'Cheetah': {
                'activity_importance': 1.5,
                'environmental_factors': ['Large exercise area', 'Enrichment activities', 'Stress management'],
                'critical_signs': ['Rapid breathing', 'Loss of appetite', 'Reduced mobility']
            }
        }
    },
    'Birds': {
        'activity_importance': 1.5,
        'diet_importance': 1.2,
        'temperature_sensitivity': 1.3,
        'environmental_factors': ['Air quality', 'Cage size', 'Social enrichment'],
        'critical_signs': ['Tail bobbing', 'Open-mouth breathing', 'Fluffed feathers']
    },
    'Reptiles': {
        'activity_importance': 0.8,
        'diet_importance': 1.0,
        'temperature_sensitivity': 2.0,
        'environmental_factors': ['Temperature gradient', 'Humidity', 'UVB exposure'],
        'critical_signs': ['Gaping mouth', 'Abnormal shedding', 'Lethargy']
    },
    'Aquatic': {
        'activity_importance': 1.0,
        'diet_importance': 1.1,
        'temperature_sensitivity': 1.5,
        'environmental_factors': ['Water quality', 'Oxygen levels', 'Tank size'],
        'critical_signs': ['Gasping at surface', 'Erratic swimming', 'Loss of color']
    }
}

def get_species_category(species_name):
    """Get the category for a given species"""
    for category, species_dict in SPECIES_CONFIG.items():
        if species_name in species_dict:
            return category
    return None

def get_species_config(species_name):
    """Get configuration for a specific species"""
    category = get_species_category(species_name)
    if category:
        return SPECIES_CONFIG[category].get(species_name)
    return None

def get_health_factors(species_name):
    """Get health factors for a species category"""
    category = get_species_category(species_name)
    if category:
        return SPECIES_HEALTH_FACTORS[category]
    return SPECIES_HEALTH_FACTORS['Mammals']  # Default to mammals 

# Add helper functions for dynamic species handling
def get_all_species():
    """Get list of all supported species"""
    species_list = []
    for category in SPECIES_CONFIG:
        species_list.extend(SPECIES_CONFIG[category].keys())
    return species_list

def get_species_vital_ranges(species):
    """Get vital sign ranges for specific species"""
    category = get_species_category(species)
    if category and species in SPECIES_CONFIG[category]:
        return SPECIES_CONFIG[category][species]['vital_signs']
    return None

def get_species_care_recommendations(species):
    """Get care recommendations for specific species"""
    category = get_species_category(species)
    if category and species in SPECIES_CONFIG[category]:
        return SPECIES_CONFIG[category][species]['recommended_care']
    return []

def get_critical_signs(species):
    """Get critical signs for species category"""
    category = get_species_category(species)
    if category in SPECIES_HEALTH_FACTORS:
        return SPECIES_HEALTH_FACTORS[category]['critical_signs']
    return []

def get_environmental_factors(species):
    """Get environmental factors for species category"""
    category = get_species_category(species)
    if category in SPECIES_HEALTH_FACTORS:
        return SPECIES_HEALTH_FACTORS[category]['environmental_factors']
    return []