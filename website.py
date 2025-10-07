"""
Antimicrobial Resistance Interactive Educational Platform

A comprehensive Streamlit-based application for AMR education, featuring:
- Interactive resistance pattern visualizations
- Stewardship impact calculators
- Global AMR dashboard with WHO GLASS data
- Molecular epidemiology tools
- Training modules and exercises

Author: Dr. Siddalingaiah H S
License: MIT
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Import custom AMR analysis modules
from Scripts.amr_surveillance_models import (
    AMRSurveillanceAnalyzer,
    StewardshipCalculator,
    TransmissionNetworkAnalyzer,
    calculate_eucast_interpretation
)

# Set page configuration
st.set_page_config(
    page_title="AMR Workshop Platform",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional appearance
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1em;
    }
    .section-header {
        color: #ff7f0e;
        font-size: 1.8em;
        font-weight: bold;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1em;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 1em;
        margin: 1em 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""

    # Sidebar navigation
    st.sidebar.image("https://www.who.int/images/default-source/imported/amr-amr-cycle.png?sfvrsn=2c4b56b6_1", width=150)
    st.sidebar.title("🦠 AMR Workshop Platform")

    # Navigation menu
    page = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Dashboard", "📊 Surveillance Analysis", "💊 Stewardship Calculator",
         "🕸️ Transmission Modeling", "📚 Training Modules", "❓ Quiz Assessment"]
    )

    # Main content display
    if page == "🏠 Dashboard":
        display_dashboard()
    elif page == "📊 Surveillance Analysis":
        display_surveillance_analysis()
    elif page == "💊 Stewardship Calculator":
        display_stewardship_calculator()
    elif page == "🕸️ Transmission Modeling":
        display_transmission_modeling()
    elif page == "📚 Training Modules":
        display_training_modules()
    else:  # Quiz Assessment
        display_quiz_assessment()

def display_dashboard():
    """Main dashboard with AMR overview and key metrics"""

    st.markdown('<h1 class="main-header">🦠 Antimicrobial Resistance Workshop Platform</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive Educational Tools for AMR Surveillance, Stewardship,& Prevention")

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Annual Global Deaths", "700,000", "+10% vs 2019")
    with col2:
        st.metric("Projected Deaths 2050", "10 million", "2.5× increase")
    with col3:
        st.metric("Economic Cost", "$1 trillion", "$300B annually")
    with col4:
        st.metric("AMR Priority Pathogens", "12", "WHO 2024 list")

    # Global overview section
    st.markdown('<h2 class="section-header">🌍 Global AMR Overview</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # WHO priority pathogens chart
        pathogens = ['E. coli', 'S. aureus', 'K. pneumoniae', 'S. pneumoniae',
                    'A. baumannii', 'P. aeruginosa']
        deaths = [95000, 80000, 68000, 49000, 43000, 38000]
        amr_rates = [13.3, 32.1, 24.4, 21.4, 78.7, 18.4]

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(x=pathogens, y=deaths, name="Annual Deaths"),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(x=pathogens, y=amr_rates, name="AMR Rate (%)",
                      mode='lines+markers', line=dict(color='red')),
            secondary_y=True
        )

        fig.update_layout(title="WHO Priority Pathogens: Deaths vs AMR Rates",
                         xaxis_tickangle=-45)
        fig.update_yaxes(title_text="Annual Deaths", secondary_y=False)
        fig.update_yaxes(title_text="AMR Rate (%)", secondary_y=True)

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Regional AMR burden
        regions = ['Africa', 'SE Asia', 'Eastern Med', 'Europe', 'Americas', 'Western Pacific']
        burden = [25, 23, 18, 15, 12, 8]  # Percentage of global AMR burden

        fig = go.Figure(data=[go.Pie(labels=regions, values=burden, pull=[0.1, 0, 0, 0, 0, 0])])
        fig.update_layout(title="Regional Distribution of AMR Burden")

        st.plotly_chart(fig, use_container_width=True)

    # Key resistance mechanisms
    st.markdown('<h3 class="section-header">🔬 Key Resistance Mechanisms</h3>', unsafe_allow_html=True)

    mechanisms = {
        'β-lactamases': 'Enzymatic degradation of penicillins/cephalosporins',
        'Efflux Pumps': 'Active removal of antibiotics from bacterial cells',
        'Target Site Modification': 'Altered penicillin-binding proteins (MRSA)',
        'Permeability Changes': 'Reduced antibiotic entry into bacterial cells',
        'Plasmid-mediated Transfer': 'Horizontal gene transfer between bacteria'
    }

    cols = st.columns(len(mechanisms))
    for i, (mech, desc) in enumerate(mechanisms.items()):
        with cols[i]:
            st.markdown(f"**{mech}**")
            st.caption(desc)

    # Interactive map will be added in surveillance section
    st.info("🔍 Click on 'Surveillance Analysis' to explore resistance patterns by region and pathogen.")

def display_surveillance_analysis():
    """Interactive AMR surveillance analysis tools"""

    st.markdown('<h2 class="section-header">📊 AMR Surveillance Analysis Platform</h2>', unsafe_allow_html=True)

    # Sample data generation for demonstration
    @st.cache_data
    def generate_sample_data():
        """Generate realistic AMR surveillance data for demonstration"""
        np.random.seed(42)

        # Pathogens and antibiotics
        pathogens = ['E. coli', 'K. pneumoniae', 'S. aureus', 'P. aeruginosa',
                    'A. baumannii', 'S. pneumoniae', 'Enterococcus spp.']
        antibiotics = ['Ciprofloxacin', 'Ceftriaxone', 'Meropenem', 'Vancomycin',
                      'Amoxicillin', 'Gentamicin', 'Colistin']

        # Regions
        regions = ['North America', 'South America', 'Europe', 'Africa',
                  'Asia', 'Middle East', 'Australia']

        # Generate synthetic data
        data = []
        for pathogen in pathogens:
            for antibiotic in antibiotics:
                for region in regions:
                    for year in [2020, 2021, 2022, 2023]:
                        # Generate realistic resistance rates
                        base_rate = np.random.uniform(5, 30)
                        region_modifier = {'Africa': 15, 'Asia': 12, 'Europe': -5,
                                         'North America': 0, 'South America': 8}[region.split()[0]]
                        year_modifier = (year - 2020) * 2  # slight upward trend

                        resistance_rate = min(95, max(2, base_rate + region_modifier + year_modifier +
                                                     np.random.normal(0, 5)))

                        data.append({
                            'pathogen': pathogen,
                            'antimicrobial': antibiotic,
                            'country_name': region,
                            'reporting_year': year,
                            'resistance_percentage': round(resistance_rate, 1),
                            'total_isolates': np.random.randint(50, 500),
                            'confidence_interval_lower': max(0, resistance_rate - np.random.uniform(3, 8)),
                            'confidence_interval_upper': min(100, resistance_rate + np.random.uniform(3, 8))
                        })

        return pd.DataFrame(data)

    # Load or generate data
    try:
        df = generate_sample_data()
    except:
        st.error("Unable to load surveillance data. Please check data sources.")
        return

    # Interactive filters
    st.markdown("### 🔍 Interactive AMR Surveillance Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_pathogen = st.selectbox(
            "Select Pathogen:",
            options=df['pathogen'].unique(),
            index=0
        )

    with col2:
        selected_antibiotic = st.selectbox(
            "Select Antibiotic:",
            options=df['antimicrobial'].unique(),
            index=0
        )

    with col3:
        selected_year = st.selectbox(
            "Select Year:",
            options=sorted(df['reporting_year'].unique()),
            index=-1
        )

    # Filter data based on selections
    filtered_data = df[
        (df['pathogen'] == selected_pathogen) &
        (df['antimicrobial'] == selected_antibiotic) &
        (df['reporting_year'] == selected_year)
    ]

    # Display results
    if not filtered_data.empty:
        # Key metrics
        avg_resistance = filtered_data['resistance_percentage'].mean()
        max_resistance = filtered_data['resistance_percentage'].max()
        regions_high_risk = filtered_data[
            filtered_data['resistance_percentage'] > 25
        ]['country_name'].tolist()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Average Resistance", f"{avg_resistance:.1f}%")
        with col2:
            st.metric("Highest Resistance", f"{max_resistance:.1f}%")
        with col3:
            st.metric("High-Risk Regions", len(regions_high_risk))

        # Regional comparison chart
        fig = px.bar(
            filtered_data,
            x='country_name',
            y='resistance_percentage',
            title=f'{selected_pathogen} Resistance to {selected_antibiotic} ({selected_year})',
            labels={'country_name': 'Region', 'resistance_percentage': 'Resistance Rate (%)'},
            color='resistance_percentage',
            color_continuous_scale='Reds'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Risk categorization
        st.markdown("### 🚨 Risk Assessment")

        categories = []
        for idx, row in filtered_data.iterrows():
            rate = row['resistance_percentage']
            if rate < 15:
                risk = "🔵 Low Risk"
            elif rate < 25:
                risk = "🟡 Medium Risk"
            else:
                risk = "🔴 High Risk"

            categories.append({
                'Region': row['country_name'],
                'Resistance Rate': f"{rate:.1f}%",
                'Risk Level': risk,
                'Sample Size': row['total_isolates']
            })

        risk_df = pd.DataFrame(categories)
        st.dataframe(risk_df, use_container_width=True)

    else:
        st.warning("No data available for selected combination. Try different parameters.")

    # Additional analysis tools
    st.markdown("---")
    st.markdown("### 📈 Temporal Trends Analysis")

    # Year comparison
    trend_years = st.multiselect(
        "Select years to compare:",
        options=sorted(df['reporting_year'].unique()),
        default=sorted(df['reporting_year'].unique())[-3:]  # Last 3 years
    )

    if trend_years and selected_pathogen and selected_antibiotic:
        trend_data = df[
            (df['pathogen'] == selected_pathogen) &
            (df['antimicrobial'] == selected_antibiotic) &
            (df['reporting_year'].isin(trend_years))
        ]

        if not trend_data.empty:
            # Group by year and region
            year_region_avg = trend_data.groupby(['reporting_year', 'country_name'])['resistance_percentage'].mean().reset_index()

            fig = px.line(
                year_region_avg,
                x='reporting_year',
                y='resistance_percentage',
                color='country_name',
                title=f'{selected_pathogen} Resistance Trends to {selected_antibiotic}',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

            # Trend analysis
            st.markdown("#### Trend Analysis")
            for region in year_region_avg['country_name'].unique():
                region_data = year_region_avg[year_region_avg['country_name'] == region]
                if len(region_data) > 1:
                    change = region_data['resistance_percentage'].iloc[-1] - region_data['resistance_percentage'].iloc[0]
                    trend = "↑ Increasing" if change > 2 else "↓ Decreasing" if change < -2 else "→ Stable"
                    st.write(f"**{region}**: {change:+.1f}% change ({trend})")

def display_stewardship_calculator():
    """Interactive antibiotic stewardship impact calculator"""

    st.markdown('<h2 class="section-header">💊 Antibiotic Stewardship Impact Calculator</h2>', unsafe_allow_html=True)

    st.markdown("""
    This calculator helps you model the impact of different antimicrobial stewardship interventions
    on resistance rates, antibiotic usage patterns, and clinical outcomes.
    """)

    # Intervention selection
    interventions = {
        'Post-Prescription Antibiotic Review': {
            'usage_reduction': 20,
            'resistance_impact': -0.15,
            'implementation_cost': 25000,
            'annual_cost': 12000,
            'infections_prevented': 80
        },
        'Computerized Decision Support System': {
            'usage_reduction': 25,
            'resistance_impact': -0.2,
            'implementation_cost': 75000,
            'annual_cost': 18000,
            'infections_prevented': 120
        },
        'Prospective Audit and Feedback': {
            'usage_reduction': 30,
            'resistance_impact': -0.25,
            'implementation_cost': 40000,
            'annual_cost': 25000,
            'infections_prevented': 150
        },
        'Formulary Restriction Programs': {
            'usage_reduction': 35,
            'resistance_impact': -0.3,
            'implementation_cost': 15000,
            'annual_cost': 8000,
            'infections_prevented': 100
        },
        'Antibiotic Time-Out Protocol': {
            'usage_reduction': 28,
            'resistance_impact': -0.22,
            'implementation_cost': 10000,
            'annual_cost': 6000,
            'infections_prevented': 95
        }
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔧 Intervention Parameters")
        selected_intervention = st.selectbox(
            "Select Stewardship Intervention:",
            options=list(interventions.keys())
        )

        # Customize parameters if needed
        customize = st.checkbox("Customize parameters")
        if customize:
            params = interventions[selected_intervention].copy()
            st.markdown("#### Baseline Parameters:")
            for key, value in params.items():
                if key in ['usage_reduction', 'resistance_impact']:
                    params[key] = st.slider(
                        f"{key.replace('_', ' ').title()}:",
                        min_value=-50, max_value=50, value=int(value*100)
                    ) / 100
                elif 'cost' in key:
                    params[key] = st.number_input(
                        f"{key.replace('_', ' ').title()}: $",
                        min_value=0, value=value, step=1000
                    )
                else:  # infections_prevented
                    params[key] = st.number_input(
                        f"{key.replace('_', ' ').title()}:",
                        min_value=0, value=value, step=10
                    )
        else:
            params = interventions[selected_intervention]

        # Hospital size input
        hospital_size = st.slider("Hospital Size (beds):", 100, 2000, 500)
        daily_bed_cost = st.number_input("Daily Bed Cost ($):", 1000, 3000, 1500)
        avg_length_stay = st.slider("Average Length of Stay for AMR Infections (days):", 2, 20, 5)

    with col2:
        # Results display
        st.markdown("### 📊 Impact Projections")

        calculator = StewardshipCalculator()
        cost_benefits, error = calculator.calculate_cost_benefit(
            "custom" if customize else selected_intervention,
            hospital_size=hospital_size,
            daily_bed_cost=daily_bed_cost,
            avg_length_stay=avg_length_stay
        )

        if cost_benefits:
            # Key metrics
            savings_per_year = cost_benefits['annual_cost_savings']
            implementation_cost = cost_benefits['implementation_cost']
            payback_period = cost_benefits['payback_period_years']
            roi_yr1 = cost_benefits['roi_year1']

            # Display metrics
            col2a, col2b = st.columns(2)

            with col2a:
                st.metric("Annual Cost Savings", f"${savings_per_year:,.0f}")
                st.metric("Payback Period", f"{payback_period:.1f} years")

            with col2b:
                st.metric("Implementation Cost", f"${implementation_cost:,.0f}")
                st.metric("ROI (Year 1)", f"{roi_yr1:.1f}%")

            # Impact projection over time
            st.markdown("#### 📈 5-Year Impact Projection")

            simulation_years = 5
            resistance_trend = []
            usage_trend = []

            baseline_resistance = 25.0  # 25% baseline resistance
            baseline_usage = 100.0     # 100 DDD/1000 patient-days

            for year in range(simulation_years + 1):
                if year == 0:
                    res_rate = baseline_resistance
                    usage_rate = baseline_usage
                else:
                    # Apply intervention effects (gradual implementation)
                    reduction_factor = 1 - (params['usage_reduction']/100) * min(1, year/2)
                    usage_rate = baseline_usage * reduction_factor

                    # Resistance reduction (delayed by 1 year)
                    if year >= 2:
                        res_reduction = abs(params['resistance_impact']) * (year-1) / simulation_years
                        res_rate = baseline_resistance * (1 - res_reduction)
                    else:
                        res_rate = baseline_resistance

                resistance_trend.append(res_rate)
                usage_trend.append(usage_rate)

            # Plot trends
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Scatter(x=list(range(simulation_years+1)), y=resistance_trend,
                          name="Resistance Rate (%)", line=dict(color='red')),
                secondary_y=False
            )

            fig.add_trace(
                go.Scatter(x=list(range(simulation_years+1)), y=usage_trend,
                          name="Antibiotic Usage", line=dict(color='blue')),
                secondary_y=True
            )

            fig.update_layout(title=f"Projected Impact of {selected_intervention}")
            fig.update_xaxes(title_text="Year")
            fig.update_yaxes(title_text="Resistance Rate (%)", secondary_y=False)
            fig.update_yaxes(title_text="Usage (DDD/1000 patient-days)", secondary_y=True)

            st.plotly_chart(fig, use_container_width=True)

    # Comparison section
    st.markdown("---")
    st.markdown("### 🔄 Intervention Comparison")

    compare = st.checkbox("Compare selected intervention with others")

    if compare:
        comparison_data = {}
        interventions_to_compare = list(interventions.keys())
        interventions_to_compare.append(selected_intervention if customize else None)
        interventions_to_compare = list(set([i for i in interventions_to_compare if i]))

        for intervention in interventions_to_compare:
            results, _ = calculator.simulate_stewardship_impact(intervention, 3)
            if results:
                cost_benefits, _ = calculator.calculate_cost_benefit(intervention)
                if cost_benefits:
                    comparison_data[intervention] = {
                        'resistance_reduction': baseline_resistance - results['resistance_trend'].iloc[-1]['resistance_rate'],
                        'usage_reduction_3yr': baseline_usage - results['usage_trend'].iloc[-1]['usage_rate'],
                        'annual_cost_savings': cost_benefits['annual_cost_savings'],
                        'payback_years': cost_benefits['payback_period_years']
                    }

        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data).T.round(2)
            st.dataframe(comparison_df, use_container_width=True)

            # Best recommendations
            best_cost_savings = comparison_df['annual_cost_savings'].idxmax()
            quickest_payback = comparison_df['payback_years'].idxmin()
            most_resistance_reduction = comparison_df['resistance_reduction'].idxmax()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.success(f"💰 Best Cost Savings: {best_cost_savings}")
            with col2:
                st.info(f"⏱️ Quickest Payback: {quickest_payback}")
            with col3:
                st.warning(f"🦠 Most Resistance Reduction: {most_resistance_reduction}")

def display_transmission_modeling():
    """Molecular epidemiology and transmission network analysis"""

    st.markdown('<h2 class="section-header">🕸️ Molecular Epidemiology & Transmission Modeling</h2>', unsafe_allow_html=True)

    st.markdown("""
    Explore how antimicrobial resistance spreads through bacterial populations using
    molecular epidemiology tools and network analysis methods.
    """)

    # Upload or generate sample genomic data
    st.markdown("### 🧬 Genomic Data Input")

    data_type = st.radio("", ["Use Sample Data", "Upload Custom Data"])

    if data_type == "Upload Custom Data":
        fasta_file = st.file_uploader("Upload FASTA sequence file (.fasta)", type=['fasta'])
        metadata_file = st.file_uploader("Upload metadata CSV (.csv)", type=['csv'])

        if fasta_file and metadata_file:
            st.success("Files uploaded successfully!")
            # Here we would process the real data
    else:
        st.info("Using sample genomic data for demonstration")

        # Generate sample transmission data
        @st.cache_data
        def generate_sample_network():
            """Generate sample transmission network data"""
            np.random.seed(42)

            # Create sample isolates and connections
            n_isolates = 50
            isolates = [f"Isolate_{i+1:02d}" for i in range(n_isolates)]

            # Create random transmission edges
            edges = []
            for i in range(n_isolates):
                # Each isolate connects to 1-3 others on average
                n_connections = np.random.poisson(2) + 1
                connections = np.random.choice(
                    isolates, size=min(n_connections, n_isolates-1),
                    replace=False
                )

                for other_isolate in connections:
                    if other_isolate != isolates[i]:
                        # Genetic distance based on sequence similarity
                        genetic_dist = np.random.uniform(2, 15)
                        transmission_prob = max(0.1, 1 - genetic_dist/20)

                        edges.append({
                            'source': isolates[i],
                            'target': other_isolate,
                            'genetic_distance': genetic_dist,
                            'transmission_probability': transmission_prob,
                            'pathogen': np.random.choice(['S. aureus', 'E. coli', 'K. pneumoniae'])
                        })

            return pd.DataFrame(edges)

        network_data = generate_sample_network()

        st.markdown("### 📊 Network Analysis Results")

        # Network statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Isolates", len(network_data['source'].unique()))
        with col2:
            st.metric("Genetic Distances", ".1f")
        with col3:
            st.metric("Transmission Links", len(network_data))

        # Interactive network visualization
        import networkx as nx

        # Create NetworkX graph
        G = nx.Graph()
        for _, row in network_data.iterrows():
            G.add_edge(row['source'], row['target'],
                      genetic_distance=row['genetic_distance'],
                      transmission_probability=row['transmission_probability'],
                      pathogen=row['pathogen'])

        # Calculate centrality measures
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)

        # Visualization
        pos = nx.spring_layout(G, seed=42)

        # Create edge trace
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        node_size = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

            # Node properties
            degree = G.degree(node)
            betweenness = betweenness_centrality[node]

            node_text.append(f"Isolate: {node}<br>Degree: {degree}<br>Centrality: {betweenness:.3f}")
            node_size.append(10 + degree * 5)
            node_color.append(betweenness)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                showscale=True,
                colorscale='YlOrRd',
                reversescale=True,
                color=node_color,
                size=node_size,
                colorbar=dict(
                    thickness=15,
                    title='Betweenness<br>Centrality',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        # Create the figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='AMR Transmission Network',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )

        st.plotly_chart(fig, use_container_width=True)

        # Key isolates analysis
        st.markdown("### 🎯 Key Isolates Analysis")

        # Most central isolates
        central_isolates = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]

        st.markdown("**Top 5 Most Connected Isolates:**")
        for isolate, centrality in central_isolates:
            st.markdown(f"- **{isolate}**: {centrality:.3f} (Degree centrality)")

        # Cluster analysis
        if len(G.edges()) > 0:
            clusters = list(nx.connected_components(G))
            n_clusters = len(clusters)

            st.markdown(f"\n**Network Structure:** {n_clusters} transmission clusters identified")
            cluster_sizes = [len(cluster) for cluster in clusters]
            st.markdown(f"Cluster sizes: {sorted(cluster_sizes, reverse=True)}")

def display_training_modules():
    """Interactive training modules with quizzes and case studies"""

    st.markdown('<h2 class="section-header">📚 AMR Training Modules</h2>', unsafe_allow_html=True)

    module = st.selectbox(
        "Select Training Module:",
        ["AMR Basics", "Clinical Decision Making", "Laboratory Diagnosis",
         "Infection Prevention", "Policy & Economics", "One Health Approach"]
    )

    if module == "AMR Basics":
        st.markdown("""
        ### 🦠 Antimicrobial Resistance Fundamentals

        #### Key Learning Objectives:
        - Understand bacterial resistance mechanisms
        - Recognize risk factors for AMR development
        - Identify appropriate antibiotic selection principles

        #### Interactive Case Study:
        """)

        # Simple case study interaction
        case_progression = st.radio(
            "Patient case: 65-year-old male with community-acquired pneumonia. Initial treatment with amoxicillin failed. What next?",
            ["Switch to ciprofloxacin", "Culture and susceptibility testing", "Add vancomycin"]
        )

        if case_progression == "Culture and susceptibility testing":
            st.success("✅ Correct! Empirical therapy changes require microbiology confirmation")
        else:
            st.info("💡 Consider microbiology-guided therapy for treatment failures")

    elif module == "Clinical Decision Making":
        st.markdown("""
        ### 💊 Clinical Decision Support for AMR

        #### Decision Framework:
        1. **Patient History**: Recent antibiotic exposure? Hospitalized recently?
        2. **Local Prevalence**: What resistance patterns exist locally?
        3. **Antibiotic Selection**: Narrowest spectrum for shortest duration
        4. **Monitoring**: Clinical response and microbiology follow-up
        """)

        # Interactive decision tree
        st.markdown("#### 📋 Patient Assessment Tool")

        age = st.slider("Patient Age:", 0, 100, 50)
        hospitalization = st.checkbox("Recent Hospitalization (<30 days)")
        antibiotic_history = st.checkbox("Antibiotic use in last 3 months")
        infection_type = st.selectbox("Infection Type:", ["UTI", "Pneumonia", "Skin/Soft Tissue", "Intra-abdominal"])

        # Risk calculation
        risk_score = 0
        risk_score += (1 if age > 65 else 0)
        risk_score += (2 if hospitalization else 0)
        risk_score += (1 if antibiotic_history else 0)

        if risk_score >= 2:
            risk_level = "🔴 High Risk - Consider broad-spectrum with microbiological confirmation"
        elif risk_score == 1:
            risk_level = "🟡 Medium Risk - Microbiological testing recommended"
        else:
            risk_level = "🟢 Low Risk - Empirical therapy may be appropriate"

        st.metric("AMR Risk Assessment", risk_level)
        st.caption(f"Risk Score: {risk_score}/4 based on patient factors")

    # Add more modules as needed...

def display_quiz_assessment():
    """Interactive quiz assessment platform"""

    st.markdown('<h2 class="section-header">❓ AMR Knowledge Assessment</h2>', unsafe_allow_html=True)

    # Simple quiz implementation
    questions = [
        {
            "question": "What is the primary mechanism of methicillin-resistant Staphylococcus aureus (MRSA)?",
            "options": ["Efflux pumps", "Target site modification", "Enzymatic degradation", "Plasma membrane changes"],
            "correct": 1,
            "explanation": "MRSA develops resistance through altered penicillin-binding proteins (PBP2a) in the bacterial cell wall."
        },
        {
            "question": "Which antibiotic class is considered 'last resort' for carbapenem-resistant infections?",
            "options": ["Tetracyclines", "Colistin (polymyxin)", "Trimethoprim-sulfamethoxazole", "Nitrofurantoin"],
            "correct": 1,
            "explanation": "Colistin (polymyxin) is considered a last resort antibiotic due to its toxicity and limited alternatives."
        },
        {
            "question": "What WHO strategy phase are we currently in for antimicrobial resistance?",
            "options": ["Awareness", "Action", "Containment", "Prevention"],
            "correct": 1,
            "explanation": "The WHO Global Action Plan has three phases: Awareness (2015-2020), Action (2021-2025), and Containment (2026-2030)."
        }
    ]

    # Quiz interface
    score = 0
    total_questions = len(questions)

    for i, q in enumerate(questions):
        st.markdown(f"**Question {i+1}:** {q['question']}")

        user_answer = st.radio(
            f"Select your answer:",
            q['options'],
            key=f"q{i}"
        )

        if st.button(f"Check Answer {i+1}", key=f"btn{i}"):
            correct_answer = q['options'][q['correct']]
            if user_answer == correct_answer:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer is: {correct_answer}")

            st.info(f"💡 {q['explanation']}")
            st.markdown("---")

    if st.button("Calculate Final Score"):
        percentage = (score / total_questions) * 100
        st.metric("Quiz Score", f"{score}/{total_questions} ({percentage:.1f}%)")

        if percentage >= 80:
            st.success("🎉 Excellent! You demonstrate strong AMR knowledge.")
        elif percentage >= 60:
            st.info("👍 Good effort! Review key concepts for deeper understanding.")
        else:
            st.warning("📚 Additional study recommended. Focus on AMR mechanisms and stewardship.")

if __name__ == "__main__":
    main()
