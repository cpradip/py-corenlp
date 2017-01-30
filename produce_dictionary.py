if __name__ == '__main__':
	f_raw = open('data/trainRaw.txt', 'r')
	f_out = open('data/trainOut.txt', 'r')
	f_entities = open('data/entity_list_comparison.txt', 'w')
	break_index = 0;
	primary_words = set([])
	dictionary_entities = {}
	k = 1

	for line_raw in f_raw:
		#print line_raw
		line_out = f_out.readline()
		#print line_out
		words_raw = line_raw.split()
		words_out = line_out.split()

		word_index = 0
		
		f_entities.write('..........................' + str(k) + '............................' + '\n')

		for word_out in words_out:
			#if (word_out != '0' and words_raw[word_index] not in primary_words):
			if (word_out != '0'):
				#print(words_raw[word_index] + '\t' + word_out + '\n')
				primary_words.add(words_raw[word_index])
				dictionary_entities[words_raw[word_index]] = word_out
				f_entities.write(words_raw[word_index] + '\t' + word_out + '\n')

			word_index += 1

		k += 1
		#break_index += 1
		#if break_index > 10:
		#	break

	f_raw.close()
	f_out.close()
	f_entities.close()

	
