# Minimal Spanning Tree Based Medical Image Segmentation

## Overview

This project implements a **graph-based image segmentation technique** using the **Minimum Spanning Tree (MST)** approach inspired by **Kruskal’s algorithm**.

The goal is to apply concepts from **graph theory and computational mathematics** to **medical image processing**, specifically for **image segmentation and noise reduction**.

Each pixel in a grayscale medical image is treated as a **node in a graph**, and edges connect neighboring pixels. The difference in pixel intensity defines the **edge weight**, which determines how pixels are grouped into segments.

The algorithm groups similar pixels into regions and performs **segment-based denoising** to improve image clarity.

---

## Objectives

* Convert medical images into **graph representations**
* Implement **MST-based segmentation**
* Apply **segment-level denoising**
* Analyze results using **quantitative metrics**
* Visualize segmentation outcomes

---

## Features

* Graph construction from grayscale images
* Kruskal-inspired **Minimum Spanning Tree segmentation**
* **Union-Find data structure** for component management
* Segment-based **image denoising**
* Performance evaluation using:

  * Mean Squared Error (MSE)
  * Peak Signal-to-Noise Ratio (PSNR)
* Automatic generation of:

  * segmentation visualization
  * denoised images
  * segment distribution histogram

---

## Project Structure

```
mst-medical-segmentation/
│
├── mst_image_processing.py
├── brain_mri.png
├── chest_xray.png
├── ct_scan.png
│
├── output_results/
│   ├── *_result.png
│   ├── *_segments.png
│
└── README.md
```

---

## Required Libraries

Install the required Python libraries:

```
pip install numpy matplotlib scikit-image
```

---

## How the Algorithm Works

### 1. Graph Representation

Each pixel is treated as a vertex in a graph.

Edges connect **4-neighbour pixels**:

* Up
* Down
* Left
* Right

Edge weight is defined as:

```
w = |I(p1) − I(p2)|
```

where
`I(p)` is the pixel intensity.

---

### 2. MST Segmentation

The algorithm processes edges in **increasing order of weight** and merges pixel components if the difference between them satisfies a **threshold condition**.

This ensures that:

* similar pixels are grouped
* strong boundaries are preserved

---

### 3. Segment-Based Denoising

After segmentation, each segment is replaced with its **average pixel intensity**:

```
I_denoised(p) = average intensity of pixels in segment
```

This reduces noise while preserving important structures.

---

## Evaluation Metrics

The performance of the algorithm is evaluated using:

### Mean Squared Error (MSE)

```
MSE = mean((original - denoised)^2)
```

Lower values indicate better denoising.

---

### Peak Signal-to-Noise Ratio (PSNR)

```
PSNR = 20 * log10(255 / sqrt(MSE))
```

Higher PSNR indicates better reconstruction quality.

---

## Running the Program

Run the Python script:

```
python mst_image_processing.py
```

The program will:

1. Load the medical images
2. Perform MST-based segmentation
3. Apply denoising
4. Compute performance metrics
5. Save visualization results

---

## Example Output

For each image the program outputs:

* Number of segments
* Execution time
* MSE
* PSNR
* Visualization images
* Segment histogram

Results are saved in the `output_results` folder.

---

## Applications

MST-based segmentation can be applied in:

* MRI analysis
* CT scan interpretation
* Tumor detection
* Anatomical structure identification
* Medical image denoising

---

## Limitations

* Processing time increases with large images
* Performance depends on the chosen threshold parameter
* May produce over-segmentation in highly textured images

---

## Future Improvements

* GPU acceleration
* Adaptive threshold optimization
* Integration with deep learning segmentation models
* Support for 3D medical images

---

## Author

Aman Govind
B.Tech Computer Science


