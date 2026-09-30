# 🌸 MAHILA MITR — Community Safety Assistance & Risk Analysis System

> **Tagline:** *"Women supporting women, wherever you need it."*  
> **Course Evaluation:** VITyarthi — Build Your Own Project  
> **Domain:** Software Engineering / Python Application Development (B.Tech CSE)

---

## 1. Project Overview

**Mahila Mitr** is a Python-based console software application designed to provide community-powered safety support, safety hazard reporting, rule-based area risk analysis, and dynamic community analytics.

Rather than acting as a static safety-tips list, Mahila Mitr implements genuine data processing pipelines:
$$\text{User Input} \longrightarrow \text{Validation} \longrightarrow \text{Algorithmic Matching / Scoring} \longrightarrow \text{JSON Persistence} \longrightarrow \text{Actionable Reports}$$

---

## 2. Key Features & Functional Modules

```
                        🌸 MAHILA MITR ARCHITECTURE
                        
                    ┌──────────────────────────────┐
                    │      Main Console Menu       │
                    │          (main.py)           │
                    └──────────────┬───────────────┘
                                   │
      ┌──────────────┬─────────────┼──────────────┬──────────────┐
      │              │             │              │              │
┌─────▼─────┐  ┌─────▼─────┐ ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
│ Module 1  │  │ Module 2  │ │ Module 3  │  │ Module 4  │  │ Module 5  │
│ Mahila    │  │ Help      │ │ Safety    │  │ Risk      │  │ Community │
│ Mitr Mgmt │  │ Request & │ │ Reports   │  │ Analyzer  │  │ Analytics │
│           │  │ Matching  │ │ (CRUD)    │  │ (Scoring) │  │           │
└─────┬─────┘  └─────┬─────┘ └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
      │              │             │              │              │
      └──────────────┴──────┬──────┴──────────────┴──────────────┘
                            │
               ┌────────────▼────────────┐
               │ Storage Layer (JSON DB) │
               │ (mahila_mitrs, reports, │
               │  help_requests, users)  │
               └─────────────────────────┘
```

### 👥 Module 1: User & Mahila Mitr Management (`user_manager.py`)
- Register new volunteer Mahila Mitrs with specialized assistance skills.
- Search volunteers by name, area, or assistance type.
- Real-time availability toggling (Available / Busy).
- Assistance types: *Emotional support*, *Accompaniment/support*, *Navigation help*, *Safe-place guidance*, *General assistance*.

### 🆘 Module 2: Help Request & Smart Matching (`help_request.py`, `matching.py`)
- Create structured help requests (Situation, Area, Urgency Level, Assistance Needed, Description).
- **Rule-Based Suitability Scoring (0–100 scale)**:
  - **Availability (30 pts)**: Must be currently available.
  - **Area Proximity (40 pts)**: Exact local area alignment.
  - **Assistance Compatibility (20 pts)**: Direct skill matching.
  - **Urgency Bonus (10 pts)**: Fast response priority for High urgency.
- Automatic ranked candidate recommendations and assignment workflow.

### 📍 Module 3: Safety Report Management (`safety_reports.py`)
- Full CRUD operations: Add, View, Update descriptions, and Delete reports.
- Structured categories (*Poor lighting*, *Harassment concern*, *Isolated area*, *Unsafe road/path*, *Suspicious activity*, *Other*).
- Multi-criteria filtering by Area, Category, and Severity.
- **Community Peer Confirmation**: Community members confirm hazards; automatically marks reports as `Verified` upon reaching $\ge 3$ confirmations.

### 🛡️ Module 4: Rule-Based Safety Risk Analyzer (`risk_analyzer.py`)
- Transparent, mathematical area risk calculation (0–100):
  $$\text{Risk Score} = \min\big(100, \text{Severity Points (max 50)} + \text{Frequency Points (max 30)} + \text{Confirmation Points (max 20)}\big)$$
- **Classification**:
  - `0 – 30` : **🟢 LOW RISK**
  - `31 – 60` : **🟡 MEDIUM RISK**
  - `61 – 100`: **🔴 HIGH RISK**
- Comparative cross-area hazard ranking and primary concern identification.

### 📊 Module 5: Community Safety Analytics (`analytics.py`)
- Dynamic computation of community metrics from live data files:
  - Total reports, severity distribution, most reported hazard, highest incident area.
  - Help request resolution rate ($\%$).
  - Volunteer network availability rate ($\%$).

---

## 3. Python Concepts Demonstrated

The codebase is structured to reflect best practices appropriate for a first-year B.Tech CSE student:

| Python Concept | Where It Is Used |
|---|---|
| **Object-Oriented Programming (OOP)** | Class definitions with encapsulation and dictionary serialization in `models.py`. |
| **Modular Programming** | Separation of functional modules (`user_manager`, `help_request`, `matching`, etc.). |
| **File I/O & JSON Serialization** | Safe reading, parsing, error recovery, and persistence in `storage.py`. |
| **Data Structures** | Lists, dictionaries, tuples, sets, and sorted key-lambdas for filtering and ranking. |
| **Validation & Error Handling** | Defensive validation functions in `validation.py`, robust `try/except` blocks. |
| **Algorithmic Scoring** | Multi-factor weighted arithmetic matching and normalization in `matching.py` and `risk_analyzer.py`. |
| **Automated Testing** | Built-in Python `unittest` suite covering all modules in `tests/test_project.py`. |

