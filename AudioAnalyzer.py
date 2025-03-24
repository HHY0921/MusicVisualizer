import math

import matplotlib.pyplot as plt
import librosa.display
import numpy as np


import pygame

def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioAnalyzer:
    def __init__(self) -> None:
        self.frequencies_index_ratio = 0  # array for frequencies
        self.time_index_ratio = 0  # array of time periods
        self.spectrogram = None  # a matrix that contains decibel values according to frequency and time indexes

    def load(self, filename):
        time_series, sample_rate = librosa.load(filename)
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

        frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies


        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

        self.time_index_ratio = len(times)/times[len(times) - 1]

        self.frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

    def show(self):

        librosa.display.specshow(self.spectrogram,
                                 y_axis='log', x_axis='time')

        plt.title('spectrogram')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()

    
    def get_decibel(self, target_time, freq):

        return self.spectrogram[int(freq*self.frequencies_index_ratio)][int(target_time*self.time_index_ratio)]


class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=400, min_decibel=-80, max_decibel=0):

        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):

        desired_height = decibel * self.__decibel_height_ratio + self.max_height # height = decibel * decible_height_ratio + max_height
        
        speed = (desired_height - self.height)/0.1 # speed to move

        self.height += speed * dt # moving

        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):

        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height)) # draw


class AverageAudioBar(AudioBar):

    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=400, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)

        self.rng = rng

        self.avg = 0

        self.rect = Rect(self.x, self.y, self.width, self.height)

    def update_all(self, dt, time, analyzer):

        self.avg = 0

        for i in range(self.rng[0], self.rng[1]):

            self.avg += analyzer.get_decibel(time, i)

        self.avg /= ((self.rng[1] - self.rng[0])+0.01) # get the sum of the decibel in the fequency range and get the average
        self.update(dt, self.avg)

    def render(self,screen):
        pygame.draw.polygon(screen, self.color, self.rect.points)
    
    def update_rect(self):
        self.rect.update(self.x, self.y, self.width, self.height)

class Rect:

    def __init__(self,x ,y, w, h):
        self.x, self.y, self.w, self.h = x,y, w, h

        
    def update(self,x,y,w,h):
        self.points = ((x,y),(x+w,y), (x+w,y-h),(x,y-h))



# define bars update