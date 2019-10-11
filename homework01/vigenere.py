def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """

    # PUT YOUR CODE HERE
    ciphertext = ''
    keyword_len = len(keyword)
    for i, letter in enumerate(plaintext):
        # Adds cycling abillity
        key_id = keyword[i % keyword_len]
        if 'a' <= key_id <= 'z':
            key = ord(key_id) - 97
        elif 'A' <= key_id <= 'Z':
            key = ord(key_id) - 65
        else:
            key = ord(key_id)

        new_letter = ''
        if 'a' <= letter <= 'z':
            new_letter = chr((ord(letter) + key - 97) % 26 + 97)
        elif 'A' <= letter <= 'Z':
            new_letter = chr((ord(letter) + key - 65) % 26 + 65)
        else:
            new_letter = letter
        ciphertext = ciphertext + new_letter

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    plaintext = ''
    keyword_len = len(keyword)
    for i, letter in enumerate(ciphertext):
        # Adds cycling abillity
        key_id = keyword[i % keyword_len]
        if 'a' <= key_id <= 'z':
            key = ord(key_id) - 97
        elif 'A' <= key_id <= 'Z':
            key = ord(key_id) - 65
        else:
            key = ord(key_id)

        new_letter = ''
        if 'a' <= letter <= 'z':
            new_letter = chr((ord(letter) - key - 97) % 26 + 97)
        elif 'A' <= letter <= 'Z':
            new_letter = chr((ord(letter) - key - 65) % 26 + 65)
        else:
            new_letter = letter
        plaintext = plaintext + new_letter

    return plaintext