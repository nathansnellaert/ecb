#!/usr/bin/env python3
"""Download concepts and codelists for ECB SDMX"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import httpx
from typing import Dict, List, Set

def download_codelists(codelist_refs: Set[str]) -> Dict[str, any]:
    """Download specified codelists"""
    base_url = "https://data-api.ecb.europa.eu/service"
    
    headers = {
        "Accept": "application/vnd.sdmx.structure+xml;version=2.1"
    }
    
    codelists = {}
    
    for i, ref in enumerate(codelist_refs, 1):
        print(f"  [{i}/{len(codelist_refs)}] Downloading codelist {ref}...")
        
        # Parse reference (e.g., "ECB:CL_FREQ:1.0")
        parts = ref.split(":")
        agency = parts[0] if len(parts) > 0 else "ECB"
        codelist_id = parts[1] if len(parts) > 1 else ref
        version = parts[2] if len(parts) > 2 else "latest"
        
        url = f"{base_url}/codelist/{agency}/{codelist_id}/{version}"
        
        try:
            response = httpx.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
        except Exception as e:
            print(f"    Error: {e}")
            continue
        
        root = ET.fromstring(response.text)
        namespaces = {
            "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
            "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
        }
        
        # Find Codelist element
        cl = root.find(".//s:Codelist", namespaces)
        if cl is None:
            print(f"    No Codelist found")
            continue
        
        codelist = {
            "id": cl.get("id"),
            "agency": cl.get("agencyID"),
            "version": cl.get("version"),
            "urn": cl.get("urn"),
            "codes": {}
        }
        
        # Get name
        name = cl.find(".//c:Name", namespaces)
        if name is not None:
            codelist["name"] = name.text
        
        # Get codes
        for code_elem in cl.findall(".//s:Code", namespaces):
            code_id = code_elem.get("id")
            code_name = code_elem.find(".//c:Name", namespaces)
            if code_name is not None:
                codelist["codes"][code_id] = code_name.text
            else:
                codelist["codes"][code_id] = code_id
        
        codelists[ref] = codelist
    
    return codelists

def download_concepts() -> Dict[str, any]:
    """Download concept schemes from ECB"""
    base_url = "https://data-api.ecb.europa.eu/service"
    
    headers = {
        "Accept": "application/vnd.sdmx.structure+xml;version=2.1"
    }
    
    print("Downloading ECB concept schemes...")
    
    # ECB typically uses a standard concept scheme
    url = f"{base_url}/conceptscheme/ECB"
    
    try:
        response = httpx.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
    except Exception as e:
        print(f"Error downloading concepts: {e}")
        return {}
    
    root = ET.fromstring(response.text)
    namespaces = {
        "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
        "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"
    }
    
    concepts = {}
    
    for cs in root.findall(".//s:ConceptScheme", namespaces):
        scheme_id = cs.get("id")
        agency = cs.get("agencyID")
        
        scheme = {
            "id": scheme_id,
            "agency": agency,
            "version": cs.get("version"),
            "concepts": {}
        }
        
        # Get name
        name = cs.find(".//c:Name", namespaces)
        if name is not None:
            scheme["name"] = name.text
        
        # Get concepts
        for concept_elem in cs.findall(".//s:Concept", namespaces):
            concept_id = concept_elem.get("id")
            concept_name = concept_elem.find(".//c:Name", namespaces)
            if concept_name is not None:
                scheme["concepts"][concept_id] = concept_name.text
            else:
                scheme["concepts"][concept_id] = concept_id
        
        concepts[f"{agency}:{scheme_id}"] = scheme
    
    return concepts

def main():
    defs_dir = Path(__file__).parent.parent / "defs"
    defs_dir.mkdir(exist_ok=True)
    
    # Load structures to get codelist references
    structures_file = defs_dir / "structures.json"
    if not structures_file.exists():
        print("Please run download_structures.py first")
        return
    
    with open(structures_file, 'r') as f:
        structures = json.load(f)
    
    # Collect all codelist references
    codelist_refs = set()
    for structure in structures.values():
        for dim in structure.get("dimensions", []):
            if dim.get("codelist"):
                codelist_refs.add(dim["codelist"])
        for attr in structure.get("attributes", []):
            if attr.get("codelist"):
                codelist_refs.add(attr["codelist"])
    
    print(f"Found {len(codelist_refs)} unique codelists to download")
    
    # Download codelists
    codelists = download_codelists(codelist_refs)
    
    # Save codelists
    output_file = defs_dir / "codelists.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(codelists, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(codelists)} codelists to {output_file}")
    
    # Download concepts
    concepts = download_concepts()
    
    # Save concepts
    output_file = defs_dir / "concepts.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(concepts, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(concepts)} concept schemes to {output_file}")

if __name__ == "__main__":
    main()