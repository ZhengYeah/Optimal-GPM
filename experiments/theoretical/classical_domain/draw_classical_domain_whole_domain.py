import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('whole_domain_L1_2.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['SW-C'], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['x'], data['PM-C'], label='PM-C', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(data['x'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.42, 0.1))
plt.ylim(0.01, 0.42)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.legend(loc='upper right')

plt.savefig('whole-domain_L1_2.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('whole_domain_L1_4.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['SW-C'], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['x'], data['PM-C'], label='PM-C', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(data['x'], data['Optimal'], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.21, 0.1))
plt.ylim(0.01, 0.21)
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.legend(loc='upper right')

plt.savefig('whole-domain_L1_4.pdf', bbox_inches='tight')
plt.show()

