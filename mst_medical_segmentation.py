import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
import time
import os
from collections import defaultdict


# --------------------------------------------------
# Output Directory
# --------------------------------------------------

OUTPUT_DIR = "output_results"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# --------------------------------------------------
# Image Loader
# --------------------------------------------------

def read_image(file_path):

    image = io.imread(file_path)

    # remove alpha channel if present
    if image.ndim == 3 and image.shape[2] == 4:
        image = image[:, :, :3]

    # convert to grayscale
    if image.ndim == 3:
        image = color.rgb2gray(image)

    image = (image * 255).astype(np.uint8)

    return image


# --------------------------------------------------
# Graph Construction
# --------------------------------------------------

def generate_edges(img):

    height, width = img.shape
    edge_list = []

    def node_index(r, c):
        return r * width + c

    for r in range(height):
        for c in range(width):

            if r < height - 1:
                w = abs(int(img[r, c]) - int(img[r+1, c]))
                edge_list.append((w, node_index(r,c), node_index(r+1,c)))

            if c < width - 1:
                w = abs(int(img[r, c]) - int(img[r, c+1]))
                edge_list.append((w, node_index(r,c), node_index(r,c+1)))

    return edge_list


# --------------------------------------------------
# Disjoint Set (Union-Find)
# --------------------------------------------------

class DisjointSet:

    def __init__(self, total_nodes):

        self.parent = list(range(total_nodes))
        self.rank = [0]*total_nodes
        self.comp_size = [1]*total_nodes
        self.internal_diff = [0]*total_nodes

    def find(self, x):

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def merge(self, a, b, weight, k):

        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return

        threshold_a = self.internal_diff[root_a] + k/self.comp_size[root_a]
        threshold_b = self.internal_diff[root_b] + k/self.comp_size[root_b]

        if weight <= min(threshold_a, threshold_b):

            if self.rank[root_a] < self.rank[root_b]:
                root_a, root_b = root_b, root_a

            self.parent[root_b] = root_a
            self.comp_size[root_a] += self.comp_size[root_b]

            self.internal_diff[root_a] = max(
                self.internal_diff[root_a],
                self.internal_diff[root_b],
                weight
            )

            if self.rank[root_a] == self.rank[root_b]:
                self.rank[root_a] += 1


# --------------------------------------------------
# MST Segmentation
# --------------------------------------------------

def perform_segmentation(img, k=250):

    h, w = img.shape
    total_pixels = h*w

    edges = generate_edges(img)

    edges = sorted(edges, key=lambda x: x[0])

    dsu = DisjointSet(total_pixels)

    for weight, u, v in edges:
        dsu.merge(u, v, weight, k)

    labels = np.zeros(total_pixels)

    for i in range(total_pixels):
        labels[i] = dsu.find(i)

    return labels.reshape(h, w)


# --------------------------------------------------
# Denoising via Segment Mean
# --------------------------------------------------

def segment_denoising(img, label_map):

    result = np.copy(img)

    segment_pixels = defaultdict(list)

    for r in range(label_map.shape[0]):
        for c in range(label_map.shape[1]):

            segment_pixels[label_map[r,c]].append(img[r,c])

    segment_means = {
        seg : np.mean(vals)
        for seg, vals in segment_pixels.items()
    }

    for r in range(label_map.shape[0]):
        for c in range(label_map.shape[1]):

            result[r,c] = segment_means[label_map[r,c]]

    return result


# --------------------------------------------------
# Evaluation Metrics
# --------------------------------------------------

def compute_mse(img1, img2):

    return np.mean((img1-img2)**2)


def compute_psnr(img1, img2):

    error = compute_mse(img1, img2)

    if error == 0:
        return 100

    return 20*np.log10(255/np.sqrt(error))


# --------------------------------------------------
# Visualization
# --------------------------------------------------

def show_results(original, labels, denoised, filename):

    fig, ax = plt.subplots(1,3, figsize=(13,4))

    ax[0].imshow(original, cmap="gray")
    ax[0].set_title("Original")

    ax[1].imshow(labels, cmap="tab20")
    ax[1].set_title("Segments")

    ax[2].imshow(denoised, cmap="gray")
    ax[2].set_title("Denoised")

    for a in ax:
        a.axis("off")

    savefile = os.path.join(OUTPUT_DIR, filename+"_result.png")

    plt.savefig(savefile)
    plt.close()

    print("Visualization saved:", savefile)


# --------------------------------------------------
# Segment Histogram
# --------------------------------------------------

def plot_histogram(labels, filename):

    plt.figure()

    plt.hist(labels.flatten(), bins=40)

    plt.title("Segment Frequency")

    plt.xlabel("Segment Label")

    plt.ylabel("Pixel Count")

    path = os.path.join(OUTPUT_DIR, filename+"_segments.png")

    plt.savefig(path)

    plt.close()

    print("Histogram saved:", path)


# --------------------------------------------------
# Experiment Runner
# --------------------------------------------------

def experiment(image_path):

    image = read_image(image_path)

    start_time = time.time()

    label_map = perform_segmentation(image)

    denoised = segment_denoising(image, label_map)

    end_time = time.time()

    num_segments = len(np.unique(label_map))

    print("\nProcessing:", image_path)
    print("Segments:", num_segments)
    print("Time:", round(end_time-start_time,3), "seconds")
    print("MSE:", compute_mse(image, denoised))
    print("PSNR:", compute_psnr(image, denoised))

    name = image_path.split(".")[0]

    show_results(image, label_map, denoised, name)

    plot_histogram(label_map, name)


# --------------------------------------------------
# Main Execution
# --------------------------------------------------

def main():

    dataset = [
        "brain_mri.png",
        "chest_xray.png",
        "ct_scan.png"
    ]

    for file in dataset:

        if os.path.exists(file):
            experiment(file)
        else:
            print("File not found:", file)


if __name__ == "__main__":
    main()