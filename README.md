
#Get it working

1. Create a directory in the machine say `mkdir path/to/folder/` and go to this directory `cd path/to/folder/`
2. Create a python virtual environment using the command `virtualenv CS535.project`. This step should create a folder inside your current directory
3. Activate the virtual environment with the command `source activate CS535.project`
4. You might need to upgrade pip `pip install --upgrade pip`.
5. Now install tweepy. `pip install tweepy`
6. Create another directory `mkdir streaming_data`
7. Run the program `python streaming.py > stdout.txt 2> stderr.txt &` to run it in the background

#References:

http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
http://scikit-learn.org/stable/modules/feature_extraction.html
http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words
https://en.wikipedia.org/wiki/Tf%E2%80%93idf
http://stackoverflow.com/questions/15507172/how-to-get-bag-of-words-from-textual-data
http://stackoverflow.com/questions/10554052/what-are-the-major-differences-and-benefits-of-porter-and-lancaster-stemming-alg
http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html
http://www.nltk.org/

