"""
Antimicrobial Resistance Surveillance Models and Analytics

Comprehensive library for AMR surveillance, stewardship modeling,
and epidemiological analysis with interactive capabilities.

Author: Dr. Siddalingaiah H S
License: MIT
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans, DBSCAN
from imblearn.over_sampling import SMOTE
from imblearn.ensemble import BalancedRandomForestClassifier
import warnings
warnings.filterwarnings('ignore')

# Set style for all visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AMRSurveillanceAnalyzer:
    """
    Core analyzer for antimicrobial resistance surveillance data
    Supports WHO GLASS, EARS-Net, and country-level surveillance data
    """

    def __init__(self):
        """Initialize AMR surveillance analyzer"""
        self.data = None
        self.pathogens = []
        self.antibiotics = []
        self.time_periods = []

    def load_glass_data(self, data_path):
        """Load WHO GLASS surveillance data"""
        try:
            self.data = pd.read_csv(data_path)

            # Standardize column names to WHO GLASS format
            column_mapping = {
                'organism': 'pathogen',
                'antibiotic': 'antimicrobial',
                'resistance_rate': 'resistance_percentage',
                'country': 'country_name',
                'year': 'reporting_year',
                'sample_size': 'total_isolates'
            }
            self.data = self.data.rename(columns=column_mapping)

            # Extract unique values
            self.pathogens = self.data['pathogen'].unique().tolist()
            self.antibiotics = self.data['antimicrobial'].unique().tolist()
            self.time_periods = sorted(self.data['reporting_year'].unique())

            print(f"✅ Loaded WHO GLASS data: {len(self.data)} records")
            print(f"   Pathogens: {len(self.pathogens)}")
            print(f"   Antibiotics: {len(self.antibiotics)}")
            print(f"   Time periods: {len(self.time_periods)}")

            return True

        except Exception as e:
            print(f"❌ Error loading GLASS data: {e}")
            return False

    def calculate_resistance_trend(self, pathogen, antibiotic, region=None):
        """Calculate resistance trend over time for specific pathogen-drug combination"""

        # Filter data
        filtered_data = self.data[
            (self.data['pathogen'] == pathogen) &
            (self.data['antimicrobial'] == antibiotic)
        ]

        if region:
            filtered_data = filtered_data[filtered_data['country_name'] == region]

        if filtered_data.empty:
            return None, "No data available for specified combination"

        # Group by year and calculate weighted mean
        yearly_trends = self._calculate_weighted_resistance(filtered_data)

        return yearly_trends, None

    def _calculate_weighted_resistance(self, data):
        """Calculate weighted resistance rates by sample size"""

        yearly_stats = []

        for year in data['reporting_year'].unique():
            year_data = data[data['reporting_year'] == year]

            if year_data.empty:
                continue

            # Weighted mean
            total_isolates = year_data['total_isolates'].sum()
            if total_isolates > 0:
                weighted_resistance = (
                    year_data['resistance_percentage'] * year_data['total_isolates']
                ).sum() / total_isolates

                weighted_se = np.sqrt(
                    (year_data['total_isolates'] / total_isolates**2 * (
                        year_data['resistance_percentage'] * (100 - year_data['resistance_percentage'])
                    )).sum()
                ) / 100

            yearly_stats.append({
                'year': year,
                'resistance_rate': weighted_resistance,
                'standard_error': weighted_se,
                'sample_size': total_isolates,
                'ci_lower': max(0, weighted_resistance - 1.96 * weighted_se),
                'ci_upper': min(100, weighted_resistance + 1.96 * weighted_se)
            })

        return pd.DataFrame(yearly_stats).sort_values('year')

    def create_resistance_heatmap(self, pathogen_list=None, antibiotic_list=None):
        """Create resistance pattern heatmap"""

        if pathogen_list is None:
            pathogen_list = self.pathogens[:10]  # Top 10 pathogens
        if antibiotic_list is None:
            antibiotic_list = self.antibiotics[:10]  # Top 10 antibiotics

        # Calculate average resistance for each pathogen-antibiotic combination
        heatmap_data = []

        for pathogen in pathogen_list:
            row_data = {'Pathogen': pathogen}
            for antibiotic in antibiotic_list:
                subset = self.data[
                    (self.data['pathogen'] == pathogen) &
                    (self.data['antimicrobial'] == antibiotic)
                ]

                if not subset.empty:
                    avg_resistance = subset['resistance_percentage'].mean()
                    row_data[antibiotic] = avg_resistance
                else:
                    row_data[antibiotic] = None

            heatmap_data.append(row_data)

        return pd.DataFrame(heatmap_data).set_index('Pathogen')

    def predict_future_trends(self, pathogen, antibiotic, years_ahead=5):
        """Predict future AMR trends using time series analysis"""

        # Get historical data
        trends, error = self.calculate_resistance_trend(pathogen, antibiotic)
        if trends is None or len(trends) < 3:
            return None, "Insufficient data for prediction"

        # Prepare for forecasting
        trends = trends.dropna()
        X = trends['year'].values.reshape(-1, 1)
        y = trends['resistance_rate'].values

        # Fit polynomial trend
        try:
            z = np.polyfit(X.flatten(), y, 2)
            p = np.poly1d(z)

            # Predict future years
            future_years = np.array(range(trends['year'].max() + 1,
                                         trends['year'].max() + years_ahead + 1))

            predictions = p(future_years)

            # Ensure predictions are within bounds
            predictions = np.clip(predictions, 0, 100)

            results = pd.DataFrame({
                'year': future_years,
                'predicted_resistance': predictions,
                'prediction_type': 'forecast'
            })

            # Calculate prediction confidence intervals
            mse = np.mean((y - p(X.flatten())) ** 2)
            prediction_variance = mse * (1 + 1/len(X) + (future_years - np.mean(X))**2 / np.sum((X.flatten() - np.mean(X))**2))
            prediction_se = np.sqrt(prediction_variance)

            results['ci_lower'] = np.clip(results['predicted_resistance'] - 1.96 * prediction_se, 0, 100)
            results['ci_upper'] = np.clip(results['predicted_resistance'] + 1.96 * prediction_se, 0, 100)

            return results, None

        except Exception as e:
            return None, f"Prediction error: {e}"

    def create_resistance_treemap(self, threshold=20):
        """Create treemap visualization of high-priority AMR threats"""

        # Calculate average resistance for each combination
        summary_data = []
        for pathogen in self.pathogens:
            for antibiotic in self.antibiotics:
                subset = self.data[
                    (self.data['pathogen'] == pathogen) &
                    (self.data['antimicrobial'] == antibiotic)
                ]

                if len(subset) >= 3:  # At least 3 data points
                    avg_resistance = subset['resistance_percentage'].mean()
                    if avg_resistance >= threshold:
                        summary_data.append({
                            'pathogen': pathogen,
                            'antibiotic': antibiotic,
                            'avg_resistance': avg_resistance,
                            'data_points': len(subset)
                        })

        if not summary_data:
            return None, "No combinations meet threshold"

        return pd.DataFrame(summary_data), None


class StewardshipCalculator:
    """
    Antimicrobial Stewardship Impact Modeling and Simulation
    """

    def __init__(self):
        """Initialize stewardship calculator"""
        self.baseline_usage = {}
        self.interventions = {}
        self.outcomes = {}

    def set_baseline_usage(self, usage_data):
        """Set baseline antimicrobial usage patterns"""
        self.baseline_usage = usage_data

    def define_intervention(self, intervention_name, intervention_params):
        """
        Define stewardship intervention parameters

        Parameters:
        intervention_params: dict with keys:
        - 'usage_reduction': percentage reduction in usage
        - 'resistance_impact': expected change in resistance rates
        - 'cost_savings': financial impact
        - 'implementation_cost': upfront costs
        """

        self.interventions[intervention_name] = intervention_params

    def simulate_stewardship_impact(self, intervention_name, simulation_years=5):
        """Simulate impact of stewardship intervention over time"""

        if intervention_name not in self.interventions:
            return None, "Intervention not defined"

        params = self.interventions[intervention_name]

        # Simulate resistance rate changes
        resistance_trend = []
        usage_trend = []

        baseline_resistance = 30.0  # Starting point
        baseline_usage = 100.0  # Starting usage

        for year in range(simulation_years + 1):
            if year == 0:
                year_resistance = baseline_resistance
                year_usage = baseline_usage
            else:
                # Apply intervention effects
                usage_reduction = params.get('usage_reduction', 0) / 100
                resistance_impact = params.get('resistance_impact', 0)

                # Gradual usage reduction
                year_usage = baseline_usage * (1 - usage_reduction * year / simulation_years)

                # Resistance reduction (delayed effect)
                resistance_delay = 2  # Years delayed effect
                if year > resistance_delay:
                    year_resistance = baseline_resistance * (1 - abs(resistance_impact) * (year - resistance_delay) / simulation_years)
                else:
                    year_resistance = baseline_resistance

            resistance_trend.append({
                'year': year,
                'resistance_rate': max(0, year_resistance),
                'intervention': intervention_name
            })

            usage_trend.append({
                'year': year,
                'usage_rate': max(0, year_usage),
                'intervention': intervention_name
            })

        return {
            'resistance_trend': pd.DataFrame(resistance_trend),
            'usage_trend': pd.DataFrame(usage_trend),
            'parameters': params
        }, None

    def calculate_cost_benefit(self, intervention_name, hospital_size=500,
                              daily_bed_cost=1500, avg_length_stay=5):
        """Calculate cost-benefit analysis for stewardship intervention"""

        if intervention_name not in self.interventions:
            return None, "Intervention not defined"

        params = self.interventions[intervention_name]

        # Calculate benefits
        infections_prevented_yearly = params.get('infections_prevented', 100)
        bed_days_saved = infections_prevented_yearly * avg_length_stay
        cost_savings_hospital = bed_days_saved * daily_bed_cost

        # Calculate costs
        implementation_cost = params.get('implementation_cost', 50000)
        annual_maintenance = params.get('annual_cost', 25000)

        # ROI calculation
        net_benefit_year1 = cost_savings_hospital - annual_maintenance
        roi_year1 = (net_benefit_year1 / implementation_cost) * 100

        payback_period = implementation_cost / max(cost_savings_hospital, 1)

        return {
            'annual_cost_savings': cost_savings_hospital,
            'implementation_cost': implementation_cost,
            'annual_maintenance': annual_maintenance,
            'net_benefit_year1': net_benefit_year1,
            'roi_year1': roi_year1,
            'payback_period_years': payback_period
        }, None

    def compare_interventions(self, intervention_list):
        """Compare multiple stewardship interventions"""

        comparison_results = {}

        for intervention in intervention_list:
            results, error = self.simulate_stewardship_impact(intervention, 3)

            if results:
                # Extract 3-year outcomes
                resistance_end = results['resistance_trend'].iloc[-1]['resistance_rate']
                usage_end = results['usage_trend'].iloc[-1]['usage_rate']

                costs_benefits, _ = self.calculate_cost_benefit(intervention)

                comparison_results[intervention] = {
                    'resistance_rate_3yr': resistance_end,
                    'usage_rate_3yr': usage_end,
                    'annual_cost_savings': costs_benefits.get('annual_cost_savings', 0) if costs_benefits else 0,
                    'payback_years': costs_benefits.get('payback_period_years', float('inf')) if costs_benefits else float('inf')
                }

        return pd.DataFrame(comparison_results).T, None


class TransmissionNetworkAnalyzer:
    """
    Molecular epidemiology and transmission network analysis
    for antimicrobial resistance patterns
    """

    def __init__(self):
        """Initialize transmission network analyzer"""
        self.genetic_data = None
        self.metadata = None
        self.network = None

    def load_genetic_data(self, sequence_file, metadata_file=None):
        """Load genomic sequencing data and metadata"""

        try:
            # Load sequence data (FASTA format)
            from Bio import SeqIO
            sequences = {}
            for record in SeqIO.parse(sequence_file, "fasta"):
                sequences[record.id] = str(record.seq)

            # Load metadata if provided
            if metadata_file:
                metadata = pd.read_csv(metadata_file)
                self.metadata = metadata.set_index('isolate_id')
            else:
                # Create basic metadata
                self.metadata = pd.DataFrame(
                    index=list(sequences.keys()),
                    data={'pathogen_type': 'Unknown'}
                )

            self.genetic_data = sequences

            print(f"✅ Loaded {len(sequences)} genetic sequences")
            return True

        except Exception as e:
            print(f"❌ Error loading genetic data: {e}")
            return False

    def calculate_pairwise_distances(self, max_dist=50):
        """Calculate pairwise genetic distances between isolates"""

        if not self.genetic_data:
            return None, "No genetic data loaded"

        isolate_ids = list(self.genetic_data.keys())
        n_isolates = len(isolate_ids)

        # Initialize distance matrix
        distance_matrix = np.zeros((n_isolates, n_isolates))

        # Calculate pairwise Hamming distances
        for i in range(n_isolates):
            for j in range(i + 1, n_isolates):
                seq1 = self.genetic_data[isolate_ids[i]]
                seq2 = self.genetic_data[isolate_ids[j]]

                # Calculate Hamming distance
                distance = sum(c1 != c2 for c1, c2 in zip(seq1, seq2))
                distance_matrix[i, j] = distance
                distance_matrix[j, i] = distance

        # Create DataFrame for easier handling
        distance_df = pd.DataFrame(
            distance_matrix,
            index=isolate_ids,
            columns=isolate_ids
        )

        return distance_df, None

    def build_transmission_network(self, distance_threshold=5, similarity_threshold=0.99):
        """Build transmission network based on genetic similarity"""

        if self.genetic_data is None:
            return None, "No genetic data loaded"

        # Calculate pairwise distances
        distances, error = self.calculate_pairwise_distances()
        if distances is None:
            return None, error

        # Create NetworkX graph
        G = nx.Graph()

        # Add nodes with metadata
        for isolate_id in distances.index:
            metadata_dict = self.metadata.loc[isolate_id].to_dict() if isolate_id in self.metadata.index else {}
            G.add_node(isolate_id, **metadata_dict)

        # Add edges based on genetic distance
        for i, isolate1 in enumerate(distances.index):
            for j, isolate2 in enumerate(distances.columns):
                if i < j:  # Avoid duplicate edges
                    distance = distances.iloc[i, j]

                    # Create edge if distance within transmission threshold
                    if distance <= distance_threshold:
                        G.add_edge(isolate1, isolate2,
                                 genetic_distance=distance,
                                 transmission_likelihood=1 / (1 + distance))

        self.network = G

        print(f"✅ Built transmission network with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        return G, None

    def analyze_clusters(self, min_cluster_size=3):
        """Identify transmission clusters in the network"""

        if self.network is None:
            return None, "No transmission network available"

        # Find connected components
        clusters = []
        for component in nx.connected_components(self.network):
            if len(component) >= min_cluster_size:
                isolates = list(component)

                # Calculate cluster statistics
                cluster_data = {
                    'cluster_size': len(component),
                    'isolates': isolates,
                    'isolate_metadata': []
                }

                # Collect metadata for cluster members
                for isolate in isolates:
                    if isolate in self.metadata.index:
                        metadata = self.metadata.loc[isolate].to_dict()
                    else:
                        metadata = {'cluster_type': 'Unknown'}

                    cluster_data['isolate_metadata'].append(metadata)

                clusters.append(cluster_data)

        # Sort by cluster size
        clusters.sort(key=lambda x: x['cluster_size'], reverse=True)

        return clusters, None

    def calculate_network_centrality(self):
        """Calculate centrality measures for transmission network"""

        if self.network is None:
            return None, "No transmission network available"

        # Calculate various centrality measures
        degree_centrality = nx.degree_centrality(self.network)
        betweenness_centrality = nx.betweenness_centrality(self.network)
        closeness_centrality = nx.closeness_centrality(self.network)

        # Combine into DataFrame
        centrality_df = pd.DataFrame({
            'isolate_id': list(self.network.nodes()),
            'degree_centrality': [degree_centrality[node] for node in self.network.nodes()],
            'betweenness_centrality': [betweenness_centrality[node] for node in self.network.nodes()],
            'closeness_centrality': [closeness_centrality[node] for node in self.network.nodes()]
        })

        return centrality_df, None

    def predict_spread_patterns(self, initial_cases, time_steps=10):
        """Predict resistance spread patterns using network models"""

        if self.network is None:
            return None, "No transmission network available"

        # Convert initial infected cases to set
        infected = set(initial_cases)
        susceptible = set(self.network.nodes()) - infected

        spread_history = [list(infected)]

        for step in range(time_steps):
            new_infections = set()

            # For each infected node
            for infected_node in infected:
                # Get neighbors (transmission contacts)
                neighbors = set(self.network.neighbors(infected_node))

                # Remove already infected neighbors
                susceptible_neighbors = neighbors - infected

                # Probabilistic infection (simplified model)
                for neighbor in susceptible_neighbors:
                    infection_prob = self.network.edges[(infected_node, neighbor)]['transmission_likelihood']
                    if np.random.random() < infection_prob:
                        new_infections.add(neighbor)

            # Update infected set
            infected.update(new_infections)
            spread_history.append(list(infected))

        return spread_history, None


class AMRResistancePredictor:
    """
    Machine Learning Models for AMR Pattern Prediction
    """

    def __init__(self):
        """Initialize resistance prediction model"""
        self.model = None
        self.feature_scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_importance = None

    def prepare_training_data(self, surveillance_data):
        """Prepare surveillance data for ML training"""

        # Create features
        features = []

        # Encode categorical features
        for col in ['pathogen', 'antimicrobial', 'country_name']:
            if col in surveillance_data.columns:
                le = LabelEncoder()
                surveillance_data[f'{col}_encoded'] = le.fit_transform(surveillance_data[col])
                self.label_encoders[col] = le
                features.append(f'{col}_encoded')

        # Numeric features
        numeric_features = ['total_isolates', 'reporting_year', 'resistance_percentage']
        features.extend(numeric_features)

        # Rolling averages (temporal patterns)
        surveillance_data = surveillance_data.sort_values(['pathogen', 'antimicrobial', 'reporting_year'])

        # Target variable: Future resistance rate
        surveillance_data['future_resistance'] = surveillance_data.groupby(
            ['pathogen', 'antimicrobial']
        )['resistance_percentage'].shift(-1)

        # Remove rows without future values
        train_data = surveillance_data.dropna(subset=['future_resistance'])

        X = train_data[features]
        y = train_data['future_resistance']

        return X, y, train_data

    def train_prediction_model(self, X, y, model_type='random_forest'):
        """Train resistance prediction model"""

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Scale features
        X_train_scaled = self.feature_scaler.fit_transform(X_train)
        X_test_scaled = self.feature_scaler.transform(X_test)

        # Choose and train model
        if model_type == 'random_forest':
            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == 'gradient_boosting':
            model = GradientBoostingRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=6
            )

        model.fit(X_train_scaled, y_train)

        # Evaluate model
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"📊 Model Training Results:")
        print(f"   MSE: {mse:.4f}")
        print(f"   R²: {r2:.4f}")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")

        # Store feature importance
        if hasattr(model, 'feature_importances_'):
            self.feature_importance = dict(zip(X.columns, model.feature_importances_))

        self.model = model

        return model, {
            'mse': mse,
            'r2': r2,
            'feature_importance': self.feature_importance
        }

    def predict_future_resistance(self, new_data):
        """Predict resistance rates for new data"""

        if self.model is None:
            return None, "Model not trained"

        # Prepare new data (encode categorical features)
        processed_data = new_data.copy()

        for col in ['pathogen', 'antimicrobial', 'country_name']:
            if col in processed_data.columns and col in self.label_encoders:
                le = self.label_encoders[col]
                # Handle unseen categories
                processed_data[f'{col}_encoded'] = processed_data[col].apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )

        # Select features (same as training)
        features = []
        for encoder_name in self.label_encoders.keys():
            features.append(f'{encoder_name}_encoded')

        numeric_features = ['total_isolates', 'reporting_year', 'resistance_percentage']
        features.extend(numeric_features)

        available_features = [f for f in features if f in processed_data.columns]
        X = processed_data[available_features]

        # Scale features
        X_scaled = self.feature_scaler.transform(X)

        # Make predictions
        predictions = self.model.predict(X_scaled)

        # Add predictions to original data
        result_data = new_data.copy()
        result_data['predicted_future_resistance'] = predictions

        return result_data, None

    def identify_high_risk_combinations(self, predictions, threshold_percentile=80):
        """Identify high-risk pathogen-antibiotic combinations"""

        if predictions is None:
            return None, "No predictions available"

        # Calculate risk threshold
        threshold = np.percentile(predictions['predicted_future_resistance'], threshold_percentile)

        # Identify high-risk combinations
        high_risk = predictions[predictions['predicted_future_resistance'] >= threshold]

        # Group by pathogen-antibiotic combinations
        risk_summary = high_risk.groupby(['pathogen', 'antimicrobial']).agg({
            'predicted_future_resistance': ['mean', 'max', 'count'],
            'total_isolates': 'sum'
        }).round(2)

        return risk_summary, None


# Utility functions for data processing
def calculate_eucast_interpretation(mic_value, breakpoint):
    """
    Determine EUCAST interpretation for MIC value against breakpoint
    """
    if mic_value <= breakpoint['susceptible']:
        return 'S'  # Susceptible
    elif mic_value > breakpoint['resistant']:
        return 'R'  # Resistant
    else:
        return 'I'  # Intermediate

def format_resistance_data(data):
    """
    Format raw lab data to standardized AMR format
    """
    formatted_data = []

    for _, row in data.iterrows():
        formatted_entry = {
            'pathogen': row.get('organism', row.get('pathogen', 'Unknown')),
            'antimicrobial': row.get('antibiotic', row.get('antimicrobial', 'Unknown')),
            'mic_value': row.get('mic', row.get('mic_value')),
            'interpretation': row.get('interpretation', row.get('susceptibility')),
            'sample_date': row.get('date', row.get('collection_date')),
            'hospital_id': row.get('hospital', row.get('facility')),
            'patient_age': row.get('age'),
            'ward_type': row.get('ward', row.get('department')),
            'empirical_regimen': row.get('treatment_before_culture')
        }
        formatted_data.append(formatted_entry)

    return pd.DataFrame(formatted_data)


# Export main classes for easy importing
__all__ = [
    'AMRSurveillanceAnalyzer',
    'StewardshipCalculator',
    'TransmissionNetworkAnalyzer',
    'AMRResistancePredictor',
    'calculate_eucast_interpretation',
    'format_resistance_data'
]


if __name__ == "__main__":
    # Example usage demonstration
    print("🦠 Antimicrobial Resistance Surveillance Models")
    print("=" * 50)

    # Example: Load and analyze GLASS data
    analyzer = AMRSurveillanceAnalyzer()
    print("AMR Surveillance Analyzer initialized")

    # Example: Stewardship calculator
    calculator = StewardshipCalculator()

    # Define example interventions
    calculator.define_intervention(
        'Antibiotic_Timeout',
        {
            'usage_reduction': 15,
            'resistance_impact': -0.2,
            'implementation_cost': 30000,
            'annual_cost': 15000,
            'infections_prevented': 75
        }
    )

    print("Stewardship Calculator initialized with example intervention")

    # Example: Cost-benefit analysis
    costs_benefits, _ = calculator.calculate_cost_benefit('Antibiotic_Timeout')
    if costs_benefits:
        print(".2f"
              ".1f")

    print("\n✅ AMR Models ready for use")
