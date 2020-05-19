from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Reply:
  """Class that represents one character's reply in an IMSDB movie script"""
  Reply: str
  Didascalie: str
  Start: int
  End: int

  def get_start(self):
    """Returns an int that represents the start of this reply in numbers of
    characters from the start of the given script.
    """
    return self.Start
  def get_end(self):
    """Returns an int that represents the end of this reply in numbers of
    characters from the start of the given script.
    """
    return self.End
