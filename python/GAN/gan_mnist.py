# coding:utf-8
import tensorflow as tf
import random
import numpy as np
import matplotlib.pyplot as plt
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def conv2d(x, w):
    """
    Calculate the convolution of a image
    :param x: Input which is a image. It should be a tensor containing [batch, in_height, in_width, in_channels]
                In this case 28x28x1 image
    :param w: A CNN kernel(sliding window). It should be a tensor containing [filter_height, filter_width, in_channels, out_channels]
    :return: A tensor which is a 'feature map'
    """
    return tf.nn.conv2d(input=x, filter=w, strides=[1, 1, 1, 1], padding='SAME')  # strides: 步伐


def avg_pool_2x2(x):
    """
    Average pooling
    ksize: The size of the sliding window of pooling. A list with the length of 4
    strides: The value of sliding and it should be the same as ksize
    :param x: Input which is a image. It should be a tensor containing [batch, in_height, in_width, in_channels]
                In this case 28x28x1 image
    :return: A pooled tensor
    """
    # ksize: 池化窗口的大小，取一个四维向量，一般是[1, height, width, 1]
    # 因为我们不想在batch和channels上做池化，所以这两个维度设为了1
    # strides: 和卷积类似，窗口在每一个维度上滑动的步长，一般也是[1, stride,stride, 1]
    return tf.nn.avg_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def discriminator(x_image, reuse=False):
    # get_variable(): get or create a variable instead of a direct call to tf.Variable
    if reuse:
        tf.get_variable_scope().reuse_variables()

    # 每一层的输入是上一层的输出(第一层的输入是28x28的图像)

    # First Conv and Pool Layers stddev为standard deviation标准差
    # W为整层对下一层的权重
    W_conv1 = tf.get_variable('d_wconv1', [5, 5, 1, 8], initializer=tf.truncated_normal_initializer(stddev=0.02))
    b_conv1 = tf.get_variable('d_bconv1', [8], initializer=tf.constant_initializer(0))  # b为偏置节点
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)  # z = W*x+b relu为激活函数
    h_pool1 = avg_pool_2x2(h_conv1)  # 池化

    # Second Conv and Pool Layers
    W_conv2 = tf.get_variable('d_wconv2', [5, 5, 8, 16], initializer=tf.truncated_normal_initializer(stddev=0.02))
    b_conv2 = tf.get_variable('d_bconv2', [16], initializer=tf.constant_initializer(0))
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = avg_pool_2x2(h_conv2)

    # First Fully Connected Layer
    W_fc1 = tf.get_variable('d_wfc1', [7 * 7 * 16, 32], initializer=tf.truncated_normal_initializer(stddev=0.02))
    b_fc1 = tf.get_variable('d_bfc1', [32], initializer=tf.constant_initializer(0))
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*16])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)  # matmul: 矩阵相乘

    # Second Fully Connected Layer
    W_fc2 = tf.get_variable('d_wfc2', [32, 1], initializer=tf.truncated_normal_initializer(stddev=0.02))
    b_fc2 = tf.get_variable('d_bfc2', [1], initializer=tf.constant_initializer(0))

    # Final Layer
    y_conv = (tf.matmul(h_fc1, W_fc2) + b_fc2)
    return y_conv


def generator(z, batch_size, z_dim, reuse=False):
    if reuse:
        tf.get_variable_scope().reuse_variables()
    g_dim = 64  # Number of filters of first layer of generator
    c_dim = 1  # Color dimension of output (MNIST is grayscale, so c_dim = 1 for us)
    s = 28  # Output size of the image
    # We want to slowly upscale the image, so these values will help make that change gradual.
    s2, s4, s8, s16 = int(s/2), int(s/4), int(s/8), int(s/16)

    h0 = tf.reshape(z, [batch_size, s16+1, s16+1, 25])
    h0 = tf.nn.relu(h0)
    # Dimensions of h0 = batch_size x 2 x 2 x 25

    # First DeConv Layer
    output1_shape = [batch_size, s8, s8, g_dim*4]
    W_conv1 = tf.get_variable('g_wconv1', [5, 5, output1_shape[-1], int(h0.get_shape()[-1])],
                              initializer=tf.truncated_normal_initializer(stddev=0.1))
    b_conv1 = tf.get_variable('g_bconv1', [output1_shape[-1]], initializer=tf.constant_initializer(.1))
    H_conv1 = tf.nn.conv2d_transpose(h0, W_conv1, output_shape=output1_shape, strides=[1, 2, 2, 1], padding='SAME')
    H_conv1 = tf.contrib.layers.batch_norm(inputs = H_conv1, center=True, scale=True, is_training=True, scope="g_bn1")
    H_conv1 = tf.nn.relu(H_conv1)
    # Dimensions of H_conv1 = batch_size x 3 x 3 x 256

    # Second DeConv Layer
    output2_shape = [batch_size, s4 - 1, s4 - 1, g_dim*2]
    W_conv2 = tf.get_variable('g_wconv2', [5, 5, output2_shape[-1], int(H_conv1.get_shape()[-1])],
                              initializer=tf.truncated_normal_initializer(stddev=0.1))
    b_conv2 = tf.get_variable('g_bconv2', [output2_shape[-1]], initializer=tf.constant_initializer(.1))
    H_conv2 = tf.nn.conv2d_transpose(H_conv1, W_conv2, output_shape=output2_shape, strides=[1, 2, 2, 1], padding='SAME')
    H_conv2 = tf.contrib.layers.batch_norm(inputs=H_conv2, center=True, scale=True, is_training=True, scope="g_bn2")
    H_conv2 = tf.nn.relu(H_conv2)
    # Dimensions of H_conv2 = batch_size x 6 x 6 x 128

    # Third DeConv Layer
    output3_shape = [batch_size, s2 - 2, s2 - 2, g_dim*1]
    W_conv3 = tf.get_variable('g_wconv3', [5, 5, output3_shape[-1], int(H_conv2.get_shape()[-1])],
                              initializer=tf.truncated_normal_initializer(stddev=0.1))
    b_conv3 = tf.get_variable('g_bconv3', [output3_shape[-1]], initializer=tf.constant_initializer(.1))
    H_conv3 = tf.nn.conv2d_transpose(H_conv2, W_conv3, output_shape=output3_shape, strides=[1, 2, 2, 1], padding='SAME')
    H_conv3 = tf.contrib.layers.batch_norm(inputs = H_conv3, center=True, scale=True, is_training=True, scope="g_bn3")
    H_conv3 = tf.nn.relu(H_conv3)
    # Dimensions of H_conv3 = batch_size x 12 x 12 x 64

    # Fourth DeConv Layer
    output4_shape = [batch_size, s, s, c_dim]
    W_conv4 = tf.get_variable('g_wconv4', [5, 5, output4_shape[-1], int(H_conv3.get_shape()[-1])],
                              initializer=tf.truncated_normal_initializer(stddev=0.1))
    b_conv4 = tf.get_variable('g_bconv4', [output4_shape[-1]], initializer=tf.constant_initializer(.1))
    H_conv4 = tf.nn.conv2d_transpose(H_conv3, W_conv4, output_shape=output4_shape, strides=[1, 2, 2, 1], padding='VALID')
    H_conv4 = tf.nn.tanh(H_conv4)
    # Dimensions of H_conv4 = batch_size x 28 x 28 x 1

    return H_conv4

