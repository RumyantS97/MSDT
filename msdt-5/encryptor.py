def shift_encrypt(text):
    """Encrypts the text by shifting each character by one in the ASCII table."""
    encrypted_text = ''.join(chr(ord(char) + 1) for char in text)
    return encrypted_text

def encrypt_file(input_filepath, output_filepath):
    """Reads a file, encrypts its content and writes the result to another file."""
    with open(input_filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    encrypted_content = shift_encrypt(content)
    
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(encrypted_content)
