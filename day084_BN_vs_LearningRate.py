# -*- coding: utf-8 -*-
"""Day084_HW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vDA6BanJgXzRh7v_t2WoXE7ntXYT3OsS

## Work
請結合前面的知識與程式碼，比較不同的 regularization 的組合對訓練的結果與影響：如 dropout, regularizers, batch-normalization 等
"""

import os
import keras
import itertools
# Disable GPU
# os.environ["CUDA_VISIBLE_DEVICES"] = ""

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

# Hint 1 : 在 Dense 層中增加 Regularizers
# Hint 2 : 增加 Dropout 層並設定 dropout ratio
# Hint 3 : 增加 Batch-normalization 層
from keras.layers import Dropout, BatchNormalization
def build_mlp(input_data, output_data, n_neurons=[512, 256, 256, 256, 128], bn=False):
    """
    Build your own model
    """
    input_layer = keras.layers.Input([input_data.shape[-1]], name='input-layer')
    if bn == True:
        x = BatchNormalization(name='input-BN-layer')(input_layer)

    for i, n_unit in enumerate(n_neurons):
        if bn == True:
            x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(x)
            x = BatchNormalization(name='BN-layer'+str(i+1))(x)
        else:
            if i == 0:
                x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(input_layer)
            else:
                x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(x)

    output_layer = keras.layers.Dense(units=output_data.shape[-1], activation='softmax', name='output-layer')(x)
    model = keras.models.Model(outputs=output_layer, inputs=input_layer)
    return model

model = build_mlp(x_train, y_train, bn=True)
model.summary()

## 超參數設定
"""
Set your hyper-parameters
"""
BATCH_SIZE = 1024
EPOCHS = 50
LEARNING_RATE = [0.05, 0.01, 0.003, 0.001]
BN = [False, True]

results = {}
"""
Write your training loop and record results
"""
for bn in BN:
    for lr in LEARNING_RATE:
        keras.backend.clear_session()
        model = build_mlp(x_train, y_train, bn=bn)
        model.summary()
        print(f'bn: {bn}\nlearning rate: {lr}')
        optimizer = keras.optimizers.adam(lr=lr)
        model.compile(loss="categorical_crossentropy", metrics=["accuracy"], optimizer=optimizer)
        model.fit(x_train, y_train, 
                  epochs=EPOCHS, 
                  batch_size=BATCH_SIZE, 
                  validation_data=(x_test, y_test),
                  shuffle=True)

        #save data for each of the condition
        train_loss = model.history.history['loss']
        valid_loss = model.history.history['val_loss']
        train_acc = model.history.history['acc']
        valid_acc = model.history.history['val_acc']

        exp_tag = f'bn: {bn},learning rate: {lr}'
        results[exp_tag] = {'train-loss': train_loss,
                            'valid-loss': valid_loss,
                            'train-acc': train_acc,
                            'valid-acc': valid_acc}

import matplotlib.pyplot as plt
# %matplotlib inline
print(results.keys())

"""
Plot results
"""
color = ['r', 'b', 'g', 'm', 'k', 'y', 'c', 'g']
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