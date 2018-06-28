___Note: This repo (capstone-35) is used only to harvest EG GULF from twitter and to conduct basic EDA on the data. For the relevant EG Arabic twitter streams and users, please refer to the capstone-34 repo. Additionally, to conduct topic modeling and classification on a corpus containing both dialects, please refer to capstone-52.___

# Twitter Dialect Datasets and Classifiers (Arabic)
A project to harvest corpora for Egyptian Arabic and Gulf Arabic from Twitter, conduct descriptive analyses of the resulting corpora, and show that a simple classifier can predict dialect quite effectively. 

## Getting Started
Clone this repository to your local harddrive: `git clone https://github.com/telsahy/capstone-35.git`

### Prerequisites
Install dependencies from the included `requirements.txt` file by running either of the following commands:
- `!pip install -r requirements.txt`
- `$ pip install -r requirements.txt`

## Harvesting Twitter Data and Required Infrastructure

### Streaming:
- Create list of dialect specific keyword search terms to use for twitter streamers.
- Create Docker file containing tweepy authentication tokens + other modules added to the jupyter scipy docker image to make the code generalized enough to work with different instances.
- Stream prefiltered keywords list for each class (EG, and GULF). Requires a crone job in order to:
	- Collect 1-username, 2-tweet, 3-location.  
	- Decode Arabic Unicode characters.
	- Store data as jsonl or json on AWS instance. 
	- Automatically restart tweet streams in case of common errors. 
    
### Storing:
- Store raw data into Mongo collection (e.g: `raw_gulf`, with documents being `raw_stream` and `raw_timelines`). 
- Raw data remains stored on AWS instance. 

### Infrastructure: 
- Two t2.micros with unique oauth to stream two dialects to decrease chances of dialects mixing. 
- One t2.large for modeling and more computationally expensive tasks. 

## Munging/Cleaning/Storing the Data
Instructions on working with resulting datasets using pandas DataFrames are provided within the related Jupyter Notebooks.   

### Cleaning data:
- Using regex to filter out emojis, links, http, excluded Arabic unicode in many cases. An easier way to clean the data is to import tweet-preprocessor, the twitter preprocessing package provided in the requirements.txt file.
- Check for duplicates before converting document formats.
- Pickle cleaned data into a seperate folder (e.g: gulf_twitter_pickled). 
	
### Storing data in MongoDB:
- Storing should be taking place at each stage of the process. 
- Build up corpus, store in Mongo collection as two documents for each class, EG and Gulf.
- Store combined documents under a new collection on Mongo.
- Store cleaned data into Mongo collection (e.g: `cleaned_gulf`, with documents being `cleaned_stream` and `cleaned_timelines`). 
    
## Basic EDA/Visualization
- Inspect keyword documents for excessive advertisement and remove duplicates.
- Inspect geographic origins of keyword documents to determine the document's utility to the overall collection. 
- Identify users who contribute most to the keyword stream and add them to the timelines stage
    
## EDA, Tokenization, and SVD 
- Perform EDA, tokenization and SVD on collected data:
	- Check for term co-ocurrences in EG and Gulf documents and add to stopwords list. 
	- Subtract co-occurances of terms between dialects from the data before tokenization?
	- Identify dialectically different keywords and include in the twitter streaming pipeline.
	- Identify users with the richest dialectal tweets and add them to timeline streams. 
	- Confirm geographic origin of tweets and make term substitutions in stop word list as needed.
	- Continue rinsing and repeating until terms appear mostly in either one or the other documents.
- Repeat same process for user timelines using Twitter's REST API
- Optional: Stanford Arabic Parser (with built-in ATB) to lametize and seg the data. Use Stanford Arabic Word Segmenter concurrently with Parser, before or after? 
- Use the three techniques below and explore best results:
	- Tfidf, SVD, latent semantic analysis
	- Okapi best match, SVD, latent semantic analysis
	- Kullback-Leibler Divergence Model, SVD. 

## Train/Test Estimators on Collected Data (Classes: EG & GULF) 

### Classifiers: 
- Naive Bayes
- Multinomial LR classifiers
- Logistic Regression

### Results:
- Perform plotting, confusion matrix, classification report, roc curve, etc.  
- Optional: Clustering estimators, DBSCAN, KMeans, Spectral Clustering

## Deep Learning - Text Classification with RNN
- Word2Vec
- Word embeddings using Keras or Gensim

## Authors
- Tamir ElSahy

## Acknowledgments
- Please refer to the research paper for list of acknowledgments
