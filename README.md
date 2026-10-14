# Disease Simulation

An agent-based simulation modelling the spread of disease across a 
2D population grid, written in Python. The simulation tracks five 
health states (healthy, infected, recovered, immune, dead) and 
supports configurable movement rules, barriers, and real-time 
visualisation.

## Features
- Moore & Von Neumann neighbourhood movement rules
- Five health states: healthy, infected, recovered, immune, dead
- Configurable recovery, death, and immunity rates
- Barriers that block disease spread across the grid
- Real-time scatter-plot visualisation per month
- Monthly statistics printed to console
- Interactive CLI for setting simulation parameters

## Tech Stack
Python 3 · NumPy · Matplotlib

## How to Run

```bash
# Clone the repository
git clone https://github.com/fatimasiraj-cybersec/disease-simulation.git
cd disease-simulation

# Install dependencies
pip install -r requirements.txt

# Run the simulation
python Disease_Simulation.py