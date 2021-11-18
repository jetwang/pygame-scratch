# encoding: utf-8
import sys

from pygamescratch.pygs import pygs
from pygamescratch.sprite import Sprite

out = sys.stdout
sys.stdout = open("../../doc/pygamescratch.md", "w")
help(Sprite)
help(pygs)
sys.stdout.close()
sys.stdout = out
