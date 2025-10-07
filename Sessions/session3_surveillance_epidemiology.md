# Session 3: Surveillance Systems and Epidemiology of AMR

## Learning Objectives
By the end of this session, participants will be able to:
- Understand different surveillance systems for antimicrobial resistance monitoring
- Interpret resistance trends and epidemiological patterns
- Apply surveillance data to inform clinical decision-making and stewardship programs
- Design basic surveillance protocols for healthcare settings

## Time Allocation
- Introduction to surveillance: 15 minutes
- Global surveillance systems: 25 minutes
- Epidemiological methods: 20 minutes
- Data analysis and interpretation: 15 minutes
- Designing surveillance programs: 15 minutes

---

## Introduction to Antimicrobial Surveillance

### Why Surveillance Matters
- **Inform clinical decisions**: Local resistance patterns guide empirical therapy
- **Monitor intervention effectiveness**: Track impact of stewardship programs
- **Detect outbreaks**: Early identification of emerging resistance threats
- **Policy development**: Evidence-based guidelines and resource allocation
- **Global health security**: International collaboration on emerging threats

### Surveillance Principles
1. **Standardized methodology**: Consistent data collection and analysis
2. **Risk-factor stratification**: Patient demographics and healthcare exposure
3. **Temporal trends**: Longitudinal resistance pattern monitoring
4. **Molecular epidemiology**: Genetic basis of resistance spread
5. **Actionable results**: Link surveillance to clinical interventions

---

## Global Surveillance Systems

### World Health Organization (WHO) Initiatives

#### Global Antimicrobial Resistance Surveillance System (GLASS)
```python
class GLASSSystem:
    def __init__(self):
        self.scope = {
            'participants': 95+ countries,
            'pathogens': ['E. coli', 'K. pneumoniae', 'S. aureus', 'S. pneumoniae', 'N. gonorrhoeae'],
            'antibiotics': ['ciprofloxacin', 'ceftriaxone', 'meropenem', 'vancomycin', 'penicillin', 'azithromycin']
        }
        self.objectives = [
            'Monitor resistance trends',
            'Guide local action plans',
            'Track global progress',
            'Inform policy development'
        ]

    def primary_focus_areas(self):
        return """
        WHO GLASS Priority Areas:
        • Bloodstream infections (Bacteria)
        • Urinary tract infections (E. coli)
        • Healthcare-associated pneumonia (Gram-negative rods)
        • Hospital-acquired methicillin-resistant S. aureus (MRSA)
        • Invasive pneumococcal disease
        • Gonococcal infections requiring treatment
        """
```

**GLASS Dashboard Features:**
- Country-specific resistance profiles
- Regional comparison capabilities
- Temporal trend visualization
- Priority pathogen surveillance
- Standardized denominator reporting

#### WHO Essential Diagnostics List
- **AMR diagnostic panel**: Priority tests for surveillance
- **Point-of-care diagnostics**: Syndromic testing approaches
- **Laboratory capacity**: Building infrastructure in LMICs

### Centers for Disease Control and Prevention (CDC)

#### Antibiotic Resistance Laboratory Network (AR Lab Network)
- **Public Health Labs**: 50 state and territorial laboratories
- **FoodNet Sites**: 10 sites tracking foodborne resistance
- **EIP Sites**: Emerging Infections Program surveillance
- **NARMS**: National Antimicrobial Resistance Monitoring System (animals & retail meat)

#### Antibiotic Resistance Threats Report (AR Threats)
```python
class CDCARThreatsReport:
    def __init__(self):
        self.categorization = {
            'urgent': ['C. auris', 'Carbapenem-resistant pathogens', 'XDR Shigella'],
            'serious': ['Clostridiodes difficile', 'Drug-resistant Campylobacter', 'ESBL-E. coli'],
            'concerning': ['Vancomycin-resistant Enterococcus', 'Donkey multidrug-resistant'],
            'watch_list': ['Eravacycline-resistant pathogens', 'Telithromycin-resistant Streptococcus']
        }

    def threat_level_assessment(self, pathogen, resistance_pattern):
        # CDC threat level assessment matrix
        # Combines mortality, incidence, transmission potential, prevention difficulty
        assessment_criteria = {
            'mortality_rate': {'high': '>25%', 'medium': '10-25%', 'low': '<10%'},
            'incidence': {'high': '>10,000 cases/year', 'medium': '1,000-10,000', 'low': '<1,000'},
            'transmission': {'high': 'nosocomial + community', 'medium': 'nosocomial', 'low': 'individual'},
            'prevention_difficulty': {'high': 'complex interventions needed', 'medium': 'some interventions', 'low': 'basic infection control'}
        }
        return f"{pathogen} assessed as {self.categorization.get(pathogen.split()[0].lower(), {}).get('category', 'unknown')} threat"
```

