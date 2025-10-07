# Session 6: Infection Prevention and Control in AMR Management

## Learning Objectives
By the end of this session, participants will be able to:
- Understand the core principles of infection prevention and control (IPC)
- Implement evidence-based strategies to prevent healthcare-associated infections
- Apply bundle interventions for high-risk procedures
- Design and evaluate hand hygiene improvement programs
- Utilize surveillance systems for HAIs and AMR transmission
- Integrate IPC into antimicrobial stewardship programs

## Core Principles of Infection Prevention & Control

### Chain of Infection Model
```
Infectious Agent ←→ Reservoir ←→ Portal of Exit ←→ Mode of Transmission ←→ Portal of Entry ←→ Susceptible Host
```

#### Breaking the Chain: AMR-Specific Interventions
- **Antimicrobial-resistant organisms** as the infectious agent
- **Colonized patients and environment** as reservoirs
- **Fecal-oral, respiratory, contact transmission** as primary modes
- **Healthcare workers and visitors** as vectors
- **Compromised patients** as susceptible hosts

### Healthcare-Associated Infections (HAIs)

#### Classification and Burden
```
Major HAI Categories:
├── Urinary Tract Infections (30-40% of HAIs)
├── Surgical Site Infections (20-30%)
├── Bloodstream Infections (10-20%)
├── Pneumonia (10-15%)
└── Skin and Soft Tissue Infections (5-10%)

AMR Impact on HAI Burden:
- CRE bacteremia: Attributable mortality 40-60%
- MRSA surgical site infection: Length of stay +10-14 days
- VRE bloodstream infection: Cost increase $10,000-40,000
- C. difficile infection: Recurrence rate 20-30% after treatment
```

#### Risk Factors for HAI Acquisition
```
Patient Factors:
├── Advanced age (>65 years)
├── Immunocompromised state
├── Severe underlying disease
├── Prior antibiotic exposure
├── Prolonged hospitalization (>7 days)
└── Invasive medical devices

Healthcare Factors:
├── High patient-to-staff ratios
├── Poor hand hygiene compliance (<60%)
├── Inadequate environmental cleaning
├── Overcrowding and understaffing
└── Lack of isolation facilities
```

## Hand Hygiene: Cornerstone of IPC

### WHO Five Moments for Hand Hygiene
```python
class HandHygieneCompliance:
    def __init__(self):
        self.moments = {
            1: "Before touching a patient",
            2: "Before clean/aseptic procedure",
            3: "After body fluid exposure risk",
            4: "After touching a patient",
            5: "After touching patient surroundings"
        }

        self.indications_by_moment = {
            1: ["patient contact"],
            2: ["injection", "blood sampling", "IV insertion"],
            3: ["blood/body fluid contact"],
            4: ["patient contact"],
            5: ["bed rails", "medical equipment", "bedside table"]
        }

    def calculate_moment_compliance(self, ward_data):
        """Calculate hand hygiene compliance by moment"""

        compliance_rates = {}
        for moment in self.moments:
            observed_opportunities = ward_data[f'moment_{moment}_opportunities']
            performed_actions = ward_data[f'moment_{moment}_performed']

            if observed_opportunities > 0:
                compliance_rates[moment] = (performed_actions / observed_opportunities) * 100
            else:
                compliance_rates[moment] = 0

        # Overall compliance (weighted average)
        total_opportunities = sum(ward_data[f'moment_{i}_opportunities'] for i in self.moments)
        total_performed = sum(ward_data[f'moment_{i}_performed'] for i in self.moments)

        overall_compliance = (total_performed / total_opportunities * 100) if total_opportunities > 0 else 0

        return {
            'by_moment': compliance_rates,
            'overall': overall_compliance,
            'total_opportunities': total_opportunities,
            'total_performed': total_performed
        }
```

### Hand Hygiene Improvement Strategies

#### Multimodal Interventions
```
WHO Multimodal Hand Hygiene Improvement Strategy:
├── System Change: Ensure availability of alcohol-based handrub
├── Training & Education: Regular sessions for all healthcare workers
├── Evaluation & Feedback: Regular compliance monitoring and reporting
├── Reminders in Workplace: Posters, screensavers, first-line supervision
├── Institutional Safety Climate: Promote hand hygiene as priority
```

