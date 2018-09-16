## songSearchEngine

#### Authors - Akash Dash, Shubham Paliwal

There are two python files in this project :
1. preprocess.py : To calculate idf, store metadata info from dataset to text file
2. search.py     : This is the main project file. It imlements the GUI, takes the queries and calculates tfidf 	and finally shows the relevant document data

The following files need to be aditionally downloaded into the sorce code folder for the program to function properly:
1. Song lyrics dataset : https://labrosa.ee.columbia.edu/millionsong/musixmatch 
2. Dataset metadata info : http://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/msd_summary_file.h5

Dependencies/Libraries : 
1. python 3
2. tkinter
3. h5py : http://docs.h5py.org/en/latest/build.html
4. Porter Stemmer : https://pypi.python.org/pypi/stemming/1.0

Running the code :
1. The file preprocess.py calculates and stores the idfs and writes metadata info of all the documents into a file. This process tkes place around 10 minutes.It needs to br run only once.
2. The file search.py implements the GUI. It takes the user query and displays the most relevant documents.




# songSearchEngine
