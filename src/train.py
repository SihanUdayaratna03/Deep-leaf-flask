import os
import json
import tensorflow as tf
from dataset import get_datasets
from model import build_model

def main():
    train_dir = '../Datasets/train'
    test_dir = '../Datasets/test'
    
    if not os.path.exists(train_dir):
        print(f"Error: Training directory {train_dir} not found!")
        print("Please download and extract the dataset first.")
        return

    # 1. Load Data
    train_ds_raw = tf.keras.utils.image_dataset_from_directory(
        train_dir, seed=123, image_size=(224, 224), batch_size=32, label_mode='categorical'
    )
    class_names = train_ds_raw.class_names
    
    # Export class names to a JSON file for the Flask app to use dynamically
    classes_path = '../classes.json'
    with open(classes_path, 'w') as f:
        json.dump(class_names, f)
    print(f"Exported {len(class_names)} classes to {classes_path}")

    train_ds, val_ds = get_datasets(train_dir, test_dir)

    # 2. Build Model
    model, base_model = build_model(num_classes=len(class_names))
    model.summary()

    # 3. Train Model (Feature Extraction)
    epochs = 10
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )

    # 4. Save Model
    model.save('../model_efficientnet.h5')
    print("Model saved to model_efficientnet.h5")

if __name__ == '__main__':
    main()
