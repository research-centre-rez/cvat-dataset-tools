---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.16.7
  kernelspec:
    display_name: python-cvr-test-repo
    language: python
    name: python-cvr-test-repo
---

```python
%load_ext autoreload
%autoreload 2
```

```python
import imageio
from pathlib import Path
import matplotlib.pyplot as plt

```

# Load Image

The following code loads image

```python
input_image_path = 'assets/plt.png'
input_image = imageio.imread(input_image_path)

plt.imshow(input_image)
```

# Process the Image

```python
import imagestuff.image_ops as imgops

thr = 127
thresholded = imgops.threshold_image(input_image,thr)
inverted = imgops.invert_image(input_image)

_,axs= plt.subplots(1,3)

imgs = [input_image,inverted,thresholded]
names = ["Original","Inverted", f"Thresholded $t={thr}"]
for ax,img,name in zip(axs,imgs,names):
    ax.imshow(img)
    ax.axis('off')
    ax.set_title(name)
plt.show()
```

# Save the Files

The result is saved to output path.

**NOTE:** The chosen path `output` is within this repository. However, since it's been added to `.gitignore` you don't need to worry about commiting it to the repository

```python
output_folder = Path('output')
output_folder.mkdir(exist_ok=True)

output_inverse = output_folder/'inversed.png'
imageio.imwrite(output_inverse,inverted)

output_thresholded = output_folder/'thresholded.png'
imageio.imwrite(output_thresholded, thresholded)

```