---

## 4. Project Structure

```
VITYARTHI PROJECT/
│
├── main.py                     # Main interactive application entry point
├── models.py                   # Class definitions (MahilaMitr, HelpRequest, SafetyReport, User)
├── storage.py                  # JSON file I/O operations and error recovery
├── validation.py               # Input validation rules and constraint checks
├── utils.py                    # Console formatting, timestamps, banners
│
├── user_manager.py             # Module 1: Mahila Mitr & User operations
├── help_request.py             # Module 2: Help request lifecycle
├── matching.py                 # Module 2: Rule-based smart matching algorithm
├── safety_reports.py           # Module 3: Safety report CRUD & confirmations
├── risk_analyzer.py            # Module 4: Area safety risk scoring engine
├── analytics.py                # Module 5: Aggregate statistics generator
│
├── data/                       # Local JSON database folder
│   ├── mahila_mitrs.json       # Registered Mahila Mitr records
│   ├── help_requests.json      # Help requests queue
│   ├── safety_reports.json     # Hazard reports and confirmations
│   └── users.json              # Community user profiles
│
├── tests/
│   └── test_project.py         # Automated unit test suite
│
├── README.md                   # Complete project documentation
├── statement.md                # Formal problem statement & requirements
└── BuildYourOwnProjectVITyarthi.pdf # Evaluation guidelines
```

---

## 5. How to Run the Application

### Prerequisites
- Python 3.8+ installed (no external `pip` packages required).

### Execution Command
Open a terminal / command prompt in the project root and run:

```bash
python main.py
```

---

## 6. How to Run the Unit Tests

Execute the automated test suite with verbose output:

```bash
python -m unittest tests/test_project.py -v
```

Expected output:
```
test_community_analytics ... ok
test_matching_algorithm_scoring ... ok
test_models_serialization ... ok
test_risk_analyzer_calculation ... ok
test_validation_choice ... ok
test_validation_id_format ... ok
test_validation_non_empty ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.010s

OK
```

---

## 7. Sample Outputs

### Sample 1: Smart Matching Recommendation Output
```
==========================================================
  HELP REQUEST #REQ102
==========================================================
  User: Kavya
  Situation: Stranded
  Area: Campus Gate
  Urgency: High
  Assistance Needed: Navigation help
  Description: Auto dropped at wrong gate, battery low.
----------------------------------------------------------
  SUITABLE MAHILA MITRS FOUND:

  1. Aanya Sharma
     Area: Campus Gate
     Availability: Available
     Skill: Accompaniment/support
     Match Score: 85/100
     Key Factors: Currently available (+30), Located in same area (+40), Cross-functional assistance (+5), High urgency bonus (+10)

  2. Ananya Joshi
     Area: Campus Gate
     Availability: Available
     Skill: Navigation help
     Match Score: 100/100
     Key Factors: Currently available (+30), Located in same area (+40), Exact match for skill (+20), High urgency bonus (+10)

  RECOMMENDED MATCH:
  ⭐ Ananya Joshi (Score: 100/100)
  Reason: Highest suitability based on availability, area and skill alignment.
==========================================================
```

### Sample 2: Area Risk Analysis Output
```
==========================================================
  SAFETY RISK ANALYSIS (ACADEMIC RULE-BASED PROTOTYPE)
==========================================================
  Target Area: Campus Gate
  Total Reports: 2
  Reports by Category:
    - Poor lighting: 1
    - Harassment concern: 1

  Highest Severity Observed: High
  Total Community Confirmations: 14
----------------------------------------------------------
  Calculated Risk Score: 86/100
  Risk Classification  : [HIGH]
  Primary Concern      : Poor lighting

  Analysis & Insights:
  The area exhibits multiple critical concerns with significant community verification. Caution is strongly advised, especially regarding 'Poor lighting'.
----------------------------------------------------------
  Score Formula Breakdown:
    - Severity Contribution    : 40/50 pts
    - Frequency Contribution   : 12/30 pts
    - Confirmation Contribution: 20/20 pts
==========================================================
```

---

## 8. Non-Functional Requirements Summary

1. **Usability**: Intuitive menu navigation with explicit numbered selections and field-level validation feedback.
2. **Reliability & Data Integrity**: Defensive file operations with fallback defaults to prevent crashes caused by corrupted data.
3. **Maintainability**: Clean modular architecture with strict separation between data models, storage, validation, and presentation logic.
4. **Resource Efficiency**: Lightweight execution with sub-second response times and zero external API dependencies.

---

## 9. Academic Disclaimer

> **Important Notice:**  
> **Mahila Mitr** is an academic prototype developed for educational demonstration in a first-year B.Tech Computer Science and Engineering course. It is **not** an emergency dispatch service or police integration system. In any critical emergency situation, users must contact official emergency services (Emergency: **112**, Women Helpline: **181**, Police: **100**).

---

## 10. Future Enhancements

- Real-time GPS distance calculation using spatial libraries.
- Integration of secure SMS / push notifications.
- Verified identity badge management.
- Trusted emergency contact auto-alerts.
- Offline-first mobile client synchronization.
