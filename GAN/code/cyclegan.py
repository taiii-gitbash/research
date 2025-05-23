# -*- coding: utf-8 -*-
"""CycleGAN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Jp607vVHwg8jUQ-bsVL7qm5C_wVQxYqB
"""

import pathlib
import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#データのパスをここで指定します。
data_root = pathlib.Path("/content/drive/MyDrive/GAN")
train_x_paths = list(data_root.glob('man/*'))
train_x_paths = [str(path) for path in train_x_paths]

train_y_paths = list(data_root.glob('woman/*'))
train_y_paths = [str(path) for path in train_y_paths]

test_x_paths = list(data_root.glob('man/*'))
test_x_paths = [str(path) for path in test_x_paths]

test_y_paths = list(data_root.glob('woman/*'))
test_y_paths = [str(path) for path in test_y_paths]

painting_path = random.choice(train_x_paths)
photo_path = random.choice(train_y_paths)

#画像を読み込む
painting = tf.keras.preprocessing.image.load_img(painting_path,)
photo = tf.keras.preprocessing.image.load_img(photo_path,)
#読み込んだ画像をnumpy arrayに変換する
painting = tf.keras.preprocessing.image.img_to_array(painting)
photo = tf.keras.preprocessing.image.img_to_array(photo)

#画像の形状を(batch,h,w,channel)に拡張する(これがないとエラーが起こる)
painting = painting[tf.newaxis]/255
photo = photo[tf.newaxis]/255

#画像を表示する
fig,axes = plt.subplots(1,2,figsize=(10,5))
ax1 = axes[0]
ax1.imshow(painting[0])
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_title("man")

ax2 = axes[1]
ax2.imshow(photo[0])
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_title("woman")

plt.show()

import pathlib
import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
AUTOTUNE = tf.data.AUTOTUNE

#データのパスをここで指定します。
data_root = pathlib.Path("/content/drive/MyDrive/GAN")
train_x_paths = list(data_root.glob('man/*'))
train_x_paths = [str(path) for path in train_x_paths][:100]

train_y_paths = list(data_root.glob('woman/*'))
train_y_paths = [str(path) for path in train_y_paths][:100]

test_x_paths = list(data_root.glob('man/*'))
test_x_paths = [str(path) for path in test_x_paths][:100]

test_y_paths = list(data_root.glob('woman/*'))
test_y_paths = [str(path) for path in test_y_paths][:100]