### European Surveillance Systems

#### European Centre for Disease Prevention and Control (ECDC)

#### European Antimicrobial Resistance Surveillance Network (EARS-Net)
- **28 EU/EEA countries** standardized data
- **Invasive isolates** from blood/cerebrospinal fluid
- **50 laboratories** participating
- **Real-time data** with annual reports

#### Healthcare-Associated Infections Surveillance Network (HAI-Net)
- **Surgical site infections**: SCIP/SSI surveillance
- **ICU-acquired infections**: Ventilator-associated, catheter-associated
- **AMR pathogen tracking**: MDR species monitoring
- **Prevention effectiveness**: Intervention impact assessment

### Asian Surveillance Initiatives

#### Nanjing Antibiotic Resistance Surveillance System (NARSS)
- **China**: Largest bacterial surveillance network
- **120 medical centers** across 31 provinces
- **Multi-pathogen surveillance**: 29 bacterial species
- **Phenotypic and genotypic** characterization
- **13,000 isolates annually**

### Regional Networks
- **Network for Surveillance of Antimicrobial Resistance in Vietnam (NASARM)**
- **Indian Council of Medical Research (ICMR)** antimicrobial resistance surveillance
- **Latin American Surveillance of Antimicrobial Resistance (ReLAVRA)**

---

## Epidemiological Methods in AMR Surveillance

### Study Designs for Resistance Monitoring

#### Point Prevalence Surveys (PPS)
```python
class PointPrevalenceSurvey:
    def __init__(self, hospital, survey_date):
        self.hospital = hospital
        self.survey_date = survey_date
        self.survey_scope = {
            'wards': 'all inpatient units',
            'time_period': '24-48 hour snapshot',
            'data_collected': ['antibiotic use', 'indication', 'duration', 'appropriateness']
        }

    def calculate_prevalence(self, numerator, denominator):
        """
        Calculate antibiotic use prevalence

        Args:
            numerator: Patients receiving antibiotics
            denominator: Total inpatients

        Returns:
            Prevalence percentage with 95% CI
        """
        import math

        prevalence = numerator / denominator
        se = math.sqrt(prevalence * (1 - prevalence) / denominator)
        ci_lower = prevalence - (1.96 * se)
        ci_upper = prevalence + (1.96 * se)

        return {
            'prevalence':/f"{prevalence:.3%} ({ci_lower:.3%} - {ci_upper:.3%})"
        }
```

**PPS Advantages:**
- Resource-efficient for multiple facilities
- Standardized methodology
- Benchmarking capability
- Links use to outcomes

#### Cohort Studies
- **Incidence tracking**: New resistance cases over time
- **Risk factor analysis**: Predisposing factors for resistance development
- **Outbreak investigation**: Transmission dynamics during clusters
- **Intervention evaluation**: Pre-post study designs

#### Case-Control Studies
- **Resistance risk factors**: Hospital exposure, prior antibiotics, comorbidities
- **Transmission drivers**: Healthcare worker practices, environmental contamination
- **Genetic markers**: Resistance gene carriage associations

### Statistical Analysis Methods

#### Time Series Analysis
```python
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

class ResistanceTrendAnalysis:
    def __init__(self, time_series_data):
        self.data = time_series_data

    def decompose_trends(self):
        """
        Decompose resistance trends into components:
        - Trend (long-term changes)
        - Seasonal (cyclical patterns)
        - Residual (random variation)
        """
        decomposition = seasonal_decompose(
            self.data['resistance_percentage'],
            model='additive',
            period=12  # Monthly data
        )

        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid
        }

    def changepoint_detection(self):
        """
        Identify significant change points in resistance trends
        Useful for outbreak detection or intervention effects
        """
        # Implement changepoint detection algorithm
        # Returns dates where trends significantly change
        pass
```

#### Multilevel Modeling
- **Facility-level variation**: Account for institutional differences
- **Geographic clustering**: Regional resistance hot spots
- **Patient risk stratification**: Individual risk factor adjustment
- **Repeated measures**: Longitudinal patient follow-up

#### Network Analysis
- **Transmission networks**: Episode 1 links using pulsotyping/WGS
- **Genetic relatedness**: Minimum spanning tree analysis
- **Outbreak investigation**: Transmission route identification
- **Super-spreaders**: High-transmission risk isolates

---

## Interpreting Surveillance Data

### Risk Stratification

#### Low vs. High Risk Environments
- **Community-onset infections**: Generally lower resistance risk
- **Healthcare-associated infections**: Significantly higher resistance rates
- **Intensive care unit**: Highest resistance burden across most pathogens

