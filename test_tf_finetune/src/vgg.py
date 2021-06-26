# encoding: utf-8

import os, sys, time
import string
import numpy as np
import tensorflow as tf


class VGG(object):
    def __init__(self):
        self.img_mean = [103.939, 116.779, 123.68]  # BGR
        # self.img_mean = [123.68, 116.779, 103.939]  # RGB

    @staticmethod
    def getTimeStamp():
        """
        Function: Get string of current time stamp
        Input:
            None
        Output:
            string, time stamp
        Date: 2018-04-24
        Author: Jie Lyu
        """
        t = time.localtime(time.time())
        t_str = time.strftime('%Y-%m-%d-%H-%M-%S', t)
        return t_str
    
    @staticmethod
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
        if initializer is None:
            initializer = tf.truncated_normal(
                shape=shape, mean=0, stddev=0.1, dtype=tf.float32)
        return tf.get_variable(initializer=initializer, name=name)

    @staticmethod
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
        with tf.name_scope(name=name):
            red, green, blue = tf.split(axis=3, num_or_size_splits=3, value=rgb)
            m = img_mean
            values = [blue - m[0], green - m[1], red - m[2]]
            bgr = tf.concat(axis=3, values=values)
        return bgr
    
    @staticmethod
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
        with tf.variable_scope(name_or_scope=name, reuse=reuse):
            w_conv = None
            b_conv = None
            with tf.variable_scope(name_or_scope='Var', reuse=reuse):
                w_conv = VGG.getTFVariable(name='w_comv', shape=w_shape)
                if has_bias is True:
                    b_conv = VGG.getTFVariable(name='b_conv', 
                                                 shape=[w_shape[-1]])
            strides = [1, int_strides, int_strides, 1]
            conv = tf.nn.conv2d(
                input=x, filter=w_conv, 
                strides=strides, padding=padding, name='conv2d')
            if has_bias is True:
                conv = conv + b_conv
            if has_relu is True:
                conv = tf.nn.relu(conv, name='relu')
        return conv, w_conv, b_conv

    @staticmethod
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
        with tf.variable_scope(name_or_scope=name, reuse=reuse):
            w_fc = None
            b_fc = None
            with tf.variable_scope(name_or_scope='Var', reuse=reuse):
                w_fc = VGG.getTFVariable(name='w_fc', shape=w_shape)
                if has_bias is True:
                    b_fc = VGG.getTFVariable(name='b_fc', 
                                               shape=[w_shape[-1]])
            fc = tf.matmul(x, w_fc, name='matmul')
            if has_bias is True:
                fc = fc + b_fc
            if has_relu is True:
                fc = tf.nn.relu(fc, name='relu')
        return fc, w_fc, b_fc

    @staticmethod
    def buildPoolLayer(x, pool_type='max', int_ksize=2, int_strides=2, 
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
        ksize = [1, int_ksize, int_ksize, 1]
        strides = [1, int_strides, int_strides, 1]
        with tf.name_scope(name=name):
            if pool_type == 'max' or name == 'maximum':
                func = tf.nn.max_pool
            elif pool_type == 'avg' or name == 'average':
                func = tf.nn.avg_pool
            else:
                info = 'Not specific pool type: {0}'.format(pool_type)
                raise ValueError(info)
            pool = func(x, ksize=ksize, strides=strides, 
                        padding=padding, name=pool_type + 'pool')
        return pool
    

class VGG16(VGG):
    def __init__(self, img_shape=[224, 224, 3], only_conv=False):
        super(VGG16, self).__init__()
        self.img_shape = img_shape
        self.only_conv = only_conv
        self.featsize_list = None

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
        with tf.variable_scope(name_or_scope=name, reuse=reuse):
            # convert rgb tp bgr, and minus mean values
            img = self.buildBGRLayer(img, self.img_mean)
            isize = self.img_shape
            self.featsize_list = [isize]
            # Conv1
            w_shape = [3, 3, 3, 64]
            self.conv1_1, self.w_conv1_1, self.b_conv1_1 = \
                self.buildConv2dLayer(x=img, w_shape=w_shape, reuse=reuse, \
                                      name='conv1_1')
            w_shape = [3, 3, w_shape[-1], 64]
            self.conv1_2, self.w_conv1_2, self.b_conv1_2 = \
                self.buildConv2dLayer(x=self.conv1_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv1_2')
            self.pool1 = self.buildPoolLayer(self.conv1_2, name='pool1')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv2
            w_shape = [3, 3, w_shape[-1], 128]
            self.conv2_1, self.w_conv2_1, self.b_conv2_1 = \
                self.buildConv2dLayer(x=self.pool1, w_shape=w_shape, \
                                      reuse=reuse, name='conv2_1')
            w_shape = [3, 3, w_shape[-1], 128]
            self.conv2_2, self.w_conv2_2, self.b_conv2_2 = \
                self.buildConv2dLayer(x=self.conv2_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv2_2')
            self.pool2 = self.buildPoolLayer(self.conv2_2, name='pool2')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv3
            w_shape = [3, 3, w_shape[-1], 256]
            self.conv3_1, self.w_conv3_1, self.b_conv3_1 = \
                self.buildConv2dLayer(x=self.pool2, w_shape=w_shape, \
                                      reuse=reuse, name='conv3_1')
            w_shape = [3, 3, w_shape[-1], 256]
            self.conv3_2, self.w_conv3_2, self.b_conv3_2 = \
                self.buildConv2dLayer(x=self.conv3_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv3_2')
            self.conv3_3, self.w_conv3_3, self.b_conv3_3 = \
                self.buildConv2dLayer(x=self.conv3_2, w_shape=w_shape, \
                                      reuse=reuse, name='conv3_3')
            self.pool3 = self.buildPoolLayer(self.conv3_3, name='pool3')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv4
            w_shape = [3, 3, w_shape[-1], 512]
            self.conv4_1, self.w_conv4_1, self.b_conv4_1 = \
                self.buildConv2dLayer(x=self.pool3, w_shape=w_shape, \
                                      reuse=reuse, name='conv4_1')
            w_shape = [3, 3, w_shape[-1], 512]
            self.conv4_2, self.w_conv4_2, self.b_conv4_2 = \
                self.buildConv2dLayer(x=self.conv4_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv4_2')
            self.conv4_3, self.w_conv4_3, self.b_conv4_3 = \
                self.buildConv2dLayer(x=self.conv4_2, w_shape=w_shape, \
                                      reuse=reuse, name='conv4_3')
            self.pool4 = self.buildPoolLayer(self.conv4_3, name='pool4')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv5
            self.conv5_1, self.w_conv5_1, self.b_conv5_1 = \
                self.buildConv2dLayer(x=self.pool4, w_shape=w_shape, \
                                      reuse=reuse, name='conv5_1')
            self.conv5_2, self.w_conv5_2, self.b_conv5_2 = \
                self.buildConv2dLayer(x=self.conv5_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv5_2')
            self.conv5_3, self.w_conv5_3, self.b_conv5_3 = \
                self.buildConv2dLayer(x=self.conv5_2, w_shape=w_shape, \
                                      reuse=reuse, name='conv5_3')
            self.pool5 = self.buildPoolLayer(self.conv5_3, name='pool5')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            if self.only_conv is False:
                # reshape and compute dimension
                fsize = self.featsize_list[-1]
                fdim = fsize[0]*fsize[1]*fsize[2]
                #print('fsize={}, fdim={}'.format(fsize, fdim))
                feat = tf.reshape(self.pool5, [-1, fdim])
                self.featsize_list.append([fdim])
                # fc6
                w_shape = [fdim, 4096]
                self.fc6, self.w_fc6, self.b_fc6 = self.buildFCLayer(
                    x=feat, w_shape=w_shape, reuse=reuse, name='fc6')
                self.featsize_list.append([w_shape[-1]])
                # fc7
                w_shape = [w_shape[-1], 4096]
                self.fc7, self.w_fc7, self.b_fc7 = self.buildFCLayer(
                    x=self.fc6, w_shape=w_shape, reuse=reuse, name='fc7')
                # fc8
                w_shape = [w_shape[-1], 1000]
                self.fc8, self.w_fc8, self.b_fc8 = self.buildFCLayer(
                    x=self.fc7, w_shape=w_shape, has_relu=False, \
                    reuse=reuse, name='fc8')
                self.featsize_list.append([w_shape[-1]])
                # softmax
                self.prob = tf.nn.softmax(self.fc8, name='softmax')
                # Return the predicted probabilities
                return self.prob
            else:
                # Return the feature maps generated by conv layers
                return self.pool5
    
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
        var_tensor = {'conv1_1': [self.w_conv1_1, self.b_conv1_1],
                      'conv1_2': [self.w_conv1_2, self.b_conv1_2],
                      'conv2_1': [self.w_conv2_1, self.b_conv2_1],
                      'conv2_2': [self.w_conv2_2, self.b_conv2_2],
                      'conv3_1': [self.w_conv3_1, self.b_conv3_1],
                      'conv3_2': [self.w_conv3_2, self.b_conv3_2],
                      'conv3_3': [self.w_conv3_3, self.b_conv3_3],
                      'conv4_1': [self.w_conv4_1, self.b_conv4_1],
                      'conv4_2': [self.w_conv4_2, self.b_conv4_2],
                      'conv4_3': [self.w_conv4_3, self.b_conv4_3],
                      'conv5_1': [self.w_conv5_1, self.b_conv5_1],
                      'conv5_2': [self.w_conv5_2, self.b_conv5_2],
                      'conv5_3': [self.w_conv5_3, self.b_conv5_3],
                      'fc6': [self.w_fc6, self.b_fc6],
                      'fc7': [self.w_fc7, self.b_fc7],
                      'fc8': [self.w_fc8, self.b_fc8]}
        return var_tensor

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
        # get variable tensor dictionary
        var_tensor = self.get_var_tensor()
        # assign each variable tensor by ndarray 
        for key, value in var_tensor.items():
            # load conv layers only
            if self.only_conv:
                if string.find(key, 'fc') != -1:
                    continue
            # fetch weights and assign to corresponding tensors
            wb = weights[key]
            for idx, tensor in enumerate(value):
                if tensor is not None:
                    sess.run(tensor.assign(wb[idx]))
                    # print('assign tensor {} [idx={}]'.format(key, idx))

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
        print('INFO: {}, Loading VGG weights from file:...\r\n\t {}'.format(self.getTimeStamp(), npy_path))
        if not os.path.isfile(npy_path):
            raise ValueError('Not exist file: {} '.format(npy_path))
        # Read weights from npy file
        weights = np.load(npy_path, encoding='latin1').item()
        self.load_weights(sess=sess, weights=weights)
        print('INFO: {}, Load VGG weights completely'.format(self.getTimeStamp()))


class VGG19(VGG16):
    def __init__(self, img_shape=[224, 224, 3], only_conv=False):
        super(VGG19, self).__init__(img_shape=img_shape, only_conv=only_conv)

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
        with tf.variable_scope(name_or_scope=name, reuse=reuse):
            # convert rgb tp bgr, and minus mean values
            img = self.buildBGRLayer(img, self.img_mean)

            isize = self.img_shape
            self.featsize_list = [isize]
            # Conv1
            w_shape = [3, 3, 3, 64]
            self.conv1_1, self.w_conv1_1, self.b_conv1_1 = \
                self.buildConv2dLayer(x=img, w_shape=w_shape, reuse=reuse, \
                                      name='conv1_1')
            w_shape = [3, 3, w_shape[-1], 64]
            self.conv1_2, self.w_conv1_2, self.b_conv1_2 = \
                self.buildConv2dLayer(x=self.conv1_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv1_2')
            self.pool1 = self.buildPoolLayer(self.conv1_2, name='pool1')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv2
            w_shape = [3, 3, w_shape[-1], 128]
            self.conv2_1, self.w_conv2_1, self.b_conv2_1 = \
                self.buildConv2dLayer(x=self.pool1, w_shape=w_shape, \
                                      reuse=reuse, name='conv2_1')
            w_shape = [3, 3, w_shape[-1], 128]
            self.conv2_2, self.w_conv2_2, self.b_conv2_2 = \
                self.buildConv2dLayer(x=self.conv2_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv2_2')
            self.pool2 = self.buildPoolLayer(self.conv2_2, name='pool2')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv3
            w_shape = [3, 3, w_shape[-1], 256]
            self.conv3_1, self.w_conv3_1, self.b_conv3_1 = \
                self.buildConv2dLayer(x=self.pool2, w_shape=w_shape, \
                                      reuse=reuse, name='conv3_1')
            w_shape = [3, 3, w_shape[-1], 256]
            self.conv3_2, self.w_conv3_2, self.b_conv3_2 = \
                self.buildConv2dLayer(x=self.conv3_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv3_2')
            self.conv3_3, self.w_conv3_3, self.b_conv3_3 = \
                self.buildConv2dLayer(x=self.conv3_2, w_shape=w_shape, \
                                      reuse=reuse, name='conv3_3')
            self.conv3_4, self.w_conv3_4, self.b_conv3_4 = \
                self.buildConv2dLayer(x=self.conv3_3, w_shape=w_shape, \
                                      reuse=reuse, name='conv3_4')
            self.pool3 = self.buildPoolLayer(self.conv3_4, name='pool3')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv4
            w_shape = [3, 3, w_shape[-1], 512]
            self.conv4_1, self.w_conv4_1, self.b_conv4_1 = \
                self.buildConv2dLayer(x=self.pool3, w_shape=w_shape, \
                                      reuse=reuse, name='conv4_1')
            w_shape = [3, 3, w_shape[-1], 512]
            self.conv4_2, self.w_conv4_2, self.b_conv4_2 = \
                self.buildConv2dLayer(x=self.conv4_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv4_2')
            self.conv4_3, self.w_conv4_3, self.b_conv4_3 = \
                self.buildConv2dLayer(x=self.conv4_2, w_shape=w_shape, \
                                      reuse=reuse, name='conv4_3')
            self.conv4_4, self.w_conv4_4, self.b_conv4_4 = \
                self.buildConv2dLayer(x=self.conv4_3, w_shape=w_shape, \
                                      reuse=reuse, name='conv4_4')
            self.pool4 = self.buildPoolLayer(self.conv4_4, name='pool4')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            # Conv5
            self.conv5_1, self.w_conv5_1, self.b_conv5_1 = \
                self.buildConv2dLayer(x=self.pool4, w_shape=w_shape, \
                                      reuse=reuse, name='conv5_1')
            self.conv5_2, self.w_conv5_2, self.b_conv5_2 = \
                self.buildConv2dLayer(x=self.conv5_1, w_shape=w_shape, \
                                      reuse=reuse, name='conv5_2')
            self.conv5_3, self.w_conv5_3, self.b_conv5_3 = \
                self.buildConv2dLayer(x=self.conv5_2, w_shape=w_shape, \
                                      reuse=reuse, name='conv5_3')
            self.conv5_4, self.w_conv5_4, self.b_conv5_4 = \
                self.buildConv2dLayer(x=self.conv5_3, w_shape=w_shape, \
                                      reuse=reuse, name='conv5_4')
            self.pool5 = self.buildPoolLayer(self.conv5_4, name='pool5')
            isize = [int(isize[0]/2), int(isize[1]/2), w_shape[-1]]
            self.featsize_list.append(isize)

            if self.only_conv is False:
                # reshape and compute dimension
                fsize = self.featsize_list[-1]
                fdim = fsize[0]*fsize[1]*fsize[2]
                #print('fsize={}, fdim={}'.format(fsize, fdim))
                feat = tf.reshape(self.pool5, [-1, fdim])
                self.featsize_list.append([fdim])
                # fc6
                w_shape = [fdim, 4096]
                self.fc6, self.w_fc6, self.b_fc6 = self.buildFCLayer(
                    x=feat, w_shape=w_shape, reuse=reuse, name='fc6')
                self.featsize_list.append([w_shape[-1]])
                # fc7
                w_shape = [w_shape[-1], 4096]
                self.fc7, self.w_fc7, self.b_fc7 = self.buildFCLayer(
                    x=self.fc6, w_shape=w_shape, reuse=reuse, name='fc7')
                # fc8
                w_shape = [w_shape[-1], 1000]
                self.fc8, self.w_fc8, self.b_fc8 = self.buildFCLayer(
                    x=self.fc7, w_shape=w_shape, has_relu=False, \
                    reuse=reuse, name='fc8')
                self.featsize_list.append([w_shape[-1]])
                # softmax
                self.prob = tf.nn.softmax(self.fc8, name='softmax')
                # Return the predicted probabilities
                return self.prob
            else:
                # Return the feature maps generated by conv layers
                return self.pool5

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
        var_tensor = {'conv1_1': [self.w_conv1_1, self.b_conv1_1],
                      'conv1_2': [self.w_conv1_2, self.b_conv1_2],
                      'conv2_1': [self.w_conv2_1, self.b_conv2_1],
                      'conv2_2': [self.w_conv2_2, self.b_conv2_2],
                      'conv3_1': [self.w_conv3_1, self.b_conv3_1],
                      'conv3_2': [self.w_conv3_2, self.b_conv3_2],
                      'conv3_3': [self.w_conv3_3, self.b_conv3_3],
                      'conv3_4': [self.w_conv3_4, self.b_conv3_4],
                      'conv4_1': [self.w_conv4_1, self.b_conv4_1],
                      'conv4_2': [self.w_conv4_2, self.b_conv4_2],
                      'conv4_3': [self.w_conv4_3, self.b_conv4_3],
                      'conv4_4': [self.w_conv4_4, self.b_conv4_4],
                      'conv5_1': [self.w_conv5_1, self.b_conv5_1],
                      'conv5_2': [self.w_conv5_2, self.b_conv5_2],
                      'conv5_3': [self.w_conv5_3, self.b_conv5_3],
                      'conv5_4': [self.w_conv5_4, self.b_conv5_4],
                      'fc6': [self.w_fc6, self.b_fc6],
                      'fc7': [self.w_fc7, self.b_fc7],
                      'fc8': [self.w_fc8, self.b_fc8]}
        return var_tensor

def main_vgg16():
    import skimage.io
    import matplotlib.pyplot as plt
    npy_path = '../models/vgg/vgg16.npy'
    img_path = '../data/face.png'
    img_path = '../data/person.jpg'

    # img = tf.constant(200, shape=[1, 224, 224, 3], dtype=tf.float32)
    img = tf.placeholder(shape=[1, 224, 224, 3], dtype=tf.float32)
    vgg16 = VGG16()
    vgg16_output = vgg16.forward(img)
    # print(vgg16_output)

    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        vgg16.load_weights_from_npy(sess=sess, npy_path=npy_path)

        image = skimage.io.imread(img_path)
        image = image[:, :, 0:3]
        image = np.expand_dims(image, axis=0)
        res = sess.run(vgg16_output, feed_dict={img:image})
        plt.plot(res[0])
        # plt.show()
        index = np.argmax(res, axis=1)
        index = index[0]
        print('index={}, score={}, cate=none'.format(index, res[0][index]))


def main_vgg19():
    import skimage.io
    import matplotlib.pyplot as plt
    npy_path = '../models/vgg/vgg19.npy'
    img_path = '../data/face.png'
    img_path = '../data/person.jpg'

    # img = tf.constant(200, shape=[1, 224, 224, 3], dtype=tf.float32)
    img = tf.placeholder(shape=[1, 224, 224, 3], dtype=tf.float32)
    vgg = VGG19()
    vgg_output = vgg.forward(img)

    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        vgg.load_weights_from_npy(sess=sess, npy_path=npy_path)

        image = skimage.io.imread(img_path)
        image = image[:, :, 0:3]
        image = np.expand_dims(image, axis=0)
        res = sess.run(vgg_output, feed_dict={img:image})
        plt.plot(res[0])
        # plt.show()
        index = np.argmax(res, axis=1)
        index = index[0]
        print('index={}, score={}, cate=none'.format(index, res[0][index]))

def main():
    print(sys.argv)
    # main_vgg16()
    main_vgg19()
    

if __name__ == '__main__':
    main()
