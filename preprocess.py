'''
========================================================================
Script to preprocess the training dataset.
This script generates two files on execution :
1. idf.txt : Inverse document frequencies
2. metadata.txt : Metadata of songs corresponding to DocID

IDF file contains inverse document frequencies of words in dataset
Metadata file contains of mapping of DocID to songname and Artist Name

File used to train dataset : 
1. mxm_dataset_train.txt 
	http://labrosa.ee.columbia.edu/millionsong/musixmatch
	Contains 5000 most frequent words from a million songs
2. msd_summary_file.h5
	Contains metadata information of the documents

========================================================================
''' 	

import math
import time
import h5py


start_time = time.time()

# Song ID and Doc Frequency Array
song_ids = set()
docFreq = [0] * 5001

#Training dataset
print("Retrieving Song IDs and Term Frequencies...")
train_dataset = open('mxm_dataset_train.txt', 'r')

# First line contains words, 2nd line onwards contains DocID and word frequencies
# Store term frequencies of different docs in songs array
train_dataset.readline()
songs = [song.rstrip('\n') for song in train_dataset]
N = len(songs)
train_dataset.close()



# Find term frequency of each word
for song in songs:
	docLine = song.split(',')
	song_ids.add(docLine[0])
	for i in range(2, len(docLine)):
		word_index = int(docLine[i][:docLine[i].index(':')])
		docFreq[word_index] += 1


# String to store data to be written to "idf.txt"
idftext = ''

# Find IDF
for i in range(len(docFreq)):
	if (docFreq[i] == 0):
		idftext += '0'
	else:
		idftext += str(math.log10(N / docFreq[i]))
	idftext += '\n'	

print("Writing IDF to file")

# Write to file
idf_file = open('idf.txt', 'w')
idf_file.write(idftext)
idf_file.close()


print("Reading from msd_summary_file.h5")
#msd_summary_file contains metadata information of all Song IDs
msd = h5py.File('./msd_summary_file.h5', 'r')
analysis_songs = msd['analysis']['songs']
metadata_songs = msd['metadata']['songs']

# to store metadata info
metadata_text = ''

# For each song , write Song ID, Artist Name, Song Name to metadata_text
for i in range(1000000):
	song_id = analysis_songs[i]['track_id'].decode('utf-8') #CSV to UTF
	if (song_id in song_ids):
		artist = metadata_songs[i]['artist_name'].decode('utf-8')
		song_name = metadata_songs[i]['title'].decode('utf-8')
		metadata_text += song_id + ',' + artist + ',' + song_name + '\n'


print("Writing metadata disk...")

# Write to file
metadata_file = open('id_to_metadata.txt', 'w')
metadata_file.write(metadata_text)
metadata_file.close()

# Preprocessing complete
print("Processing done !!!")
end_time = time.time()
print("Time Taken: " + str((end_time - start_time) / 60) + " minutes")