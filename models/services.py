from dataclasses import dataclass

@dataclass
class battleserver:
    region: str
    name: None
    ipv4: str
    bsPort: int
    webSocketPort: int
    outOfBandPort: int