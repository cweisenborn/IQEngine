from unittest import mock
from unittest.mock import AsyncMock

import numpy
import pytest
from app.models import DataSource
from azure.storage.blob import BlobProperties
from tests.test_data import test_datasource

test_binary = b"the quick brown fox jumps over the lazy dog"
test_blob_properties = BlobProperties()
test_blob_properties.size = 100


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_invalid_format(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with invalid format. Returns 400."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int16).tobytes()
    format = "invalid"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 400


async def mock_get_test_datasource():
    return DataSource(**test_datasource)


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_ci16_le(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with iq16_le. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int16).tobytes()
    format = "ci16_le"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_ci16(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with ci16. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int16).tobytes()
    format = "ci16"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_ci16_be(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with ci16_be. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int16).tobytes()
    format = "ci16_be"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_cf32_le(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with cf32_le. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.float32).tobytes()
    format = "cf32_le"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_cf32(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with cf32. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.float32).tobytes()
    format = "cf32"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_cf32_be(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with cf32_be. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.float32).tobytes()
    format = "cf32_be"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_ci8(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with ci8. Returns populated float of float array."""
    from app import datasources

    AsyncMock()
    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int8).tobytes()
    format = "ci8"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_i8(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with i8. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int8).tobytes()
    format = "i8"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format={format}&block_size=1&block_indexes_str=1&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=100)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_multiple_arr_elements_returns_data(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with i8. Returns populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int8).tobytes()
    input_arr_str = "1,3"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format=i8&block_size=1&block_indexes_str={input_arr_str}&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr + arr


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=2)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_offset_larger_than_blob_size(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with offset larger than blob size. Returns partially populated float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int8).tobytes()
    input_arr_str = "2"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format=i8&block_size=1&block_indexes_str={input_arr_str}&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == b""


@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=3)
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_iq_data_with_offset_plus_count_larger_than_blob_size(mock_decrypt, mock_get_file_length, client):
    """Get IQ data with offset plus count larger than blob size. Returns empty float of float array."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    arr = numpy.array([1, 2, 3, 4, 5, 6, 7, 8], dtype=numpy.int8).tobytes()

    input_arr_str = "1"
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/file_path/iq-data?format=i8&block_size=1&block_indexes_str={input_arr_str}&filepath=test"
        )
        assert response.status_code == 200
        assert response.content == arr


@mock.patch("app.iq_router.AzureBlobClient.blob_exist", return_value=False)
@mock.patch("app.iq_router.AzureBlobClient.can_write", return_value=False)
@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=20480)  # 5120 samples * 4 bytes per ci16_le sample
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_minimap_with_small_file(mock_decrypt, mock_get_file_length, mock_can_write, mock_blob_exist, client):
    """Test minimap generation with small file (5120 samples = 80 FFTs). Should use 80 FFTs instead of trying to get 200."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    
    # Create a small test file with 5120 samples (80 FFTs with fft_size=64)
    # ci16_le = 4 bytes per sample (2 bytes I + 2 bytes Q)
    arr = numpy.random.randint(-32768, 32767, size=5120 * 2, dtype=numpy.int16).tobytes()
    format = "ci16_le"
    
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/test_file/minimap-data?format={format}&filepath=test_file"
        )
        assert response.status_code == 200
        # The response should contain valid minimap data without errors


@mock.patch("app.iq_router.AzureBlobClient.blob_exist", return_value=False)
@mock.patch("app.iq_router.AzureBlobClient.can_write", return_value=False)
@mock.patch("app.iq_router.AzureBlobClient.get_file_length", return_value=819200)  # 102400 samples * 8 bytes per cf32_le sample
@mock.patch("app.iq_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_get_minimap_with_large_file(mock_decrypt, mock_get_file_length, mock_can_write, mock_blob_exist, client):
    """Test minimap generation with large file (102400 samples = 1600 FFTs). Should downsample to 200 FFTs."""
    from app import datasources

    client.app.dependency_overrides[datasources.get] = mock_get_test_datasource
    
    # Create a large test file with 102400 samples (1600 FFTs with fft_size=64)
    # cf32_le = 8 bytes per sample (4 bytes I + 4 bytes Q)
    arr = numpy.random.randn(102400 * 2).astype(numpy.float32).tobytes()
    format = "cf32_le"
    
    with mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=arr):
        response = client.get(
            f"/api/datasources/"
            f'{test_datasource["account"]}/{test_datasource["container"]}'
            f"/test_file/minimap-data?format={format}&filepath=test_file"
        )
        assert response.status_code == 200
        # The response should contain valid minimap data with downsampled FFTs
