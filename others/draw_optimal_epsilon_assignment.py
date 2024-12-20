import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


plt.rcParams['text.usetex'] = True
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'
pi = np.pi


arc_1 = 2.98821984 + pi
arc_2 = 3.29178016 - pi

len_1 = 0.3296301942256927
len_2 = 0.6703698057743073

# draw polar plot
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, polar=True)
ax.set_theta_zero_location('E')
ax.set_theta_direction(1)
ax.set_ylim(0, 1)
ax.set_yticks([len_1, len_2])
ax.set_yticklabels(['0.33', '0.67'])
ax.set_xlim(0, 2*pi)
ax.set_xticks([arc_1, arc_2])
# color the area
ax.fill_between([arc_1, arc_2], len_1, len_2, color='gray', alpha=0.5)
plt.savefig('polar_mechanism_1.pdf', bbox_inches='tight')
plt.show()


arc_1 = 2.98821984 - pi / 2
arc_2 = 3.29178016 - pi / 2

len_1 = 0.6592603884513853
len_2 = 1

# draw polar plot
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111, polar=True)
ax.set_theta_zero_location('E')
ax.set_theta_direction(1)
ax.set_ylim(0, 1)
ax.set_yticks([len_1, len_2])
ax.set_yticklabels(['0.66', '1'])
ax.set_xlim(0, 2*pi)
ax.set_xticks([arc_1, arc_2])
# color the area
ax.fill_between([arc_1, arc_2], len_1, len_2, color='gray', alpha=0.5)
plt.savefig('polar_mechanism_2.pdf', bbox_inches='tight')
plt.show()

# p = 1.9347923344020317 * 3.1350026504398723