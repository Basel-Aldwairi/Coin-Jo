from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

train_ds, val_ds = image_dataset_from_directory(
    '../Data/proccessed',
    batch_size=32,
    image_size=(224, 224),
    subset='both',
    seed=18,
    validation_split=0.2,
)
base = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

base.trainable = False
inputs = Input(shape=(224, 224, 3))

x = preprocess_input(inputs)
x = base(x)
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
# x = Dense(64, activation='sigmoid')(x)

outputs = Dense(4, activation='softmax')(x)
model = Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
    )

checkpoint = ModelCheckpoint('model_ckeckpoint.weights.h5',
                             monitor='val_accuracy',
                             save_weights_only=True
                             )

model.fit(train_ds,
          validation_data=val_ds,
          epochs=10,
          callbacks=[early_stop, checkpoint]
          )

model.save('coin_model.keras')