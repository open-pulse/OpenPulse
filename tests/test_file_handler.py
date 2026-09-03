import pytest
import numpy as np
import warnings
import tempfile

from pathlib import Path
from unittest.mock import MagicMock, patch

from pulse.interface.user_input.data_handler.file_handlers.file_handler import FileHandler
from pulse.interface.user_input.data_handler.file_handlers.hdf5_file_handler import HDF5FileHandler
from pulse.interface.user_input.data_handler.file_handlers.spreadsheet_file_handler import SpreadsheetFileHandler
from pulse.interface.user_input.data_handler.file_handlers.text_file_handler import TextFileHandler
from pulse.interface.user_input.data_handler.imported_data import (
    SimulationData,
    TextData,
    SpreadsheetData,
)


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def sample_array():
    return np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])


@pytest.fixture
def temp_txt_file(sample_array):
    """Creates a temporary .txt file with numeric data."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        np.savetxt(f, sample_array, delimiter=",")
        return Path(f.name)


@pytest.fixture
def temp_csv_file(sample_array):
    """Creates a temporary .csv file with numeric data."""
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        np.savetxt(f, sample_array, delimiter=",")
        return Path(f.name)


# ==============================================================================
# 1. Routing by extension
# ==============================================================================

class TestReadRouting:
    """Ensures that read() delegates to the correct handler based on file extension."""

    @pytest.mark.parametrize("extension", TextFileHandler.EXTENSIONS)
    def test_routes_text_extensions_to_text_handler(self, extension):
        mock_result = MagicMock(spec=TextData)
        fake_path = Path(f"file{extension}")

        with patch.object(TextFileHandler, "read", return_value=mock_result) as mocked_read:
            result = FileHandler.read(fake_path)

        mocked_read.assert_called_once_with(fake_path)
        assert result is mock_result

    @pytest.mark.parametrize("extension", HDF5FileHandler.EXTENSIONS)
    def test_routes_hdf5_extensions_to_hdf5_handler(self, extension):
        mock_result = MagicMock(spec=SimulationData)
        fake_path = Path(f"file{extension}")

        with patch.object(HDF5FileHandler, "read", return_value=mock_result) as mocked_read:
            result = FileHandler.read(fake_path)

        mocked_read.assert_called_once_with(fake_path)
        assert result is mock_result

    @pytest.mark.parametrize("extension", SpreadsheetFileHandler.EXTENSIONS)
    def test_routes_spreadsheet_extensions_to_spreadsheet_handler(self, extension):
        mock_result = MagicMock(spec=SpreadsheetData)
        fake_path = Path(f"file{extension}")

        with patch.object(SpreadsheetFileHandler, "read", return_value=mock_result) as mocked_read:
            result = FileHandler.read(fake_path)

        mocked_read.assert_called_once_with(fake_path)
        assert result is mock_result

    def test_read_raises_value_error_for_unknown_extension(self):
        with pytest.raises(ValueError, match=r"Invalid suffix \.xyz"):
            FileHandler.read(Path("file.xyz"))


# ==============================================================================
# 2. Multiple files and empty input
# ==============================================================================

class TestReadMultipleFiles:
    """Ensures that read() handles lists of paths and empty selections."""

    def test_read_empty_string_returns_none(self):
        assert FileHandler.read("") is None

    def test_read_none_returns_none(self):
        assert FileHandler.read(None) is None

    def test_read_empty_list_returns_none(self):
        assert FileHandler.read([]) is None

    def test_read_list_returns_list_of_imported_data(self, temp_txt_file, temp_csv_file):
        result = FileHandler.read([temp_txt_file, temp_csv_file])

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, TextData) for item in result)

    def test_read_list_of_strings_returns_list_of_imported_data(self, temp_txt_file):
        result = FileHandler.read([str(temp_txt_file)])

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], TextData)

    def test_read_list_skips_handlers_returning_none(self, temp_txt_file):
        with patch.object(TextFileHandler, "read", return_value=None):
            assert FileHandler.read([temp_txt_file]) is None


# ==============================================================================
# 3. Save methods
# ==============================================================================

class TestSaveMethods:
    """Ensures that save_* methods forward all parameters correctly to their handlers."""

    def test_save_text_file_delegates_with_defaults(self, sample_array, tmp_path):
        output_path = tmp_path / "output.txt"

        with patch.object(TextFileHandler, "save") as mocked_save:
            FileHandler.save_text_file(output_path, sample_array)

        mocked_save.assert_called_once_with(
            output_path, sample_array, delimiter=",", header=""
        )

    def test_save_text_file_delegates_with_custom_params(self, sample_array, tmp_path):
        output_path = tmp_path / "output.txt"

        with patch.object(TextFileHandler, "save") as mocked_save:
            FileHandler.save_text_file(output_path, sample_array, delimiter=";", header="x,y")

        mocked_save.assert_called_once_with(
            output_path, sample_array, delimiter=";", header="x,y"
        )

    def test_save_text_file_accepts_string_path(self, sample_array, tmp_path):
        output_path = tmp_path / "output.txt"

        with patch.object(TextFileHandler, "save") as mocked_save:
            FileHandler.save_text_file(str(output_path), sample_array)

        mocked_save.assert_called_once_with(
            output_path, sample_array, delimiter=",", header=""
        )

    def test_save_text_file_raises_for_invalid_extension(self, sample_array, tmp_path):
        with pytest.raises(ValueError, match=r"Invalid suffix \.xlsx"):
            FileHandler.save_text_file(tmp_path / "output.xlsx", sample_array)

    def test_save_spreadsheet_file_delegates_correctly(self, tmp_path):
        mock_df = MagicMock()
        output_path = tmp_path / "output.xlsx"

        with patch.object(SpreadsheetFileHandler, "save") as mocked_save:
            FileHandler.save_spreadsheet_file(output_path, "Sheet1", mock_df, index_rows=True, append=True)

        mocked_save.assert_called_once_with(output_path, "Sheet1", mock_df, True, True)

    def test_save_spreadsheet_file_uses_defaults(self, tmp_path):
        mock_df = MagicMock()
        output_path = tmp_path / "output.xlsx"

        with patch.object(SpreadsheetFileHandler, "save") as mocked_save:
            FileHandler.save_spreadsheet_file(output_path, "Sheet1", mock_df)

        mocked_save.assert_called_once_with(output_path, "Sheet1", mock_df, False, False)

    def test_save_spreadsheet_file_raises_for_invalid_extension(self, tmp_path):
        with pytest.raises(ValueError, match=r"Invalid suffix \.txt"):
            FileHandler.save_spreadsheet_file(tmp_path / "output.txt", "Sheet1", MagicMock())


# ==============================================================================
# 4. Error message helpers
# ==============================================================================

class TestExtensionsErrorMessage:
    """Ensures the extension list is rendered in a readable way."""

    def test_empty_extensions_returns_empty_string(self):
        assert FileHandler.generate_extensions_string_for_error_message([]) == ""

    def test_single_extension_returns_itself(self):
        assert FileHandler.generate_extensions_string_for_error_message([".txt"]) == ".txt"

    def test_two_extensions_are_joined_with_or(self):
        result = FileHandler.generate_extensions_string_for_error_message([".txt", ".csv"])
        assert result == ".txt or .csv"

    def test_many_extensions_are_comma_separated_with_final_or(self):
        result = FileHandler.generate_extensions_string_for_error_message([".txt", ".dat", ".csv"])
        assert result == ".txt, .dat or .csv"

    def test_raise_extensions_error_lists_accepted_extensions(self):
        with pytest.raises(ValueError, match=r"Invalid suffix \.xyz\. Use \.txt or \.csv"):
            FileHandler.raise_extensions_error(Path("file.xyz"), [".txt", ".csv"])


# ==============================================================================
# 5. Integration tests with real files (text files)
# ==============================================================================

class TestIntegrationTextFile:
    """Integration tests reading real files from disk."""

    def test_read_txt_returns_text_data(self, temp_txt_file):
        result = FileHandler.read(temp_txt_file)
        assert isinstance(result, TextData)

    def test_read_csv_returns_text_data(self, temp_csv_file):
        result = FileHandler.read(temp_csv_file)
        assert isinstance(result, TextData)

    def test_read_txt_data_matches_original(self, temp_txt_file, sample_array):
        result = FileHandler.read(temp_txt_file)
        np.testing.assert_array_almost_equal(result.data, sample_array)

    def test_save_and_read_roundtrip(self, sample_array, tmp_path):
        path = tmp_path / "roundtrip.txt"

        FileHandler.save_text_file(path, sample_array)
        result = FileHandler.read(path)

        np.testing.assert_array_almost_equal(result.data, sample_array)

    def test_read_txt_with_header_ignores_header(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
            f.write("# freq, amplitude\n")
            f.write("1.0, 2.0\n")
            f.write("3.0, 4.0\n")
            path = Path(f.name)

        result = FileHandler.read(path)
        assert result.data.shape == (2, 2)

    def test_read_txt_file_sets_correct_name(self, temp_txt_file):
        result = FileHandler.read(temp_txt_file)
        assert result.filename == temp_txt_file.name

    def test_read_txt_file_sets_path_and_extension(self, temp_txt_file):
        result = FileHandler.read(temp_txt_file)
        assert result.path == temp_txt_file
        assert result.extension == ".txt"


# ==============================================================================
# 6. Edge cases and errors
# ==============================================================================

class TestEdgeCases:
    """Tests boundary behaviors and error handling."""

    def test_read_accepts_string_path(self, temp_txt_file):
        result = FileHandler.read(str(temp_txt_file))
        assert isinstance(result, TextData)

    def test_read_accepts_path_object(self, temp_txt_file):
        result = FileHandler.read(Path(temp_txt_file))
        assert isinstance(result, TextData)

    def test_save_text_to_nonexistent_directory_raises(self, sample_array, tmp_path):
        with pytest.raises(FileNotFoundError):
            FileHandler.save_text_file(tmp_path / "missing" / "output.txt", sample_array)

    def test_save_spreadsheet_to_nonexistent_directory_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            FileHandler.save_spreadsheet_file(tmp_path / "missing" / "output.xlsx", "Sheet1", MagicMock())

    def test_read_txt_empty_file_returns_empty_data(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
            path = Path(f.name)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            result = FileHandler.read(path)

        assert isinstance(result, TextData)
        assert result.data.size == 0
