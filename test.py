import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import urllib.request as urllib


f = urllib.request.urlopen("https://philchodrow.github.io/PIC16A/homework/main.jpg")
main = mpimg.imread(f, format = "jpg").copy()
f = urllib.request.urlopen("https://philchodrow.github.io/PIC16A/homework/cutout.jpg")
cutout= mpimg.imread(f, format = "jpg").copy()
fig, ax = plt.subplots(1, 2)
ax[0].imshow(main)
ax[1].imshow(cutout)



plt.imshow(main)