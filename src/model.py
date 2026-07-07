import tensorflow as tf
from tensorflow.keras.applications import EfficientNetV2B0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

def build_model(num_classes, img_size=(224, 224)):
    """
    Builds a modern EfficientNetV2 model for transfer learning.
    """
    base_model = EfficientNetV2B0(
        input_shape=img_size + (3,),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze the base model
    base_model.trainable = False

    # Create new classification head
    inputs = tf.keras.Input(shape=img_size + (3,))
    # EfficientNetV2 has built-in preprocessing, so no manual scaling is needed
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    outputs = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs, outputs)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model, base_model
