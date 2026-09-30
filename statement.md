# 🌸 MAHILA MITR — Project Statement & Requirements Specification

## 1. Project Title
**MAHILA MITR — Community Safety Assistance & Risk Analysis System**  
*Course Project Submission for VITyarthi — Build Your Own Project*

---

## 2. Problem Statement
Women in public and collegiate environments frequently experience non-emergency situations where they feel unsafe, uncomfortable, or stranded (e.g., poorly illuminated streets, unmonitored bus stops, or unfamiliar routes). While traditional emergency police/ambulance services exist for critical life-threatening events, there is a distinct operational gap for everyday community-level peer support and decentralized hazard reporting.

Without a structured peer-assistance channel, safety concerns often go unrecorded, and individuals have no systematic method to request proximity-based non-emergency accompaniment or verify local safety conditions.

---

## 3. Project Objectives
The objective of **Mahila Mitr** is to develop a modular, Python-based academic console application that delivers:
1. **Volunteer Network Management**: A system to register, update, and search community volunteers ("Mahila Mitrs") who can offer non-emergency assistance.
2. **Rule-Based Smart Matching**: An algorithmic approach to match help requests with available Mahila Mitrs based on availability, geographic area, assistance specialization, and urgency.
3. **Safety Concern Lifecycle & Confirmation**: A community hazard reporting module supporting complete CRUD operations and verification through peer confirmations.
4. **Transparent Safety Risk Analyzer**: A rule-based scoring formula evaluating area hazard levels (0–100 scale: Low, Medium, High) based on report severity, frequency, and community confirmations.
5. **Real-Time Community Analytics**: Dynamic statistical calculation of community safety trends, resolution rates, and volunteer metrics from stored project data.

---

## 4. Target Users
- **Women seeking peer support**: Individuals who feel uncomfortable or stranded in public spaces and need non-emergency accompaniment or guidance.
- **Mahila Mitr Volunteers**: Registered community members offering non-emergency assistance (accompaniment, navigation, safe-place guidance, emotional support).
- **Community Safety Observers**: Users who report local infrastructural and safety hazards (poor lighting, isolated paths, suspicious activity) to inform peers.

---

## 5. Scope & Boundaries
- **Academic Prototype**: Designed as a first-year B.Tech CSE software demonstration.
- **Local Persistence**: Data stored in structured JSON files (`mahila_mitrs.json`, `help_requests.json`, `safety_reports.json`, `users.json`).
- **No Production Emergency Dispatch**: Clearly differentiated from official emergency response services (Emergency: 112 / Women Helpline: 181).
- **Rule-Based Analysis**: Uses transparent mathematical formulas rather than black-box machine learning or external paid APIs.

---

## 6. Functional Requirements
- **FR1 (Volunteer Management)**: Register volunteers, toggle availability status, update assistance specializations, and perform multi-field search.
- **FR2 (Help Request & Matching)**: Create help requests with situation, area, urgency, and description; compute ranked suitability scores (0–100) for candidates.
- **FR3 (Safety Reports & CRUD)**: Submit, view, filter (by area/category/severity), update, and delete safety reports; support peer confirmations.
- **FR4 (Risk Scoring)**: Compute area risk scores using weighted formula:
  $$\text{Risk Score} = \min(100, \text{Severity Points} + \text{Frequency Points} + \text{Confirmation Points})$$
- **FR5 (Analytics)**: Generate aggregate statistics including resolution rates, top concerns, and volunteer availability.

---

## 7. Non-Functional Requirements
1. **Usability**: Interactive, clear numbered console menus with input guidance and friendly validation prompts.
2. **Reliability & Error Handling**: Graceful exception handling for missing files, corrupted JSON, and invalid user inputs without application crashes.
3. **Maintainability & Modularity**: Separation of concerns across 10 specialized Python files adhering to single-responsibility principles.
4. **Resource Efficiency**: Minimal CPU and memory footprint with zero third-party framework dependencies, using standard Python libraries.
