"""General SDMX utilities for ECB connector with streaming XML parsing"""
import xml.etree.ElementTree as ET
import pandas as pd
import pyarrow as pa
from typing import Dict, Any, Optional, Iterator
from pathlib import Path
import json
from utils import get
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from io import BytesIO
import httpx

# Custom exception for rate limiting
class RateLimitError(Exception):
    pass

# Load codelists and structures once at module level
_CODELISTS = None
_STRUCTURES = None

def _load_metadata():
    """Load codelists and structures from cached files"""
    global _CODELISTS, _STRUCTURES
    
    if _CODELISTS is None:
        codelist_file = Path(__file__).parent / "defs" / "codelists.json"
        if codelist_file.exists():
            with open(codelist_file, 'r') as f:
                _CODELISTS = json.load(f)
        else:
            _CODELISTS = {}
    
    if _STRUCTURES is None:
        structures_file = Path(__file__).parent / "defs" / "structures.json"
        if structures_file.exists():
            with open(structures_file, 'r') as f:
                _STRUCTURES = json.load(f)
        else:
            _STRUCTURES = {}

# Load metadata on import
_load_metadata()

def get_structure_key(dataflow_id: str) -> Optional[str]:
    """Find the structure key for a given dataflow"""
    # Load dataflows to map dataflow_id to structure
    dataflows_file = Path(__file__).parent / "defs" / "dataflows.json"
    if dataflows_file.exists():
        with open(dataflows_file, 'r') as f:
            dataflows = json.load(f)
        
        for df in dataflows:
            if df.get("id") == dataflow_id:
                if df.get("structure_id"):
                    return f"{df['structure_agency_id']}:{df['structure_id']}:{df.get('structure_version', 'latest')}"
    
    return None

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=30, min=30, max=300),
    retry=retry_if_exception_type(RateLimitError),
    before_sleep=lambda retry_state: print(f"Rate limited. Waiting {retry_state.next_action.sleep} seconds before retry {retry_state.attempt_number}/3...")
)
def fetch_data(dataflow_id: str, apply_labels: bool = True, max_size_bytes: int = 10_000_000_000) -> pa.Table:
    """
    Fetch actual data for the dataset using streaming for memory efficiency
    
    Args:
        dataflow_id: The dataset identifier (e.g., "EXR")
        apply_labels: Whether to apply codelist labels (default: True)
        max_size_bytes: Maximum response size (default 10GB)
    
    Returns:
        PyArrow Table with the fetched data
    """
    base_url = "https://data-api.ecb.europa.eu/service"
    
    # Using recommended Accept header for ECB
    headers = {
        "Accept": "application/vnd.sdmx.structurespecificdata+xml;version=2.1"
    }
    
    # Use httpx directly for streaming support
    with httpx.Client(timeout=1800) as client:
        response = client.get(f"{base_url}/data/{dataflow_id}", headers=headers)
        
        # Check HTTP status
        if response.status_code != 200:
            if response.status_code == 429:
                raise RateLimitError(f"Rate limited by ECB API for {dataflow_id}")
            else:
                raise Exception(f"HTTP {response.status_code} error for {dataflow_id}: {response.text[:500]}")
        
        # Check content size
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > max_size_bytes:
            raise Exception(f"Dataset {dataflow_id} exceeds 10GB limit ({int(content_length):,} bytes)")
        
        # Process streaming
        all_dfs = []
        for batch_df in parse_sdmx_streaming(response):
            all_dfs.append(batch_df)
        
        # Combine all batches
        if not all_dfs:
            return pa.Table.from_pandas(pd.DataFrame())
        
        df = pd.concat(all_dfs, ignore_index=True)
        
        # Apply labels if requested and structure info is available
        if apply_labels and _STRUCTURES and _CODELISTS:
            structure_key = get_structure_key(dataflow_id)
            if structure_key and structure_key in _STRUCTURES:
                df = apply_codelist_labels(df, _STRUCTURES[structure_key])
        
        # Lowercase all column names
        df.columns = [col.lower() for col in df.columns]
        
        # Convert to PyArrow Table
        return pa.Table.from_pandas(df)

