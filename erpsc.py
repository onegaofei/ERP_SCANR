from __future__ import print_function, division
import numpy as np
import os
import datetime
import requests
import pickle
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

###########################################################
###################### ERPSC - Class ######################
###########################################################

class ERPSC_Base():
    """ Base class for ERPSC analyses. """

    def __init__(self):

        # 
        self.eutils_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'

        #
        self.save_loc = ('/Users/thomasdonoghue/Documents/' + 
                        'Research/1-Projects/ERP-SCANR/2-Data/')

        # Initliaze list of erp & cog terms to use
        self.erps = list()
        self.cogs = list()

        # Initialize counters for numbers of terms
        self.nERPs = int()
        self.nCOGs = int()

        # Initialize vector of counts of number of papers for each term
        self.ERP_counts = np.zeros(0)
        self.COG_counts = np.zeros(0)

        # Initialize for date that data is collected
        self.date = ''


    def set_erps(self, erps):
        """Sets the given list of strings as erp terms to use. """

        self.erps = erps
        self.nERPs = len(erps)
        self.ERP_counts = np.zeros([self.nERPs])


    def set_cogs(self, cogs):
        """Sets the given list of strings as cog terms to use. """

        self.cogs = cogs
        self.nCOGs = len(cogs)
        self.COG_counts = np.zeros([self.nCOGs])



class ERPSC_Count(ERPSC_Base):
    """This is a class for counting co-occurence of pre-specified ERP & Cognitive terms. """

    def __init__(self):

        # Inherit from the ERPSC base class
        ERPSC_Base.__init__(self)

        # Set the esearch url for pubmed
        self.eutils_search = self.eutils_url + 'esearch.fcgi?db=pubmed&field=word&term='

        # Initialize data output variables
        self.dat_numbers = np.zeros(0)
        self.dat_percent = np.zeros(0)


    def scrape_data(self):
        """Search through pubmed for all abstracts with co-occurence of ERP & COG terms. 

        The scraping does an exact word search for two terms (one ERP and one COG)
        The HTML page returned by the pubmed search includes a 'count' field. 
        This field contains the number of papers with both terms. This is extracted. 
        """

        # Set date of when data was scraped
        self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        # Initialize right size matrices to store data
        self.dat_numbers = np.zeros([self.nERPs, self.nCOGs])
        self.dat_percent = np.zeros([self.nERPs, self.nCOGs])

        # Loop through each ERP term
        for erp in self.erps:
            # Within each ERP, loop through each COG term
            for cog in self.cogs:

                # Get the indices of the current erp & cog terms
                erp_ind = self.erps.index(erp)
                cog_ind = self.cogs.index(cog)

                # Make URL - Exact Term Version
                url = self.eutils_search + '"' + erp + '"AND"' + cog + '"'

                # Make URL - Non-exact term version
                #url = self.eutils_search + erp + ' erp ' + cog

                # Pull the page, and parse with Beatiful Soup
                page = requests.get(url)
                page_soup = BeautifulSoup(page.content)

                # Get all 'count' tags
                counts = page_soup.find_all('count')

                # Initialize empty temp vector to hold counts
                vec = []

                # Loop through counts, extracting into vec
                for i in range(0, len(counts)):
                    count = counts[i]
                    ext = count.text
                    vec.append(int(ext))

                # Add the total number of papers for erp & cog
                self.ERP_counts[erp_ind] = vec[1]
                self.COG_counts[cog_ind] = vec[2]

                # Add the number & percent of overlapping papers
                self.dat_numbers[erp_ind, cog_ind] = vec[0]
                self.dat_percent[erp_ind, cog_ind] = vec[0]/vec[1]


    def check_erps(self):
        """"Prints out the COG terms most associatied with each ERP. """

        # Loop through each erp term, find maximally associated cog term and print out
        for erp in self.erps:

            erp_ind = self.erps.index(erp)
            cog_ind = np.argmax(self.dat_percent[erp_ind, :])

            print("For the  {:5} the most common association is \t {:10} with \t %{:05.2f}"
                    .format(erp, self.cogs[cog_ind], \
                            self.dat_percent[erp_ind, cog_ind]*100))


    def check_cogs(self):
        """Prints out the ERP terms most associated with each COG. """
        
        # Loop through each cig term, find maximally associated erp term and print out
        for cog in self.cogs:

            cog_ind = self.cogs.index(cog)
            erp_ind = np.argmax(self.dat_percent[:, cog_ind])

            print("For  {:20} the strongest associated ERP is \t {:5} with \t %{:05.2f}"
                    .format(cog, self.erps[erp_ind], \
                            self.dat_percent[erp_ind, cog_ind]*100))


    def check_top(self):
        """Check the terms with the most papers. """
        
        # Find and print the erp term for which the most papers were found
        print("The most studied ERP is  {:6}  with {:8.0f} papers"
                .format(self.erps[np.argmax(self.ERP_counts)], \
                        self.ERP_counts[np.argmax(self.ERP_counts)]))

        # Find and print the cog term for which the most papers were found
        print("The most studied COG is  {:6}  with {:8.0f}  papers"
                .format(self.cogs[np.argmax(self.COG_counts)], \
                        self.COG_counts[np.argmax(self.COG_counts)]))


    def check_counts(self, dat):
        """Check how many papers found for each term. """

        # Check counts for all ERP terms
        if dat is 'erp':
            for erp in self.erps:
                erp_ind = self.erps.index(erp)
                print('{:5} - {:8.0f}'.format(erp, self.ERP_counts[erp_ind]))

        # Check counts for all COG terms
        elif dat is 'cog':
            for cog in self.cogs:
                cog_ind = self.cogs.index(cog)
                print('{:18} - {:10.0f}'.format(cog, self.COG_counts[cog_ind]))


    def save_pickle(self):
        """   """

        # Save pickle file
        save_file = os.path.join(self.save_loc, 'counts', 'counts.p')
        pickle.dump( self, open(save_file, 'wb') )


