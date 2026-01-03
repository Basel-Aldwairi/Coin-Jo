import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
from coin_model import get_plot

# print(matplotlib.get_backend())

predictions= [(np.float32(0.5479318), '0.5 JD'),
               (np.float32(0.0145562235), '0.25 JD'),
               (np.float32(0.14330193), '10 Piasters'),
               (np.float32(0.29421005), '5 Piasters')]

fig, ax = get_plot(predictions)

plt.show(block=True)
# input('Press any key to exit')