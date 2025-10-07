# Session 5: Data Analysis & Interpretation in AMR Surveillance

## Learning Objectives
By the end of this session, participants will be able to:
- Apply statistical methods for analyzing AMR surveillance data
- Interpret resistance trends using epidemiological principles
- Perform risk factor analysis for AMR emergence
- Use molecular epidemiology tools for outbreak investigation
- Apply machine learning approaches to resistance prediction
- Create meaningful dashboards for AMR monitoring

## Introduction to AMR Data Analysis

### Data Sources and Types

#### Surveillance Systems Data
```
WHO GLASS Data Structure:
├── Pathogen identification (species, subspecies)
├── Antibiotic susceptibility test results
├── MIC values and interpretive categories
├── Geographic and temporal metadata
├── Clinical vs. community isolation context
└── Specimen type and ward location
```

#### Laboratory Information Systems
- **WHONET**: Software platform linking laboratories to surveillance
- **External Quality Assessment (EQA)**: Provider proficiency testing
- **AST Method Standardization**: Disk diffusion, broth microdilution, gradient strips

### Quality Assurance Standards

#### CLSI/GLASS Standards
```python
class AST_Quality_Assurance:
    def __init__(self):
        self.clsi_breakpoints = {
            'cefotaxime': {'S': '<=2', 'R': '>4'},
            'ciprofloxacin': {'S': '<=1', 'R': '>4'},
            'gentamicin': {'S': '<=4', 'R': '>16'}
        }

    def validate_ast_result(self, antibiotic, mic_value):
        """Validate MIC interpretation against CLSI breakpoints"""
        breakpoints = self.clsi_breakpoints.get(antibiotic, {})

        if not breakpoints:
            return "No CLSI breakpoint established"

        if mic_value <= float(breakpoints['S']):
            return "Susceptible"
        elif mic_value >= float(breakpoints['R']):
            return "Resistant"
        else:
            return "Intermediate"
```

## Statistical Analysis Methods

### Descriptive Epidemiology

#### Resistance Rate Calculations
```python
def calculate_resistance_rates(isolates_data, antibiotic_of_interest):
    """
    Calculate resistance rates with confidence intervals

    Args:
        isolates_data: Dictionary of isolate results
        antibiotic_of_interest: Target antibiotic for analysis

    Returns:
        Dictionary with resistance rates and statistics
    """

    total_isolates = len(isolates_data)
    resistant_count = sum(1 for isolate in isolates_data
                         if isolate[antibiotic_of_interest] == 'R')

    resistance_rate = resistant_count / total_isolates * 100

    # Calculate 95% confidence interval
    import math

    if total_isolates > 0:
        se = math.sqrt((resistance_rate/100 * (1 - resistance_rate/100)) / total_isolates)
        ci_lower = max(0, (resistance_rate/100 - 1.96 * se) * 100)
        ci_upper = min(100, (resistance_rate/100 + 1.96 * se) * 100)
    else:
        ci_lower, ci_upper = 0, 0

    return {
        'resistance_rate_percent': resistance_rate,
        'total_isolates': total_isolates,
        'resistant_isolates': resistant_count,
        'confidence_interval': f"{ci_lower:.1f}-{ci_upper:.1f}%"
    }
```

#### Temporal Trend Analysis
```
Important Metrics:
├── Annual percent change in resistance rates
├── Seasonal variation patterns
├── Step changes following intervention
├── Time series decomposition (trend, seasonal, noise)
└── Forecasting future resistance patterns
```

### Multilevel Statistics for AMR

#### Hierarchical Models
```python
import statsmodels.api as sm
import pandas as pd

class AMR_Hierarchical_Analysis:
    def __init__(self):
        self.hospital_levels = [
            'ward', 'hospital', 'region', 'national'
        ]

    def fit_multilevel_model(self, resistance_data, hospital_hierarchy):
        """
        Fit multilevel logistic regression for resistance
        """

        # Model: Resistance ~ Hospital Factors + Patient Factors + Antibiotics
        formula = """
        resistance ~
            antibiotic_type +
            hospital_location +
            patient_age +
            recent_admission +
            (1 | hospital_id) +
            (1 | region)
        """

        model = sm.MixedLM.from_formula(formula, resistance_data,
                                       groups=["hospital_id", "region"])

        result = model.fit()
        return result
```

#### Risk Factor Attribution

#### Geographic Hotspot Analysis
Using spatial statistics to identify resistance hotspots:
- **Moran's I**: Spatial autocorrelation testing
- **Getis-Ord Gi***: Local cluster identification
- **Spatial regression models**: Incorporating geographic covariates

