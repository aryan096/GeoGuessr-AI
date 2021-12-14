import os
import sys
import argparse
import re
from datetime import datetime
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras.applications import VGG16
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.layers import \
    Conv2D, MaxPool2D, Dropout, Flatten, Dense


import hyperparameters as hp
from model import GeoLocationCNN
from preprocess import Datasets
from skimage.transform import resize
from tensorboard_utils import \
        ImageLabelingLogger, ConfusionMatrixLogger, CustomModelSaver

from tensorflow.keras import layers, models, Model, optimizers
from skimage.io import imread
from skimage.segmentation import mark_boundaries
from matplotlib import pyplot as plt
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def parse_args():
    """ Perform command-line argument parsing. """

    parser = argparse.ArgumentParser(
        description="Geoguessr AI!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--load-checkpoint',
        default=None,
        help='''Path to model checkpoint file (should end with the
        extension .h5). Checkpoints are automatically saved when you
        train your model. If you want to continue training from where
        you left off, this is how you would load your weights.''')
    parser.add_argument(
        '--load-vgg',
        help='''Path to pre-trained VGG-16 file.''')
    parser.add_argument(
        '--confusion',
        action='store_true',
        help='''Log a confusion matrix at the end of each
        epoch (viewable in Tensorboard). This is turned off
        by default as it takes a little bit of time to complete.''')
    parser.add_argument(
        '--data',
        default='actualdata'+os.sep,
        help='Location where the dataset is stored.')
    parser.add_argument(
        '--evaluate',
        action='store_true',
        help='''Skips training and evaluates on the test set once.
        You can use this to test an already trained model by loading
        its checkpoint.''')
 
    return parser.parse_args()


def train(model, datasets, checkpoint_path, logs_path, init_epoch):
    """ Training routine. """

    # Keras callbacks for training
    callback_list = [
        tf.keras.callbacks.TensorBoard(
            log_dir=logs_path,
            update_freq='batch',
            profile_batch=0),
        ImageLabelingLogger(logs_path, datasets),
        CustomModelSaver(checkpoint_path, '3', hp.max_num_weights)
    ]

    # Include confusion logger in callbacks if flag set
    if ARGS.confusion:
        callback_list.append(ConfusionMatrixLogger(logs_path, datasets))

    # Begin training
    model.fit(
        x=datasets.train_data,
        validation_data=datasets.test_data,
        epochs=hp.num_epochs,
        batch_size=None,
        callbacks=callback_list,
        initial_epoch=init_epoch,
    )


def test(model, test_data):
    """ Testing routine. """

    # Run model on test set
    model.evaluate(
        x=test_data,
        verbose=1,
    )


def main():
    """ Main function. """
    #tf.config.set_visible_devices([], 'GPU')
    time_now = datetime.now()
    timestamp = time_now.strftime("%m%d%y-%H%M%S")
    init_epoch = 0
    use_vgg = 0

    # If loading from a checkpoint, the loaded checkpoint's directory
    # will be used for future checkpoints
    if ARGS.load_vgg is not None:
        use_vgg = 1

        checkpoint_path = "checkpoints" + os.sep + \
            "vgg_model" + os.sep + timestamp + os.sep

        logs_path = "logs" + os.sep + "vgg_model" + \
            os.sep + timestamp + os.sep

            # Make checkpoint directory if needed
        if not ARGS.evaluate and not os.path.exists(checkpoint_path):
            os.makedirs(checkpoint_path)

        datasets = Datasets(ARGS.data)

        vgg_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

        # Freeze four convolution blocks
        for layer in vgg_model.layers[:15]:
            layer.trainable = False# Make sure you have frozen the correct layers
        for i, layer in enumerate(vgg_model.layers):
            print(i, layer.name, layer.trainable)

        x = vgg_model.output
        x = Flatten()(x) # Flatten dimensions to for use in FC layers
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x) # Dropout layer to reduce overfitting
        x = Dense(89, activation='softmax')(x) # Softmax for multiclass
        model = Model(inputs=vgg_model.input, outputs=x)

        lr_reduce = ReduceLROnPlateau(monitor='val_accuracy', factor=0.6, patience=8, verbose=1, mode='max', min_lr=5e-5)

        checkpoint = ModelCheckpoint('vgg16_finetune.h15', monitor= 'val_accuracy', mode= 'max', save_best_only = True, verbose= 1)
  
        learning_rate= 1e-4
        model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizers.Adam(lr=learning_rate), metrics=["accuracy"])
        
        model.summary()

        if ARGS.evaluate:
            test(model, datasets.test_data)

        else:
            train(model, datasets, checkpoint_path, logs_path, init_epoch)


    # if ARGS.load_checkpoint is not None:
    #     ARGS.load_checkpoint = os.path.abspath(ARGS.load_checkpoint)

    #     # Get timestamp and epoch from filename
    #     regex = r"(?:.+)(?:\.e)(\d+)(?:.+)(?:.h5)"
    #     init_epoch = int(re.match(regex, ARGS.load_checkpoint).group(1)) + 1
    #     timestamp = os.path.basename(os.path.dirname(ARGS.load_checkpoint))


    # model = GeoLocationCNN()

    # model(tf.keras.Input(shape=(1280, 320, 3)))



    # # Compile model graph
    # model.compile(
    #     optimizer=model.optimizer,
    #     loss=model.loss_fn,
    #     metrics=["sparse_categorical_accuracy"])


# Make arguments global
ARGS = parse_args()

main()