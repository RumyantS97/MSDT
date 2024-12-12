import pytest
from unittest.mock import patch, mock_open
from text_aligner import align_text_right

# Простые тесты
def test_align_text_right_simple_case(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    line = "a"
    input_file.write_text(line, encoding='utf-8')
    align_text_right(str(input_file), str(output_file), 10)
    assert output_file.read_text(encoding='utf-8') == f"{line:>10}"

def test_align_text_right_empty_file(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("", encoding='utf-8')

    with pytest.raises(SystemExit):
        align_text_right(str(input_file), str(output_file), 10)

def test_align_text_right_lines(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"
    line = "This is a long\n line that exceeds the limit"
    input_file.write_text(line, encoding='utf-8')
    align_text_right(str(input_file), str(output_file), 10)
    assert output_file.read_text(encoding='utf-8') == (
        f"This is a \n line that"
    )

def test_align_text_right_file_not_found():
    with pytest.raises(SystemExit):
        align_text_right("non_existent_file.txt", "output.txt", 10)

def test_align_text_right_invalid_max_width(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("Some text", encoding='utf-8')
    with pytest.raises(ValueError):
        align_text_right(str(input_file), str(output_file), -5)

# Сложные тесты
@pytest.mark.parametrize("max_width,expected_output", [
    (5, "Hello\nWorld"),
    (10, "     Hello\n     World"),
    (15, "          Hello\n          World"),
])
def test_align_text_right_with_different_widths(tmp_path, max_width, expected_output):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_file.write_text("Hello\nWorld", encoding='utf-8')
    align_text_right(str(input_file), str(output_file), max_width)
    assert output_file.read_text(encoding='utf-8') == expected_output

def test_align_text_right_mocked_io():
    input_content = "Line1\nLine2\nLine3"
    expected_output = "  Line1\n  Line2\n  Line3"

    with patch("builtins.open", mock_open(read_data=input_content)) as mock_file:
        with patch("sys.stdout.write") as mock_stdout:
            align_text_right("input.txt", "output.txt", 7)

            mock_stdout.assert_any_call("  Line1")
            mock_stdout.assert_any_call("  Line2")
            mock_stdout.assert_any_call("  Line3")
            mock_stdout.assert_any_call("\n")

            mock_file().write.assert_called_once_with(expected_output.replace("\n", "\n"))
            assert mock_stdout.call_count == 10
            assert mock_file().write.call_count == 1 


