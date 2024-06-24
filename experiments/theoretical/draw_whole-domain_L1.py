import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('./whole-domain_L1.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['x'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['x'], data['PM'], label='PM', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(data['x'], data['Optimal'], label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.25, 0.1))
plt.legend(loc='lower right')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))

plt.savefig('whole-domain_L1.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('./worst-case_L2.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['Epsilon'], data['PM'], label='PM',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['Optimal'], label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Worst-case square error')
plt.xticks(np.arange(1, 9, 1))
plt.yticks(np.arange(0, 0.25, 0.1))
plt.legend(loc='upper right')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))

plt.savefig('worst-case_L2.pdf', bbox_inches='tight')
plt.show()