# Read the data from MNIST dataset
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/")

# Get the training dataset
x_train = mnist.train.images[:55000, :]
print(x_train.shape)

# Print an arbitary image from the training dataset
randomNum = random.randint(0, 55000)
image = x_train[randomNum].reshape([28, 28])
plt.imshow(image, cmap=plt.get_cmap('gray_r'))
plt.show()

sess = tf.Session()
z_dimensions = 100
z_test_placeholder = tf.placeholder(tf.float32, [None, z_dimensions])  # type of the elements to be fed, shape

sample_image = generator(z_test_placeholder, 1, z_dimensions)
test_z = np.random.normal(-1, 1, [1, z_dimensions])

sess.run(tf.global_variables_initializer())
temp = (sess.run(sample_image, feed_dict={z_test_placeholder: test_z}))

my_i = temp.squeeze()
plt.imshow(my_i, cmap='gray_r')
plt.show()

# Start training a GAN
batch_size = 16
tf.reset_default_graph()  # Since we changed our batch size (from 1 to 16), we need to reset our Tensorflow graph

sess = tf.Session()
x_placeholder = tf.placeholder("float", shape=[None, 28, 28, 1])  # Placeholder for input images to the discriminator
z_placeholder = tf.placeholder(tf.float32, [None, z_dimensions])  # Placeholder for input noise vectors to the generator

Dx = discriminator(x_placeholder)  # Dx will hold discriminator prediction probabilities for the real MNIST images
Gz = generator(z_placeholder, batch_size, z_dimensions)  # Gz holds the generated images
Dg = discriminator(Gz, reuse=True)  # Dg will hold discriminator prediction probabilities for generated images

# generator的损失函数
g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dg, labels=tf.ones_like(Dg)))

# discriminator的损失函数
d_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dx, labels=tf.ones_like(Dx)))
d_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=Dg, labels=tf.zeros_like(Dg)))
d_loss = d_loss_real + d_loss_fake

tvars = tf.trainable_variables()
d_vars = [var for var in tvars if 'd_' in var.name]
g_vars = [var for var in tvars if 'g_' in var.name]

trainerD = tf.train.GradientDescentOptimizer(0.01).minimize(d_loss, var_list=d_vars)
trainerG = tf.train.GradientDescentOptimizer(0.01).minimize(g_loss, var_list=g_vars)

sess.run(tf.global_variables_initializer())
iterations = 2000

print('Start training...')
for i in range(iterations):
    if i%100 == 0:
        print('Iteration', i)
    z_batch = np.random.normal(-1, 1, size=[batch_size, z_dimensions])
    real_image_batch = mnist.train.next_batch(batch_size)
    real_image_batch = np.reshape(real_image_batch[0], [batch_size, 28, 28, 1])
    # Update the discriminator
    _, dLoss = sess.run([trainerD, d_loss], feed_dict={z_placeholder: z_batch, x_placeholder:real_image_batch})
    # Update the generator
    _, gLoss = sess.run([trainerG, g_loss], feed_dict={z_placeholder: z_batch})

sample_image = generator(z_placeholder, 1, z_dimensions)
z_batch = np.random.normal(-1, 1, size=[1, z_dimensions])
temp = (sess.run(sample_image, feed_dict={z_placeholder: z_batch}))
my_i = temp.squeeze()
plt.imshow(my_i, cmap='gray_r')
plt.show()

print('Finished')
