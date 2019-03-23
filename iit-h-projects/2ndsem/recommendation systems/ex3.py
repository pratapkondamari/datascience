# -*- coding: utf-8 -*-
"""
Created on Tue May  2 18:31:05 2017

@author: Raja Pratap
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy
import sys

def weighted_review_rating(upvotes, downvotes, totalvotes, rating):
    wtrating = rating
    if not totalvotes == 0:
        wtrating = ((upvotes-downvotes)/totalvotes)*rating
    return wtrating

def get_category_list(category):
    categories = category
    categories = categories.strip('[]')
    categories = categories.replace('u\'','')
    categories = categories.replace('\'','')
    categories = categories.split(',')
    return categories

        
class MRTopKProducts(MRJob):
    def configure_options(self):
        super(MRTopKProducts, self).configure_options()
        self.add_file_option('--k')
            
    def average_review_rating(ratings):
        return numpy.mean(ratings)
    
    def mapper_init(self):
        # extract k value from commandine
        self.k = self.options.k

    def reducer_init(self):
        # extract k value from commandine
        self.k = self.options.k
    
    
    def map_get_weighted_review_rating(self, _, line):
        try:
            fields=line.split('|||')
            
            if len(fields) == 10: # processing reading reviews.csv
                upvotes = int(fields[3])
                totalvotes = int(fields[4])
                downvotes = totalvotes - upvotes
                rating = float(fields[6])
                wtRating = weighted_review_rating(upvotes, downvotes, totalvotes, rating)
                yield (fields[1], wtRating)
            
            else:
                yield (None, 0) #just in case if any of the fields are missing, skipping
        
        except:
            #print('exception occurred:',sys.exc_info()[0], fields)    
            yield (None, 0) #unable to parse values - some ratings has | in front, skipping them
                
    def reducer_average_weighted_review_rating(self, product_id, values):
        
        list_values = list(values)
        print ('***',list_values)
        yield product_id, numpy.average(list_values)
             
                
    def steps(self):
        return [MRStep(mapper_init=self.mapper_init,
                       mapper=self.map_get_weighted_review_rating,                       
                       reducer=self.reducer_average_weighted_review_rating,
                       reducer_init=self.reducer_init)]
if __name__ == '__main__':
    MRTopKProducts.run()
    