#### Monitoring and Feedback
- **Direct observation**: Gold standard methodology
- **Product consumption**: Alcohol-based handrub usage as proxy measure
- **Electronic monitoring**: Automated systems for research settings
- **Patient involvement**: Patient education and observation programs

### Target Compliance Rates
- **Hospital-wide target**: ≥80% for all moments combined
- **High-risk areas target**: ≥90% (ICU, transplant units, etc.)
- **Moment-specific targets**: Varies by complexity and risk

## Environmental Cleaning and Disinfection

### Principles of Environmental Hygiene
```python
class EnvironmentalHygieneProgram:
    def __init__(self):
        self.cleaning_priorities = {
            'high_touch_surfaces': [
                'bed rails', 'bedside tables', 'doorknobs', 'light switches',
                'medical equipment surfaces', 'computer keyboards', 'phones'
            ],
            'patient_zone_items': [
                'commodes', 'bathroom surfaces', 'floors', 'walls near beds'
            ],
            'shared_equipment': [
                'stethoscopes', 'blood pressure cuffs', 'thermometers',
                'portable X-ray machines', 'ultrasound probes'
            ]
        }

        self.cleaning_frequencies = {
            'terminal_clean': 'After patient discharge/transfer',
            'daily_clean': 'End of each shift',
            'between_patients': 'After each patient contact',
            'high_risk_cleaning': 'Multiple times per day'
        }

    def assess_cleaning_effectiveness(self, surface_samples):
        """Evaluate environmental cleaning using ATP bioluminescence"""

        cleaning_effectiveness = {}

        for surface_type, readings in surface_samples.items():
            before_cleaning = readings['before_mean']
            after_cleaning = readings['after_mean']

            effectiveness = ((before_cleaning - after_cleaning) / before_cleaning) * 100
            cleaning_effectiveness[surface_type] = effectiveness

        return cleaning_effectiveness
```

### MDRO-Specific Cleaning Protocols

#### Contact Precautions for MDROs
```
Standard + Contact Precautions (CRE, MRSA, VRE):
├── Gloves: Upon room entry, change between patient contacts
├── Gown: For patient contact, if substantial contact expected
├── Patient-dedicated equipment: Stethoscopes, BP cuffs
├── Single-patient room preferred (cohort if necessary)
├── Remove PPE before leaving room, perform hand hygiene
└── Environmental cleaning with disinfectant
```

#### Enhanced Disinfection Strategies
- **Ultraviolet-C (UV-C) light**: Automated room disinfection
- **Hydrogen peroxide vapor**: Whole-room fumigation
- **Chlorine dioxide gas**: Surface and air disinfection
- **Copper alloy surfaces**: Continuous antimicrobial activity

### Water and Equipment Sterilization
- **Medical device reprocessing**: High-level disinfection standards
- **Dialysis water treatment**: Ultrapure water for hemodialysis
- **Endoscope cleaning**: Automated endoscope reprocessors with tracking
- **Ventilator circuits**: Appropriate humidification and changing protocols

## Bundle Interventions for High-Risk Procedures

### Central Line-Associated Bloodstream Infection (CLABSI) Prevention Bundle
```python
class CLABSI_Prevention_Bundle:
    def __init__(self):
        self.bundle_elements = [
            "hand_hygiene_before_insertion",
            "maximal_barrier_precautions",
            "chlorhexidine_skin_preparation",
            "optimal_catheter_site_selection",
            "daily_line_assessment_and_removal"
        ]

        self.success_metrics = {
            'clabsi_rate_reduction': 'Target: >=70% reduction',
            'bundle_compliance': 'Target: >=95%',
            'line_days_per_1000_patient_days': 'Measure denominator'
        }

    def implement_bundle(self, icu_ward):
        """
        Implement and monitor CLABSI prevention bundle

        Args:
            icu_ward: Dictionary with ward characteristics and baseline data

        Returns:
            Implementation plan and monitoring strategy
        """

        # Baseline CLABSI rate assessment
        baseline_rate = self.calculate_baseline_clabsi_rate(icu_ward)

        # Training program development
        training_program = {
            'insertion_training': 'Central venous catheter insertion simulation',
            'maintenance_training': 'Line management and dressing change procedures',
            'assessment_training': 'Daily line necessity evaluation'
        }

        # Monitoring and feedback system
        monitoring_system = {
            'daily_audits': 'Bundle element compliance',
            'weekly_feedback': 'Ward-specific performance reports',
            'monthly_reviews': 'Trend analysis and corrective actions'
        }

        # QI methodology: PDSA cycles for bundle refinement
        quality_improvement = {
            'plan': 'Baseline current state',
            'do': 'Implement bundle elements',
            'study': 'Measure impact on CLABSI rates',
            'act': 'Standardize successful elements, address gaps'
        }

        return {
            'baseline_rate': baseline_rate,
            'training_program': training_program,
            'monitoring_system': monitoring_system,
            'qi_methodology': quality_improvement
        }
```

