import hashlib


def sha3_224(string: str) -> str:
    """
    Returns a SHA 3-224 encrypted string

    Usage:
     out = sha3_224("spam")

     print(out)

     # e9346410b094e8bf214233c23fa0a37cb6fe19fc1ae9a9dc4e932bf9
    """
    method = hashlib.sha3_224()
    method.update(string.encode("utf-8"))
    output = method.hexdigest()
    return output


def sha3_256(string: str) -> str:
    """
    Returns a SHA 3-256 encrypted string

    Usage:
     out = sha3_256("spam")

     print(out)

     # 4790d2f7d40398ef18d0a958faab5817b02c451fa20d4ae07d578b6ef24d24cc
    """
    method = hashlib.sha3_256()
    method.update(string.encode("utf-8"))
    output = method.hexdigest()
    return output


def sha3_384(string: str) -> str:
    """
    Returns a SHA 3-384 encrypted string

    Usage:
     out = sha3_384("spam")

     print(out)

     # be6120dc6799da3e69db0e1ea16e22359815abf07a30155472292d550a08abbce96cbd6570aaa4742ccb9f1c3692015a
    """
    method = hashlib.sha3_384()
    method.update(string.encode("utf-8"))
    output = method.hexdigest()
    return output


def sha3_512(string: str) -> str:
    """
    Returns a SHA 3-512 encrypted string

    Usage:
     out = sha3_512("spam")

     print(out)

     # e147ae894d01af80cad59c62264ee10758ac6239fabcfc0e1ebe4cd3221c5bdbbfd23277b08798aa7a8397011c5352a0e3fed7d59f92fade9f586c1fd0e45714
    """
    method = hashlib.sha3_512()
    method.update(string.encode("utf-8"))
    output = method.hexdigest()
    return output
