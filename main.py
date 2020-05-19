"""For all scripts in a directory, generate corresponding json file"""

import os
import time

from Movie import Movie
from ScriptParser import ScriptParser

MOVIE_SCRIPTS_PATH = "./scripts"
PARSED_SCRIPTS_PATH = "./parsed_scripts"

def main():

	parser = ScriptParser()

	start = time.time()

	for filename in os.listdir(MOVIE_SCRIPTS_PATH):

		if not filename.endswith(".txt"):
			continue

		# read the raw script and get characters list
		with open(os.path.join(MOVIE_SCRIPTS_PATH, filename), "r", encoding="utf8") as script:
			text = script.read()

		# get characters list
		characters = parser.parse(text)

		# get title
		title = parser.get_title(text)

		# get author
		author = parser.get_author(text)

		# get genre
		genre = parser.get_genre(text)

		# create Movie object
		m = Movie(title, author, genre, characters)

		# convert characters list into a JSON file
		with open(os.path.join(PARSED_SCRIPTS_PATH, filename[:-4] + ".json"), "w") as json_script:
			json_script.write(m.to_json())

		print("processed %s." % filename)

		# debug break
		#break
	
	end = time.time()

	print("\n processed all scripts in %f [s]" % start - end)

if __name__ == "__main__":
    main()