### Ventilator-Associated Pneumonia (VAP) Prevention Bundle
```
Key Bundle Elements:
├── Elevation of head of bed (30-45°)
├── Daily sedation vacation and assessment
├── Deep venous thrombosis prophylaxis
├── Stress ulcer prophylaxis
├── Oral care with chlorhexidine
└── Subglottic suctioning (where available)
```

### Surgical Site Infection (SSI) Prevention Bundle
```
Preoperative Phase:
├── Appropriate antibiotic prophylaxis timing
├── Hair removal with clippers (not razors)
├── Normothermia maintenance
├── Glycemic control in diabetics
└── Nasal decolonization for MSSA/MRSA

Intraoperative Phase:
├── Normothermia maintenance
├── Supplemental oxygen
├── Antimicrobial irrigation for contaminated cases
└── Proper skin preparation with appropriate antiseptic

Postoperative Phase:
├── Antibiotic redosing during prolonged procedures
├── Postoperative glycemic control
├── Wound care protocols
└── Early mobilization and nutrition
```

## Isolation Precautions for AMR Pathogens

### Transmission-Based Precautions

#### Contact Precautions
**Indicated for**: MRSA, VRE, CRE, multidrug-resistant Acinetobacter, C. difficile
- **Gloves and gown** required for patient contact
- **Patient placement**: Private room preferred, cohorting acceptable
- **Equipment**: Dedicated patient equipment
- **Transportation**: Patient contained during transport

#### Droplet Precautions
**Indicated for**: Respiratory tract colonization with resistant organisms
- **Surgical mask** worn by healthcare workers within 6 feet
- **Patient placement**: Private room, door may remain open
- **Patient transport**: Mask patient during transport

#### Airborne Precautions
**Indicated for**: Rarely required for typical AMR organisms (exception: extensively drug-resistant TB)

### Personal Protective Equipment (PPE) Management

#### PPE Usage Hierarchy
```
Based on Risk Assessment:
├── Standard Precautions: All patient care (hand hygiene + gloves)
├── Contact Precautions: + gown for contact with patient/environment
├── Droplet Precautions: + surgical mask for close contact
├── Airborne Precautions: + N95 respirator + negative pressure room
```

#### PPE Optimization Strategies
- **Extended use vs. reuse**: N95 respirators during shortages
- **Alternative PPE**: PAPRs for aerosol-generating procedures
- **Donning/doffing protocols**: Systematic approach to prevent contamination
- **Waste management**: Proper disposal to prevent environmental contamination

### Decolonization Strategies

#### MRSA Decolonization
```
Nasal and skin decolonization protocol:
├── Intranasal mupirocin ointment twice daily × 5-10 days
├── Daily chlorhexidine gluconate body wash × 5-10 days
├── Weekly surveillance cultures post-decolonization
└── Retreatment if recolonization detected
```

#### CRE Decolonization
```
Selective digestive decontamination:
├── Oral gentamicin and colistin
├── Intravenous aminoglycoside with colistin
├── Duration: 7-14 days depending on clearance
├── Follow-up surveillance cultures
```

## Surveillance Systems for IPC and AMR

### Healthcare-Associated Infection Surveillance

