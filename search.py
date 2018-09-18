''' This is the Song lyrics search engine which retrieves song lyrics according to given query from Million
Song Dataset
Author:Shubham Paliwal,Akash Dash '''

import math
from stemming.porter2 import stem
import tkinter as window


class Searcher(window.Frame):
	

	def __init__(self, master = None):
	
		window.Frame.__init__(self, master)
		self.entry = window.StringVar()
		self.msg = window.StringVar()
		self.grid()
		self.configureGrid()
		self.createWidgets()
		self.setMessage('Loading data, please wait...')

	def configureGrid(self):
		''' Configure the gui grid layout. '''
		self.rowconfigure(0, minsize = 50)
		self.columnconfigure(0, minsize = 80)
		self.rowconfigure(1, minsize = 50)
		self.columnconfigure(1, minsize = 80)
		self.rowconfigure(2, minsize = 50)
		self.columnconfigure(2, minsize = 80)
		self.rowconfigure(3, minsize = 50)
		self.columnconfigure(3, minsize = 80)
		self.rowconfigure(4, minsize = 50)
		self.columnconfigure(4, minsize = 80)
		self.rowconfigure(5, minsize = 50)
		self.columnconfigure(5, minsize = 80)
		self.rowconfigure(6, minsize = 50)
		self.columnconfigure(6, minsize = 80)
		self.rowconfigure(7, minsize = 50)
		self.columnconfigure(7, minsize = 80)
		self.rowconfigure(8, minsize = 50)

	def createWidgets(self):
		''' Define the attributes of the GUI elements. '''
			# The Label above the Entry Text Box
		self.label = window.Label(self, justify = window.LEFT, text = 'Please enter your query here ')
		self.label.grid(row = 0, column = 0, rowspan = 1, columnspan = 7, padx = 25, pady = 5, sticky = window.W)
		# The quit Button
		self.quitButton = window.Button(self, text = 'Quit', command = self.quit)
		self.quitButton.grid(row = 8, column = 7, rowspan = 1, columnspan = 1, padx = 15, pady = 25, sticky = window.N + window.E + window.S + window.W)

		# The Search Button
		self.enterButton = window.Button(self, text = 'Search', command = self.search)
		self.enterButton.grid(row = 1, column = 7, rowspan = 1, columnspan = 1, padx = 15, pady = 15, sticky = window.N + window.E + window.S + window.W)

		# The Entry Text Box
		self.entryBox = window.Entry(self, width = 60, bd = 3, relief = window.RIDGE, textvariable = self.entry)
		self.entryBox.grid(row = 1, column = 0, rowspan = 1, columnspan = 7, padx = 20, pady = 5, sticky = window.N + window.E + window.S + window.W)

		

		# The Message Box to display the output
		self.messageBox = window.Message(self, anchor = window.NW, padx = 25, pady = 25, width = 500, justify = window.LEFT, relief = window.RIDGE, bd = 3, textvariable = self.msg)
		self.messageBox.grid(row = 2, column = 0, rowspan = 7, columnspan = 7, padx = 20, pady = 25, sticky = window.N + window.E + window.S + window.W)


	def setMessage(self, message):
		self.msg.set(message)


	
	###########  Loading Data prepared by preprocess.py###########


	def preprocessLoader(self):


		# Reading through idf.txt
		self.idf_file = open('idf.txt', 'r')

		# storing idf values in idfs linewise
		self.idfs = [float(idf.rstrip('\n')) for idf in self.idf_file]

		self.idf_file.close()

		self.songs = open('mxm_dataset_train.txt', 'r')

		# Loading all different words from dataset in words
		self.words = self.songs.readline().strip().split(',')

		# Loading all the trackids
		self.tracks = [track.rstrip('\n') for track in self.songs]

		self.songs.close()

		# Mapping Track IDs to Artist Names and song titles by reading from file id_to_metadata

		self.metadata_file = open('id_to_metadata.txt', 'r')

		self.id_to_metadata = {}

			#looping through id_to_metadata file
		for itm in self.metadata_file:				
			track = itm.strip().split(',')							#tokenizing on basis of ','
			self.id_to_metadata[track[0]] = (track[1], track[2]) 	#track[0]->track-id,track[1]-Artist names,track[2]-Song titles

		self.metadata_file.close()


	


		
		

		
		self.word_to_index = {}
		#Mapping words to their indexes
		for i in range(1, len(self.words)):
			self.word_to_index[self.words[i]] = i

		# Mapping  word indices and Track IDs to term frequencies
		self.tf_wordi_termi = 5001 * [0]
		self.tf_termi_wordi = {}

		for i in range(0, 5001):
			self.tf_wordi_termi[i] = {}

		for track in self.tracks:
			attrib = track.split(',')
			track_id = attrib[0]
			self.tf_termi_wordi[track_id] = {}
			for i in range(2, len(attrib)):
				word_index = int(attrib[i][:attrib[i].index(':')])
				freq = int(attrib[i][(attrib[i].index(':') + 1):])
				self.tf_wordi_termi[word_index][track_id] = freq
				self.tf_termi_wordi[track_id][word_index] = freq
		self.setMessage('Loading Complete.')

	########## Stemming the Query ##########
	

	def stemQuery(self, query):
		
		query = query.replace('\n', ' ')
		query = query.replace('\r', ' ')

		query = query.replace("'m ", " am ")
		query = query.replace("'re ", " are ")
		query = query.replace("'ve ", " have ")
		query = query.replace("'d ", " would ")
		query = query.replace("'ll ", " will ")
		query = query.replace(" he's ", " he is ")
		query = query.replace(" she's ", " she is ")
		query = query.replace(" it's ", " it is ")
		query = query.replace(" ain't ", " is not ")
		query = query.replace("n't ", " not ")
		query = query.replace("'s ", " ")
		query = query.lower()

		

		punct = (',', "'", '"', ",", ';', ':', '.', '?', '!', '(', ')',
		                '_', '|', '-')
		for p in punct:
		    query = query.replace(p, '')

		words = filter(lambda x: x.strip() != '', query.split(' '))

		# Stemming words using Porter Stemmer
		words = map(lambda x: stem(x), words)

		return list(words)

	
	###### Query TF-IDF Calculation ############

	def queryTfidfs(self):
		''' Calculating the TFIDF vector components for the query. '''
		self.query_vector_length = 0.0
		self.query_tfidfs = {}
		
		for query_tf_key in self.query_tfs:
			self.query_tfidfs[query_tf_key] =  (1 + math.log10(self.query_tfs[query_tf_key])) * self.idfs[query_tf_key]
			self.query_vector_length += self.query_tfidfs[query_tf_key] ** 2
		self.query_vector_length = math.sqrt(self.query_vector_length)



	######### TFIDF Calculation Function ########


	def tfidfScore(self, track_id):
		'''
		Calculate TF-idf vector of document track_id
		'''

	
		document_tfidfs = {}
		document_vector_length = 0.0
		for track_word_key in self.tf_termi_wordi[track_id]:
			document_tfidfs[track_word_key] = (1 + math.log10(self.tf_termi_wordi[track_id][track_word_key])) * self.idfs[track_word_key]
			document_vector_length += document_tfidfs[track_word_key] ** 2
		document_vector_length = math.sqrt(document_vector_length)

		# Compute the query-document TFIDF Score
		tfidf_score = 0.0
		for query_tf_key in self.query_tfs:
			if query_tf_key in self.tf_termi_wordi[track_id]:
				tfidf_score += self.query_tfidfs[query_tf_key] * document_tfidfs[query_tf_key]
		tfidf_score /= (document_vector_length * self.query_vector_length)

		return tfidf_score

	########Ranking the most related documents##############

	def mostRelated(self):
		
		topTracks = []
		curMax = 0.0
		for i in range(0, 10):
			for tfidfs_key in self.doc_tfidfs:
				if tfidfs_key > curMax and self.doc_tfidfs[tfidfs_key] not in topTracks:
					curMax = tfidfs_key
			if (curMax == 0.0):
				break
			topTracks.append(self.doc_tfidfs[curMax])
			curMax = 0.0
		return topTracks



	######### Query Processing Function #########
	

	def answer(self, query):
		

		# Query Term Frequencies
		self.query_tfs = {}

		# List of (stemmed) query words
		query_words = self.stemQuery(query)

		for qword in query_words:
			if qword in self.word_to_index:
				qword_index = self.word_to_index[qword]
				if self.idfs[qword_index] >= 0.2:
					if qword_index in self.query_tfs:
						self.query_tfs[qword_index] = self.query_tfs[qword_index] + 1
					else:
						self.query_tfs[qword_index] = 1

		# Compute TFIDFs for the query
		self.queryTfidfs()

		matches = {}
		for query_tfs_key in self.query_tfs:
			for track_id in self.tf_wordi_termi[query_tfs_key]:
				if track_id in matches:
					matches[track_id] += 1
				else:
					matches[track_id] = 1

		# Set of tracks to check
		tracks_to_check = set()
		for track_id in self.id_to_metadata:
			if track_id in matches and matches[track_id] >= len(self.query_tfs) / 2:
				tracks_to_check.add(track_id)

		# TFIDFs for all documents
		self.doc_tfidfs = {}
		for track_id in tracks_to_check:
			self.doc_tfidfs[self.tfidfScore(track_id)] = track_id

		return self.mostRelated()




    #####Search begins(start of query processing)#########

	def search(self):
		

		# Getting the text from the entry box
		query = self.entry.get()

		# Get most relevant tracks
		relevant_tracks = self.answer(query)

		msg = ''

		if len(relevant_tracks) < 1:
			msg += '\nSorry,No lyrics match your query'
		else:
			msg+= '\nThe top tracks you want are:\n\n'
			counter = 1
			for top_track_id in relevant_tracks:
				metaarray = self.id_to_metadata[top_track_id]
				msg += str(counter) + ". " + metaarray[0] + " - " + metaarray[1] + '\n'
				counter += 1

		
		self.setMessage(msg)


###############################################################################

root = window.Tk()
process = Searcher(root)
process.master.title('Lyrics Miner')
process.after(500, process.preprocessLoader)
process.mainloop()
