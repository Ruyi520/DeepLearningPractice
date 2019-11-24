
# coding: utf-8

# In[91]:


'''
卷积神经网络：添加过拟合优化Drop_out
'''

from keras.utils import np_utils
from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as k
import matplotlib.pyplot as plt
import numpy as np


def loadData(path = 'mnist.npz'):
    f = np.load(path)
    X_train, y_train = f['x_train'], f['y_train']
    X_test, y_test = f['x_test'], f['y_test']
    f.close()
    
    return (X_train,y_train),(X_test,y_test)


# 从Keras导入Mnist数据集
(X_train, y_train), (X_test, y_test) = loadData()


#画出一部分图像进行展示
fig = plt.figure()
for i in range(9):
  plt.subplot(3,3,i+1)
  plt.tight_layout()
  plt.imshow(X_train[i], cmap='gray', interpolation='none')
  plt.title("Digit: {}".format(y_train[i]))
  plt.xticks([])
  plt.yticks([])
fig


# In[92]:


X_train.shape


# In[93]:


img_x,img_y = 28,28

X_train =  X_train.reshape(X_train.shape[0],img_x,img_y,1).astype('float32') 
X_test = X_test.reshape(X_test.shape[0],img_x,img_y,1).astype('float32')


# 数据标准化
X_train = X_train /255
X_test = X_test /255

#由于最终的输出结果是0-10的数字，属于多目标预测，因此进行one_hot编码，提高效率
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test) # y_test 由一维矩阵转换为二维矩阵
num_classes = 10

def create_model():
    model = Sequential()
    model.add(Conv2D(32,kernel_size=(5,5),activation='relu',input_shape=(img_x,img_y,1)))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
    model.add(Conv2D(64,kernel_size=(5,5),activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu')) #全连接层， 128神经元
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    return model
#开始训练
model = create_model()
model.fit(X_train,y_train,epochs = 3,batch_size = 200)

score = model.evaluate(X_test, y_test, verbose=0)
print('MLP: %.2f%%' % (score[1]*100))

