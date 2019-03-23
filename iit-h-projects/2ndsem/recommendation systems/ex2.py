# -*- coding: utf-8 -*-
"""
Created on Tue May  2 15:04:42 2017

@author: Raja Prathap
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import operator

class MRMostUsedWord(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_date_count,
                   combiner=self.combiner_count_reviews,
                   reducer=self.reducer_count_reviews) 
                   ,MRStep(reducer=self.reducer_sort_per_count)
        ]

    def mapper_get_date_count(self, _, line):
        fields=line.split('|||')
        if len(fields) == 10:
            yield (fields[-1], 1)
        else:
            yield (None, 1)

    def combiner_count_reviews(self, dt, counts):
        # optimization: sum the words we've seen so far
        yield (dt, sum(counts))

    def reducer_count_reviews(self, dt, counts):
        yield None, (dt, sum(counts))

    # discard the key; it is just None
    def reducer_sort_per_count(self, _, count_date_pairs):
        # each item of count_date_pairs is (date, count),
        # so yielding one results in key=counts, value=word
        #print(count_date_pairs)
        try:
            yield sorted(count_date_pairs, key=operator.itemgetter(1), reverse = True)
        except:            
            print("exception occurred for:", count_date_pairs)

if __name__ == '__main__':
    MRMostUsedWord.run()
    
#use below command to run this program
#python ex2.py reviews.csv --output-dir ex2