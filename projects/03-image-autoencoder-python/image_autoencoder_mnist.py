"""
Image Autoencoder (MNIST)
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

OUT_DIR = Path(__file__).resolve().parent / "assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main(encoding_dim: int = 32, epochs: int = 50, batch_size: int = 256) -> None:
    input_img = Input(shape=(784,))
    encoded = Dense(encoding_dim, activation="relu")(input_img)
    decoded = Dense(784, activation="sigmoid")(encoded)

    autoencoder = Model(input_img, decoded)
    encoder = Model(input_img, encoded)

    encoded_input = Input(shape=(encoding_dim,))
    decoder_layer = autoencoder.layers[-1]
    decoder = Model(encoded_input, decoder_layer(encoded_input))

    autoencoder.compile(optimizer="adadelta", loss="binary_crossentropy")

    (x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
    x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

    autoencoder.fit(
        x_train, x_train,
        epochs=epochs, batch_size=batch_size,
        shuffle=True, validation_data=(x_test, x_test),
        verbose=2
    )

    encoded_imgs = encoder.predict(x_test, verbose=0)
    decoded_imgs = decoder.predict(encoded_imgs, verbose=0)

    n = 10
    plt.figure(figsize=(20, 4))
    for i in range(n):
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(x_test[i].reshape(28, 28), cmap="gray")
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(decoded_imgs[i].reshape(28, 28), cmap="gray")
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

    plt.tight_layout()
    out = OUT_DIR / "mnist_autoencoder_reconstruction.png"
    plt.savefig(out, dpi=200)
    plt.close()
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
