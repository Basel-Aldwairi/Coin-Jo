
import tensorflow as tf

tf.config.set_visible_devices([], 'GPU')
tf.config.optimizer.set_jit(False)

from tensorflow.keras.utils import image_dataset_from_directory
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt


from tensorflow.keras.models import Model,load_model



model = load_model('coin_model.keras')

train_ds, val_ds = image_dataset_from_directory(
    '../Data/proccessed',
    batch_size=32,
    image_size=(224, 224),
    subset='both',
    seed=18,
    validation_split=0.2,
)


y_true = []
y_pred = []

for images, labels in val_ds:
    preds = model.predict(images)
    y_true.extend(labels.numpy())
    y_pred.extend(np.argmax(preds, axis=1))

y_true = np.array(y_true)
y_pred = np.array(y_pred)

cm = confusion_matrix(y_true, y_pred)
print(cm)
print(classification_report(y_true, y_pred, target_names=['1-2 Dinar','1-4 Dinar','5-Piasters','10-Piasters']))


plt.figure(figsize=(7,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['1-2 Dinar','1-4 Dinar','5-Piasters','10-Piasters'],
            yticklabels=['1-2 Dinar','1-4 Dinar','5-Piasters','10-Piasters'])

plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

