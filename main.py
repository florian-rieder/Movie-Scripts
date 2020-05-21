"""For all scripts in a directory, generate corresponding json file"""

import os
import time
import json

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
		movie = parser.parse(text)

		# convert to json object and format into a prettified string
		movie_json = json.loads(movie.to_json())
		movie_json_string = json.dumps(movie_json, indent=4)

		# write json string to a file
		with open(os.path.join(PARSED_SCRIPTS_PATH, filename[:-4] + ".json"), "w") as json_script:
			json_script.write(movie_json_string)

		print("processed %s." % filename)

		# debug break
		#break
	
	end = time.time()

	print("\n processed all scripts in %f [s]" % float(end - start))

if __name__ == "__main__":
    main()