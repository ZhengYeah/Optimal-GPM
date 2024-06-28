import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

# Load data
data = pd.read_csv('./mean_classical.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['Epsilon'], data['PM'], label='PM', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['GPM'], label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.plot(data['Epsilon'], data['UB_GPM'], label='GPM (unbias)', linewidth=2, linestyle='--', color=[1, 0, 1])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Mean estimation error')
plt.ylim(0, 0.1)
plt.xticks(np.arange(1, 9, 1))
# plt.yticks(np.arange(0, 0.1, 0.02))
leg = plt.legend(loc='upper right')
for i, test in enumerate(leg.get_texts()):
    if i == 3:
        test.set_fontsize(14)

plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%g'))

plt.savefig('mean_classical.pdf', bbox_inches='tight')
plt.show()


# Load data
data = pd.read_csv('./distribution_classical.csv')
plt.figure(figsize=(5, 4))
plt.plot(data['Epsilon'], data['SW'], label='SW', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(data['Epsilon'], data['PM'], label='PM',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(data['Epsilon'], data['GPM'], label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Distribution estimation error')
plt.xticks(np.arange(1, 9, 1))
# plt.yticks(np.arange(0, 0.25, 0.1))
plt.legend(loc='upper right')
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.ticklabel_format(axis='y', style='sci', scilimits=(2, 2))

plt.savefig('distribution_classical.pdf', bbox_inches='tight')
plt.show()
