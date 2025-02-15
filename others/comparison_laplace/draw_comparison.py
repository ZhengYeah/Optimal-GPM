import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'
pi = np.pi

# Load data
data = pd.read_csv('comparison_laplace.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['epsilon'], data['error_laplace'], label='Laplace', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['epsilon'], data['error_truncated_laplace'], label='Truncated Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='x', markersize=8)
plt.plot(data['epsilon'], data['error_gpm'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.xticks(np.arange(0, 10, 2))
plt.yticks(np.arange(0, 1.21, 0.3))
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
leg = plt.legend(loc='upper right')

plt.savefig('comparison_laplace.pdf', bbox_inches='tight')
plt.show()