class words_results():
    """   """

    def __init__(self, erp):

        #
        self.erp = erp

        #
        self.ids = list()

        #
        self.nArticles = int()

        #
        self.years = list()
        self.titles = list()
        self.words = list()



class ERPSC_Words(ERPSC_Base):
    """This is a class for searching through words in the abstracts of specified papers. """

    def __init__(self):

        # Inherit from ERPSC Base Class
        ERPSC_Base.__init__(self)

        # 
        self.eutils_search = self.eutils_url + 'esearch.fcgi?db=pubmed&field=word&term='
        self.search_retmax = '&retmax=10'

        #
        self.eutils_fetch = self.eutils_url + 'efetch.fcgi?db=pubmed&retmode=xml&id='

        #
        self.results = list()


    def scrape_data(self):
        """   """

        # Set date of when data was collected
        self.date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        #
        for erp in self.erps:

            #
            cur_erp = words_results(erp)

            # 
            url = self.eutils_search + '"' + erp + '"' + self.search_retmax

            # Get page and parse
            page = requests.get(url)
            page_soup = BeautifulSoup(page.content)


            # Get all ids
            ids = page_soup.find_all('id')

            # Convert ids to string
            ids_str = _ids_to_str(ids)

            # Get article page
            art_url = self.eutils_fetch + ids_str
            art_page = requests.get(art_url)
            art_page_soup = BeautifulSoup(art_page.content, "xml")

            # Pull out articles
            articles = art_page_soup.findAll('PubmedArticle')

            # Check how many articles there are
            cur_erp.nArticles = len(articles)

            for art in range(0, cur_erp.nArticles):

                #
                cur_erp.ids.append(int(ids[art].text))

                #
                try:
                    cur_erp.titles.append(articles[art].find('ArticleTitle').text)
                except AttributeError:
                    cur_erp.titles.append(None)

                #
                try:
                    #cur_erp.words.append(articles[art].find('AbstractText').text)
                    cur_erp.words.append(_process_words(articles[art].find('AbstractText').text))
                except AttributeError:
                    cur_erp.words.append(None)   

                #
                try:
                    cur_erp.years.append(int(articles[art].find('DateCreated').find('Year').text))
                except AttributeError:
                    cur_erp.years.append(None)

            #
            self.results.append(cur_erp)

    def save_pickle(self):
        """   """

        # Save pickle file
        save_file = os.path.join(self.save_loc, 'words', 'words.p')
        pickle.dump( self, open(save_file, 'wb') )


###################################################################
#################### ERPSC - Functions (Public) ###################
###################################################################


def load_pickle_counts():
    """    """

    #
    save_loc = ('/Users/thomasdonoghue/Documents/Research/1-Projects/ERP-SCANR/2-Data/counts/')
    return pickle.load( open( os.path.join(save_loc, 'counts.p'), 'rb'))

def load_pickle_words():
    """    """

    #
    save_loc = ('/Users/thomasdonoghue/Documents/Research/1-Projects/ERP-SCANR/2-Data/words/')
    return pickle.load( open( os.path.join(save_loc, 'words.p'), 'rb'))


###################################################################
#################### ERPSC - Functions (Local) ####################
###################################################################

def _ids_to_str(ids):
    """Takes a list of pubmed ids, returns a str of the ids separated by commas. """
    
    # Check how many ids in list
    nIds = len(ids)
    
    # Initialize string with first id
    ids_str = str(ids[0].text)
    
    # Loop through rest of the id's, appending to end of id_str
    for i in range(1, nIds):
        ids_str = ids_str + ',' + str(ids[i].text)
        
    # Return string of ids
    return ids_str

def _process_words(words):
    """   """
    
    # Remove stop words, and anything that is only one character (punctuation). Return the result
    return [word.lower() for word in words if ((not word.lower() in stopwords.words('english')) & (len(word) > 1))]

    #words_processed = [word.lower() for word in words if ((not word.lower() in stopwords.words('english')) & (len(word) > 1))]
    #return words_processed
