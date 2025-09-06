#!/usr/bin/env python3
"""Download data structures for ECB dataflows"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import httpx
from typing import Dict, Any, List

def parse_dimension(dim_elem: ET.Element, namespaces: Dict[str, str]) -> Dict[str, Any]:
    """Parse a dimension element"""
    dim = {
        "id": dim_elem.get("id"),
        "position": dim_elem.get("position"),
        "type": "Dimension"
    }
    
    # Get concept reference
    concept_ref = dim_elem.find(".//s:ConceptIdentity/Ref", namespaces)
    if concept_ref is not None:
        dim["concept"] = concept_ref.get("id")
        dim["concept_agency"] = concept_ref.get("agencyID")
    
    # Get codelist reference
    codelist = dim_elem.find(".//s:LocalRepresentation/s:Enumeration/Ref", namespaces)
    if codelist is not None:
        dim["codelist"] = f"{codelist.get('agencyID')}:{codelist.get('id')}:{codelist.get('version', 'latest')}"
    
    # Check if it's a time dimension
    time_dim = dim_elem.find(".//s:TimeDimension", namespaces)
    if time_dim is not None:
        dim["type"] = "TimeDimension"
    
    return dim

def parse_attribute(attr_elem: ET.Element, namespaces: Dict[str, str]) -> Dict[str, Any]:
    """Parse an attribute element"""
    attr = {
        "id": attr_elem.get("id"),
        "assignmentStatus": attr_elem.get("assignmentStatus"),
        "type": "Attribute"
    }
    
    # Get concept reference
    concept_ref = attr_elem.find(".//s:ConceptIdentity/Ref", namespaces)
    if concept_ref is not None:
        attr["concept"] = concept_ref.get("id")
        attr["concept_agency"] = concept_ref.get("agencyID")
    
    # Get codelist reference
    codelist = attr_elem.find(".//s:LocalRepresentation/s:Enumeration/Ref", namespaces)
    if codelist is not None:
        attr["codelist"] = f"{codelist.get('agencyID')}:{codelist.get('id')}:{codelist.get('version', 'latest')}"
    
    # Get text format if present
    text_format = attr_elem.find(".//s:LocalRepresentation/s:TextFormat", namespaces)
    if text_format is not None:
        attr["textFormat"] = {
            "textType": text_format.get("textType"),
            "isMultiLingual": text_format.get("isMultiLingual"),
        }
    
    # Get attachment level
    attachment = attr_elem.find(".//s:AttributeRelationship", namespaces)
    if attachment is not None:
        dim_ref = attachment.find(".//s:Dimension/Ref", namespaces)
        if dim_ref is not None:
            attr["attachmentLevel"] = "Dimension"
            attr["attachmentDimension"] = dim_ref.get("id")
        elif attachment.find(".//s:PrimaryMeasure", namespaces) is not None:
            attr["attachmentLevel"] = "Observation"
        else:
            attr["attachmentLevel"] = "Dataset"
    
    return attr

def download_structure(structure_ref: str) -> Dict[str, Any]:
    """Download a single data structure definition"""
    base_url = "https://data-api.ecb.europa.eu/service"
    
    # Parse structure reference (e.g., "ECB:ECB_EXR1:1.0")
    parts = structure_ref.split(":")
    agency = parts[0] if len(parts) > 0 else "ECB"
    structure_id = parts[1] if len(parts) > 1 else structure_ref
    version = parts[2] if len(parts) > 2 else "latest"
    
    headers = {
        "Accept": "application/vnd.sdmx.structure+xml;version=2.1"
    }
    
    url = f"{base_url}/datastructure/{agency}/{structure_id}/{version}"
    
    try:
        response = httpx.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
    except Exception as e:
        print(f"    Error fetching structure {structure_ref}: {e}")
        return None
    
    root = ET.fromstring(response.text)
    namespaces = {
        "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
        "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
    }
    
    # Find DataStructure element
    dsd = root.find(".//s:DataStructure", namespaces)
    if dsd is None:
        print(f"    No DataStructure found for {structure_ref}")
        return None
    
    structure = {
        "id": dsd.get("id"),
        "agency": dsd.get("agencyID"),
        "version": dsd.get("version"),
        "urn": dsd.get("urn"),
        "dimensions": [],
        "attributes": [],
        "primaryMeasure": None
    }
    
    # Get name
    name = dsd.find(".//c:Name", namespaces)
    if name is not None:
        structure["name"] = name.text
    
    # Get dimensions
    dimensions_container = dsd.find(".//s:DataStructureComponents/s:DimensionList", namespaces)
    if dimensions_container is not None:
        for dim_elem in dimensions_container.findall(".//s:Dimension", namespaces):
            structure["dimensions"].append(parse_dimension(dim_elem, namespaces))
        
        # Time dimension
        time_dim = dimensions_container.find(".//s:TimeDimension", namespaces)
        if time_dim is not None:
            structure["dimensions"].append(parse_dimension(time_dim, namespaces))
    
    # Get primary measure
    measure = dsd.find(".//s:DataStructureComponents/s:MeasureList/s:PrimaryMeasure", namespaces)
    if measure is not None:
        structure["primaryMeasure"] = {
            "id": measure.get("id"),
            "concept": None
        }
        concept_ref = measure.find(".//s:ConceptIdentity/Ref", namespaces)
        if concept_ref is not None:
            structure["primaryMeasure"]["concept"] = concept_ref.get("id")
    
    # Get attributes
    attributes_container = dsd.find(".//s:DataStructureComponents/s:AttributeList", namespaces)
    if attributes_container is not None:
        for attr_elem in attributes_container.findall(".//s:Attribute", namespaces):
            structure["attributes"].append(parse_attribute(attr_elem, namespaces))
    
    return structure

def main():
    # Load dataflows
    defs_dir = Path(__file__).parent.parent / "defs"
    dataflows_file = defs_dir / "dataflows.json"
    
    if not dataflows_file.exists():
        print("Please run download_dataflows.py first")
        return
    
    with open(dataflows_file, 'r') as f:
        dataflows = json.load(f)
    
    print(f"Loading structures for {len(dataflows)} dataflows...")
    
    # Collect unique structure references
    structure_refs = set()
    for df in dataflows:
        if df.get("structure_id"):
            ref = f"{df.get('structure_agency_id', 'ECB')}:{df['structure_id']}:{df.get('structure_version', 'latest')}"
            structure_refs.add(ref)
    
    print(f"Found {len(structure_refs)} unique structures to download")
    
    # Download each structure
    structures = {}
    for i, ref in enumerate(structure_refs, 1):
        print(f"  [{i}/{len(structure_refs)}] Downloading {ref}...")
        structure = download_structure(ref)
        if structure:
            structures[ref] = structure
    
    print(f"Successfully downloaded {len(structures)} structures")
    
    # Save structures
    output_file = defs_dir / "structures.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structures, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()