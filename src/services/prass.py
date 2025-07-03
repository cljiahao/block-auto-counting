from pathlib import Path
import urllib.parse

from core.config import service_settings
from core.exceptions import NoResultsFound
from core.logging import logger
from services.base import APIClient
from utils.debug import error_handler

API_PRASS_ITEM_ENDPOINT = "/data"


@error_handler()
def check_lot(lot_no: str) -> tuple[str, str]:
    """Check if Lot Number input exists in PRASS database"""
    if lot_no.lower() == service_settings.TEST_LOT_NO:
        return service_settings.TEST_ITEM, "100000"

    if not service_settings.PRASS_URL:
        raise NoResultsFound(f"PRASS URL is not configured.")

    api_client = APIClient(service_settings.PRASS_URL)
    search_params = urllib.parse.urlencode({"lotNo": lot_no})
    prass_data = api_client.get(f"{API_PRASS_ITEM_ENDPOINT}?{search_params}")

    if not isinstance(prass_data, dict):
        raise NoResultsFound(f"Lot number: {lot_no} not found in PRASS Server.")

    input_qty = prass_data[service_settings.QUANTITY_COLUMN]
    item = prass_data[service_settings.ITEM_COLUMN]
    logger.debug(f"Lot : {lot_no} - Item : {item} with Input Quantity : {input_qty}")

    return item, input_qty


@error_handler()
def send_prass_file_server(prass_txt_path: Path):
    if not prass_txt_path.exists():
        raise FileNotFoundError(f"Label file not found: {prass_txt_path}")

    file_path_list: dict[str, Path] = {
        "file": prass_txt_path,
    }

    api_client = APIClient(service_settings.FILE_SERVER)
    result = api_client.post_files("", file_path_list=file_path_list)

    logger.info(
        f"Successfully posted model files ({prass_txt_path}) to {service_settings.FILE_SERVER}"
    )

    return result
