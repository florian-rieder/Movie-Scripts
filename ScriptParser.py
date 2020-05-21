import re

from Reply import Reply
from Character import Character

class ScriptParser():
	"""Parser for movie scripts. """

	minimum_replies = 1 # number of replies under which a character will not be kept in the results

	character_blacklist = [
		' - ', ' -- ', '...', 
		'LATER', 'LATE', 'FADE OUT', 'FADE IN', 'CUT TO', 'EXT.', 'EXTERIOR',
		'INT.', 'INTERIOR', 'INSIDE', 'OUTSIDE', 'ANGLE ON', 'MUSIC ON', 'MUSIC UP', 
		'CLOSE ON', 'THE END', 'CUT FROM', 'CAMERA', 'LENS', 'MINIATURE', 'ANGLE', 'POV', 
		'SUNSET', 'AERIAL VIEW', 'FANTASY', 'CLOSE UP', 'SLOW MOTION', 'CLOSE-UP', 'END '
		'DAY', 'NIGHT', 'MORNING', 'WEEK', 'THE ', 'SCENE', 'ACTION', 'CONTINUED', 'CHANGED', 'HORIZON', 
		'ENDS', 'MONTAGE', 'FROM', 'WIDE-SHOT', 'SHOT', 'EXPLOSION', 'THEY', 'DISSOLVE',
		'CONTINUED', 'ROOM', 'UP AHEAD', 'SHOOTING SCRIPT', 'NEARBY', 'CUTS', 'SEES', 'INSERT'
		' ON '
	]

	reply_blacklist = [
		'LATER', 'FADE OUT', 'FADE IN', 'CUT TO', 'EXT.', 'EXTERIOR', 
		'INT.', 'INTERIOR', 'INSIDE', 'OUTSIDE', 'ANGLE ON', 'MUSIC ON', 'MUSIC UP', 
		'CLOSE ON', 'THE END', 'CUT FROM', 'CAMERA', 'LENS', 'MINIATURE', 'ANGLE', 'POV', 'DISSOLVE', 
		'SUNSET', 'AERIAL VIEW', 'FANTASY', 'CLOSE UP', 'SLOW MOTION', 'CLOSE-UP'
	]

	def parse(self, text):
		"""
		This method takes a movie script (str) as an input, and returns a list
		of all the characters in this movie script (Character class).
		"""
		characters = self._get_characters(text)

		# si moins de 5 personnages cas spécial

		# identifier le stereotype de cas spécial
		allSameLine1 = ['American-Outlaws.txt', 'Made.txt', 'Omega-Man', 'Training-Day.txt']
		noCapsColon2 = ['Mary-Poppins.txt', 'Napoleon-Dynamite.txt', 'Withnail-and-I.txt']
		sameLineRepliesNoCaps3 = ['Benny-&-Joon.txt', 'Dawn of the Dead', 'Little-Mermaid,-The.txt', 'Mulan.txt', 'Ninth-Gate,-The.txt', 'Rescuers-Down-Under,-The.txt', 'Village,-The.txt']
		sameLineRepliesCaps4 = ['Aladdin.txt', 'Labyrinth', 'Legend', 'Nightbreed', 'Star-Wars-Revenge-of-the-Sith.txt', 'Star-Wars-The-Phantom-Menace', 'White-Ribbon,-The.txt']
		noCaps5 = ['Pokemon-Mewtwo-Returns.txt']
		notScript6 = ['Artist, The', 'E.T.', 'Passion of Joan of Arc, The', 'Night Time (The Poltergeist Treatment)']

		# si aucun ne fonctionne, avertir l'utilisateur

		return characters

	def _get_characters(self, text):
		"""
		Input: correctly formatted movie script (str)
		Output: list of characters extracted from the script
		"""
		# group 1: character name, group 2: didascalie
		header_regex = re.compile(r"(?m)^[ \t]*([A-Z][A-Z -]+?)(\([\w'\.]+\))?$")
		# group 1: didascalie, group 2: reply text, group 3: final punctuation mark
		reply_regex = re.compile(r"(?m)^\s*(\([\w][\w '.,\n]+?\))?([\w\s,\.:;!?'\"-]+?(([!?.\"-]|(\.{3} ))\n))")

		characters = dict()
		
		matches = list(header_regex.finditer(text))
		for idx, m in enumerate(matches):
			
			char_name = m.group(1).strip()
			char_didascalie = m.group(2) if m.group(2) else ""
			
			# get segment substring: from end of this character header to the start
			# of the next one (or the end of the script if this is the last character header)
			if idx != len(matches)-1:
				next_match = matches[idx+1]
				segment = text[m.end():next_match.start()]
			else:
				segment = text[m.end():]

			# clean segment
			replies = list()

			reply_matches = list(reply_regex.finditer(segment))
			for idx, rm in enumerate(reply_matches):
				
				# reject matches after the first if they don't have a didascalie
				# may lead to loss of data, for instance if there is a punctuation mark
				# at the end of a line in the middle of a reply.
				# but it is an efficient way of rejecting all other text following a reply
				if idx > 0 and not rm.group(1):
					break
				
				# clean reply and didascalie
				didascalie = self._clean_padding((char_didascalie + " " + rm.group(1) if rm.group(1) else ""))
				reply_text = self._clean_padding(rm.group(2))

				# compute start and end positions of the reply 
				reply_start = m.end() + rm.start(2)
				reply_end = m.end() + rm.end(2)
				
				# store in dataclass
				reply = Reply(reply_text, didascalie, reply_start, reply_end)

				# store dataclass instance in the list of replies for this character
				replies.append(reply)
				
			# store in dataclasses
			if char_name not in characters:
				characters[char_name] = Character(char_name, replies)
			else:
				characters[char_name].Replies += replies

		# nettoyer liste personnages

		characters_list = self._clean_character_list(list(characters.values()))

		return characters_list
    
	def get_title(self, text):
		"""Finds the title of the movie"""
		title = re.findall(r"(?<=\t).+(?=\s+Writers :)", text)
		return title

	def get_author(self, text):
		"""Finds a list of the movie's authors"""
		auteurs = re.findall(r"(?<=Writers : ).+(?=\n)", text)
		return auteurs

	def get_genre(self, text):
		"""Finds the list of the movie's genres"""
		genre = re.findall(r"(?<=Genres : ).+(?=\n)", text)
		return genre

	def _clean_padding(self, segment):
		"""Removes all extra padding and line breaks from a string. Returns a correctly formatted string"""
		return " ".join([l.strip() for l in segment.split("\n")]).strip()

	def _clean_character_list(self, charlist):
		# for each character, remove replies that contain bad words
		clean_charlist = list()

		for char in charlist:
			charname = char.Character
			keep_char = True

			clean_replies = list()
			for r in char.Replies:
				reply = r.Reply
				keep_reply = True

				# check if this reply satisfies all the conditions to be kept
				if (
					any([w in reply for w in self.reply_blacklist]) or 	# remove reply if any bad word is contained in it (case sensitive)
					re.search(r"\d+\.", reply) 							# remove replies that contain a page number (numbers followed by a dot)
				):
					keep_reply = False
				
				if keep_reply:
					clean_replies.append(r)
			
			# overwrite character's replies list
			char.Replies = clean_replies

			# check if this character satisfies all the conditions to be kept
			if (
				len(char.Replies) < self.minimum_replies or					# remove characters that have less than the minimum number of replies
				any([w in charname for w in self.character_blacklist]) or 	# remove characters which have bad words in them indicating they're not characters
				charname.count(" ") > 5 or 									# remove characters whose name contains too many spaces
				(charname.startswith('(') and charname.endswith(')')) or
				charname.endswith(".") or
				charname.endswith(" -") or 
				charname.startswith("ON ") or 
				charname.startswith("BACK ") or
				charname.startswith("CUT ")
			):
				keep_char = False

			if keep_char:
				clean_charlist.append(char)

		return clean_charlist