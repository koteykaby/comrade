from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

# Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Set certificate details
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, "coh2soviet"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Relic Link"),
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
])

# Create certificate
cert = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.utcnow()
).not_valid_after(
    datetime.utcnow() + timedelta(days=365)
).add_extension(
    x509.SubjectAlternativeName([
        x509.DNSName("reliclink.com"),
        x509.DNSName("*.reliclink.com"),
    ]),
    critical=False,
).sign(private_key, hashes.SHA256(), default_backend())

# Write private key to file
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# Write certificate to file
with open("certificate.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Self-signed certificate and private key generated successfully:")
print(" - Private key: private_key.pem")
print(" - Certificate: certificate.pem")