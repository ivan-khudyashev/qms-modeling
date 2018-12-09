"""This module is intended to add path of root of QMS project in PATH
for execution.
Hence, THIS MODULE MUST BE EXECUTED from root of the project, because
os.path.abspath(".") command generate path according to execution's 
start point
"""
import os, sys
sys.path.insert(0, os.path.abspath("."))