#### NHSN Surveillance Definitions
```
CLABSI Definition Elements:
├── Laboratory-confirmed bloodstream infection
├── Central line present for >2 calendar days
├── Positive blood culture
├── No other source of infection identified

Secondary BSI Attribution:
├── CLABSI must meet all CLABSI criteria
├── Excludes single positive cultures coinciding with death
├── Excludes cases where another source identified within 24 hours
```

#### MRSA Bacteremia Surveillance
```
Case Definition:
├── Positive blood culture for MRSA
├── Within 3 calendar days of hospital admission
├── No previous positive culture within prior 14 days
└── Clinical evidence of infection (not colonization)
```

### Antimicrobial Resistance Surveillance

#### Device-Associated Infection Rates
```python
def calculate_device_associated_rates(infection_events, device_days, patient_days):
    """
    Calculate device-associated infection rates

    Args:
        infection_events: Number of infections occurring in patients with device
        device_days: Number of days patients had device in place
        patient_days: Number of days patients were in unit

    Returns:
        Standardized infection ratio and confidence intervals
    """

    # Device utilization ratio (DUR)
    # How aggressively devices are used in unit
    device_utilization_ratio = device_days / patient_days

    # Device-associated infection rate
    infection_rate = infection_events / device_days * 1000  # per 1000 device-days

    # Risk-adjusted rates using SIR (Standardized Infection Ratio)
    # SIR = Observed / Expected (using external benchmarks)

    # This is a simplified calculation
    # In practice, more complex risk adjustment models are used

    return {
        'device_utilization_ratio': device_utilization_ratio,
        'infection_rate_per_1000_device_days': infection_rate,
        'interpretation': self.interpret_rate(infection_rate, device_type)
    }

def interpret_rate(self, rate, device_type):
    """Interpret infection rate based on established benchmarks"""

    benchmark_rates = {
        'central_line': {'excellent': '<1.0', 'good': '1.0-2.0', 'needs_improvement': '>2.0'},
        'ventilator': {'excellent': '<2.0', 'good': '2.0-5.0', 'needs_improvement': '>5.0'},
        'catheter': {'excellent': '<2.5', 'good': '2.5-5.0', 'needs_improvement': '>5.0'}
    }

    if device_type in benchmark_rates:
        thresholds = [float(rate) for rate in benchmark_rates[device_type].values()]
        if rate <= thresholds[0]:
            return "Excellent performance"
        elif rate <= thresholds[1]:
            return "Good performance - room for improvement"
        else:
            return "Needs improvement - focus on bundle compliance"

    return "Rate interpretation requires device-specific benchmarks"
```

## Infection Control Committee Structure

### Roles and Responsibilities
```
Infection Control Committee Composition:
├── Infection Control Medical Director
├── Infection Control Nurse Manager
├── Hospital Epidemiologist
├── Antimicrobial Stewardship Physician
├── Microbiology Laboratory Director
├── Occupational Health Representative
├── Senior Administration Representative
├── Quality Improvement Specialist

Core Functions:
├── Policy development and oversight
├── Surveillance system design and monitoring
├── Outbreak investigation and response
├── Education and training programs
├── Performance improvement initiatives
└── Regulatory compliance monitoring
```

### Quality Improvement Methods

#### Root Cause Analysis (RCA)
```python
class RootCauseAnalysis:
    def __init__(self, adverse_event):
        self.event = adverse_event
        self.five_whys_questions = [
            "What happened?",
            "Why did this happen?",
            "Why did that happen?",
            "Why did that happen?",
            "Why did that happen?"
        ]

    def perform_five_whys(self):
        """Systematic root cause identification"""

        current_level = self.event
        root_causes = []

        for question in self.five_whys_questions:
            print(f"{question}")
            print(f"Answer: {current_level}")

            # Identify contributing factors at each level
            contributing_factors = self.analyze_contributing_factors(current_level)
            root_causes.extend(contributing_factors)

            # Move to next level (why did this happen?)
            if contributing_factors:
                current_level = f"Contributing factors: {'; '.join(contributing_factors)}"

        return root_causes

    def develop_corrective_actions(self, root_causes):
        """Develop targeted corrective actions"""

        actions = []
        for cause in root_causes:
            if "education" in cause.lower():
                actions.append("Develop training program to address knowledge gaps")
            elif "policy" in cause.lower():
                actions.append("Revise policy and update procedures")
            elif "supplies" in cause.lower():
                actions.append("Improve supply chain and availability")
            elif "compliance" in cause.lower():
                actions.append("Implement compliance monitoring system")

        return actions
```

