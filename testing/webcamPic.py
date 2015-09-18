#!/usr/bin/python3

import pygame
import pygame.camera

pygame.camera.init()
pygame.camera.list_cameras()
cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()
img = cam.get_image()
pygame.image.save(img, "pygame.png")
cam.stop()