### Molecular Epidemiology

#### Whole Genome Sequencing Analysis
```python
class Molecular_Epidemiology_Analysis:
    def __init__(self, wgs_data):
        self.wgs_data = wgs_data
        self.resistance_gene_database = self.load_resistance_database()

    def identify_resistance_determinants(self, genome_assembly):
        """Identify resistance genes and mutations"""

        resistance_findings = {}

        # Screen for acquired resistance genes
        for resistance_class, genes in self.resistance_gene_database.items():
            hits = self.blast_search(genome_assembly, genes)
            if hits:
                resistance_findings[resistance_class] = hits

        # Identify chromosomal mutations
        gyrase_mutations = self.identify_gyrase_mutations(genome_assembly)
        pbp_mutations = self.identify_pbp_mutations(genome_assembly)

        return {
            'acquired_resistance': resistance_findings,
            'chromosomal_mutations': {
                'gyrase': gyrase_mutations,
                'penicillin_binding_proteins': pbp_mutations
            }
        }

    def construct_transmission_network(self, isolate_collection):
        """Build transmission network using SNP analysis"""

        # Core genome MLST
        cgmlst_profiles = self.run_cgmlst(isolate_collection)

        # Transmission threshold: <10 SNPs suggests recent transmission
        transmission_links = []
        for pair in isolate_collection.pairs():
            snp_distance = self.calculate_snp_distance(pair.isolate1, pair.isolate2)
            if snp_distance < 10:
                transmission_links.append({
                    'from': pair.isolate1.name,
                    'to': pair.isolate2.name,
                    'snp_distance': snp_distance
                })

        return transmission_links
```

#### Outbreak Investigation Tools
- **Phylogenetic analysis**: BEAST, RAxML for outbreak reconstruction
- **SNP-based clustering**: >95% similarity suggests clonal outbreak
- **Core genome MLST**: Standardized typing method
- **cgSNP analysis**: Single nucleotide polymorphism clustering

## Machine Learning Applications

### Resistance Prediction Models

#### Risk Prediction for Hospitals
```python
import sklearn.ensemble
import sklearn.model_selection

class AMR_Prediction_Model:
    def __init__(self, historical_data):
        self.features = [
            'antibiotic_usage_density',
            'hand_hygiene_compliance',
            'isolation_precautions_adherence',
            'prior_resistance_rates'
        ]

        self.target = 'resistance_rate_next_year'

    def train_predictive_model(self, X_train, y_train):
        """Train random forest model for resistance prediction"""

        rf_model = sklearn.ensemble.RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )

        # Cross-validation for model evaluation
        cv_scores = sklearn.model_selection.cross_val_score(
            rf_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error'
        )

        rf_model.fit(X_train, y_train)

        return rf_model, cv_scores

    def predict_future_resistance(self, current_hospital_data):
        """Predict future resistance rates"""

        predictions = self.model.predict(current_hospital_data)
        return predictions
```

#### Multi-Drug Resistance Classification
- **Binary classification**: Sensitive vs. resistant
- **Multi-class classification**: MIC interpretation categories
- **Multi-label classification**: Resistance to multiple antibiotics
- **Survival analysis**: Time to resistance development

### Image Recognition for AST
Using deep learning for automatic susceptibility testing:
- **Colony counting**: Automated optical density readings
- **Zone diameter measurement**: Disk diffusion interpretation
- **Growth curve analysis**: MIC determination
- **Morphological changes**: Resistance phenotype detection

## Interactive Dashboard Development

### Streamlit Dashboard Creation
```python
import streamlit as st
import plotly.express as px
import pandas as pd

class AMR_Dashboard:
    def __init__(self, surveillance_data):
        self.data = surveillance_data
        st.title("🦠 AMR Surveillance Dashboard")

    def create_resistance_trend_plot(self):
        """Create interactive resistance trend visualization"""

        fig = px.line(
            self.data,
            x='collection_date',
            y='resistance_percentage',
            color='antibiotic',
            facet_col='pathogen',
            title="AMR Trends Over Time"
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Resistance Rate (%)",
            legend_title="Antibiotic"
        )

        return fig

    def geographical_hotspot_map(self):
        """Create choropleth map of resistance rates"""

        fig = px.choropleth(
            self.data,
            locations='country_code',
            color='resistance_rate',
            hover_name='country',
            title="Global AMR Resistance Rates"
        )

        return fig

    def risk_factor_analysis(self):
        """Interactive risk factor visualization"""

        selected_factor = st.selectbox(
            "Select Risk Factor:",
            ['antibiotic_use', 'compliance', 'isolation', 'density']
        )

        fig = px.scatter(
            self.data,
            x=selected_factor,
            y='resistance_rate',
            color='hospital_type',
            size='isolate_count',
            trendline="ols"
        )

        return fig

# Dashboard usage
if __name__ == "__main__":
    dashboard = AMR_Dashboard(load_amr_data())

    # Resistance trends
    st.plotly_chart(dashboard.create_resistance_trend_plot())

    # Geographic visualization
    st.plotly_chart(dashboard.geographical_hotspot_map())

    # Risk factor analysis
    st.plotly_chart(dashboard.risk_factor_analysis())
```