#### Failure Mode and Effects Analysis (FMEA)
```
FMEA Process:
├── Define the process or system
├── Identify potential failure modes
├── Determine potential effects of failures
├── Assign Risk Priority Number (RPN) = Severity × Occurrence × Detection
├── Identify corrective actions for high-risk items
└── Monitor implementation and effectiveness
```

## Session Exercises

### Exercise 1: Bundle Implementation Planning
**Scenario**: Implement CLABSI prevention bundle in a 20-bed ICU with current CLABSI rate of 3.2 per 1000 line days.

**Tasks**:
1. Assess current bundle compliance through chart review and direct observation
2. Develop implementation timeline and training plan
3. Design monitoring system with run charts and statistical process control
4. Create stakeholder communication and engagement strategy

### Exercise 2: Hand Hygiene Improvement Program
**Current Status**: Ward has 45% overall hand hygiene compliance.

**Tasks**:
1. Perform baseline assessment of compliance by moment and location
2. Identify barriers to compliance through staff surveys and observations
3. Design multimodal improvement strategy with specific interventions
4. Develop monitoring and feedback mechanisms

### Exercise 3: Environmental Cleaning Audit
**Focus Area**: Medical-surgical ward with recent CRE outbreak.

**Tasks**:
1. Develop environmental cleaning audit tool
2. Conduct baseline cleaning effectiveness assessment
3. Identify high-touch surfaces with highest contamination risk
4. Design improved cleaning protocol and training program

### Exercise 4: Outbreak Investigation Response
**Situation**: Three patients with CRE bloodstream infections within 7 days.

**Tasks**:
1. Perform epidemiological investigation including case finding and epicurve construction
2. Assess infection control practices and compliance
3. Implement enhanced interventions (hand hygiene, contact precautions, environmental cleaning)
4. Monitor effectiveness of control measures and declare outbreak controlled

## Integration with Antimicrobial Stewardship

### IPC-ASP Synergy
```
Complementary Strategies:
├── ASP: Optimize antibiotic selection and duration
├── IPC: Prevent transmission of resistant organisms
├── Surveillance: Monitor both resistance patterns and infection rates
├── Education: Joint training on appropriate use and infection control
└── Combined metrics: Antibiotic consumption vs. HAI rates
```

### Combined Quality Measures
- **Antibiotic utilization metrics**: Defined daily doses per 1000 patient days
- **HAI rates**: Standardized infection ratios by device type
- **Resistance rates**: Percent resistant for key pathogen-antibiotic combinations
- **Composite measures**: Combined endpoint looking at utilization, resistance, and infections

## Key Takeaways

### Essential Principles
1. **Hand hygiene is the single most important IPC intervention**
2. **Bundle approaches provide synergistic infection prevention**
3. **MDRO transmission requires enhanced precautions**
4. **Environmental cleaning is often underemphasized**
5. **Surveillance drives improvement initiatives**

### Core Competencies Developed
- Evidence-based bundle implementation and monitoring
- Hand hygiene program design and improvement
- Isolation precaution protocols for MDROs
- Environmental cleaning strategy development
- Quality improvement methodology application

### Success Factors
- **Leadership commitment** and accountability at all levels
- **Multidisciplinary collaboration** between IPC and ASP programs
- **Measurement and feedback** systems built into routine practice
- **Education and training** as ongoing, not one-time activities
- **Culture of safety** where staff feel empowered to speak up

**Effective infection prevention and control is fundamental to any AMR containment strategy, requiring systematic approaches to break transmission cycles.**

### Recommended Resources
- **CDC HICPAC Guidelines**: Comprehensive infection control recommendations
- **WHO Guidelines on Core Components of IPC Programs**: Global standards
- **SHEA/IDSA Compendium**: Evidence-based infection control practices
- **Epicenter Training Materials**: Workshop-based IPC education

### Next Session Preview
**Session 7: One Health Approaches to AMR Prevention and Control**
