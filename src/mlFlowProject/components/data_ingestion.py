import os
import urllib.request as request
import zipfile
from mlFlowProject import logger
from mlFlowProject.utils.common import get_size
from pathlib import Path
from mlFlowProject.entity.config_entity import DataIngestionConfig
import requests


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            # Construct the appropriate URL if the file is hosted on Google Drive
            url = self.config.source_URL
            
            # Extract file ID based on the URL format
            file_id = self._extract_file_id(url)
            
            if file_id:
                gdrive_url = f'https://drive.google.com/uc?id={file_id}&export=download'
                self._download_from_gdrive(gdrive_url)
            else:
                logger.error("Unable to extract file ID from the provided URL.")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def _extract_file_id(self, url: str) -> str:
        """Extract the file ID from a Google Drive URL."""
        if '/d/' in url:
            try:
                file_id = url.split('/d/')[1].split('/')[0]  # Extract file ID
                logger.info(f"Extracted file ID: {file_id}")
                return file_id
            except IndexError:
                logger.error("Invalid URL format: Unable to extract file ID.")
                return None
        elif 'uc?id=' in url:
            # This is a direct download link, so extract the ID directly
            file_id = url.split('uc?id=')[1].split('&')[0]
            logger.info(f"Extracted file ID: {file_id}")
            return file_id
        else:
            logger.error("URL does not contain a valid Google Drive file ID.")
            return None

    def _download_from_gdrive(self, gdrive_url: str):
        """Download file from Google Drive using the constructed URL."""
        try:
            # Download the file from Google Drive
            response = requests.get(gdrive_url)
            response.raise_for_status()  # Check if the request was successful

            with open(self.config.local_data_file, 'wb') as f:
                f.write(response.content)
            logger.info(f"File downloaded successfully: {self.config.local_data_file}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download the file from Google Drive: {e}")

    def extract_zip_file(self):
        """
        Check if the file is a zip file and extract it.
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)

        # Check if the file is a zip file
        if self.config.local_data_file.endswith('.zip'):
            try:
                with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                    zip_ref.extractall(unzip_path)
                logger.info(f"Extracted zip file to: {unzip_path}")
            except zipfile.BadZipFile:
                logger.error(f"File {self.config.local_data_file} is not a valid zip file.")
        else:
            logger.error(f"File {self.config.local_data_file} is not a valid zip file.")
