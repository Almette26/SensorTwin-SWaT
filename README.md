# SensorTwin — Stație de tratare a apei (SWaT)
**Curs:** Inteligență Computațională III — Aplicații SIVA (Master Anul II, ETTI-UPB)  
**Student:** Joitoiu Robert-Cristian  
**Tema:** S2 — SensorTwin — Stație de apă (SWaT): anomalie de proces / atac  

## Descrierea Proiectului
Proiectarea unui Digital Twin pentru monitorizarea în timp real și detecția anomaliilor de proces / atacurilor cibernetico-fizice pe infrastructura critică SWaT (Secure Water Treatment testbed).

## Setul de Date
* **Sursă:** iTrust, Center for Research in Cyber Security, Singapore University of Technology and Design (SUTD).
* **Structură:** 51 de fluxuri multivariate de senzori și actuatori (P1–P6), logate la 1 Hz.
* **Segmente:**
  * `normal.csv` (~496.000 instanțe, 7 zile regim normal continuu).
  * `attack.csv` (~450.000 instanțe, 4 zile cu 36/41 de scenarii de atac).

## Articole-Ancoră
1. **D. Shalyga, P. Filonov, A. Lavrentyev (Kaspersky Lab, 2018)** — *Anomaly Detection for Water Treatment System based on Neural Network with Automatic Architecture Optimization* (arXiv:1807.07282).
2. **M. U. Ozbek et al. (IEEE CASCON 2026)** — *Robustness of Anomaly Detection Models for Industrial Control Systems under Training-Time Data Contamination* (arXiv:2608.23547).

## Structura Repository-ului
* `checkpoints/` — Prezentările checkpoint (CP0–CP6) în format PDF.
* `notebooks/` — Experimente interactive și explorare date.
* `src/` — Pipeline de preprocesare, modele și funcții de evaluare.