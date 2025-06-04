import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter

plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('ablation_whole_domain_L2_PM.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['PM'], label='PM', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(data['x'], data['PM_truncation'], label='T-PM', linewidth=2, linestyle='--', color=[0, 0, 1], marker='.', markersize=8, markevery=2)
plt.plot(data['x'], data['Optimal'], label='OGPM on [-1,1)', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Squared error')
plt.xticks(np.arange(-1, 1.1, 0.5))
plt.yticks(np.arange(0, 1.2, 0.2))
plt.ylim(0, 1.2)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.legend(loc='upper right')

plt.savefig('ablation_PM.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('ablation_whole_domain_l2_SW.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0], marker='+', markersize=8, markevery=3)
plt.plot(data['x'], data['SW_truncation'], label='T-SW', linewidth=2, linestyle='--', color=[0, 0, 0], marker='.', markersize=8, markevery=2)
plt.plot(data['x'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Squared error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.18, 0.1))
plt.ylim(0, 0.18)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.legend(loc='upper right')

plt.savefig('ablation_SW.pdf', bbox_inches='tight')
plt.show()

