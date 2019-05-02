# -*- coding: utf-8 -*-
"""Day083_HW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-asLprZ4UKnECNMKco_3EjVbcFQW9sJv

## Work
1. 試比較有 BN 在 Batch_size = 2, 16, 32, 128, 256 下的差異
2. 請嘗試將 BN 放在 Activation 之前，並比較訓練結果
3. 請於 BN 放在 Input Layer 後，並比較結果
"""

import os
import keras

# Disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = ""

(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
print(f'x_train shape: {x_train.shape}\ny_train shape: {y_train.shape}')

## 資料前處理
def preproc_x(x, flatten=True):
    x = x / 255
    if flatten == True:
        x = x.reshape(len(x), -1)
    return x

def preproc_y(y, n_classes=10):
    if y.shape[-1] == 1:
        y = keras.utils.to_categorical(y, n_classes)
    return y

# Preproc the inputs
x_train = preproc_x(x_train)
x_test = preproc_x(x_test)

# Preprc the outputs
y_train = preproc_y(y_train)
y_test = preproc_y(y_test)
print(f'x_train shape: {x_train.shape}\ny_train shape: {y_train.shape}')

from keras.layers import BatchNormalization, Activation
def build_mlp(input_data, output_data, n_neurons=[512, 256, 256, 256, 128], bn=False):
    """
    Build your own model
    """
    input_layer = keras.layers.Input([input_data.shape[-1]], name='input-layer')
    if bn == True:
        for i, n_unit in enumerate(n_neurons):
            if i == 0:
                x = BatchNormalization(name='BN-layer'+str(i+1))(input_layer)
                x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(x)
            else:
                x = BatchNormalization(name='BN-layer'+str(i+1))(x)
                x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(x)
    else:
        for i, n_unit in enumerate(n_neurons):
            if i == 0:
                x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(input_layer)
            else:
                x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(x)
    output_layer = keras.layers.Dense(units=output_data.shape[-1], activation='softmax', name='output-layer')(x)
    model = keras.models.Model(inputs=input_layer, outputs=output_layer)
    return model
model = build_mlp(x_train, y_train)
model.summary()

## 超參數設定
"""
Set your hyper-parameters
"""
BN = [False, True]
BATCH_SIZE = 1024
EPOCHS = 50
LEARNING_RATE = 0.003

results = {}
"""
Write your training loop and record results
"""
for bn in BN:
    model = build_mlp(x_train, y_train, bn=bn)
    model.summary()
    optimizer = keras.optimizers.adam(lr=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train,
                batch_size=BATCH_SIZE,
                epochs=EPOCHS,
                validation_data=(x_test, y_test),
                shuffle=True)
    
    train_loss = model.history.history['loss']
    valid_loss = model.history.history['val_loss']
    train_acc = model.history.history['acc']
    valid_acc = model.history.history['val_acc']
    
    exp_tag = f'mini-batchs normalization: {bn}'
    results[exp_tag] = {'train-loss': train_loss,
                        'valid-loss': valid_loss,
                        'train-acc': train_acc,
                        'valid-acc': valid_acc}

import matplotlib.pyplot as plt
# %matplotlib inline

"""
Plot results
"""

color = ['r', 'b', 'g', 'm', 'k', 'y']
plt.figure(figsize=(10, 8))
for i, condition in enumerate(results.keys()):
    plt.plot(range(len(results[condition]['train-loss'])), results[condition]['train-loss'], '-', color=color[i], label=condition)
    plt.plot(range(len(results[condition]['valid-loss'])), results[condition]['valid-loss'], '--', color=color[i], label=condition)
plt.legend()
plt.title('Loss')
plt.show()

plt.figure(figsize=(10, 8))
for i, condition in enumerate(results.keys()):
    plt.plot(range(len(results[condition]['train-acc'])), results[condition]['train-acc'], '-', color=color[i], label=condition)
    plt.plot(range(len(results[condition]['valid-acc'])), results[condition]['valid-acc'], '--', color=color[i], label=condition)
plt.legend()
plt.title('Accuracy')
plt.show()