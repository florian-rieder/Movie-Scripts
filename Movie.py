from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Movie:
	"""This class represents a movie.
	Title, Author, Genre: metadata
	Characters: list of Character objects, representing all the characters
	present in this movie script
	"""
	Title: str
	Author: list = field(default_factory=list)
	Genre: list = field(default_factory=list)
	Characters: list = field(default_factory=list)