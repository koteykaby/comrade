from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
from pathlib import Path

DOMAIN = "coh2-api.reliclink.com"
OUT_DIR = Path("ssl")
OUT_DIR.mkdir(exist_ok=True)

key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
)

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Comrade"),
    x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "API"),
    x509.NameAttribute(NameOID.COMMON_NAME, DOMAIN),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName(DOMAIN)]),
        critical=False,
    )
    .sign(key, hashes.SHA256())
)

key_path = OUT_DIR / f"{DOMAIN}-key.pem"
with open(key_path, "wb") as f:
    f.write(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

cert_path = OUT_DIR / f"{DOMAIN}.pem"
with open(cert_path, "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Output:")
print(cert_path)
print(key_path)
