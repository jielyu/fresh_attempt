# encoding: utf-8

import time
import string
import tensorflow as tf


class Util(object):
    def __init__(self):
        pass

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
                w_conv = Util.getTFVariable(name='w_comv', shape=w_shape)
                if has_bias is True:
                    b_conv = Util.getTFVariable(name='b_conv', 
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
                w_fc = Util.getTFVariable(name='w_fc', shape=w_shape)
                if has_bias is True:
                    b_fc = Util.getTFVariable(name='b_fc', 
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