#### Patient Risk Factors for MDR
```python
def calculate_mdr_risk_score(patient_factors):
    """
    Calculate multivariate risk score for multidrug-resistant infection

    Based on CDC/IDSA guidelines for antibiotic-resistant pathogens
    """
    risk_score = 0

    # Healthcare exposure (4 points)
    risk_factors = {
        'hospitalization_last_30_days': 2,
        'surgery_last_30_days': 2,
        'long_term_care_resident': 1,
        'hemodialysis': 1,
        'central_venous_catheter_current': 1,
        'indwelling_urinary_catheter': 1
    }

    # Prior antibiotic exposure (3 points)
    antibiotic_history = {
        'broad_spectrum_abx_last_90_days': 2,
        'multiple_abx_courses': 1,
        'prior_mdr_infection': 3
    }

    # Infection characteristics (3 points)
    infection_factors = {
        'severe_illness': 2,
        'prior_treatment_failure': 2,
        'known_resistant_isolate': 3
    }

    return risk_score
```

### Clinical Decision-Making from Surveillance

#### Empirical Therapy Selection
```python
class EmpiricalRegimenSelection:
    def __init__(self, institution_location, unit_type, infection_type):
        self.institution = institution_location
        self.unit = unit_type  # ICU, ward, clinic
        self.infection = infection_type  # UTI, pneumonia, bloodstream
        self.local_susceptibility_data = self.load_local_data()

    def recommend_empiric_regimen(self):
        """
        Generate evidence-based empirical regimen recommendations

        Based on local antibiogram and CDC/IDSA guidelines
        """

        if self.unit == 'ICU' and self.infection == 'pneumonia':
            # Check local Pseudomonas aeruginosa susceptibility
            if self.local_susceptibility_data['p_aeruginosa']['meropenem'] > 80:
                return "Meropenem + vancomycin (if MRSA risk)"
            else:
                return "Meropenem + ciprofloxacin + vancomycin"

        elif self.infection == 'UTI' and self.unit == 'clinic':
            # Community-acquired UTI E. coli susceptibility
            if self.local_susceptibility_data['e_coli']['ciprofloxacin'] > 85:
                return "Oral ciprofloxacin alternatives preferable"
            else:
                return "Nitrofurantoin or fosfomycin preferred"

        return "Float ID consultation - high resistance risk"
```

### Benchmarking and Target Setting

#### Target Metrics
- **Resistance targets**: Specific pathogen-antibiotic combinations
- **Usage thresholds**: Defined daily dose (DDD) per 1000 patient-days
- **Appropriateness rates**: Percentage appropriate antibiotic orders
- **De-escalation rates**: Within 48-72 hours of culture results

#### Improvement Targets (Typical Goals)
- **90% appropriate indication** for antibiotic initiation
- **95% de-escalation** within 48 hours of culture results
- **80-90% completion** of prescribed duration
- **<25% broad-spectrum use** in non-ICU patients

---

## Designing Surveillance Programs

### Institutional Surveillance Framework

#### Step 1: Define Objectives
- **What to measure**: Key pathogens, usage patterns, outcomes
- **Frequency**: Real-time dashboards vs. periodic audits
- **Scope**: Institution-wide vs. unit-specific monitoring
- **Audience**: ASP team, administration, external regulators

#### Step 2: Data Collection System
```python
class SurveillanceSystemDesign:
    def __init__(self):
        self.data_sources = []
        self.metrics_definition = {}
        self.collection_frequency = {}
        self.quality_control = {}

    def define_key_metrics(self):
        """Establish measurable indicators for surveillance"""
        self.data_sources = [
            'laboratory_information_systems',
            'pharmacy_management_systems',
            'electronic_health_records',
            'infection_control_databases'
        ]

        self.metrics_definition = {
            'process_measures': [
                'percentage_orders_reviewed_by_stewardship',
                'time_to_culture_collection',
                'antibiogram_update_frequency'
            ],
            'outcome_measures': [
                'clostridium_difficile_rates',
                'mortality_from_mdr_infections',
                'length_of_stay_difference'
            ],
            'balancing_measures': [
                'patient_satisfaction_scores',
                'all_cause_readmission_rates'
            ]
        }

    def establish_data_quality(self):
        """Quality control measures for surveillance data"""
        self.quality_control = {
            'data_validation': 'double-entry verification',
            'incomplete_records': '<5% missing key fields',
            'denominator_accuracy': 'regular patient census validation',
            'resistance_interpretation': 'CLSI/EUCAST standards'
        }
```

#### Step 3: Implementation Strategy
- **Phased rollout**: Pilot in high-risk units first
- **Staff training**: Data abstractor training and competency verification
- **Technology integration**: Automated data extraction where possible
- **Sustainability planning**: Resource allocation for ongoing operation

#### Step 4: Analysis
