# Copyright (C) 2015-2018: The University of Edinburgh
#                 Authors: Craig Warren and Antonis Giannopoulos
#
# This file is part of gprMax.
#
# gprMax is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gprMax is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gprMax.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np

from gprMax.utilities import round_value


def gaussian(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    ampvalue = np.exp(-zeta * delay**2)
    return amp * ampvalue


def gaussiandot(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    ampvalue = -2 * zeta * delay * np.exp(-zeta * delay**2)
    return amp * ampvalue


def gaussianprime(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    ampvalue = -2 * zeta * delay * np.exp(-zeta * delay**2)
    return amp * ampvalue


def gaussiandotnorm(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    normalise = np.sqrt(np.exp(1) / (2 * zeta))
    ampvalue = -2 * zeta * delay * np.exp(-zeta * delay**2) * normalise
    return amp * ampvalue


def gaussiandoubleprime(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    ampvalue = 2 * zeta * (2 * zeta * delay**2 - 1) * np.exp(-zeta * delay**2)
    return amp * ampvalue


def gaussiandotdot(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    ampvalue = 2 * zeta * (2 * zeta * delay**2 - 1) * np.exp(-zeta * delay**2)
    return amp * ampvalue


def gaussiandotdotnorm(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    normalise = 1 / (2 * zeta)
    ampvalue = 2 * zeta * (2 * zeta * delay**2 - 1) * np.exp(-zeta * delay**2) * normalise
    return amp * ampvalue


def ricker(time, dt, amp=1, freq=None, chi=0,  zeta=0, **kwargs):
    delay = time - chi
    normalise = 1 / (2 * zeta)
    ampvalue = - (2 * zeta * (2 * zeta * delay**2 - 1) * np.exp(-zeta * delay**2)) * normalise
    return amp * ampvalue


def sine(time, dt, amp=1, freq=None, **kwargs):
    if time * freq > 1:
        ampvalue = 0
    else:
        ampvalue = np.sin(2 * np.pi * freq * time)
    return amp * ampvalue


def contsine(time, dt, amp=1, freq=None, **kwargs):
    rampamp = 0.25
    ramp = rampamp * time * freq
    if ramp > 1:
        ramp = 1
    ampvalue = ramp * np.sin(2 * np.pi * freq * time)
    return amp * ampvalue


def impulse(time, dt, amp=1, freq=None, **kwargs):
    # time < dt condition required to do impulsive magnetic dipole
    if time == 0 or time < dt:
        ampvalue = 1
    elif time >= dt:
        ampvalue = 0
    return amp * ampvalue


class Waveform(object):
    """Definitions of waveform shapes that can be used with sources."""

    # types = ['gaussian', 'gaussiandot', 'gaussiandotnorm', 'gaussiandotdot', 'gaussiandotdotnorm', 'gaussianprime', 'gaussiandoubleprime', 'ricker', 'sine', 'contsine', 'impulse', 'user']

    # Information about specific waveforms:
    #
    # gaussianprime and gaussiandoubleprime waveforms are the first derivative and second derivative of the 'base' gaussian
    # waveform, i.e. the centre frequencies of the waveforms will rise for the first and second derivatives.
    #
    # gaussiandot, gaussiandotnorm, gaussiandotdot, gaussiandotdotnorm, ricker waveforms have their centre frequencies
    # specified by the user, i.e. they are not derived from the 'base' gaussian

    def __init__(self, type=None, amp=1, freq=None, id=None, **kwargs):
        self.ID = id
        self.type = type
        self.amp = amp
        self.freq = freq
        self.userfunc = None
        self.chi = 0
        self.zeta = 0

    def calculate_coefficients(self):
        """Calculates coefficients (used to calculate values) for specific waveforms."""

        if self.type in ['gaussian', 'gaussiandot', 'gaussiandotnorm', 
                    'gaussianprime', 'gaussiandoubleprime']:
            self.chi = 1 / self.freq
            self.zeta = 2 * np.pi**2 * self.freq**2
        elif self.type == 'gaussiandotdot' or self.type == 'gaussiandotdotnorm' or self.type == 'ricker':
            self.chi = np.sqrt(2) / self.freq
            self.zeta = np.pi**2 * self.freq**2

    def calculate_value(self, time, dt):
        """Calculates value of the waveform at a specific time.

        Args:
            time (float): Absolute time.
            dt (float): Absolute time discretisation.

        Returns:
            ampvalue (float): Calculated value for waveform.
        """
        self.calculate_cofficients()
        if callable(self.userfunc):
            return self.userfunc(time, dt)
        if isinstance(self.type, str):
            if self.type in globals():
                func = globals()[self.type]
            else:
                func = None
        else:
            func = self.type
        if callable(func):
            return func(time, dt, **self.__dict__)
        else:
            raise NotImplementedError

        # # Waveforms
        # if self.type == 'gaussian':
        #     delay = time - self.chi
        #     ampvalue = np.exp(-self.zeta * delay**2)

        # elif self.type == 'gaussiandot' or self.type == 'gaussianprime':
        #     delay = time - self.chi
        #     ampvalue = -2 * self.zeta * delay * np.exp(-self.zeta * delay**2)

        # elif self.type == 'gaussiandotnorm':
        #     delay = time - self.chi
        #     normalise = np.sqrt(np.exp(1) / (2 * self.zeta))
        #     ampvalue = -2 * self.zeta * delay * np.exp(-self.zeta * delay**2) * normalise

        # elif self.type == 'gaussiandotdot' or self.type == 'gaussiandoubleprime':
        #     delay = time - self.chi
        #     ampvalue = 2 * self.zeta * (2 * self.zeta * delay**2 - 1) * np.exp(-self.zeta * delay**2)

        # elif self.type == 'gaussiandotdotnorm':
        #     delay = time - self.chi
        #     normalise = 1 / (2 * self.zeta)
        #     ampvalue = 2 * self.zeta * (2 * self.zeta * delay**2 - 1) * np.exp(-self.zeta * delay**2) * normalise

        # elif self.type == 'ricker':
        #     delay = time - self.chi
        #     normalise = 1 / (2 * self.zeta)
        #     ampvalue = - (2 * self.zeta * (2 * self.zeta * delay**2 - 1) * np.exp(-self.zeta * delay**2)) * normalise

        # elif self.type == 'sine':
        #     ampvalue = np.sin(2 * np.pi * self.freq * time)
        #     if time * self.freq > 1:
        #         ampvalue = 0

        # elif self.type == 'contsine':
        #     rampamp = 0.25
        #     ramp = rampamp * time * self.freq
        #     if ramp > 1:
        #         ramp = 1
        #     ampvalue = ramp * np.sin(2 * np.pi * self.freq * time)

        # elif self.type == 'impulse':
        #     # time < dt condition required to do impulsive magnetic dipole
        #     if time == 0 or time < dt:
        #         ampvalue = 1
        #     elif time >= dt:
        #         ampvalue = 0

        # elif self.type == 'user':
        #     ampvalue = self.userfunc(time)

        # ampvalue *= self.amp

        # return ampvalue
