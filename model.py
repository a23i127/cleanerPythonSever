import json
from dataclasses import dataclass
@dataclass
class RoomCleanliness:
    score: int
    state: str
    advice: str