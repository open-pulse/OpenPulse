import pytest
import numpy as np
import warnings
import tempfile

from pathlib import Path
from unittest.mock import MagicMock, patch

from pulse.interface.user_input.data_handler.file_handlers.file_handler import FileHandler
from pulse.interface.user_input.data_handler.imported_data import (
    SimulationData,
    TextData,
    SpreadsheetData,
)


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def file_handler():
    return FileHandler()


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

    @pytest.mark.parametrize("extension", [".txt", ".dat", ".csv"])
    def test_routes_text_extensions_to_text_handler(self, file_handler, extension):
        mock_result = MagicMock(spec=TextData)
        file_handler._text_file_handler.read = MagicMock(return_value=mock_result)

        fake_path = Path(f"file{extension}")

        with patch.object(Path, "suffix", new_callable=lambda: property(lambda self: extension)):
            result = file_handler.read(fake_path)

        file_handler._text_file_handler.read.assert_called_once()
        assert result is mock_result

    @pytest.mark.parametrize("extension", [".h5", ".hdf5"])
    def test_routes_hdf5_extensions_to_hdf5_handler(self, file_handler, extension):
        mock_result = MagicMock(spec=SimulationData)
        file_handler._hdf5_file_handler.read = MagicMock(return_value=mock_result)

        fake_path = Path(f"file{extension}")

        with patch.object(Path, "suffix", new_callable=lambda: property(lambda self: extension)):
            result = file_handler.read(fake_path)

        file_handler._hdf5_file_handler.read.assert_called_once()
        assert result is mock_result

    @pytest.mark.parametrize("extension", [".xls", ".xlsx"])
    def test_routes_spreadsheet_extensions_to_spreadsheet_handler(self, file_handler, extension):
        mock_result = MagicMock(spec=SpreadsheetData)
        file_handler._spreadsheet_file_handler.read = MagicMock(return_value=mock_result)

        fake_path = Path(f"file{extension}")

        with patch.object(Path, "suffix", new_callable=lambda: property(lambda self: extension)):
            result = file_handler.read(fake_path)

        file_handler._spreadsheet_file_handler.read.assert_called_once()
        assert result is mock_result

    def test_read_raises_value_error_for_unknown_extension(self, file_handler):
        with pytest.raises(ValueError, match=r"Invalid suffix \.xyz"):
            file_handler.read(Path("file.xyz"))


# ==============================================================================
# 2. Save methods
# ==============================================================================

class TestSaveMethods:
    """Ensures that save_* methods forward all parameters correctly to their handlers."""

    def test_save_text_file_delegates_with_defaults(self, file_handler, sample_array, tmp_path):
        file_handler._text_file_handler.save = MagicMock()
        output_path = tmp_path / "output.txt"

        file_handler.save_text_file(output_path, sample_array)

        file_handler._text_file_handler.save.assert_called_once_with(
            output_path, sample_array, delimiter=",", header=""
        )

    def test_save_text_file_delegates_with_custom_params(self, file_handler, sample_array, tmp_path):
        file_handler._text_file_handler.save = MagicMock()
        output_path = tmp_path / "output.txt"

        file_handler.save_text_file(output_path, sample_array, delimiter=";", header="x,y")

        file_handler._text_file_handler.save.assert_called_once_with(
            output_path, sample_array, delimiter=";", header="x,y"
        )

    def test_save_spreadsheet_file_delegates_correctly(self, file_handler, tmp_path):
        mock_df = MagicMock()
        file_handler._spreadsheet_file_handler.save = MagicMock()
        output_path = tmp_path / "output.xlsx"

        file_handler.save_spreadsheet_file(output_path, "Sheet1", mock_df, index_rows=True)

        file_handler._spreadsheet_file_handler.save.assert_called_once_with(
            output_path, "Sheet1", mock_df, True
        )

    def test_save_spreadsheet_file_default_index_rows(self, file_handler, tmp_path):
        mock_df = MagicMock()
        file_handler._spreadsheet_file_handler.save = MagicMock()
        output_path = tmp_path / "output.xlsx"

        file_handler.save_spreadsheet_file(output_path, "Sheet1", mock_df)

        file_handler._spreadsheet_file_handler.save.assert_called_once_with(
            output_path, "Sheet1", mock_df, False
        )


# ==============================================================================
# 3. Integration tests with real files (text files)
# ==============================================================================

class TestIntegrationTextFile:
    """Integration tests reading real files from disk."""

    def test_read_txt_returns_text_data(self, file_handler, temp_txt_file):
        result = file_handler.read(temp_txt_file)
        assert isinstance(result, TextData)

    def test_read_csv_returns_text_data(self, file_handler, temp_csv_file):
        result = file_handler.read(temp_csv_file)
        assert isinstance(result, TextData)

    def test_read_txt_data_matches_original(self, file_handler, temp_txt_file, sample_array):
        result = file_handler.read(temp_txt_file)
        np.testing.assert_array_almost_equal(result.data, sample_array)

    def test_save_and_read_roundtrip(self, file_handler, sample_array, tmp_path):
        path = tmp_path / "roundtrip.txt"

        file_handler.save_text_file(path, sample_array)
        result = file_handler.read(path)

        np.testing.assert_array_almost_equal(result.data, sample_array)

    def test_read_txt_with_header_ignores_header(self, file_handler):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
            f.write("# freq, amplitude\n")
            f.write("1.0, 2.0\n")
            f.write("3.0, 4.0\n")
            path = Path(f.name)

        result = file_handler.read(path)
        assert result.data.shape == (2, 2)

    def test_read_txt_file_sets_correct_name(self, file_handler, temp_txt_file):
        result = file_handler.read(temp_txt_file)
        assert result.filename == temp_txt_file.stem


# ==============================================================================
# 4. Edge cases and errors
# ==============================================================================

class TestEdgeCases:
    """Tests boundary behaviors and error handling."""

    def test_read_accepts_string_path(self, file_handler, temp_txt_file):
        result = file_handler.read(str(temp_txt_file))
        assert isinstance(result, TextData)

    def test_read_accepts_path_object(self, file_handler, temp_txt_file):
        result = file_handler.read(Path(temp_txt_file))
        assert isinstance(result, TextData)

    def test_save_text_to_nonexistent_directory_raises(self, file_handler, sample_array):
        with pytest.raises(FileNotFoundError):
            file_handler.save_text_file("/does/not/exist/output.txt", sample_array)

    def test_read_txt_empty_file_returns_empty_data(self, file_handler):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
            path = Path(f.name)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            result = file_handler.read(path)

        assert isinstance(result, TextData)
        assert result.data.size == 0