def parse_sdmx_streaming(response: httpx.Response, batch_size: int = 50000) -> Iterator[pd.DataFrame]:
    """
    Parse SDMX XML response using streaming to minimize memory usage.
    Yields DataFrames in batches.
    
    Args:
        response: The HTTP response containing XML data
        batch_size: Number of observations to accumulate before yielding
        
    Yields:
        DataFrames containing parsed observations
    """
    # ECB might use structure-specific format, so we need to handle both
    namespaces = {
        "m": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
        "g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
        "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific"
    }
    
    # Use iterparse for streaming
    parser = ET.iterparse(BytesIO(response.content), events=('start', 'end'))
    parser = iter(parser)
    
    # Get root element
    event, root = next(parser)
    
    current_series_data = {}
    batch_data = []
    series_count = 0
    obs_count = 0
    is_generic = False
    is_structure_specific = False
    
    for event, elem in parser:
        if event == 'end':
            # Detect format from namespace
            if not is_generic and not is_structure_specific:
                if elem.tag.startswith("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}"):
                    is_generic = True
                elif elem.tag.startswith("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific}"):
                    is_structure_specific = True
            
            # Generic format parsing
            if is_generic:
                # Process Series element
                if elem.tag.endswith('Series'):
                    # Extract series-level data
                    current_series_data = {}
                    
                    # Get series key (dimensions)
                    for key_value in elem.findall(".//g:Value[@id]", namespaces):
                        if key_value.getparent().tag.endswith('SeriesKey'):
                            current_series_data[key_value.get("id")] = key_value.get("value")
                    
                    # Get series-level attributes
                    for attr in elem.findall(".//g:Value[@id]", namespaces):
                        if attr.getparent().tag.endswith('Attributes') and \
                           attr.getparent().getparent() == elem:
                            current_series_data[attr.get("id")] = attr.get("value")
                    
                    series_count += 1
                    
                # Process Observation element
                elif elem.tag.endswith('Obs'):
                    obs_data = current_series_data.copy()
                    
                    # Time dimension
                    time_elem = elem.find(".//g:ObsDimension", namespaces)
                    if time_elem is not None:
                        obs_data["TIME_PERIOD"] = time_elem.get("value")
                    
                    # Observation value
                    value_elem = elem.find(".//g:ObsValue", namespaces)
                    if value_elem is not None:
                        value_str = value_elem.get("value")
                        if value_str is not None:
                            try:
                                obs_data["OBS_VALUE"] = float(value_str)
                            except (ValueError, TypeError):
                                obs_data["OBS_VALUE"] = value_str
                        else:
                            obs_data["OBS_VALUE"] = None
                    else:
                        obs_data["OBS_VALUE"] = None
                    
                    # Observation attributes
                    for attr in elem.findall(".//g:Value[@id]", namespaces):
                        if attr.getparent().tag.endswith('Attributes'):
                            obs_data[attr.get("id")] = attr.get("value")
                    
                    batch_data.append(obs_data)
                    obs_count += 1
            
            # Structure-specific format parsing
            elif is_structure_specific:
                # Process Series element
                if elem.tag.endswith('Series'):
                    # Extract dimension values from attributes
                    current_series_data = {k: v for k, v in elem.attrib.items() 
                                         if not k.startswith('{') and k != 'IDREF'}
                    series_count += 1
                
                # Process Observation element
                elif elem.tag.endswith('Obs'):
                    obs_data = current_series_data.copy()
                    
                    # Get observation attributes
                    for k, v in elem.attrib.items():
                        if not k.startswith('{'):
                            if k in ['TIME_PERIOD', 'TIME']:
                                obs_data["TIME_PERIOD"] = v
                            elif k in ['OBS_VALUE', 'VALUE']:
                                if v is not None:
                                    try:
                                        obs_data["OBS_VALUE"] = float(v)
                                    except (ValueError, TypeError):
                                        obs_data["OBS_VALUE"] = v
                                else:
                                    obs_data["OBS_VALUE"] = None
                            else:
                                obs_data[k] = v
                    
                    batch_data.append(obs_data)
                    obs_count += 1
            
            # Yield batch if size reached
            if len(batch_data) >= batch_size:
                yield pd.DataFrame(batch_data)
                batch_data = []
            
            # Clear processed elements to free memory
            elem.clear()
            # Remove references to allow garbage collection
            if hasattr(elem, '_parent'):
                elem._parent = None
    
    # Yield any remaining data
    if batch_data:
        yield pd.DataFrame(batch_data)
    
    # Clear root
    root.clear()

def apply_codelist_labels(df: pd.DataFrame, structure: Dict[str, Any]) -> pd.DataFrame:
    """Apply codelist labels to dataframe columns based on structure"""
    df = df.copy()
    
    # Process dimensions
    for dim in structure.get("dimensions", []):
        dim_id = dim.get("id")
        codelist_ref = dim.get("codelist")
        
        if dim_id in df.columns and codelist_ref and codelist_ref in _CODELISTS:
            codelist = _CODELISTS[codelist_ref]["codes"]
            # Replace codes with labels directly
            df[dim_id] = df[dim_id].map(lambda x: codelist.get(x, x))
    
    # Process attributes
    for attr in structure.get("attributes", []):
        attr_id = attr.get("id")
        codelist_ref = attr.get("codelist")
        
        if attr_id in df.columns and codelist_ref and codelist_ref in _CODELISTS:
            codelist = _CODELISTS[codelist_ref]["codes"]
            # Replace codes with labels directly
            df[attr_id] = df[attr_id].map(lambda x: codelist.get(x, x))
    
    return df