
#change cwd to script path, for debugging
import os
import sys
os.chdir(sys.path[0])

import argparse
import pickle
import random
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt


import MNIST_util
import nn_layer
import ANN
import CNN


import loss
import optimizer

# ========== Net Trainer - Begin ==========

def get_batch (X, Y, batch_size):
# randomly select batch_size data samples
  N = len(X)
  i = random.randint(1, N-batch_size)
  return X[i:i+batch_size], Y[i:i+batch_size]

def MakeOneHot (Y, D_out):
  N = Y.shape[0]
  Z = np.zeros((N, D_out))
  Z[np.arange(N), Y] = 1
  return Z

class MNIST_Trainer ():
  def __init__(self, X_train, Y_train, Net='LeNet5', opti='SGDMomentum'):
    # Prepare Data: Load, Shuffle, Normalization, Batching, Preprocessing
    self.X_train = X_train
    self.Y_train = Y_train

    self.batch_size = 64
    # D_in: input depth of network, 784, 28*28 input grayscale image
    self.D_in = 784
    # D_out: output depth of network = 10, the 10 digits
    self.D_out = 10

    print ('  Net: ' + str(Net))
    print ('  batch_size: ' + str(self.batch_size))
    print ('  D_in: ' + str(self.D_in))
    print ('  D_out: ' + str(self.D_out))
    print ('  Optimizer: ' + opti)

    # =======================
    if Net == 'TwoLayerNet':
      # H is the size of the one hidden layer.
      H=400
      self.model = ANN.TwoLayerNet (self.D_in, H, self.D_out)
    elif Net == 'ThreeLayerNet':
      # H1, H2 are the size of the two hidden layers.
      H1=300
      H2=100
      self.model = ANN.ThreeLayerNet (self.D_in, H1, H2, self.D_out)
      
    elif Net == 'LeNet5':
      self.model = CNN.LeNet5()

    # store training loss over iterations, for later visualization
    self.losses = []

    if opti == 'SGD':
      self.opti = optimizer.SGD (self.model.get_params(), lr=0.0001, reg=0)
    else:
      self.opti = optimizer.SGDMomentum (self.model.get_params(), lr=0.0001, momentum=0.80, reg=0.00003)

    self.criterion = loss.CrossEntropyLoss()


  def Train (self, Iter = None):
    if not Iter:
      Iter = 25000

    for i in range(Iter):
      # get batch, make onehot
      X_batch, Y_batch = get_batch (self.X_train, self.Y_train, self.batch_size)
      Y_batch = MakeOneHot (Y_batch, self.D_out)

      # forward, loss, backward, step
      Y_pred = self.model.forward (X_batch)
      loss, dout = self.criterion.get (Y_pred, Y_batch)
      self.model.backward (dout)
      self.opti.step()

      #LeNet5 is so slow that i print every single iter to see progress
      #print ('Iter %d (%.2f%%), loss = %f' % (i, 100.0*i/Iter, loss))

      if i % 100 == 0:
        print ('Iter %d (%.2f%%), loss = %f' % (i, 100.0*i/Iter, loss))
        self.losses.append(loss)

      #if i==0:
      #  viz_batch (X_batch, i)

    return self.model

# ========== Net Trainer - End ==========

# ========== Evaluation - Begin ==========

def determine_Train_Acc (model, X_train, Y_train):
  Y_pred = model.forward (X_train)
  result = np.argmax (Y_pred, axis=1) - Y_train
  result = list (result)

  n_correct = result.count(0)
  n_total = X_train.shape[0]
  Acc = float(n_correct) / n_total
  print ('TRAIN--> Correct: %d out of %d. Acc=%f' \
    % (n_correct, n_total, Acc))
  return Acc

def determine_Test_Acc (model, X_test, Y_test):
  Y_pred = model.forward (X_test)
  result = np.argmax (Y_pred, axis=1) - Y_test
  result = list (result)

  n_correct = result.count(0)
  n_total = X_test.shape[0]
  Acc = float(n_correct) / n_total
  print ('TEST--> Correct: %d out of %d. Acc=%f' \
    % (n_correct, n_total, Acc))
  return Acc

# ========== Evaluation - End ==========


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-model', dest='model', default='TwoLayerNet', choices=['TwoLayerNet', 'ThreeLayerNet', 'LeNet5'], help="Select the NeuralNet model")
  parser.add_argument('-iter', dest='iter', default=25000, type=int, help="Training iterations")
  parser.add_argument('-opti', dest='opti', default='SGDMomentum', choices=['SGDMomentum', 'SGD'], help="Select optimizer")
  args = parser.parse_args()


  X_train, Y_train, X_test, Y_test = MNIST_util.MNIST_preparation ()

  # Net: TwoLayerNet, ThreeLayerNet, LeNet5
  if args.model == 'TwoLayerNet':
    Net = 'TwoLayerNet'
  if args.model == 'ThreeLayerNet':
    Net = 'ThreeLayerNet'
  if args.model == 'LeNet5':
    Net = 'LeNet5'
    img_shape = (1, 28, 28)
    X_train = X_train.reshape(-1, *img_shape)
    X_test = X_test.reshape(-1, *img_shape)


  # optim: SGD, SGDMomentum
  opti = args.opti
  trainer = MNIST_Trainer (X_train, Y_train, Net, opti)

  #For 25000 iter TwoLayerNet, we should get train Acc 0.937983, test Acc 0.938700
  #For 25000 iter ThreeLayerNet, we should get train Acc 0.953133, test Acc 0.952500
  #For 1000 iter LeNet5, we should get test Acc 0.1135
  Iter = args.iter
  model = trainer.Train (Iter)

  # save params
  weights = model.get_params()
  with open ('~weights.pkl','wb') as f:
    pickle.dump (weights, f)

  # plot training loss over iterations
  plt.plot(range(0, Iter, 100), trainer.losses)
  #plt.savefig("Q1p1.png")
  #plt.savefig("Q1p2.png")
  #plt.savefig("Q2.png")
  #plt.savefig("Q3.png")
  plt.show()

  determine_Train_Acc (model, X_train, Y_train)
  determine_Test_Acc (model, X_test, Y_test)
