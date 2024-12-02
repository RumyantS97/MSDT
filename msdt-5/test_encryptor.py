import pytest
from unittest.mock import mock_open, patch
from src.encryptor import shift_encrypt, encrypt_file

# Тесты для функции shift_encrypt

def test_shift_encrypt_empty_string():
    assert shift_encrypt("") == "", "Should return an empty string for empty input"

def test_shift_encrypt_single_character():
    assert shift_encrypt("a") == "b", "Failed to encrypt a single character"

def test_shift_encrypt_multiple_characters():
    assert shift_encrypt("abc") == "bcd", "Failed for a sequence of characters"

@pytest.mark.parametrize("input_text, expected_output", [
    ("xyz", "yza"),
    ("123", "234"),
    ("!\"#", "\"$%"),
    ("Hello, World!", "Ifmmp-!Xpsme\"")
])
def test_shift_encrypt_parameterized(input_text, expected_output):
    assert shift_encrypt(input_text) == expected_output

# Тесты для функции encrypt_file с использованием моков

@pytest.mark.parametrize("file_content, encrypted_content", [
    ("hello", "ifmmp"),
    ("test", "uftu"),
    ("Python", "Qzuipo")
])
def test_encrypt_file_mock(file_content, encrypted_content):
    m = mock_open(read_data=file_content)
    with patch("builtins.open", m):
        encrypt_file("dummy_input_path", "dummy_output_path")
        m.assert_called_once_with("dummy_input_path", 'r', encoding='utf-8')
        handle = m()
        handle.write.assert_called_once_with(encrypted_content)

# Тест с использованием временных файлов

@pytest.mark.parametrize("original, encrypted", [
    ("data.txt", "data_encrypted.txt")
])
def test_encrypt_file_system(original, encrypted, tmpdir):
    original_path = tmpdir.join(original)
    encrypted_path = tmpdir.join(encrypted)
    
    original_path.write("hello")
    
    encrypt_file(str(original_path), str(encrypted_path))
    
    assert encrypted_path.read() == "ifmmp"

# Тесты для краевых случаев

def test_shift_encrypt_non_printable_characters():
    assert shift_encrypt("\n\t") == "\x0b\x0c", "Failed to encrypt non-printable characters"

def test_shift_encrypt_full_ascii_range():
    all_chars = ''.join(chr(i) for i in range(32, 127))
    shifted_chars = ''.join(chr(i + 1) for i in range(32, 127))
    assert shift_encrypt(all_chars) == shifted_chars, "Failed to shift full ASCII range correctly"
