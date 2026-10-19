# Disease Simulation

An agent-based simulation modelling the spread of disease across a 2D population grid. Tracks five health states (healthy, infected, recovered, immune, dead) with configurable movement rules, barriers, and automated parameter sweeps.

## Features
- Moore & Von Neumann neighbourhood movement rules
- Five health states with configurable recovery, death, and immunity rates
- Barriers that block movement and constrain spread
- Real-time scatter-plot visualisation per month
- Automated parameter sweep (`experiments.py`) to measure peak infection rates across population sizes and neighbourhood types
- Uses binomial distributions for realistic infection/recovery spread

## Tech Stack
Python 3 · NumPy · Matplotlib

## How to Run ? 

First, clone the repository and install the required dependencies:

git clone https://github.com/fatimasiraj-cybersec/disease-simulation.git
cd disease-simulation
pip install -r requirements.txt

To run a single interactive simulation:

python Disease_Simulation.py

To run the automated parameter sweep:

python experiments.py

## Output
The simulation prints monthly statistics to the console and generates scatter plots (simulation_month_X.png) showing the spatial distribution of each health status.

## License
MIT