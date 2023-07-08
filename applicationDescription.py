#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 11:33:00 2023

@author: anton
"""
from SLiCAP import *
htmlPage("Application Description")
text2html("""A low-noise RF amplifier converts the voltage of 300Ω balanced floating source
into a current for a mixer.""")
head2html("Target specification")
file2html("targetSpecs.html")
head2html("Environmental conditions")
text2html("The audio amplifier should operate from 0 to 70 degrees Celsius.")
head2html("Design tasks")
file2html("designTasks.html")
