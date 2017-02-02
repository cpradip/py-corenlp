def get_list_from_data_files():
	f_raw = open('data/trainRaw.txt', 'r')
	f_out = open('data/trainOut.txt', 'r')
	f_entities = open('data/entity_list_comparison_1.txt', 'w')
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
		
		f_entities.write('..........................  ' + str(k) + '  ...........................' + '\n')

		for word_out in words_out:
			#if (word_out != '0' and words_raw[word_index] not in primary_words):
			if (word_out != '0'):
				#print(words_raw[word_index] + '\t' + word_out + '\n')
				primary_words.add(words_raw[word_index])
				dictionary_entities[words_raw[word_index]] = word_out
				#f_entities.write(words_raw[word_index] + '\t' + word_out + '\n')
				f_entities.write(words_raw[word_index] + ' : ' + word_out + '\n')

			word_index += 1

		k += 1
		#break_index += 1
		#if break_index > 10:
		#	break

	f_raw.close()
	f_out.close()
	f_entities.close()

def arrange_the_values_in_files():
	f_data = open('data/entity_list.txt', 'r')
	f_arranged = open('data/entity_list_arranged.txt', 'w')

	for line_data in f_data:
		words_data = line_data.split('\t')
		entity_word = words_data[0].title()
		label_word = words_data[1]

		f_arranged.write(line_data)
		f_arranged.write(entity_word + '\t' + label_word)


if __name__ == '__main__':
	arrange_the_values_in_files()
