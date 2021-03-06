import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

learning_rate = 0.001
training_iters = 100000
batch_size = 128
display_step = 10

n_input = 28
n_steps = 28
n_hidden = 128
n_classes = 10

x = tf.placeholder(tf.float32, [None, n_steps, n_input])
y = tf.placeholder(tf.float32, [None, n_classes])

weights = tf.Variable(tf.random_normal([n_hidden, n_classes]))
biases = tf.Variable(tf.random_normal([n_classes]))

print(x)

x2 = tf.transpose(x, [1, 0, 2])

print(x2)

x2= tf.reshape(x2, [-1, n_input])

print(x2)
x2 = tf.split(0, n_steps, x2 )

print(x2)
print(len(x2))

lstm_cell = tf.nn.rnn_cell.BasicLSTMCell( n_hidden, forget_bias=1.0)
outputs, states = tf.nn.rnn(lstm_cell, x2, dtype=tf.float32)
pred = tf.matmul(outputs[-1], weights ) + biases

cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(pred, y))
train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(init)
    step = 1

    while step * batch_size < training_iters:
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        print(batch_x.shape)
        batch_x = batch_x.reshape((batch_size, n_steps, n_input))
        sess.run(train, feed_dict={x: batch_x, y: batch_y})
        if step % display_step == 0:
            acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
            loss = sess.run(cost, feed_dict={x: batch_x, y: batch_y})
            print ("step : %d, acc: %f" % ( step, acc ))
        step += 1
    print("train complete!")

    test_len = 128
    test_data = mnist.test.images[:test_len].reshape((-1, n_steps, n_input))

    print(test_data.shape)

    test_label = mnist.test.labels[:test_len]
    print("test accuracy: ", sess.run( accuracy, feed_dict={x: test_data, y: test_label}))