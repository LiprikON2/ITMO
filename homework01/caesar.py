def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """

    # PUT YOUR CODE HERE
    ciphertext = ''
    for letter in plaintext:
        new_letter = ''
        if 'a' <= letter <= 'z':
            new_letter = chr((ord(letter) + 3 - 97) % 26 + 97)
        elif 'A' <= letter <= 'Z':
            new_letter = chr((ord(letter) + 3 - 65) % 26 + 65)
        else:
            new_letter = letter
        ciphertext = ciphertext + new_letter

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """

    # PUT YOUR CODE HERE
    plaintext = ''
    for letter in ciphertext:
        new_letter = ''
        if 'a' <= letter <= 'z':
            new_letter = chr((ord(letter) - 3 - 97) % 26 + 97)
        elif 'A' <= letter <= 'Z':
            new_letter = chr((ord(letter) - 3 - 65) % 26 + 65)
        else:
            new_letter = letter
        plaintext = plaintext + new_letter

    return plaintext