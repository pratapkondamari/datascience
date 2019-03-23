# -*- coding: utf-8 -*-
"""
Created on Tue May  2 21:04:10 2017

@author: aruna
"""

import sys, os, re
from mrjob.job import MRJob
from mrjob.job import MRStep


class MRJoin(MRJob):
  
  SORT_VALUES = True
  
  def steps(self):      
      return [
              MRStep(mapper=self.mapper_productwise,                     
                     reducer=self.combiner_categorywise)
              ]
        
  def mapper_productwise(self, _, line):    
    
      fields=line.split('|||')
        if len(fields) == 10:
            yield (fields[1], 1)
        else:
            yield (None, 1)
            
    
    if len(splits) == 2: # country data
      symbol = 'A'
      countryName = splits[0]
      country2digit = splits[1]
      yield country2digit, [symbol, countryName]
    else: # person data
      symbol = 'B'
      personName = splits[0]
      personType = splits[1]
      country2digit = splits[2]
      yield country2digit, [symbol, personName, personType]
  
  def reducer(self, key, values):
    values = [x for x in values]
    if len(values) > 1: # our join hit
      country = values[0]
      for value in values[1:]:
        yield key, [country, value]
    else: # our join missed
      pass
      
if __name__ == '__main__':
  MRJoin.run()