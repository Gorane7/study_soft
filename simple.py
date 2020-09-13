from os import path
from random import random

def get_questions(filename):
	file = open(filename, 'r')
	questions = []
	mode = 'next'
	for line in file.readlines():
		if mode == 'next':
			questions.append([])
			questions[-1].append(line.strip('\n'))
			questions[-1].append([])
			mode = 'loading'
		elif mode == 'loading':
			stripped = line.strip('\n')
			if len(stripped) == 0:
				mode = 'next'
			else:
				questions[-1][-1].append(stripped)
	return questions

def get_stats(filename, questions):
	if path.isfile(filename):
		file = open(filename, 'r')
		lines = list(map(lambda x: float(x.strip('\n')), file.readlines()))
		file.close()
		return lines
	return [1] * len(questions)

def pick_random(stats):
	total = sum(stats)
	choice = random() * total
	for i, stat in enumerate(stats):
		choice -= stat
		if choice <= 0:
			return i

def save_stats(stats, filename):
	file = open(filename, 'w')
	file.writelines(list(map(lambda x: str(x) + '\n', stats)))
	file.close()

if __name__ == '__main__':
	reduction_factor = 2
	increase_factor = 10
	questions = get_questions('questions.txt')
	stats = get_stats('stats.txt', questions)
	for i in range(1000):
		picked = pick_random(stats)
		print(questions[picked][0])
		input('Valmis?')
		print('\n'.join(questions[picked][1]))
		knew = input('Teadsid (Y/n) ? ')
		if knew.lower() == 'n':
			stats[picked] = stats[picked] * increase_factor
		else:
			stats[picked] = stats[picked] / reduction_factor
		print()
		save_stats(stats, 'stats.txt')
		#print(picked)
	print(stats)