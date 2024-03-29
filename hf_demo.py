import os
import sys
import shutil
import argparse
from pathlib import Path
import torch
from transformers import AutoModelForImageClassification, AutoFeatureExtractor
from PIL import Image

# Check for CUDA availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def is_relevant(image_path, model, feature_extractor):
    image = Image.open(image_path).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    # Assuming the model outputs relevance in a specific way, e.g., index 1 is relevant
    # You might need to adjust the logic based on your model's output
    predictions = torch.nn.functional.softmax(logits, dim=-1)
    # Assuming index 1 is relevant class
    return predictions[0, 1] > 0.5

def main(folder_path, trash_folder, model_url):
    # Load model and feature extractor from Hugging Face
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_url)
    model = AutoModelForImageClassification.from_pretrained(model_url).to(device)
    model.eval()  # Set the model to evaluation mode
    
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if is_relevant(image_path, model, feature_extractor):
            print(f"Image {image_name} is relevant.")
        else:
            trash_path = os.path.join(trash_folder, image_name)
            shutil.move(image_path, trash_path)
            print(f"Moved {image_name} to trash.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter irrelevant images using a Hugging Face model.")
    parser.add_argument("--folder-path", type=str, required=True, help="Path to the folder containing images.")
    parser.add_argument("--trash-folder", type=str, required=True, help="Path to the trash folder.")
    parser.add_argument("--model-url", type=str, required=True, help="URL of the Hugging Face model.")
    args = parser.parse_args()

    main(args.folder_path, args.trash_folder, args.model_url)
