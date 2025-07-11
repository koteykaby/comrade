import base64
import zlib
import argparse
import hexdump

parser = argparse.ArgumentParser(description="Decodes options and slot info from advertisement packets")
parser.add_argument("data", help="required to decode data (options/slotinfo)")
parser.add_argument("-o", "--output", default="output.bin", help="output file")
parser.add_argument("--isfile", action="store_true", help="data is file")  

args = parser.parse_args()

try:
    if args.isfile:
        with open(args.data, 'rb') as f:
            data = f.read()
        
        for zlib_header in (b'\x78\x01', b'\x78\x9C', b'\x78\xDA'):
            zlib_pos = data.find(zlib_header)
            if zlib_pos != -1:
                try:
                    decompressed_d = zlib.decompress(data[zlib_pos:])
                    print("[+] Successfully decompressed!")
                    hexdump.hexdump(decompressed_d)
                    with open(args.output, 'wb') as f_out:
                        f_out.write(decompressed_d)
                    break
                except zlib.error:
                    continue
        else:
            print("[-] Error: Could not find valid zlib data in the file!")
    else:
        decoded_d = base64.b64decode(args.data)
        
        for zlib_header in (b'\x78\x01', b'\x78\x9C', b'\x78\xDA'):
            zlib_pos = decoded_d.find(zlib_header)
            if zlib_pos != -1:
                try:
                    decompressed = zlib.decompress(decoded_d[zlib_pos:])
                    print("[+] Successfully decompressed!")
                    hexdump.hexdump(decompressed)
                    with open(args.output, 'wb') as f_out:
                        f_out.write(decompressed)
                    break
                except zlib.error:
                    continue
        else:
            print("[-] Error: Could not find valid zlib data in the base64 decoded string!")
        
        with open(f'decoded_ONLY_{args.output}', 'wb') as f_dec:
            f_dec.write(decoded_d)

except Exception as e:
    print(f"[-] Error: {e}")