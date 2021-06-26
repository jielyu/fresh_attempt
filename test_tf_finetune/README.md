# tf-finetune
provide code to finetune several famous models
[TOC]
## VGG
/src/vgg.py provide 3 classes which are described as the following:

### VGG
Basic class which provides some static method as tools
```python
def getTimeStamp()
    """
    Function: Get string of current time stamp
    Input:
        None
    Output:
        string, time stamp
    Date: 2018-04-24
    Author: Jie Lyu
    """

def getTFVariable(name, shape, initializer=None):
    """
    Function: Create a variavle tensor with the specific shape
    Input:
        name, name of the variable 
        shape, shape of the variable
        initializer=None, initializer
    Output:
        var
    Date: 2018-04-24
    Author: Jie Lyu
    """

def buildBGRLayer(rgb, img_mean, name='BGRLayer'):
    """
    Function: Convert RGB images to BGR format
    Input: 
        rgb, tensor, 4d[n, h, w, c(r,g,b)]
        img_mean, mean values for all channels, list, 3-element, [b,g,r]
        name, sub-net name
    Output:
        bgr, tensor, 4d[n,h,w,c(b,g,r)]
    Date: 2018-04-25
    Author: Jie Lyu
    """
    
def buildConv2dLayer(x, w_shape, int_strides=1, padding='SAME',
                         has_bias=True, has_relu=True, reuse=False, 
                         name='Conv'):
    """
    Function: Build a conv2d layer
    Input:
        x,              input tensor, 4d[n, h, w, c]
        w_shape, list,  4-element, [h, w, pre_ch, num_output]
        int_strides=1,  int, strides number
        padding='SAME', set padding style
        has_bias=True,  set with/without bias component
        has_relu=True,  set followed/unfollowed with relu activation
        reuse=False,    set reuse flag
        name='Conv',    set name of this sub-net
    Output:
        conv,           out results of conv
        w_conv,         filters of conv layer
        b_conv          biases of conv layer
    Date: 2018-04-24
    Author: Jie Lyu
    """ 
    
def buildFCLayer(x, w_shape, has_bias=True, has_relu=True, 
                     reuse=False, name='FC'):
    """
    Function: Build a full-connected layer
    Input:
        x,              input tensor, 2d[n, feat_dim]
        w_shape, list,  2-element, [feat_dim, num_output]
        has_bias=True,  set with/without bias component
        has_relu=True,  set followed/unfollowed with relu activation
        reuse=False,    set reuse flag
        name='FC',      set name of this sub-net
    Output:
        fc,             out results of inner-producted
        w_fc,           filters of full-connected layer
        b_fc            biases of full-connected layer
    Date: 2018-04-24
    Author: Jie Lyu
    """
    
def buildPool(x, pool_type='max', int_ksize=2, int_strides=2, 
                    padding='SAME', name='Pool'):
    """
    Function: Build a pooling layer
    Input:
        x,                  input tensor, 4d[n, h, w, c]
        pool_type='max',    set pooling type, max or avg, string
        int_ksize=2,        set pooling kernel size, int
        int_strides=2,      set strides, int
        padding='SAME',     set padding style
        name='Pool'         set name of the sub-net
    Output:
        pool, result of pooling layer
    Date: 2018-04-24
    Author: Jie Lyu
    """
```

### VGG16
weight file: https://mega.nz/#!YU1FWJrA!O1ywiCS2IiOlUCtCpI6HTJOMrneN-Qdv3ywQP5poecM

Inherited from class VGG
```python
def forward(self, img, reuse=False, trainable=False, name='VGG16'):
    """
    Function: Build forward graph of vgg16 network
    Input:
        img,                tensor, 4d, [n, h, w, c] 
        reuse=False,        set reuse flag
        trainable=False,    set trainable flag
        name='VGG16'        set name of the sub-set
    Output:
        feature map         conv feature or fc feature
    Date: 2018-04-24
    Author: Jie Lyu
    """
    
def get_var_tensor(self):
    """
    Function: Get a mapping from name to variable tensors
    Input:
        None
    Output:
        var_tensor, dict, {'name': [w_tensor, b_tensor]}
    Date: 2018-04-24
    Author: Jie Lyu
    """
    
def load_weights(self, sess, weights):
    """
    Function: Load weights from ndarray
    Input: 
        sess,   tf.Session() 
        weights, all weights, ndarray
    Output:
        None
    Date: 2018-04-24
    Author: Jie Lyu
    """
    
def load_weights_from_npy(self, sess, npy_path):
    """
    Function: Load weights from npy file
    Input: 
        sess,   tf.Session() 
        npy_path, path of a npy file
    Output:
        None
    Date: 2018-04-24
    Author: Jie Lyu
    """
```

### VGG19
weight file: https://mega.nz/#!xZ8glS6J!MAnE91ND_WyfZ_8mvkuSa2YcA7q-1ehfSm-Q1fxOvvs

Inherited from class VGG16

Overwrite two function: forward, get_var_tensor

```python
def forward(self, img, reuse=False, trainable=False, name='VGG19'):
    """
    Function: Build forward graph of vgg19 network
    Input:
        img,                tensor, 4d, [n, h, w, c] 
        reuse=False,        set reuse flag
        trainable=False,    set trainable flag
        name='VGG19'        set name of the sub-set
    Output:
        feature map         conv feature or fc feature
    Date: 2018-04-24
    Author: Jie Lyu
    """
    
def get_var_tensor(self):
    """
    Function: Get a mapping from name to variable tensors
    Input:
        None
    Output:
        var_tensor, dict, {'name': [w_tensor, b_tensor]}
    Date: 2018-04-24
    Author: Jie Lyu
    """
```

### Tesing Function
```python
def main_vgg16()

def main_vgg19()
```
