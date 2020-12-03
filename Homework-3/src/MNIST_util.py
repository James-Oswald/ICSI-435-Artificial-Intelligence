


import numpy as np
import pickle
import skimage.io as io
from urllib import request
import gzip

# ========== Download Load/Save MNIST - Begin ==========

filename = [
	['training_images','train-images-idx3-ubyte.gz'],
	['test_images','t10k-images-idx3-ubyte.gz'],
	['training_labels','train-labels-idx1-ubyte.gz'],
	['test_labels','t10k-labels-idx1-ubyte.gz']
]

def download_mnist():
  base_url = 'http://yann.lecun.com/exdb/mnist/'
  for name in filename:
    print('Downloading '+name[1]+'...')
    request.urlretrieve(base_url+name[1], name[1])
  print('Download complete.')

def save_mnist():
  mnist = {}
  for name in filename[:2]:
    with gzip.open(name[1], 'rb') as f:
      mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1,28*28)
  for name in filename[-2:]:
    with gzip.open(name[1], 'rb') as f:
      mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
  with open('mnist.pkl', 'wb') as f:
    pickle.dump(mnist,f)
  print ('Save complete.')

def load_MNIST_pkl ():
  with open('mnist.pkl','rb') as f:
    mnist = pickle.load(f)
  return mnist['training_images'], mnist['training_labels'], mnist['test_images'], mnist['test_labels']

# ========== Download Load/Save MNIST - End ==========

# ========== MNIST Visualization - Begin ==========

def get_MNIST_train_viz_pngs (X_train, Y_train):
  # each digit has around 6K images (max 6742).
  print ('MNIST train %d images' % (X_train.shape[0]))

  Iw = 28  # width of each digit image
  Ih = 28  # height of each digit image
  Tnx = 90 # number of X tile images
  Tny = 75 # number of Y tile images
  Tw = Tnx * Iw
  Th = Tny * Ih
  for d in range (10):
    # Get images of each digit
    Xd = X_train[Y_train==d]
    print ('Train: digit%d has %d images' % (d, Xd.shape[0]))

    TileI = np.zeros ((Th, Tw), dtype=np.uint8)
    i=0
    for ty in range (Tny):
      for tx in range (Tnx):
        if i>= Xd.shape[0]:
          continue
        I = Xd[i].reshape (28, 28)
        x0 = tx*Iw
        y0 = ty*Ih
        x1 = x0+Iw
        y1 = y0+Ih
        TileI[y0:y1, x0:x1] = I
        i += 1

    file = 'Train%0ds.png' % (d)
    io.imsave(file, TileI)
  return TileI

def get_MNIST_test_viz_pngs (X_test, Y_test):
  # each digit has around 1K images (max 1135).
  print ('MNIST test %d images' % (X_test.shape[0]))

  Iw = 28  # width of each digit image
  Ih = 28  # height of each digit image
  Tnx = 35 # number of X tile images
  Tny = 33 # number of Y tile images
  Tw = Tnx * Iw
  Th = Tny * Ih
  for d in range (10):
    # Get images of each digit
    Xd = X_test[Y_test==d]
    print ('Test: digit%d has %d images' % (d, Xd.shape[0]))

    TileI = np.zeros ((Th, Tw), dtype=np.uint8)
    i=0
    for ty in range (Tny):
      for tx in range (Tnx):
        if i>= Xd.shape[0]:
          continue
        I = Xd[i].reshape (28, 28)
        x0 = tx*Iw
        y0 = ty*Ih
        x1 = x0+Iw
        y1 = y0+Ih
        TileI[y0:y1, x0:x1] = I
        i += 1

    file = 'Test%0ds.png' % (d)
    io.imsave(file, TileI)

def viz_batch (X_batch, iter):
  Iw = 28  # width of each digit image
  Ih = 28  # height of each digit image
  Tnx = 8 # number of X tile images
  Tny = 8 # number of Y tile images
  Tw = Tnx * Iw
  Th = Tny * Ih
  TileI = np.zeros ((Th, Tw), dtype=np.uint8)
  i=0
  for ty in range (Tny):
    for tx in range (Tnx):
      if i>= X_batch.shape[0]:
        continue
      I = X_batch[i].reshape (28, 28)
      I += 0.1306
      I *= 255
      x0 = tx*Iw
      y0 = ty*Ih
      x1 = x0+Iw
      y1 = y0+Ih
      TileI[y0:y1, x0:x1] = I
      i += 1

    file = 'Batch%0d.png' % (iter)
    io.imsave(file, TileI)

# ========== MNIST Visualization - End ==========

# ========== MNIST Preparation - Begin ==========

def MNIST_preparation ():
  #mnist.init()
  X_train, Y_train, X_test, Y_test = load_MNIST_pkl ()
  # This normalize all pixel to be within [0 to 1]
  X_train, X_test = X_train/float(255), X_test/float(255)
  # Subtract mean: np.mean(X_train) = 0.1306, np.mean(X_test) = 0.1325
  train_mean = np.mean(X_train)
  test_mean = np.mean(X_test)
  print ('X_train mean: %f, X_test mean: %f' % (train_mean, test_mean))
  X_train -= train_mean
  X_test -= test_mean

  return X_train, Y_train, X_test, Y_test

# ========== MNIST Preparation - End ==========

if __name__ == '__main__':

  if 0:
    download_mnist()
    save_mnist()

  if 0:
    # Show samples from MNIST
    X_train, Y_train, X_test, Y_test = load_MNIST_pkl ()
    
    if 1:
      display_image(X_train, Y_train, 1)
      
    if 0:
      TileIs = get_MNIST_train_viz_pngs(X_train, Y_train)
      
      for i in range(len(TileIs)):
        file = 'Train%0ds.png' % (i)
        print ('Saving %s' % (file))
        io.imsave (file, TileIs[i])
        
    if 0:
      get_MNIST_test_viz_pngs (X_test, Y_test)
      
      for i in range(len(TileIs)):
        file = 'Test%0ds.png' % (i)
        print ('Saving %s' % (file))
        io.imsave (file, TileIs[i])
        