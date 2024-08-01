import ssl

def secure_communication():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="path/to/certfile", keyfile="path/to/keyfile")
    context.verify_mode = ssl.CERT_REQUIRED
    return context
