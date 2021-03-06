# -*- coding: utf-8 -*-
"""Day087HW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14nJz-ydO65F1KfmgYYNCsbStI22JDuoC

## Work
1. 請改變 reduce_lr 的 patience 和 factor 並比較不同設定下，對訓練/驗證集的影響
2. 請將 optimizer 換成 Adam、RMSprop 搭配 reduce_lr 並比較訓練結果
"""

import os
import keras
# Disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = ""

(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
print(f'x_train shape: {x_train.shape}\ny_train shape: {y_train.shape}\nx_test shape: {x_test.shape}\ny_test shape: {y_test.shape}')

## 資料前處理
def preproc_x(x, flatten=True):
    x = x / 255.
    if flatten:
        x = x.reshape((len(x), -1))
    return x

def preproc_y(y, num_classes=10):
    if y.shape[-1] == 1:
        y = keras.utils.to_categorical(y, num_classes)
    return y

# Preproc the inputs
x_train = preproc_x(x_train)
x_test = preproc_x(x_test)

# Preprc the outputs
y_train = preproc_y(y_train)
y_test = preproc_y(y_test)
print(f'x_train shape: {x_train.shape}\ny_train shape: {y_train.shape}\nx_test shape: {x_test.shape}\ny_test shape: {y_test.shape}')

def build_mlp(input_data, output_data, n_neurons=[512, 256, 128]):
    """
    Build your own model
    """
    input_layer = keras.layers.Input([input_data.shape[-1]], name='input-layer')
    for i, n_unit in enumerate(n_neurons):
        if i == 0:
            x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(input_layer)
        else:
            x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden-layer'+str(i+1))(x)
            
    output_layer = keras.layers.Dense(units=output_data.shape[-1],activation='softmax' , name='output-layer')(x)
    model = keras.models.Model(inputs=input_layer, outputs=output_layer)
    return model
model = build_mlp(x_train, y_train)
model.summary()

"""
Set your hyper-parameters
"""
LEARNING_RATE = [0.1, 3e-3, 1e-3]
EPOCHS = 50
BATCH_SIZE = 1024
MOMENTUM = 0.95

"""
Set model checkpoint callbacks
Write your training loop and show the results
"""
from keras.callbacks import ReduceLROnPlateau

reduce_lr = ReduceLROnPlateau(factor=0.5, 
                              min_lr=1e-4, 
                              monitor='val_loss', 
                              patience=5, 
                              verbose=1)

"""
plot the results
"""
results={}
for lr in LEARNING_RATE:
    keras.backend.clear_session()
    model = build_mlp(x_train, y_train)
    model.summary()
    print(f'LR: {lr}')
    optimizer = keras.optimizers.SGD(lr=lr, momentum=MOMENTUM, nesterov=True)
    model.compile(loss="categorical_crossentropy", metrics=["accuracy"], optimizer=optimizer)

    model.fit(x_train, y_train, 
              epochs=EPOCHS, 
              batch_size=BATCH_SIZE, 
              validation_data=(x_test, y_test), 
              shuffle=True,
              callbacks=[reduce_lr]
             )

    # Collect results
    #save data
    train_acc = model.history.history['acc']
    train_loss = model.history.history['loss']
    valid_acc = model.history.history['val_acc']
    valid_loss = model.history.history['val_loss']
    exp_tag = f'LR: {lr}'
    results[exp_tag] = {'train-loss': train_loss,
                        'train-acc': train_acc,
                        'valid-loss': valid_loss,
                        'valid-acc': valid_acc}

import matplotlib.pyplot as plt
# %matplotlib inline

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