#訓練用の写真をクロッピング、左右反転、正規化するための関数
def preprocess_image_train(path):
    image = tf.io.read_file(path)
    # 生データのテンソルを画像のテンソルに変換する。
    # これによりshape=(240,240,3)になる
    image = tf.image.decode_jpeg(image, channels=3)
    # モデルに合わせてリサイズする
    image = tf.image.resize(image, [286, 286],method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    #指定した範囲を切り取るクロッピング
    image = tf.image.random_crop(
      image, size=[256,256, 3])

    #ランダムなミラーリング
    image = tf.image.random_flip_left_right(image)
    #正規化を行う
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1

    return image

def preprocess_image_test(path):
    image = tf.io.read_file(path)
    # 生データのテンソルを画像のテンソルに変換する。
    # これによりshape=(240,240,3)になる
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.random_crop(
      image, size=[256,256, 3])

    #ランダムなミラーリング
    image = tf.image.random_flip_left_right(image)
    #正規化を行う
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1

    return image

#arrayからtensorへ変換します
train_x = tf.data.Dataset.from_tensor_slices(train_x_paths)
train_y = tf.data.Dataset.from_tensor_slices(train_y_paths)
test_x = tf.data.Dataset.from_tensor_slices(test_x_paths)
test_y = tf.data.Dataset.from_tensor_slices(test_y_paths)

#各データの出力数を変数に格納します
len_train_x = len(train_x)
len_train_y = len(train_y)
len_test_x = len(test_x)
len_test_y = len(test_y)

#画像のパスから画像データをtensorとして取り出し、前処理、バッチ化を行います。
train_x = train_x.map(
    preprocess_image_train, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_train_x).batch(1)

train_y = train_y.map(
    preprocess_image_train, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_train_y).batch(1)

test_x = test_x.map(
    preprocess_image_test, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_test_x).batch(1)

test_y = test_y.map(
    preprocess_image_test, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_test_y).batch(1)

#適当な一組の画像ペアを取り出します
sample_x = next(iter(train_x))
sample_y = next(iter(train_y))

#元の画像と左右反転画像を表示させます。
plt.subplot(221)
plt.title('man')
plt.imshow(sample_x[0] * 0.5 + 0.5)
plt.axis('off')

plt.subplot(222)
plt.title('man with random jitter')
plt.imshow(tf.image.random_flip_left_right(sample_x[0]) * 0.5 + 0.5)
plt.axis('off')

plt.subplot(223)
plt.title('woman')
plt.imshow(sample_y[0] * 0.5 + 0.5)
plt.axis('off')

plt.subplot(224)
plt.title('woman with random jitter')
plt.imshow(tf.image.random_flip_left_right(sample_y[0]) * 0.5 + 0.5)
plt.axis('off')

import pathlib
import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
AUTOTUNE = tf.data.AUTOTUNE

#データのパスをここで指定します。
data_root = pathlib.Path("/content/drive/MyDrive/GAN")
train_x_paths = list(data_root.glob('man/*'))
train_x_paths = [str(path) for path in train_x_paths][:100]

train_y_paths = list(data_root.glob('woman/*'))
train_y_paths = [str(path) for path in train_y_paths][:100]

test_x_paths = list(data_root.glob('man/*'))
test_x_paths = [str(path) for path in test_x_paths][:100]

test_y_paths = list(data_root.glob('woman/*'))
test_y_paths = [str(path) for path in test_y_paths][:100]

#訓練用の写真をクロッピング、左右反転、正規化するための関数
def preprocess_image_train(path):
    image = tf.io.read_file(path)
    # 生データのテンソルを画像のテンソルに変換する。
    # これによりshape=(240,240,3)になる
    image = tf.image.decode_jpeg(image, channels=3)
    # モデルに合わせてリサイズする
    image = tf.image.resize(image, [286, 286],method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    #指定した範囲を切り取るクロッピング
    image = tf.image.random_crop(
      image, size=[256,256, 3])

    #ランダムなミラーリング
    image = tf.image.random_flip_left_right(image)
    #正規化を行う
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1

    return image

def preprocess_image_test(path):
    image = tf.io.read_file(path)
    # 生データのテンソルを画像のテンソルに変換する。
    # これによりshape=(240,240,3)になる
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.random_crop(
      image, size=[256,256, 3])

    #ランダムなミラーリング
    image = tf.image.random_flip_left_right(image)
    #正規化を行う
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1

    return image

#arrayからtensorへ変換します
train_x = tf.data.Dataset.from_tensor_slices(train_x_paths)
train_y = tf.data.Dataset.from_tensor_slices(train_y_paths)
test_x = tf.data.Dataset.from_tensor_slices(test_x_paths)
test_y = tf.data.Dataset.from_tensor_slices(test_y_paths)

#各データの出力数を変数に格納します
len_train_x = len(train_x)
len_train_y = len(train_y)
len_test_x = len(test_x)
len_test_y = len(test_y)

#画像のパスから画像データをtensorとして取り出し、前処理、バッチ化を行います。
train_x = train_x.map(
    preprocess_image_train, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_train_x).batch(1)

train_y = train_y.map(
    preprocess_image_train, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_train_y).batch(1)

test_x = test_x.map(
    preprocess_image_test, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_test_x).batch(1)

test_y = test_y.map(
    preprocess_image_test, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_test_y).batch(1)

#適当な一組の画像ペアを取り出します
sample_x = next(iter(train_x))
sample_y = next(iter(train_y))

#元の画像と左右反転画像を表示させます。
plt.subplot(221)
plt.title('man')
plt.imshow(sample_x[0] * 0.5 + 0.5)
plt.axis('off')

plt.subplot(222)
plt.title('man with random jitter')
plt.imshow(tf.image.random_flip_left_right(sample_x[0]) * 0.5 + 0.5)
plt.axis('off')

plt.subplot(223)
plt.title('woman')
plt.imshow(sample_y[0] * 0.5 + 0.5)
plt.axis('off')

plt.subplot(224)
plt.title('woman with random jitter')
plt.imshow(tf.image.random_flip_left_right(sample_y[0]) * 0.5 + 0.5)
plt.axis('off')

#import libraries
import sys
import importlib
import tensorflow as tf

# パスを通す
MODULE_PATH = "/content/drive/MyDrive/GAN/pix2pix"
sys.path.append(MODULE_PATH)
#pix2pix.pyをimport
import pix2pix

#pix2pixモデルからgeneratorとdiscriminatorモデルをロードします
OUTPUT_CHANNELS = 3

#生成器gとfのモデル(unet model)
generator_g = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')
generator_f = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')

#識別器xとyのモデル(unet model)
discriminator_x = pix2pix.discriminator(norm_type='instancenorm', target=False)
discriminator_y = pix2pix.discriminator(norm_type='instancenorm', target=False)

print("Models are loaded!")

import pathlib
import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
AUTOTUNE = tf.data.AUTOTUNE
import sys

PATH = "/mnt/lib/ztodataset/CycleGan/tensorflow_examples/models/pix2pix"
sys.path.append(PATH)

import pix2pix

#データのパスをここで指定します。
data_root = pathlib.Path("/content/drive/MyDrive/GAN")
train_x_paths = list(data_root.glob('man/*'))
train_x_paths = [str(path) for path in train_x_paths][:10]

train_y_paths = list(data_root.glob('woman/*'))
train_y_paths = [str(path) for path in train_y_paths][:10]

test_x_paths = list(data_root.glob('man/*'))
test_x_paths = [str(path) for path in test_x_paths][:10]

test_y_paths = list(data_root.glob('woman/*'))
test_y_paths = [str(path) for path in test_y_paths][:10]

#訓練用の写真をクロッピング、左右反転、正規化するための関数
def preprocess_image_train(path):
    image = tf.io.read_file(path)
    # 生データのテンソルを画像のテンソルに変換する。
    # これによりshape=(240,240,3)になる
    image = tf.image.decode_jpeg(image, channels=3)
    # モデルに合わせてリサイズする
    image = tf.image.resize(image, [286, 286],method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    #指定した範囲を切り取るクロッピング
    image = tf.image.random_crop(
      image, size=[256,256, 3])

    #ランダムなミラーリング
    image = tf.image.random_flip_left_right(image)
    #正規化を行う
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1

    return image

def preprocess_image_test(path):
    image = tf.io.read_file(path)
    # 生データのテンソルを画像のテンソルに変換する。
    # これによりshape=(240,240,3)になる
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.random_crop(
      image, size=[256,256, 3])

    #ランダムなミラーリング
    image = tf.image.random_flip_left_right(image)
    #正規化を行う
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1

    return image

#arrayからtensorへ変換します
train_x = tf.data.Dataset.from_tensor_slices(train_x_paths)
train_y = tf.data.Dataset.from_tensor_slices(train_y_paths)
test_x = tf.data.Dataset.from_tensor_slices(test_x_paths)
test_y = tf.data.Dataset.from_tensor_slices(test_y_paths)

#各データの出力数を変数に格納します
len_train_x = len(train_x)
len_train_y = len(train_y)
len_test_x = len(test_x)
len_test_y = len(test_y)

#画像のパスから画像データをtensorとして取り出し、前処理、バッチ化を行います。
train_x = train_x.map(
    preprocess_image_train, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_train_x).batch(1)

train_y = train_y.map(
    preprocess_image_train, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_train_y).batch(1)

test_x = test_x.map(
    preprocess_image_test, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_test_x).batch(1)

test_y = test_y.map(
    preprocess_image_test, num_parallel_calls=AUTOTUNE).cache().shuffle(
    len_test_y).batch(1)

#適当な一組の画像ペアを取り出します
sample_x = next(iter(train_x))
sample_y = next(iter(train_y))

#model
#pix2pixモデルからgeneratorとdiscriminatorモデルをロードします
OUTPUT_CHANNELS = 3

#unet model
generator_g = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')
generator_f = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')

discriminator_x = pix2pix.discriminator(norm_type='instancenorm', target=False)
discriminator_y = pix2pix.discriminator(norm_type='instancenorm', target=False)

#学習前のモデルを用いて変換を行います
to_y = generator_g(sample_x)
to_x = generator_f(sample_y)
plt.figure(figsize=(8, 8))
contrast = 8

imgs = [sample_x, to_y, sample_y, to_x]
title = ['man', 'To woman', 'woman', 'To man']

for i in range(len(imgs)):
  plt.subplot(2, 2, i+1)
  plt.title(title[i])
  if i % 2 == 0:
    plt.imshow(imgs[i][0] * 0.5 + 0.5)
  else:
    plt.imshow(imgs[i][0] * 0.5 * contrast + 0.5)
plt.show()

LAMBDA = 10

#交差エントロピー
loss_obj = tf.keras.losses.BinaryCrossentropy(from_logits=True)

#discriminatorの損失
def discriminator_loss(real, generated):
  real_loss = loss_obj(tf.ones_like(real), real)

  generated_loss = loss_obj(tf.zeros_like(generated), generated)

  total_disc_loss = real_loss + generated_loss

  return total_disc_loss * 0.5

#generatorの損失
def generator_loss(generated):
  return loss_obj(tf.ones_like(generated), generated)

#サイクル一貫性損失
def calc_cycle_loss(real_image, cycled_image):
  loss1 = tf.reduce_mean(tf.abs(real_image - cycled_image))

  return LAMBDA * loss1

#アイデンティティー損失
def identity_loss(real_image, same_image):
  loss = tf.reduce_mean(tf.abs(real_image - same_image))
  return LAMBDA * 0.5 * loss

#generator g fの最適化手法
#Adamと呼ばれる最適化手法を用います
generator_g_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
generator_f_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

#discriminator x yの最適化手法
#Adamと呼ばれる最適化手法を用います
discriminator_x_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
discriminator_y_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

#途中で学習が中断した時用に記録を残す
checkpoint_path = "./checkpoints/train"

ckpt = tf.train.Checkpoint(generator_g=generator_g,
                           generator_f=generator_f,
                           discriminator_x=discriminator_x,
                           discriminator_y=discriminator_y,
                           generator_g_optimizer=generator_g_optimizer,
                           generator_f_optimizer=generator_f_optimizer,
                           discriminator_x_optimizer=discriminator_x_optimizer,
                           discriminator_y_optimizer=discriminator_y_optimizer)

ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)

#最新版のチェックポイントをここで保存します
if ckpt_manager.latest_checkpoint:
  ckpt.restore(ckpt_manager.latest_checkpoint)
  print ('Latest checkpoint restored!!')

#予測画像を出力するための関数
def generate_images(model, test_input):
  prediction = model(test_input)

  plt.figure(figsize=(12, 12))

  display_list = [test_input[0], prediction[0]]
  title = ['Input Image', 'Predicted Image']

  for i in range(2):
    plt.subplot(1, 2, i+1)
    plt.title(title[i])
    plt.imshow(display_list[i] * 0.5 + 0.5)
    plt.axis('off')
  plt.show()

import time
from IPython.display import clear_output

# デバイスの設定（GPUが使えるならGPU、使えない場合はCPU）
device = ['/device:GPU:0' if tf.test.gpu_device_name() == '/device:GPU:0' else '/cpu:0'][0]

# 学習エポック数
EPOCHS = 50

@tf.function
def train_step(real_x, real_y, device):
    with tf.device(device):
        with tf.GradientTape(persistent=True) as tape:
            # Generator G (X -> Y) と Generator F (Y -> X) の変換
            fake_y = generator_g(real_x, training=True)
            cycled_x = generator_f(fake_y, training=True)

            fake_x = generator_f(real_y, training=True)
            cycled_y = generator_g(fake_x, training=True)

            # same_x と same_y がアイデンティティー損失に使われます
            same_x = generator_f(real_x, training=True)
            same_y = generator_g(real_y, training=True)

            # 識別器xに本物のxを通した時の結果
            disc_real_x = discriminator_x(real_x, training=True)
            # 識別器yに本物のyを通した時の結果
            disc_real_y = discriminator_y(real_y, training=True)
            # 識別器xに偽物(生成した)のxを通した時の結果
            disc_fake_x = discriminator_x(fake_x, training=True)
            # 識別器yに偽物(生成した)のyを通した時の結果
            disc_fake_y = discriminator_y(fake_y, training=True)

            # 損失を計算
            gen_g_loss = generator_loss(disc_fake_y)
            gen_f_loss = generator_loss(disc_fake_x)

            # サイクル一貫性の損失
            total_cycle_loss = calc_cycle_loss(real_x, cycled_x) + calc_cycle_loss(real_y, cycled_y)

            # Generatorの合計損失
            total_gen_g_loss = gen_g_loss + total_cycle_loss + identity_loss(real_y, same_y)
            total_gen_f_loss = gen_f_loss + total_cycle_loss + identity_loss(real_x, same_x)

            # Discriminatorの損失
            disc_x_loss = discriminator_loss(disc_real_x, disc_fake_x)
            disc_y_loss = discriminator_loss(disc_real_y, disc_fake_y)

        # GeneratorとDiscriminatorにおいて勾配を計算
        generator_g_gradients = tape.gradient(total_gen_g_loss, generator_g.trainable_variables)
        generator_f_gradients = tape.gradient(total_gen_f_loss, generator_f.trainable_variables)

        discriminator_x_gradients = tape.gradient(disc_x_loss, discriminator_x.trainable_variables)
        discriminator_y_gradients = tape.gradient(disc_y_loss, discriminator_y.trainable_variables)

        # 勾配をoptimizerに適用
        if generator_g_gradients:
            generator_g_optimizer.apply_gradients(zip(generator_g_gradients, generator_g.trainable_variables))

        if generator_f_gradients:
            generator_f_optimizer.apply_gradients(zip(generator_f_gradients, generator_f.trainable_variables))

        if discriminator_x_gradients:
            discriminator_x_optimizer.apply_gradients(zip(discriminator_x_gradients, discriminator_x.trainable_variables))

        if discriminator_y_gradients:
            discriminator_y_optimizer.apply_gradients(zip(discriminator_y_gradients, discriminator_y.trainable_variables))


# 学習開始
for epoch in range(EPOCHS):
    start = time.time()

    n = 0
    for image_x, image_y in tf.data.Dataset.zip((train_x, train_y)):
        train_step(image_x, image_y, device)
        if n % 10 == 0:
            print('.', end='')
        n += 1

    clear_output(wait=True)
    # 途中経過を表示 (画像がそれっぽくなっていくのがわかる)
    generate_images(generator_f, sample_y)

    # 5エポック毎にモデルの保存を行う
    if (epoch + 1) % 5 == 0:
        ckpt_save_path = ckpt_manager.save()
        print('Saving checkpoint for epoch {} at {}'.format(epoch+1, ckpt_save_path))

    print('Time taken for epoch {} is {} sec\n'.format(epoch + 1, time.time() - start))

# モデル保存時
generator_g.save('/content/drive/MyDrive/GAN/g.keras', save_format='keras')
generator_f.save('/content/drive/MyDrive/GAN/f.keras', save_format='keras')

import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
# 画像の読み込みと前処理関数
def load_image(image_path, image_size=(256, 256)):
    img = image.load_img(image_path, target_size=image_size)  # 画像をリサイズ
    img = image.img_to_array(img)  # NumPy配列に変換
    img = (img / 127.5) - 1  # [-1, 1] の範囲に正規化
    return img
# ディレクトリのパス（適切なパスに変更してください）
test_man_dir = '/content/drive/MyDrive/GAN/test/man'  # 男性画像のディレクトリ
test_woman_dir = '/content/drive/MyDrive/GAN/test/woman'  # 女性画像のディレクトリ

# ディレクトリ内の画像ファイルのリスト
test_man_files = os.listdir(test_man_dir)
test_woman_files = os.listdir(test_woman_dir)

# 画像をリストに読み込む
test_man_images = [load_image(os.path.join(test_man_dir, file)) for file in test_man_files]
test_woman_images = [load_image(os.path.join(test_woman_dir, file)) for file in test_woman_files]

# テスト用のデータセットに変換（バッチ処理のためにTensorに変換）
test_man = tf.convert_to_tensor(np.array(test_man_images), dtype=tf.float32)
test_woman = tf.convert_to_tensor(np.array(test_woman_images), dtype=tf.float32)

print(f'Test man images shape: {test_man.shape}')
print(f'Test woman images shape: {test_woman.shape}')

import os

checkpoint_dir = './checkpoints'  # チェックポイントの保存先
if not os.path.exists(checkpoint_dir):
    print("Checkpoint directory does not exist.")
else:
    checkpoint_files = os.listdir(checkpoint_dir)
    print("Checkpoint files:", checkpoint_files)

def generate_images_from_model(generator_f, generator_g, test_man, test_woman):
    # man -> woman に変換
    generated_woman = generator_f(test_man, training=False)

    # woman -> man に変換
    generated_man = generator_g(test_woman, training=False)

    # 生成された画像を表示
    plt.figure(figsize=(8, 8))

    # man -> woman の結果
    plt.subplot(1, 2, 1)
    for i in range(generated_woman.shape[0]):
        plt.subplot(1, generated_woman.shape[0], i + 1)
        plt.imshow(generated_woman[i].numpy() * 0.5 + 0.5)  # 正規化されている場合、元に戻す
        plt.axis('off')
    plt.title("Man -> Woman")

    # woman -> man の結果
    plt.subplot(1, 2, 2)
    for i in range(generated_man.shape[0]):
        plt.subplot(1, generated_man.shape[0], i + 1)
        plt.imshow(generated_man[i].numpy() * 0.5 + 0.5)  # 正規化されている場合、元に戻す
        plt.axis('off')
    plt.title("Woman -> Man")

    plt.show()

import tensorflow as tf
import os

# モデルを保存したチェックポイントのディレクトリを指定
checkpoint_dir = './checkpoints/train'  # チェックポイントが保存されているディレクトリ
checkpoint = tf.train.Checkpoint(generator_f=generator_f,
                                 generator_g=generator_g,
                                 discriminator_x=discriminator_x,
                                 discriminator_y=discriminator_y)

# チェックポイントマネージャーを作成
ckpt_manager = tf.train.CheckpointManager(checkpoint, directory=checkpoint_dir, max_to_keep=5)

# 最新のチェックポイントを読み込む
ckpt_restore_path = ckpt_manager.latest_checkpoint

if ckpt_restore_path:
    checkpoint.restore(ckpt_restore_path)
    print(f"Restored checkpoint from {ckpt_restore_path}")
else:
    print("No checkpoint found!")

import tensorflow as tf
import os

input_dir = '/content/drive/MyDrive/GAN/test/man'  # テスト画像が保存されているディレクトリ
output_dir = '/content/drive/MyDrive/GAN/test/output'  # 生成した画像を保存するディレクトリ
def load_and_preprocess_image(image_path, target_size=(256, 256)):
    # 画像を読み込み
    image = tf.io.read_file(image_path)
    image = tf.image.decode_jpeg(image, channels=3)  # JPG 画像をデコード

    # アスペクト比を変更せずにリサイズ（もし必要なら）
    image = tf.image.resize(image, target_size, method=tf.image.ResizeMethod.BICUBIC)

    # 画像を正規化（-1, 1の範囲にする）
    image = (image / 127.5) - 1
    return image

def generate_men_images_from_women(generator_g, input_dir, output_dir):
    # 入力ディレクトリ内の画像ファイルを取得
    image_paths = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir) if fname.endswith('.jpg') or fname.endswith('.png')]

    # 各画像を処理
    for image_path in image_paths:
        # 元の画像を読み込み
        original_image = tf.io.read_file(image_path)
        original_image = tf.image.decode_jpeg(original_image, channels=3)
        original_shape = tf.shape(original_image)  # 元の画像のサイズを取得

        # 画像を前処理（リサイズ）
        image = load_and_preprocess_image(image_path, target_size=(256, 256))  # 生成器に入力する画像を256x256にリサイズ
        image = image[None, ...]  # バッチ次元を追加（形状 [1, height, width, channels]）

        # 画像を男性に変換
        generated_men = generator_g(image, training=False)

        # 画像を元の範囲に戻す（-1,1 -> 0,1）
        generated_men = (generated_men + 1) / 2.0  # [-1, 1] -> [0, 1]

        # 元の画像サイズにパディングを追加
        padded_generated_men = tf.image.resize_with_crop_or_pad(generated_men, original_shape[0], original_shape[1])

        # 保存用のファイル名を生成
        output_filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, output_filename)

        # 画像を保存
        tf.keras.preprocessing.image.save_img(output_path, padded_generated_men[0])  # バッチの最初の画像を保存

        print(f"Generated and saved: {output_path}")


# 推論を実行（変換）
generate_men_images_from_women(generator_g, input_dir, output_dir)#generator_g は男性➡女性