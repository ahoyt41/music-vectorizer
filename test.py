with open("RUshEconvertedwhitemidi.mid", 'rb') as f:
    header_label = f.read(4)
    print("Chunk ID", header_label.decode('ascii'))
    header_size = f.read(4)
    print("Header size", int.from_bytes(header_size, byteorder='big'))
    format_type = int.from_bytes(f.read(2), 'big')
    print("file format", format_type)
    num_tracks = int.from_bytes(f.read(2), 'big')
    print("num tracks", num_tracks)
    divisor = int.from_bytes(f.read(2), 'big')
    time_div_type = "frames per second" if divisor >> 15 else "ticks per beat"
    print(time_div_type)
    tick_rate = 0x7FFF & divisor
    