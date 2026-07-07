import tensorflow as tf

def get_datasets(train_dir, test_dir, img_size=(224, 224), batch_size=32):
    """
    Creates tf.data.Dataset objects for training and validation using the modern image_dataset_from_directory.
    """
    train_ds = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        seed=123,
        image_size=img_size,
        batch_size=batch_size,
        label_mode='categorical'
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        test_dir,
        seed=123,
        image_size=img_size,
        batch_size=batch_size,
        label_mode='categorical'
    )

    # Prefetching for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds
