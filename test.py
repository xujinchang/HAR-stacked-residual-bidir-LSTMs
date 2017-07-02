
from lstm_architecture import one_hot, run_with_config, test_with_config

import numpy as np

import os

from read_emotion import load_Y_my, load_X_my

from jiangwei import do_pca, load_X_pca

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
#--------------------------------------------
# Neural net's config.
#--------------------------------------------

class Config(object):
    """
    define a class to store parameters,
    the input should be feature mat of training and testing
    """

    def __init__(self, X_train, X_test):
        # Data shaping
        self.train_count = len(X_train)  # 451 training series
        self.test_data_count = len(X_test)  # 36 testing series
        self.n_steps = len(X_train[0])  # 128 time_steps per series
        self.n_classes = 2  # Final output classes

        # Training
        self.learning_rate = 0.001
        self.lambda_loss_amount = 0.005
        self.training_epochs = 10000
        self.batch_size = 30
        self.clip_gradients = 15.0
        self.gradient_noise_scale = None
        # Dropout is added on inputs and after each stacked layers (but not
        # between residual layers).
        self.keep_prob_for_dropout = 0.5  # **(1/3.0)0.85

        # Linear+relu structure
        self.bias_mean = 0.3
        # I would recommend between 0.1 and 1.0 or to change and use a xavier
        # initializer
        self.weights_stddev = 0.2

        ########
        # NOTE: I think that if any of the below parameters are changed,
        # the best is to readjust every parameters in the "Training" section
        # above to properly compare the architectures only once optimised.
        ########

        # LSTM structure
        # Features count is of 9: three 3D sensors features over time
        self.n_inputs = len(X_train[0][0])
        self.n_hidden = 28  # nb of neurons inside the neural network
        # Use bidir in every LSTM cell, or not:
        self.use_bidirectionnal_cells = False

        # High-level deep architecture
        self.also_add_dropout_between_stacked_cells = False  # True
        # NOTE: values of exactly 1 (int) for those 2 high-level parameters below totally disables them and result in only 1 starting LSTM.
        self.n_layers_in_highway = 3  # Number of residual connections to the LSTMs (highway-style), this is did for each stacked block (inside them).
        self.n_stacked_layers = 3  # Stack multiple blocks of residual
        # layers.


#--------------------------------------------
# Dataset-specific constants and functions + loading
#--------------------------------------------

# Useful Constants

# Those are separate normalised input features for the neural network

X_train_signals_paths = "/home/xujinchang/caffe-blur-pose/valid_fc7_feature_new.fea"
X_test_signals_paths = "/home/xujinchang/caffe-blur-pose/test_fc7_feature_new.fea"
y_train_path = "/home/xujinchang/caffe-blur-pose/valid_y_label_2.fea"
y_test_path = "/home/xujinchang/caffe-blur-pose/valid_y_label_2.fea"
#X_train = load_X_my(X_train_signals_paths)
X_valid_path  ="/localSSD/xjc/codalab_train/valid/valid_fc7_feature_new.fea"
#X_valid_path = "/localSSD/xjc/codalab_train/test/final_fc7_feature_new.fea"
#X_test = load_X_my(X_test_signals_paths)
X_valid_result = load_X_pca(X_valid_path)
X_valid_result = do_pca(X_valid_result)


n_layers_in_highway = 0
n_stacked_layers = 2
trial_name = "{}x{}".format(n_layers_in_highway, n_stacked_layers)
class EditedConfig(Config):
    def __init__(self, X, Y):
        super(EditedConfig, self).__init__(X, Y)
        self.n_layers_in_highway = n_layers_in_highway
        self.n_stacked_layers = n_stacked_layers

pred_out = test_with_config(EditedConfig, X_valid_result)
print type(pred_out)
fx = open('test_reslut','w')
print >>fx, (pred_out)
fx.close()
fy = open('test_label_result','w')
for item in xrange(0,len(pred_out)):
    print np.argmax(pred_out[item])
    fy.write(str(np.argmax(pred_out[item]))+'\n')

fy.close()

