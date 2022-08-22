from ast import parse
from enum import Enum, auto
from dataclasses import dataclass
from functools import reduce
import io

class InvalidMidi(Exception):
    pass

class DivType(Enum):
    TICKS_PER_QUARTER = auto()
    FRAMES_PER_SECOND = auto()


def read_multi_byte(f: io.BufferedWriter, num = 0) -> int:
    data = f.read(1)[0]
    if data & 0x80 == 0:
        return (num << 7) | data
    return read_multi_byte(f, ((num << 7) | (data & 0x7f)))

def bytes_to_int(data: bytes) -> int:
    return reduce(
        lambda num, b: (num << 8) | b,
        data
    )

@dataclass
class MidiHeader:
    format: int
    num_tracks: int
    div_type: DivType
    div: float



def parse_header(f: io.BufferedIOBase) -> MidiHeader:
    if f.read(4) != b'MThd':
        raise InvalidMidi
    # read header length. this will always be six
    f.read(4)
    midi_format = bytes_to_int(f.read(2))
    num_tracks = bytes_to_int(f.read(2))
    div = f.read(2)
    # parse division
    if div[0] & 0x80:
        div_type = DivType.FRAMES_PER_SECOND
        frame_rate = (((div[0] & 0x7f) ^ 0xff) + 1)
        frame_rate = 29.97 if frame_rate == 29 else frame_rate
        ticks_per_frame = div[1]
        div_val = ticks_per_frame / frame_rate
    else:
        div_type = DivType.TICKS_PER_QUARTER
        div_val = ((div[0] & 0x7f) << 8) | div[1]

    return MidiHeader(
        midi_format,
        num_tracks,
        div_type,
        div_val
    )
    
def read(filename: str) -> any:
    with open(filename, 'rb') as f:
        header = parse_header(f)
        print(header)

if __name__ == "__main__":
    # flip data should be 0x0a84
    read("ABBA_-_Alaska.mid")
