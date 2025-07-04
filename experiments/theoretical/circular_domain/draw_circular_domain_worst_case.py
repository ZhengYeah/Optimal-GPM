import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('worst_case_circular_L1.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['SW'], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['Epsilon'], data['PM'], label='PM-C',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Worst-case square error')
plt.xticks(np.arange(1, 9, 1))
# plt.yticks(np.arange(0, 0.25, 0.1))
plt.legend(loc='upper right')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.savefig('worst_case_circular_L1.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('worst_case_circular_L2.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['SW'], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['Epsilon'], data['PM'], label='PM-C',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Worst-case square error')
plt.xticks(np.arange(1, 9, 1))
# plt.yticks(np.arange(0, 0.25, 0.1))
plt.legend(loc='upper right')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.savefig('worst_case_circular_L2.pdf', bbox_inches='tight')
plt.show()