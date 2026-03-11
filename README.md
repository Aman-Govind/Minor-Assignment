# MST-Based Medical Image Segmentation and Denoising

## Overview

This project demonstrates the application of **Minimum Spanning Trees (MST)** in **medical image processing**. The algorithm is inspired by **Kruskal’s algorithm** and is used to perform **image segmentation and denoising** on grayscale medical images such as MRI, CT scans, and X-rays.

Each pixel of the image is treated as a **node in a graph**, and edges connect neighboring pixels. The edge weights are determined by the difference in pixel intensity. Using an MST-based approach, similar pixels are grouped into segments while preserving important boundaries.

After segmentation, **segment-based denoising** is applied by replacing pixel values with the mean intensity of their respective segments.

---

## Project Structure

```
.
├── mst_medical_segmentation.py     # Main Python implementation
├── brain_mri.png                   # MRI test image
├── chest_xray.png                  # Chest X-ray test image
├── ct_scan.png                     # CT scan test image
├── Minor assignment REPORT.pdf     # Assignment report
│
└── output_results/                 # Generated output images
```

---

## Features

* Graph representation of images
* MST-based image segmentation
* Union-Find data structure for efficient merging
* Segment-based image denoising
* Performance evaluation using MSE and PSNR
* Visualization of segmentation results
* Histogram showing segment distribution

---

## Required Libraries

Install the necessary Python libraries before running the program:

```
pip install numpy matplotlib scikit-image
```

---

## Algorithm Steps

### 1. Image Loading

Medical images are loaded and converted into **grayscale format**.

---

### 2. Graph Construction

Each pixel is considered a vertex in a graph.

Edges are created between **4-neighbour pixels**:

* Up
* Down
* Left
* Right

The weight of each edge is calculated as:

```
w = |I(p1) − I(p2)|
```

where `I(p)` represents pixel intensity.

---

### 3. MST-Based Segmentation

Edges are sorted by weight and processed using a **Union-Find structure**.

Two components are merged if the edge weight satisfies a **threshold condition**, ensuring that similar pixels belong to the same segment.

---

### 4. Segment-Based Denoising

For each segment:

```
new_pixel_value = mean intensity of all pixels in that segment
```

This helps reduce noise while maintaining structural boundaries.

---

## Evaluation Metrics

### Mean Squared Error (MSE)

```
MSE = mean((original − denoised)^2)
```

Lower values indicate better denoising.

---

### Peak Signal-to-Noise Ratio (PSNR)

```
PSNR = 20 log10(255 / √MSE)
```

Higher PSNR values indicate better reconstruction quality.

---

## How to Run

Run the program using:

```
python mst_medical_segmentation.py
```

The script will:

1. Load the three test images
2. Perform segmentation
3. Apply denoising
4. Calculate evaluation metrics
5. Save output images in `output_results/`

---

## Output

For each input image, the program generates:

* Segmented visualization
* Denoised image
* Segment distribution histogram
* Performance metrics (MSE, PSNR, execution time)

All results are saved inside the **output_results** folder.

---

## Applications

* MRI analysis
* CT scan segmentation
* X-ray image enhancement
* Tumor and anatomical structure detection
* Medical image noise reduction

---

## Author

Aman Govind
B.Tech Computer Science

