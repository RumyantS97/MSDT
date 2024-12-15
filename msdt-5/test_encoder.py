import os
import pytest
from unittest.mock import mock_open, patch
from encoder import FileManager

# Тесты для проверки шифрования сообщения

def test_text_encryption_pass():
    assert FileManager().Vigenere_Encrypt(
        "a text message to check the operability of the method",
        "unittest"
    ) == "u bxqx fyfatzi mi kaxgc num htwkuoqebxq is mai fygphw"


@pytest.mark.xfail()
def test_text_encryption_error():
    assert FileManager().Vigenere_Encrypt(
        "creating an error",
        "password"
    ) == "creating an error"


# Тесты на проверку чтения файла

def test_read_file_pass():
    assert FileManager().Read_File(
        "input.txt",
        "unittest"
    ) == "u bxqx fyfatzi mi kaxgc num htwkuoqebxq is mai fygphw"

def test_catch_exception():
    with pytest.raises(Exception) as e:
        FileManager().Read_File( "crack.txt", "crack" )
    assert str(e.value) == "No such file or directory"


# Тест с параметром
@pytest.mark.parametrize( 'text, keyword, result',
                         [ ( "the weather is so good outside today", "december", "wlg ifekkit ut jr isae fxxumpf krhcc" ),
                           ( "text for the test with parameters", "sunday", "lykw dgl whc nrvt ocgk nslnperwlf" ) ] )
def test_with_parameters(text, keyword, result):
    assert FileManager().Vigenere_Encrypt(text, keyword) == result


# Имитирование записи
@pytest.fixture
def mock_file():
    m = mock_open()
    with patch("builtins.open", m):
        yield m

# Использование моков
def test_write_file_with_mocks(mock_file):
    file_manager = FileManager()
    text_to_write = "EncryptedText"
    # Вызываем метод для записи файла
    file_manager.Write_File("dummy_output.txt", text_to_write)
    # Проверка правильности аргументов
    mock_file.assert_called_once_with("dummy_output.txt", 'w')
    # Проверка правльное записи
    mock_file().write.assert_called_once_with(text_to_write)


# Использование стабов
@patch( "builtins.open", new_callable = mock_open )
def test_write_file_with_stubs(mock_file):
    file_manager = FileManager()
    text_to_write = "EncryptedText"
    file_manager.Write_File( "dummy_output.txt", text_to_write )
    # проверка открытия
    mock_file.assert_called_once_with( "dummy_output.txt", 'w' )
    # проверка записи
    mock_file().write.assert_called_once_with(text_to_write)


# Тест на удаление файла
def test_delete_file_not_found():
    with pytest.raises(Exception) as e:
        FileManager().Read_File( "crack.txt", "crack" )
    assert str(e.value) == "No such file or directory"
