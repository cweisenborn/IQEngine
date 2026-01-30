from unittest import mock
from unittest.mock import Mock

import pytest
from app import datasources
from app.models import DataSource
from tests.test_data import test_datasource, valid_metadata


def override_dependency_datasources_get():
    return DataSource(**test_datasource)


@mock.patch("app.datasources_router.AzureBlobClient.blob_exist", return_value=True)
@mock.patch("app.datasources_router.AzureBlobClient.get_blob_content", return_value=b"<image data>")
@mock.patch(
    "app.metadata.get_metadata",
    return_value=valid_metadata,
)
@mock.patch("app.datasources_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_api_get_thumbnail_with_image(
    mock_decrypt: Mock,
    mock_get_metadata: Mock,
    mock_get_blob_content: Mock,
    mock_blob_exist: Mock,
    client,
):
    client.app.dependency_overrides[datasources.get] = override_dependency_datasources_get

    response = client.get(f'/api/datasources/{test_datasource["account"]}/{test_datasource["container"]}/file_path.jpg')
    assert response.status_code == 200
    mock_get_metadata.assert_not_called()
    mock_get_blob_content.assert_called_once()
    mock_blob_exist.assert_called_once()
    mock_decrypt.mock_calls == 2


@mock.patch("app.azure_client.AzureBlobClient.get_file_length", return_value=20480)  # 5120 samples * 4 bytes for ci16_le
@mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=b"<small file content>")
@pytest.mark.asyncio
async def test_get_new_thumbnail_with_small_file(mock_get_blob_content: Mock, mock_get_file_length: Mock):
    """Test thumbnail generation with small file (5120 samples = 20480 bytes for ci16_le)."""
    from app.azure_client import AzureBlobClient

    client = AzureBlobClient(account="test", container="test", awsAccessKeyId=None)
    
    # Mock get_spectrogram_image to avoid actual image generation in test
    with mock.patch("app.azure_client.get_spectrogram_image", return_value=b"<thumbnail>") as mock_spectrogram:
        result = await client.get_new_thumbnail(data_type="ci16_le", filepath="test.sigmf-meta")
        
        # Verify get_file_length was called
        mock_get_file_length.assert_called_once()
        
        # Verify get_blob_content was called with adjusted parameters
        # For a 20480 byte file, skip_bytes should be 0 (since 256000 > 20480)
        # and read_length should be 20480 (min of 512*1024 and 20480)
        mock_get_blob_content.assert_called_once()
        call_args = mock_get_blob_content.call_args
        assert call_args[0][1] == 0  # skip_bytes should be 0 for small file
        assert call_args[0][2] == 20480  # read_length should be entire file
        
        # Verify spectrogram generation was called
        mock_spectrogram.assert_called_once()
        assert result == b"<thumbnail>"


@mock.patch("app.azure_client.AzureBlobClient.get_file_length", return_value=1000000)  # Large file (1MB)
@mock.patch("app.azure_client.AzureBlobClient.get_blob_content", return_value=b"<large file content>")
@pytest.mark.asyncio
async def test_get_new_thumbnail_with_large_file(mock_get_blob_content: Mock, mock_get_file_length: Mock):
    """Test thumbnail generation with large file maintains original behavior."""
    from app.azure_client import AzureBlobClient

    client = AzureBlobClient(account="test", container="test", awsAccessKeyId=None)
    
    # Mock get_spectrogram_image to avoid actual image generation in test
    with mock.patch("app.azure_client.get_spectrogram_image", return_value=b"<thumbnail>") as mock_spectrogram:
        result = await client.get_new_thumbnail(data_type="cf32_le", filepath="test.sigmf-meta")
        
        # Verify get_file_length was called
        mock_get_file_length.assert_called_once()
        
        # Verify get_blob_content was called with original parameters
        # For a 1MB file, skip_bytes should still be 256000
        # and read_length should be min(512*1024, 1000000-256000) = 524288
        mock_get_blob_content.assert_called_once()
        call_args = mock_get_blob_content.call_args
        assert call_args[0][1] == 256000  # skip_bytes should be original value
        assert call_args[0][2] == 524288  # read_length should be 512*1024
        
        # Verify spectrogram generation was called
        mock_spectrogram.assert_called_once()
        assert result == b"<thumbnail>"


""" stopped working while doing a refactor but cant figure out why
@mock.patch("app.datasources_router.AzureBlobClient.blob_exist", return_value=False)
@mock.patch(
    "app.metadata.get_metadata",
    return_value=Metadata(**valid_metadata),
)
@mock.patch(
    "app.azure_client.AzureBlobClient.get_new_thumbnail",
    return_value=b"<thumbnail data>",
)
@mock.patch("app.datasources_router.AzureBlobClient.upload_blob", return_value=None)
@mock.patch("app.datasources_router.decrypt", return_value="secret")
@pytest.mark.asyncio
async def test_api_get_thumbnail_with_no_image(
    mock_decrypt: Mock,
    mock_upload_blob: Mock,
    mock_get_new_thumbnail: Mock,
    mock_get_metadata: Mock,
    mock_blob_exist: Mock,
    client,
):
    client.app.dependency_overrides[
        datasources.get
    ] = override_dependency_datasources_get
    response = client.get(
        f'/api/datasources/{test_datasource["account"]}/{test_datasource["container"]}/file_path.jpg'
    )
    assert response.status_code == 200
    mock_get_metadata.assert_called_once()
    mock_get_new_thumbnail.assert_called_once()
    mock_upload_blob.assert_called_once()
    mock_blob_exist.assert_called_once()
    mock_decrypt.mock_calls == 2
"""
