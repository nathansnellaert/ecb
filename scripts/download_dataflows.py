#!/usr/bin/env python3
"""Download all ECB dataflows and save to defs directory"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import httpx

def download_dataflows():
    """Fetch all dataflows (datasets) from ECB SDMX API"""
    print("Fetching all dataflows from ECB...")
    
    base_url = "https://data-api.ecb.europa.eu/service"
    
    # ECB uses /dataflow endpoint to get all dataflows
    # We request all dataflows from ECB agency
    print("  Step 1: Getting dataflow list...")
    
    headers = {
        "Accept": "application/vnd.sdmx.structure+xml;version=2.1"
    }
    
    response = httpx.get(
        f"{base_url}/dataflow/ECB", 
        headers=headers,
        timeout=60.0
    )
    response.raise_for_status()
    
    root = ET.fromstring(response.text)
    namespaces = {
        "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
        "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
    }
    
    dataflows = []
    for df in root.findall(".//s:Dataflow", namespaces):
        # Get basic attributes
        dataflow = {
            "id": df.get("id"),
            "agencyID": df.get("agencyID"),
            "version": df.get("version"),
            "isExternalReference": df.get("isExternalReference"),
            "isFinal": df.get("isFinal"),
            "validFrom": df.get("validFrom"),
            "validTo": df.get("validTo"),
            "urn": df.get("urn")
        }
        
        # Get structure reference
        structure = df.find(".//s:Structure", namespaces)
        if structure is not None:
            ref = structure.find(".//Ref", namespaces)
            if ref is not None:
                dataflow["structure_id"] = ref.get("id")
                dataflow["structure_version"] = ref.get("version")
                dataflow["structure_agency_id"] = ref.get("agencyID")
                dataflow["structure_package"] = ref.get("package")
                dataflow["structure_class"] = ref.get("class")
        
        # Get all names (multiple languages)
        names = {}
        for name in df.findall(".//c:Name", namespaces):
            lang = name.get("{http://www.w3.org/XML/1998/namespace}lang", "en")
            names[lang] = name.text
        dataflow["names"] = names
        dataflow["name"] = names.get("en", names.get(list(names.keys())[0]) if names else df.get("id"))
        
        # Get all descriptions (multiple languages)
        descriptions = {}
        for desc in df.findall(".//c:Description", namespaces):
            lang = desc.get("{http://www.w3.org/XML/1998/namespace}lang", "en")
            descriptions[lang] = desc.text
        dataflow["descriptions"] = descriptions
        dataflow["description"] = descriptions.get("en", "")
        
        # Get annotations
        annotations = []
        for annotation in df.findall(".//c:Annotations//c:Annotation", namespaces):
            ann = {}
            ann_id = annotation.get("id")
            if ann_id:
                ann["id"] = ann_id
            ann_title = annotation.find(".//c:AnnotationTitle", namespaces)
            if ann_title is not None:
                ann["title"] = ann_title.text
            ann_type = annotation.find(".//c:AnnotationType", namespaces)
            if ann_type is not None:
                ann["type"] = ann_type.text
            ann_text = annotation.find(".//c:AnnotationText", namespaces)
            if ann_text is not None:
                ann["text"] = ann_text.text
                ann["text_lang"] = ann_text.get("{http://www.w3.org/XML/1998/namespace}lang", "en")
            if ann:
                annotations.append(ann)
        if annotations:
            dataflow["annotations"] = annotations
        
        dataflows.append(dataflow)
    
    return dataflows


def main():
    # Create data directory
    data_dir = Path(__file__).parent.parent / "defs"
    data_dir.mkdir(exist_ok=True)
    
    # Download dataflows
    dataflows = download_dataflows()
    print(f"Found {len(dataflows)} dataflows")
    
    # Sort by ID for consistent ordering
    dataflows.sort(key=lambda x: x.get("id", ""))
    
    # Save to file
    output_file = data_dir / "dataflows.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataflows, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to {output_file}")
    
    # Print summary
    print("\nDataflow summary:")
    for df in dataflows[:10]:  # Show first 10
        print(f"  - {df['id']}: {df['name']}")
    if len(dataflows) > 10:
        print(f"  ... and {len(dataflows) - 10} more")

if __name__ == "__main__":
    main()