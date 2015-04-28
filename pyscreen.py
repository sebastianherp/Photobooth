# -*- coding: utf-8 -*-
import os
import pygame
import time
import random


class pyscreen :
    screen = None;
        
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer" http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available Start with fbcon since directfb hangs with composite 
        # output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
	# Initialise audio mixer
	pygame.mixer.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def clear(self, color = (0, 0, 0)):
        self.screen.fill(color)
        # Update the display
        pygame.display.update()

    def display_text(self, text, flip_h = False, flip_v = False, size_factor = 10, foreground = (0, 0, 0), background = (255, 255, 255), center_text = True):
	self.screen.fill(background)
	if size_factor == 0:
	    size_factor = 1

	info = pygame.display.Info()
	font = pygame.font.Font(None, info.current_h / size_factor)

	lines = text.split("\n")
	counter = 0
	length = len(lines)
	offset = (0, 0)
	size = (info.current_w, info.current_h)

	if flip_v:
	    lines = list(reversed(lines))

	for line in lines:
		text_surface = font.render(lines[counter], True, foreground)
	        # flip text?
        	if flip_h or flip_v:
            	    text_surface = pygame.transform.flip(text_surface, flip_h, flip_v)

		text_x = offset[0] + (size[0] - text_surface.get_width()) / 2
	        text_y = offset[0] + (size[1] - length * text_surface.get_height() ) / 2 + counter * text_surface.get_height()
		counter = counter+1
		self.screen.blit(text_surface, (text_x, text_y))


	pygame.display.update()

    def display_image(self, path, flip_h = False, flip_v = False, border = 50, background = (0, 0, 0), keep_aspect_ratio = True):
	self.screen.fill( background )
	image = pygame.image.load(path)
	info = pygame.display.Info()

	if keep_aspect_ratio:
	    new_height = info.current_h - border*2
	    new_width = image.get_width() * new_height / image.get_height()
	    if new_width > info.current_w - border*2:
		new_width = info.current_w - border*2
		new_height = image.get_height() * new_width / image.get_width()
	    	image = pygame.transform.scale(image, (new_width, new_height))
		rect = image.get_rect().move(border, (info.current_h - new_height) / 2)
	    else:
		image = pygame.transform.scale(image, (new_width, new_height))
		rect = image.get_rect().move((info.current_w - new_width) / 2, border)

	else:
	    image = pygame.transform.scale(image, (info.current_w - border*2, info.current_h - border*2))
	    rect = image.get_rect().move(border, border)

	# flip image?
	if flip_h or flip_v:
	    image = pygame.transform.flip(image, flip_h, flip_v)

	self.screen.blit(image, rect)
	pygame.display.update()

    def load_sound(self, path):
	pygame.mixer.music.load(path)

    def play_sound(self):
	pygame.mixer.music.play()
