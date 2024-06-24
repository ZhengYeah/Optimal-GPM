import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('./whole-domain_circular_L2.csv')

fig, ax = plt.subplots()
fig.set_size_inches(5, 4)
fig.canvas.draw()

ax.plot(data['x'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
ax.plot(data['x'], data['PM'], label='PM', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
ax.plot(data['x'], data['Optimal'], label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
ax.set_xlabel(r'Input $x$')
ax.set_ylabel(r'Absolute error')
ax.set_xticks([0, 1.57, 3.14, 4.71, 6.28])
ax.set_xticklabels(['$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
# plt.yticks(np.arange(0, 0.25, 0.1))
ax.legend(loc='upper right')
fig.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.savefig('whole-domain_circular_L2.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('worst-case_circular_L1.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['Epsilon'], data['PM'], label='PM',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['Optimal'], label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Worst-case square error')
plt.xticks(np.arange(1, 9, 1))
# plt.yticks(np.arange(0, 0.25, 0.1))
plt.legend(loc='upper right')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

plt.savefig('worst-case_circular_L1.pdf', bbox_inches='tight')
plt.show()