## Session Exercises

### Exercise 1: Resistance Trend Analysis
**Case Study**: Hospital X has observed increasing vancomycin resistance in Enterococcus faecium over 5 years.

**Tasks**:
1. Calculate annual resistance rates and confidence intervals
2. Create a control chart to detect special cause variation
3. Perform time series analysis to identify trend and seasonality
4. Recommend interventions based on statistical findings

### Exercise 2: Outbreak Investigation
**Scenario**: A ward outbreak of ESBL-producing E. coli affecting 12 patients.

**Tasks**:
1. Calculate attack rates and person-time incidence
2. Construct an epidemic curve
3. Identify potential source based on temporal pattern
4. Recommend control measures based on epidemiological findings

### Exercise 3: Molecular Surveillance Analysis
**Data**: WGS data from 50 CRE isolates collected hospital-wide.

**Tasks**:
1. Perform core genome MLST analysis
2. Construct phylogenetic tree and transmission network
3. Identify transmission clusters (SNP threshold <10)
4. Recommend infection control interventions

### Exercise 4: Predictive Modeling
**Dataset**: 3-year hospital AMR surveillance data linked to antibiotic usage and compliance metrics.

**Tasks**:
1. Select appropriate features for resistance prediction model
2. Train and validate machine learning model
3. Identify highest impact modifiable risk factors
4. Present model-based intervention recommendations

## Advanced Topics

### Natural Language Processing for AMR Reports
```python
import spacy
import transformers

class AMR_Text_Analysis:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.clinical_ner = transformers.pipeline("ner",
                                               model="clinical-ner-model")

    def extract_resistance_patterns(self, microbiology_report):
        """Extract AMR information from unstructured text"""

        # Named entity recognition for resistance patterns
        entities = self.clinical_ner(microbiology_report)

        resistance_findings = {
            'pathogen': None,
            'resistance_profile': [],
            'susceptibility_profile': [],
            'inferred_mechanism': None
        }

        for entity in entities:
            if entity['entity_group'] == 'PATHOGEN':
                resistance_findings['pathogen'] = entity['word']
            elif entity['entity_group'] == 'RESISTANCE':
                resistance_findings['resistance_profile'].append(entity['word'])

        return resistance_findings
```

### Real-Time Surveillance Systems
- **Electronic Laboratory Reports (ELR)**: Automated surveillance
- **WHONET integration**: Standardized data collection
- **Dashboards with alerts**: Automated outlier detection
- **Mobile applications**: Field data collection

### Genomic Surveillance Networks

#### Integrated Datasets
- **GLASS ENSEMBLE**: Combining human, animal, environmental data
- **GAMMA**: Genomic AMR monitoring and research
- **COMPARE**: Clinical and molecular data integration

## Key Takeaways

### Essential Concepts
1. **Quality data is foundational** for meaningful AMR surveillance
2. **Statistical methods enable risk factor identification** and trend analysis
3. **Molecular epidemiology provides transmission insights** essential for control
4. **Machine learning enhances prediction and early detection**
5. **Interactive dashboards facilitate decision-making** at all levels

### Technical Skills Developed
- Hypothesis testing for resistance pattern analysis
- Multilevel modeling for complex surveillance data
- Machine learning model implementation and interpretation
- Dashboard development for stakeholder communication
- Genomic analysis pipeline utilization

### Future Directions
- **Real-time genomic surveillance** integrating with traditional systems
- **AI-driven outbreak prediction** and intervention optimization
- **Integrated One Health surveillance** platforms
- **Standardized global data sharing** frameworks

**The ability to analyze and interpret AMR data effectively is crucial for evidence-based policy development and intervention prioritization.**

### Recommended Resources
- **Statistical Methods for Disease Surveillance**: Comprehensive methodology
- **Molecular Epidemiology of Infectious Diseases**: Genomic analysis techniques
- **Applied Longitudinal Data Analysis**: Time series methods for surveillance
- **Machine Learning for Public Health**: Predictive modeling applications

### Next Session Preview
**Session 6: Infection Prevention and Control in AMR Management**
