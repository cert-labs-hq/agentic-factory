from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

class SliceValidator:
    """
    Validates individual slice JSON files against the master schema contract.
    """
    def __init__(self, schema_path: Path):
        """
        Initializes the validator with the path to the master schema.
        
        :param schema_path: Path to .factory/contracts/schema_file.json
        """
        pass

    def validate(self, slice_data: Dict[str, Any]) -> bool:
        """
        Validates the provided slice data against the schema.
        
        :param slice_data: Dictionary containing slice metadata.
        :return: True if valid, False otherwise.
        """
        pass

class RegistryAggregator:
    """
    Scans the slices directory and aggregates metadata into a unified registry structure.
    """
    def __init__(self, slices_dir: Path, validator: SliceValidator):
        """
        Initializes the aggregator with the source directory and a validator.
        
        :param slices_dir: Path to .factory/slices/
        :param validator: An instance of SliceValidator to ensure data integrity.
        """
        pass

    def discover_slices(self) -> List[Path]:
        """
        Scans the slices directory for valid JSON files matching the [A-Z]{3}-[0-9]{3} pattern.
        
        :return: List of Paths to discovered slice files.
        """
        pass

    def aggregate(self) -> Dict[str, Any]:
        """
        Reads discovered slices, validates them, and produces the aggregated registry object.
        Includes global metrics like status counts and total token investment.
        
        :return: The complete registry dictionary, ready for serialization.
        """
        pass

class RegistryWriter:
    """
    Handles the serialization and validation of the final index.json registry file.
    """
    def __init__(self, output_path: Path, aggregate_schema_path: Path):
        """
        Initializes the writer with the destination and the aggregate contract path.
        
        :param output_path: Path to .factory/index.json
        :param aggregate_schema_path: Path to .factory/contracts/aggregate_slice_info.json
        """
        pass

    def write(self, registry_data: Dict[str, Any]) -> None:
        """
        Serializes the registry data to JSON and writes it to the output path.
        Also validates the final file against the aggregate schema.
        
        :param registry_data: The aggregated registry dictionary.
        """
        pass
