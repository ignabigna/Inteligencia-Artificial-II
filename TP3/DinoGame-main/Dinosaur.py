import subprocess
try:
    import tensorflow as tf
except ImportError as err:
    subprocess.check_call(['pip', 'install', 'tensorflow'])
    subprocess.check_call(['pip', 'install', 'Pillow'])
    import tensorflow as tf

import pygame
import os
import glob
from NeuralNetwork import NeuralNetwork
import numpy as np
from keras._tf_keras.keras.preprocessing.image import load_img, img_to_array

# Bring images from assets
RUNNING = [os.path.join("TP3\DinoGame-main\Assets\Dino", "DinoRun1.png"),
           os.path.join("TP3\DinoGame-main\Assets\Dino", "DinoRun2.png")]
JUMPING = [os.path.join("TP3\DinoGame-main\Assets\Dino", "DinoJump.png")]
DUCKING = [os.path.join("TP3\DinoGame-main\Assets\Dino", "DinoDuck1.png"),
           os.path.join("TP3\DinoGame-main\Assets\Dino", "DinoDuck2.png")]
CLASSES = ["JUMP", "DUCK", "RIGHT"]

class Dinosaur(NeuralNetwork):
    # Define as global the starting position for the dinosaur
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self, id, mask_color=None, autoplay=False):
        # As 'NeuralNetwork' serves as base class for the dinosaur, start its 'brain'
        super().__init__()
        
        self.id = id
        self.color = mask_color
        self.autoPlay = autoplay
        self.duck_img = self.load_images(DUCKING)
        self.run_img = self.load_images(RUNNING)
        self.jump_img = self.load_images(JUMPING)

        self.resetStatus()
        
        # If a tensorflow model is provided, load it
        model_file = glob.glob('*.h5')
        if model_file:
            # Cargar el modelo si el archivo existe
            self.model = tf.keras.models.load_model(model_file[0])
            self.model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

    def resetStatus(self):
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.alive = True
        self.score = 0

    def load_images(self, base_name):
        images = []
        for image_path in base_name:
            result = pygame.image.load(image_path).convert_alpha()

            # Apply the color mask if a color is selected
            if self.color:
                result.fill(self.color, special_flags=pygame.BLEND_ADD)
            images.append(result)

        return images

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if self.autoPlay:
            if userInput == "JUMP" and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif userInput == "DUCK":
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput == "DUCK"):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False
        else:
            if userInput[pygame.K_UP] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif userInput[pygame.K_DOWN]:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

        if not self.dino_jump and self.dino_rect.y < self.Y_POS:
            self.dino_rect.y += 8
            if self.dino_rect.y >= self.Y_POS:
                self.dino_rect.y = self.Y_POS

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]

        if (self.dino_rect.y < self.Y_POS):
            self.dino_rect.y += self.JUMP_VEL * 6
            if (self.dino_rect.y >= self.Y_POS_DUCK):
                self.dino_rect.y = self.Y_POS_DUCK
        else:
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            self.jump_vel = self.JUMP_VEL

        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.step_index += 1

    def jump(self):
        self.image = self.jump_img[0]

        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

            if self.dino_rect.y >= self.Y_POS:
                self.dino_rect.y = self.Y_POS
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def predict(self):
        self.autoPlay = True
        img = load_img("./images/live/temp.png", color_mode='grayscale', target_size=(58,56))
        img_array = img_to_array(img)
        img_array = img_array / 255.0  # Normaliza los valores de píxeles entre 0 y 1
        img_array = np.expand_dims(img_array, axis=0)

        predictions = self.model.predict(img_array)
        predicted_class_index = np.argmax(predictions)

        self.update(CLASSES[predicted_class_index])