import os
import numpy as np
from streaming import MDSWriter, MDSDataset
import torch
from torch.utils.data import DataLoader

def generate_synthetic_cifar_data(num_samples, data_dir):
    """
    Generates a synthetic CIFAR-like dataset and writes it to disk using MDSWriter.
    """
    os.makedirs(data_dir, exist_ok=True)
    columns = {
        'image': 'jpeg',  # Store images as JPEG
        'label': 'int'    # Store labels as integers
    }
    with MDSWriter(out=data_dir, columns=columns) as out:
        for _ in range(num_samples):
            # Generate a random image (32x32 pixels with 3 color channels)
            image = np.random.randint(0, 256, size=(32, 32, 3), dtype=np.uint8)
            # Generate a random label between 0 and 9
            label = np.random.randint(0, 10, dtype=np.int32)
            # Write the sample to disk
            sample = {
                'image': image,
                'label': label
            }
            out.write(sample)
    print(f"Generated {num_samples} synthetic images at '{data_dir}'.")

def get_streaming_cifar_dataset(data_dir):
    """
    Creates a StreamingDataset from the data written by MDSWriter.
    """
    dataset = MDSDataset(
        local=data_dir,
        remote=None,  # Set to None since data is local
        shuffle=True,
        batch_size=1  # Will be overridden by DataLoader's batch_size
    )
    return dataset

def main():
    data_dir = './synthetic_cifar'
    num_samples = 10000  # Adjust the number of samples as needed

    # Step 1: Generate synthetic CIFAR-like data
    generate_synthetic_cifar_data(num_samples, data_dir)

    # Step 2: Create a StreamingDataset
    dataset = get_streaming_cifar_dataset(data_dir)

    # Step 3: Use DataLoader to iterate over the dataset
    dataloader = DataLoader(dataset, batch_size=32, num_workers=4)

    # Example: Iterate over one epoch
    for batch_idx, batch in enumerate(dataloader):
        images = batch['image']  # Tensor of shape [batch_size, 32, 32, 3]
        labels = batch['label']  # Tensor of shape [batch_size]
        
        # Convert images to proper shape for PyTorch models ([batch_size, channels, height, width])
        images = images.permute(0, 3, 1, 2).float() / 255.0  # Normalize pixel values

        # Your training or evaluation code here
        # For demonstration, we'll just print the batch shape
        print(f"Batch {batch_idx}: images shape {images.shape}, labels shape {labels.shape}")

        # Break after first batch for demonstration purposes
        if batch_idx == 0:
            break

if __name__ == '__main__':
    main()
