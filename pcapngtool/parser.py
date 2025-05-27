import argparse
import json
import pyshark
from urllib.parse import urlparse, parse_qs

cmdargs_p = argparse.ArgumentParser()
cmdargs_p.add_argument('--pcapng', help='path to .pcapng file')
cmdargs = cmdargs_p.parse_args()

cap = pyshark.FileCapture(str(cmdargs.pcapng), display_filter='http')

def resp_conv(string):
    n = string.replace(":", "")
    r = bytes.fromhex(n).decode('utf-8')
    return json.loads(r)

def convert_to_unk_format(data):
    if isinstance(data, (list, tuple)):
        converted = {f"unk{i}": convert_to_unk_format(value) for i, value in enumerate(data)}
        return converted
    elif isinstance(data, dict):
        return {key: convert_to_unk_format(value) for key, value in data.items()}
    else:
        return data

for packet in cap:
    try:
        if 'HTTP' in packet and hasattr(packet.http, 'request_method'):
            full_url = packet.http.request_uri
            parsed_url = urlparse(full_url)
            path = parsed_url.path
            query = parsed_url.query
            args = parse_qs(query)

            data = {
                'request': {
                    'path': path,
                    'args': {key: value[0] for key, value in args.items()}
                },
                'response': None  
            }

            filename = f"{path.replace('/', '_').replace('?', '_')}.json"
            filename = filename.replace('&', '_').replace('=', '_')

            with open(f"protocols/{filename}", 'w') as json_file:
                json.dump(data, json_file, indent=4)
            
            print(f"parsed!: {filename}")
        
        if 'HTTP' in packet and hasattr(packet.http, 'file_data') and hasattr(packet.http, 'response_code'):
            resp_data = resp_conv(packet.http.file_data)
            processed_data = convert_to_unk_format(resp_data)
            print(json.dumps(processed_data, indent=4))
            
            path = urlparse(packet.http.request_uri).path
            
            filename = f"{path.replace('/', '_').replace('?', '_')}.json"
            filename = filename.replace('&', '_').replace('=', '_')
            
            filepath = f"parsed_protocols/{filename}"

            with open(filepath, 'r') as json_file:
                combined_data = json.load(json_file)
                combined_data['response'] = processed_data

            with open(filepath, 'w') as json_file:
                json.dump(combined_data, json_file, indent=4)
                print(f"Response added: {filename}")
    except AttributeError:
        continue
    except json.decoder.JSONDecodeError:
        continue
                                  
cap.close()