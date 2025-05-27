import base64
import zlib
import argparse

parser = argparse.ArgumentParser(description="Decodes options and slot info from advertisement packets")
parser.add_argument("data", help="required to decode data (options/slotinfo)")
parser.add_argument("-o", "--output", default="output.bin", help="output file")

args = parser.parse_args()

decoded_d = base64.b64decode(args.data)

zlibbed_start = decoded_d.find(b'\x78\xDA')

if zlibbed_start != -1:
    data = decoded_d[zlibbed_start:]
    decompressed = zlib.decompress(data)
    print('decompressed!')
    with open(args.output, 'wb') as f:
        f.write(decompressed)
        f.close()
        
with open(f'decoded_ONLY_{args.output}.bin', 'wb') as f:
    f.write(decoded_d)
    f.close()