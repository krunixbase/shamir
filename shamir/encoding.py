import base64


def encode_share(share):
    x, y = share
    payload = f"{x}:{y}".encode("utf-8")
    return base64.urlsafe_b64encode(payload).decode("ascii")


def decode_share(encoded_share):
    payload = base64.urlsafe_b64decode(encoded_share.encode("ascii"))
    x_str, y_str = payload.decode("utf-8").split(":")
    return int(x_str), int(y_str)


def encode_shares(shares):
    return [encode_share(share) for share in shares]


def decode_shares(encoded_shares):
    return [decode_share(share) for share in encoded_shares]

