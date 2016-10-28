from __future__ import print_function, division
import os
import numpy as np

#import pickle
#import datetime
#import requests
#from bs4 import BeautifulSoup
#import nltk
#from nltk.corpus import stopwords

"""
This ....

Details on NCBI E-utils: http://www.ncbi.nlm.nih.gov/books/NBK25500/

TODO:
  - Figure out 'HTTP POST' for large # of ID fetches
"""

#################################################################################
################################ ERPSC - Classes ################################
#################################################################################

class ERPDB(object):
    """Class to hold database information ERP SCANR project."""

    def __init__(self):

        # Set base path for the project
        self.project_path = ("/Users/thomasdonoghue/Documents/"
                             "Research/1-Projects/ERP-SCANR/")

        # Set the data path
        self.data_path = os.path.join(self.project_path, '2-Data')

        # Set paths to different data types
        self.dict_path = os.path.join(self.data_path, 'dicts')
        self.counts_path = os.path.join(self.data_path, 'counts')
        self.words_path = os.path.join(self.data_path, 'words')


class URLS(object):
    """Class to hold URL information for ERP SCANR project."""

    def __init__(self, database):
        """Initialize the ncbi e-utils urls.

        Parameters
        ----------
        db : str
            Which database to use.
                Options: {'pubmed', 'pmc'}
        """

        # Set which database is being used
        self.db = database

        # Set up the base url for ncbi e-utils
        self.base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

        self.search = self.base_url + 'esearch.fcgi?db=pmc&field=word&term='

        self.fetch = self.base_url + ''

        self.retmax = ''


class ERPSCBase(object):
    """Base class for ERPSC analyses."""

    def __init__(self):

        # Set the base path for the NCBI eutils
        self.eutils_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

        # Set path (on Tom's laptop) to save out the data
        #self.save_loc = ("/Users/thomasdonoghue/Documents/"
        #                 "Research/1-Projects/ERP-SCANR/2-Data/")

        # Initialize list of erps & term terms to use
        self.erps = list()
        self.terms = list()

        # Initialize counters for numbers of terms
        self.n_erps = int()
        self.n_terms = int()

        # Initialize vector of counts of number of papers for each term
        self.erp_counts = np.zeros(0)
        self.term_counts = np.zeros(0)

        # Initialize for date that data is collected
        self.date = ''


    def set_erps(self, erps):
        """Sets the given list of strings as erp terms to use.

        Parameters
        ----------
        erps : list(str)
            List of ERP terms to be used.
        """

        # Set given list as the erps
        self.erps = erps

        # Set the number of erps
        self.n_erps = len(erps)

        # Initialize count variable to the correct length
        self.erp_counts = np.zeros([self.n_erp_terms])


    def set_erps_file(self, f_name):
        """Load ERP terms from a txt file.

        Parameters
        ----------
        f_name : str
            Name of the file to be loaded as ERP terms.
        """

        # Get ERPSC database object to set paths
        db = ERPDB()

        # Open file
        txt_file = open(os.path.join(db.dict_path, f_name), 'r')

        # Read file and input ERP terms
        erps = txt_file.read().splitlines()

        # Set the number of erps
        self.n_erps = len(erps)

        # Drop number indices for erps, and set as list
        for i in range(self.n_erps):
            self.erps.append(erps[i][3:].split(','))

        # Initialize count variable to the correct length
        self.erp_counts = np.zeros([self.n_erps])


    def check_erps(self):
        """Print out the current list of erps."""

        print('List of ERPs used: \n')
        for i in range(self.n_erps):
            print(", ".join(e for e in self.erps[i]))


    def set_terms(self, terms):
        """Sets the given list of strings as term terms to use.

        Parameters
        ----------
        terms : list(str)
            List of terms to be used.
        """

        # Set given list as the terms
        self.terms = terms

        # Set the number of terms
        self.n_terms = len(terms)

        # Initialize count variable to the correct length
        self.term_counts = np.zeros([self.n_term_terms])


    def set_terms_file(self, f_name):
        """Load terms from a txt file.

        Parameters
        ----------
        f_name : str
            Name of the file to be loaded as terms.
        """

        # Get ERPSC database object to set paths
        db = ERPDB()

        # Open file
        txt_file = open(os.path.join(db.dict_path, f_name), 'r')

        # Read file and input ERP terms
        self.terms = txt_file.read().splitlines()

        # Set the number of terms
        self.n_terms = len(self.terms)

        # Initialize count variable to the correct length
        self.term_counts = np.zeros([self.n_terms])


    def check_terms(self):
        """Print out the current list of terms."""

        print('List of terms used: \n')
        print("\n".join(self.terms))
