import random
import numpy as np
from Disease_Simulation import Simulation, simulation_parameters

for neighbourhood in ["moore", "von neumann"]:
    for pop in [50, 100, 200, 400]:
        peaks = []
        for seed in range(20):
            random.seed(seed)
            np.random.seed(seed)
            stats = Simulation(pop, neighbourhood, 0.1, 0.05, 0.2, simulation_parameters, verbose=False)
            peaks.append(max(s["infected"] for s in stats) / pop)
        print(f"{neighbourhood}, pop={pop}: mean peak infected = {np.mean(peaks):.1%} (sd {np.std(peaks):.1%})") 