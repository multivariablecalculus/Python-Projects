import tensorflow as tf
from keras.api import layers
import matplotlib.pyplot as plt
import numpy as np
import IPython from display

#Data
(tr_img, _), (_, _) = tf.keras.datasets.fashion_mnist.load_data()
tr_img = tr_img.reshape(tr_img.shape[0], 28, 28, 1).astype('float32')
tr_img = (tr_img - 127.5) / 127.5  #pls do not ask me why i didn't use the other moderation

bfz = 60000
btz = 256

#Training
tr_data = tf.data.Dataset.from_tensor_slices(tr_img).shuffle(bfz).batch(btz)

#Gen model
def generator_mod():
    model = tf.keras.Sequential()
    model.add(layers.Dense(7*7*256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((7, 7, 256)))
    assert model.output_shape == (None, 7, 7, 256)  # Note: None is the batch size

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    assert model.output_shape == (None, 28, 28, 1)

    return model

#Discrim
def discriminator_mod():
    model = tf.keras.Sequential()
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same', input_shape=[28, 28, 1]))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model

#Loss-Optmizing
cr_ent = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def discriml(realo, fakeo):
    real_loss = cr_ent(tf.ones_like(realo), realo)
    fake_loss = cr_ent(tf.zeros_like(fakeo), fakeo)
    total_loss = real_loss + fake_loss
    return total_loss

def genl(fakeo):
    return cr_ent(tf.ones_like(fakeo), fakeo)

generator = generator_mod()
discriminator = discriminator_mod()

gen_opt = tf.keras.optimizers.Adam(1e-4)
discrim_opt = tf.keras.optimizers.Adam(1e-4)

#Train loop
EPOCHS = 50
noise_dim = 100
num_ex = 16

seed = tf.random.normal([num_ex, noise_dim]) #for preloads

@tf.function
def tr_sp(images):
    noise = tf.random.normal([btz, noise_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        realo = discriminator(images, training=True)
        fakeo = discriminator(generated_images, training=True)

        gen_loss = genl(fakeo)
        disc_loss = discriml(realo, fakeo)

    gen_grad = gen_tape.gradient(gen_loss, generator.trainable_variables)
    discrim_grad = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    gen_opt.apply_gradients(zip(gen_grad, generator.trainable_variables))
    discrim_opt.apply_gradients(zip(discrim_grad, discriminator.trainable_variables))

def train(dataset, epochs):
    for epoch in range(epochs):
        for image_batch in dataset:
            tr_sp(image_batch)

        # GIFs
        display.clear_output(wait=True)
        gen_img(generator, epoch + 1, seed)

    # Epoch recall
    display.clear_output(wait=True)
    gen_img(generator, epochs, seed)

def gen_img(model, epoch, test_input):
    predictions = model(test_input, training=False)

    fig = plt.figure(figsize=(4, 4))

    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i+1)
        plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='gray')
        plt.axis('off')

    plt.savefig('image_at_epoch_{:04d}.png'.format(epoch))
    plt.show()

#Final Train
train(tr_data, EPOCHS)
