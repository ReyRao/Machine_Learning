# -*- coding: utf-8 -*-
"""Day082_HW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ay9assCouG19dylDEflkiGlf-bUErZiR

## Work
1. 請比較使用不同層數以及不同 Dropout rate 對訓練的效果
2. 將 optimizer 改成使用 Adam 並加上適當的 dropout rate 檢視結果
"""

import os
import keras
import itertools
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
        y = keras.utils.to_categorical(y, num_classes=n_classes)
    return y

# Preproc the inputs
x_train = preproc_x(x_train)
x_test = preproc_x(x_test)

# Preprc the outputs
y_train = preproc_y(y_train)
y_test = preproc_y(y_test)
print(f'x_train shape: {x_train.shape}\ny_train shape: {y_train.shape}')

from keras.layers import Dropout
def build_mlp(input_data, output_data, dropout=0.0, n_neurons=[512, 256, 256, 256, 128]):
    """
    Build your own model
    """
    input_layer = keras.layers.Input([input_data.shape[-1]], name='input-layer')
    for i, n_unit in enumerate(n_neurons):
        if i == 0:
            x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(input_layer)
        else:
            x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(x)
            if i%2 == 0:
                x = Dropout(rate=dropout, name='dropout-layer'+str(i+1))(x)
    output_layer = keras.layers.Dense(units=output_data.shape[-1], activation='softmax', name='output-layer')(x)
    model = keras.models.Model(inputs=input_layer, outputs=output_layer)
    return model

model = build_mlp(x_train, y_train)
model.summary()

## 超參數設定
"""
Set Hyper-parameters here
"""
BATCH_SIZE = 1024
EPOCHS = 50
LEARNING_RATE = 0.003
DROPOUT = [0.1, 0.25, 0.33]

results = {}
"""
Write your training loop and record results
"""
for dropout in DROPOUT:
    model = build_mlp(x_train, y_train, dropout=dropout)
    model.summary()
    optimizer = keras.optimizers.adam(lr=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=['accuracy'])
    model.fit(x_train, y_train,
             batch_size=BATCH_SIZE,
             epochs=EPOCHS,
             validation_data=(x_test, y_test),
             shuffle=True)
    
    train_loss = model.history.history['loss']
    train_acc = model.history.history['acc']
    valid_loss = model.history.history['val_loss']
    valid_acc = model.history.history['val_acc']
    
    exp_tag = f'dropout: {dropout}'
    results[exp_tag] = {'train-loss': train_loss,
                        'valid-loss': valid_loss,
                        'train-acc': train_acc,
                        'valid-acc': valid_acc}

import matplotlib.pyplot as plt
# %matplotlib inline
"""
Plot results
"""
color = ['r', 'b', 'g', 'y', 'm', 'k']
plt.figure(figsize=(10, 8))
for i, condition in enumerate(results.keys()):
    plt.plot(range(len(results[condition]['valid-loss'])), results[condition]['valid-loss'], '-', label=condition ,color=color[i])
    plt.plot(range(len(results[condition]['train-loss'])), results[condition]['train-loss'], '--', label=condition ,color=color[i])
plt.title('Loss')
plt.legend()
plt.show()

plt.figure(figsize=(10, 8))
for i, condition in enumerate(results.keys()):
    plt.plot(range(len(results[condition]['valid-acc'])), results[condition]['valid-acc'], '-', label=condition ,color=color[i])
    plt.plot(range(len(results[condition]['train-acc'])), results[condition]['train-acc'], '--', label=condition ,color=color[i])
plt.title('Accuracy')
plt.legend()
plt.show()