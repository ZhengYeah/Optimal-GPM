import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'Times New Roman'

# Load data
data = pd.read_csv('./whole-domain_L1.csv')

plt.plot(data['x'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['x'], data['PM'], label='PM',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['x'], data['Optimal'], label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'$L_1$ error')
plt.yticks(np.arange(0, 0.25, 0.05))
plt.legend(loc='upper right')

plt.show()
plt.savefig('whole-domain_L1.pdf', bbox_inches='tight')
