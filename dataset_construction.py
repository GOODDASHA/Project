#coding=utf-8
import csv
import os
import gc

rawdata_filename = 'raw_journal_relation.txt'
input_directory = '/Users/elvin/Desktop/Project_iofiles/Input'
rawdata_file = os.path.join(input_directory, rawdata_filename)


header = ['edition',
		  'referenced num this year', 
		  'published num in the first 6 months',
		  'published num this year',
		  'num of paper', 
		  'num of self_scitation in the first 6 months',
		  'num of self_scitation',
		  'num of reference this year',
		  'review doctype num', 
		  'something',
		  'num authors']

data_set = {}

def initialize(ds, journal):

	if journal in ds or journal=='':
		return ds
	ds[journal] = {str(year):
					{
						'edition':'',
		  				'referenced num this year':0, 
		  				'published num in the first 6 months':0,
		  				'published num this year':0,
		  				'num authors':set(),
		  				'num of paper':0,
		  				'num of self_scitation in the first 6 months':0,
		  				'num of self_scitation':0,
		  				'num of reference this year':0,
		  				'review doctype num':0,
		  				'something':0
					}
						for year in range(2008, 2014)}
	return ds

def collect_journal_names():
	ds = {}
	_dict = {}

	with open(rawdata_file, 'rb') as input_txtfile:
		for n, line in enumerate(input_txtfile):
			if not n%100000:
				print 'collecting and initializing', n
			line = line.strip('\n').split('\t')
			journal = line[0]

			ref_journals = line[1].split('|')

			ds = initialize(ds, journal)

			for _journal in  ref_journals:
				ds = initialize(ds, _journal)

			info =  line[2].split('|')
			year = eval(info[2])[0][:4]
			paper = eval(info[0])[0]
			_dict[paper] = [journal, year]


	return ds, _dict



def collecting_features(ds, _something_dict):
	m = {}

	with open(rawdata_file, 'rb') as input_txtfile:

		for n, line in enumerate(input_txtfile):
		
			if not n%100000:
				print n
			line = line.strip('\n').split('\t')

			# journal relations
			journal = line[0]
			if journal == '':
				continue
			#print journal
			ref_journals = line[1].split('|')


			info = []
			for x in line[2].split('|'):
				if len(x) > 0:
					info.append(eval(x))
				else:
					info.append(x)

			edition = info[1][0]
			year, month, day = info[2][0].split('-')
			authors = set(info[6])
			num_ref_papers = len(info[9])
			doctype = info[4][0]
			ds[journal][year]['edition'] = edition
			if doctype == 'Review':
				ds[journal][year]['review doctype num'] += 1
			for _journal in ref_journals:
				if _journal == '':
					continue
				ds[_journal][year]['referenced num this year'] += 1


				if journal == _journal:
					ds[_journal][year]['num of self_scitation'] += 1
					if int(month) < 7:
						ds[_journal][year]['num of self_scitation in the first 6 months'] += 1

			if int(month) < 7:
				ds[journal][year]['published num in the first 6 months'] += 1
				

				
				for _paper in info[-1]:
					try:
						_journal, _year = _something_dict[_paper]


						if  int(_year) < int(year) and int(_year) > int(year)-3:

							ds[_journal][year]['something'] += 1
						if  int(_year) > int(year):
							#print _paper
							#break
							pass
						'''

						otherpaper    p1   		p2
									  j1   		j2
						this year     t1  		t2
						'''
					except:
						m[_paper] = 1
						if not len(m)%100000:
							print len(m), 'paper not found'

			ds[journal][year]['published num this year'] += 1
			ds[journal][year]['num authors'] = ds[journal][year]['num authors'].union(authors)
			ds[journal][year]['num of paper'] += 1
			ds[journal][year]['num of reference this year'] += num_ref_papers


	return ds

def write(data_set):
	with open('dataset.csv', 'wb') as output_csvfile:
		writer = csv.writer(output_csvfile, delimiter=',')
		writer.writerow(['journal','year'] + header)
		for journal in data_set:
			for year in range(2008, 2014):
				year = str(year)
				line = [journal, year]
				for x in header[:-1]:
					line.append(data_set[journal][year][x])
				line.append(len(data_set[journal][year][header[-1]]))
				writer.writerow(line)










#data_set, something_dict  = collect_journal_names()
#data_set= collecting_features(data_set, something_dict)

#write(data_set)


def add_label():
	with open('dataset.csv', 'rb') as input_csvfile:
		with open('labeled_dataset.csv', 'wb') as output_csvfile:

			dr = csv.DictReader(input_csvfile)
			writer = csv.writer(output_csvfile, delimiter=',')
			writer.writerow( header)
			for line in dr:
				journal_name = line['journal']
				year = int(line['year'])
				target = int(journal_name in bad_journal_dict[year])

				if year < 2010:
					self_cited_last_year = 0
					self_cited_2_years_ago = 0
				else:
					self_cited_last_year = int(journal_name in bad_journal_dict[year-1])
					self_cited_2_years_ago = int(journal_name in bad_journal_dict[year-2])

				line = [line[x] for x in header[:-3]]
				line.append(self_cited_last_year)
				line.append(self_cited_2_years_ago)
				line.append(target)
				writer.writerow(line)

header = ['journal', 'year'] +header + ['self_cited_last_year', 'self_cited_2_years_ago', 'target']

ext = '.txt'
bad_journal_dir = '/Users/elvin/Desktop/Project_iofiles/Bad_Journal'
bad_journal_dict = {}
for year in range(2007, 2014):

	bad_journal_filename = str(year) + ext
	bad_journal_file = os.path.join(bad_journal_dir, bad_journal_filename)

	journal_set = set([x.strip() for x in open(bad_journal_file, 'rb').read().split('\r')])
	bad_journal_dict[year] = journal_set




def add_ranks():


	# add pagerank

	journal_pageranks = {}
	with open('journal_pageranks', 'rb') as pr:
		for line in pr:
			line = line.strip().split('\t')
			journal = line[0]
			rank = float(line[1])
			journal_pageranks[journal] = rank

	journal_trutranks = {}
	for year in range(2010, 2014):
		
		file_name = 'journal_trustranks_from_%d_to_%d.txt'%(year-2, year)
		with open(file_name, 'rb') as tr:

			for line in tr:
				line = line.strip().split('\t')
				journal = line[0]
				rank = line[1]

				if journal in journal_trutranks:

					journal_trutranks[journal][year] = rank
				else:
					journal_trutranks[journal] = {year:rank}

	with open('dataset_with_ranks.csv', 'wb') as output_csvfile:

		with open('labeled_dataset.csv', 'rb') as input_csvfile:

			dr = csv.DictReader(input_csvfile)
			writer = csv.writer(output_csvfile, delimiter=',')
			writer.writerow( header)
			for line in dr:
				journal_name = line['journal']
				year = int(line['year'])
				try:
					pagerank = journal_pageranks[journal_name]
				except:
					pagerank = 0
				try:
				

					trustrank = journal_trutranks[journal_name][year]
				except:
					trustrank = 0
				line['pagerank'] = pagerank
				line['trustrank'] = trustrank
				line = [line[x] for x in header]
				writer.writerow(line)

	# add trustrank


#add_label()
header = ['journal', 'year'] + ['pagerank', 'trustrank'] + header[2:]

add_ranks()


















