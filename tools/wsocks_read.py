import zlib
import argparse
from hexdump import hexdump

parser = argparse.ArgumentParser(description='tool to view battleserver packets uncompressed')
parser.add_argument('data', type=str, help='packet in hex string')

args = parser.parse_args()
input_data = args.data

byte_data = bytes.fromhex(input_data)
print(byte_data)
hexdump(byte_data)

zlib_start = byte_data.find(b'\x78\x01')
is_compressed = zlib_start != -1
decompressed = None
            
if is_compressed:
    try:
        decompressed = zlib.decompress(byte_data[zlib_start:])
        print("Decompressed packet:")
        hexdump(decompressed)
        with open('orig.bin', 'wb') as f:
            f.write(byte_data)
            f.close()
        with open('decomp.bin', 'wb') as f:
            f.write(decompressed)
            f.close()
        print('data has written to files!')
    except zlib.error as e:
        print(f"zlib error: {e}")
