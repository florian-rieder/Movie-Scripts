from dataclasses import dataclass
from dataclasses import field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Character:
  """Class that represents one character of an IMSDB movie script"""
  Character: str
  Replies: list = field(default_factory=list)

  def get_replies(self):
    """Returns a list of Reply objects, that represent every reply spoken by
    this character in the given script.
    """
    return self.Replies