import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable

f_name = "left.npy"
data = np.load(f_name)
df = pd.DataFrame(data)
mean = df.mean().values.tolist()
print(mean)

data_color = [x/25000 for x in mean]

my_cmap = plt.cm.get_cmap('YlOrRd')
colors = my_cmap(data_color)

fake = [10000 for x in range(7)]
plt.bar(range(0, 7), mean[:-1], 
color = colors)

title = f_name.split(".")[0]
plt.title(title)
plt.xlabel('sensor')
plt.ylabel('pressure')
plt.ylim((0, 25000))

plt.show()