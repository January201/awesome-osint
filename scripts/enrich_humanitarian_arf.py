#!/usr/bin/env python3
"""
Humanitarian OSINT Tool Enrichment Script
Tags existing ARF.json tools for Family Reunification missions.
Differentiates between API and Non-API tools for field deployment.
"""

# =============================================================================
# 1. IMPORTS (Standard → Third Party → Local)
# =============================================================================

# Standard libraries first
import os
import sys
import json
import time
import logging
from typing import Dict, List, Any, Optional

# Third party libraries
# (No external dependencies required for this script)

# Your own modules
# (Assuming script runs from root, no local imports needed for standalone operation)

# =============================================================================
# 2. LOGGING SETUP (Immediately after imports)
# =============================================================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="humanitarian_enrich.log",
    filemode="w"
)
logger = logging.getLogger(__name__)

# Also log to console for immediate feedback
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# =============================================================================
# 3. CONSTANTS & CONFIG
# =============================================================================

# File paths
ARF_INPUT_PATH = "public/arf.json"
ARF_OUTPUT_PATH = "public/arf_humanitarian.json"
REPORT_PATH = "tools/humanitarian_tool_report.json"

# Processing limits
MAX_TOOLS_PROCESS = 500  # Safety limit
BATCH_SIZE = 50  # Log progress every N tools

# Versioning
SCRIPT_VERSION = "1.0.0"
MISSION_TYPE = "Family_Reunification"
DATE_STAMP = time.strftime("%Y-%m-%d")

# Humanitarian Tags
HUMANITARIAN_CATEGORIES = [
    "People Search",
    "Social Networks",
    "Missing Persons",
    "Refugee Support",
    "Image Analysis",
    "Communication",
    "Location Services"
]

# Tool Classification Lists (Manual Curation for Accuracy)
NON_API_TOOLS = {
    "Sherlock", "TinEye", "PhoneInfoga", "ExifTool", "theHarvester",
    "Amass", "Google Lens", "Wayback Machine", "Facebook Search",
    "Telegram Search", "WhatsApp Check", "Mapillary", "OpenStreetMap",
    "WikiMapia", "Bellingcat Tools", "InVID", "Forensically"
}

API_TOOLS = {
    "Maltego", "Shodan", "Hunter.io", "SpiderFoot", "DomainTools",
    "HaveIBeenPwned", "Pipl", "Intelx", "DeHashed", "Censys"
}

# Safety Flags
SAFETY_LEVELS = {
    "High": "Safe for field use, no data leaves device or uses public endpoints.",
    "Medium": "Data sent to third-party servers, use with caution for vulnerable subjects.",
    "Low": "Not recommended for active conflict zones or vulnerable subjects."
}

# =============================================================================
# 4. GLOBAL STATE
# =============================================================================

# Track processing stats
stats = {
    "total_nodes": 0,
    "processed_nodes": 0,
    "tagged_humanitarian": 0,
    "api_tools": 0,
    "non_api_tools": 0,
    "errors": 0
}

# Cache for processed names to avoid duplicates
processed_names = set()

# =============================================================================
# 5. HELPER / UTILITY FUNCTIONS
# =============================================================================

def is_rate_limited(tool_name: str) -> bool:
    """
    Simulate rate limiting check for API tools.
    In production, this would track actual API call counts.
    """
    # Placeholder for future API rate limit logic
    return False

def format_tool_name(name: str) -> str:
    """Clean and standardize tool names."""
    if not name:
        return ""
    return name.strip()[:100]

def classify_tool_api_status(name: str, description: str = "") -> str:
    """
    Determine if a tool requires an API key.
    Returns: 'Non-API', 'API', or 'Unknown'
    """
    name_lower = name.lower()
    desc_lower = description.lower()
    
    # Check explicit lists first
    for api_tool in API_TOOLS:
        if api_tool.lower() in name_lower:
            return "API"
    
    for non_api_tool in NON_API_TOOLS:
        if non_api_tool.lower() in name_lower:
            return "Non-API"
    
    # Heuristics based on description
    if "api" in desc_lower and ("key" in desc_lower or "subscription" in desc_lower):
        return "API"
    
    if "browser extension" in desc_lower or "command line" in desc_lower or "local" in desc_lower:
        return "Non-API"
    
    # Default assumption
    return "Unknown"

def assign_safety_level(api_status: str, category: str) -> str:
    """Assign safety level based on API status and category."""
    if api_status == "Non-API":
        return "High"
    elif api_status == "API":
        # Some API tools are safer than others
        if "Image" in category or "Search" in category:
            return "Medium"
        else:
            return "Medium"
    return "Low"

def map_to_framework_phase(category: str) -> List[str]:
    """Map tool categories to the 8-Phase Framework."""
    phase_map = {
        "People Search": ["Phase 2", "Phase 3", "Phase 4"],
        "Social Networks": ["Phase 2", "Phase 3", "Phase 4"],
        "Image Analysis": ["Phase 2", "Phase 3", "Phase 6"],
        "Communication": ["Phase 2", "Phase 3", "Phase 4"],
        "Location Services": ["Phase 1", "Phase 3", "Phase 4"],
        "Missing Persons": ["Phase 1", "Phase 3", "Phase 5"],
        "Domain Tools": ["Phase 2", "Phase 4"],
        "Default": ["Phase 3"]
    }
    
    for key, phases in phase_map.items():
        if key in category:
            return phases
    return phase_map["Default"]

# =============================================================================
# 6. COMMAND HANDLERS (Simulated for Script Logic)
# =============================================================================

def handle_validation(update_context: Dict) -> bool:
    """
    Validate input file exists and is readable.
    Simulates the 'start' command validation logic.
    """
    path = update_context.get("path", "")
    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return False
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            json.load(f)
        logger.info(f"Validation successful: {path}")
        return True
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return False

def handle_help_request() -> None:
    """Log help information."""
    logger.info(f"Script Version: {SCRIPT_VERSION}")
    logger.info(f"Mission: {MISSION_TYPE}")
    logger.info(f"Input: {ARF_INPUT_PATH}")
    logger.info(f"Output: {ARF_OUTPUT_PATH}")

# =============================================================================
# 7. MESSAGE HANDLER (Core Logic - Recursive Node Processing)
# =============================================================================

async def process_node(node: Dict[str, Any], parent_category: str = "") -> Optional[Dict[str, Any]]:
    """
    Recursively process each node in the ARF tree.
    Follows the exact 8-step logic pattern: Get → Validate → Log → Process → Format → Save.
    """
    
    # STEP 1 — Get node data
    if not isinstance(node, dict):
        return node
    
    name = node.get("name", "")
    url = node.get("url", "")
    children = node.get("children", [])
    description = node.get("description", "")
    
    # STEP 2 — Rate limit check (Simulated)
    if is_rate_limited(name):
        logger.warning(f"Rate limited: {name}")
        return node
    
    # STEP 3 — Validate input
    if not name and not children:
        return node  # Skip empty nodes
    
    # STEP 4 — Log the request
    if name and name not in processed_names:
        logger.debug(f"Processing: {name}")
    
    # STEP 5 — Process / Enrich Data
    if name and name not in processed_names:
        processed_names.add(name)
        stats["processed_nodes"] += 1
        
        # Classify API Status
        api_status = classify_tool_api_status(name, description)
        if api_status == "API":
            stats["api_tools"] += 1
        elif api_status == "Non-API":
            stats["non_api_tools"] += 1
        
        # Determine Humanitarian Relevance
        is_humanitarian = False
        humanitarian_tags = []
        
        # Check category keywords
        human_keywords = ["people", "social", "missing", "refugee", "image", "photo", "phone", "email", "search", "find"]
        for keyword in human_keywords:
            if keyword in name.lower() or keyword in description.lower() or keyword in parent_category.lower():
                is_humanitarian = True
                humanitarian_tags.append(keyword.title())
                break
        
        # Explicit list check
        if name in NON_API_TOOLS or name in API_TOOLS:
            is_humanitarian = True
            if "Search" not in humanitarian_tags:
                humanitarian_tags.append("Search")
        
        if is_humanitarian:
            stats["tagged_humanitarian"] += 1
            
            # Add Enrichment Fields
            node["humanitarian"] = {
                "relevant": True,
                "missionType": MISSION_TYPE,
                "apiRequired": api_status != "Non-API",
                "apiStatus": api_status,
                "safetyLevel": assign_safety_level(api_status, parent_category),
                "frameworkPhases": map_to_framework_phase(parent_category),
                "tags": humanitarian_tags,
                "bestFor": "Family reunification and missing persons search",
                "caution": "Verify identity before contact. Do not expose location of vulnerable subjects." if api_status == "Non-API" else "Use secure connection. Do not store data locally."
            }
            
            # Add specific use case from our guide
            if "Sherlock" in name:
                node["humanitarian"]["useCase"] = "Track displaced persons via username across social platforms."
            elif "TinEye" in name or "Image" in name:
                node["humanitarian"]["useCase"] = "Match photos of lost children against news/NGO databases."
            elif "Phone" in name:
                node["humanitarian"]["useCase"] = "Verify if old phone numbers are active/roaming in safe zones."
            elif "Exif" in name:
                node["humanitarian"]["useCase"] = "Extract GPS coordinates from last known photos."

    # STEP 6 — Format response (Recursive processing for children)
    if children:
        new_children = []
        current_category = name if not parent_category else parent_category
        
        for child in children:
            result = await process_node(child, current_category)
            if result is not None:
                new_children.append(result)
        
        node["children"] = new_children
    
    # STEP 7 — Send reply (Return processed node)
    return node

# STEP 8 — Update database (Handled in main save function)

# =============================================================================
# 8. AI CALL FUNCTION (Simulated for File I/O)
# =============================================================================

async def load_arf_data(path: str) -> Optional[Dict]:
    """Load ARF JSON data with error handling."""
    try:
        logger.info(f"Loading data from {path}...")
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info("Data loaded successfully.")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading file: {e}")
        return None

async def save_arf_data(data: Dict, path: str) -> bool:
    """Save enriched ARF JSON data."""
    try:
        logger.info(f"Saving enriched data to {path}...")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info("Data saved successfully.")
        return True
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return False

# =============================================================================
# 9. ERROR HANDLER
# =============================================================================

async def handle_error(error: Exception, context: str = "") -> None:
    """Log errors and alert admin (via log file)."""
    logger.error(f"Error in {context}: {str(error)}")
    
    # In a bot, this would send a message to ADMIN_ID
    # For this script, we ensure it's in the log file
    logger.critical(f"CRITICAL: Script may need manual intervention. Check {context}.")

# =============================================================================
# 10. REGISTER ALL HANDLERS (Execution Flow)
# =============================================================================

def register_execution_flow(app_context: Dict) -> None:
    """Register the sequence of operations."""
    app_context["steps"] = [
        "validate_input",
        "load_data",
        "process_tree",
        "save_output",
        "generate_report"
    ]
    logger.info("Execution flow registered.")

# =============================================================================
# 11. STARTUP TASKS
# =============================================================================

async def on_startup() -> bool:
    """Run pre-flight checks."""
    logger.info("="*50)
    logger.info(f"Starting Humanitarian Enrichment Script v{SCRIPT_VERSION}")
    logger.info("="*50)
    
    # Check input file
    if not os.path.exists(ARF_INPUT_PATH):
        logger.error(f"Input file missing: {ARF_INPUT_PATH}")
        logger.error("Please ensure public/arf.json exists.")
        return False
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(ARF_OUTPUT_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    
    logger.info("Pre-flight checks passed.")
    return True

# =============================================================================
# 12. MAIN FUNCTION
# =============================================================================

def main():
    """Main entry point following the 12-step protocol."""
    
    # 1. Build app context
    app_context = {
        "version": SCRIPT_VERSION,
        "mission": MISSION_TYPE
    }
    
    # 2. Register execution flow
    register_execution_flow(app_context)
    
    # 3. Startup tasks
    # Using asyncio.run for async functions
    import asyncio
    
    startup_success = asyncio.run(on_startup())
    if not startup_success:
        logger.error("Startup failed. Exiting.")
        sys.exit(1)
    
    # 4. Execute Main Logic
    try:
        # Validate
        if not handle_validation({"path": ARF_INPUT_PATH}):
            sys.exit(1)
        
        # Load
        arf_data = asyncio.run(load_arf_data(ARF_INPUT_PATH))
        if not arf_data:
            sys.exit(1)
        
        stats["total_nodes"] = len(str(arf_data)) # Rough estimate
        
        # Process
        logger.info("Processing tool tree...")
        enriched_data = asyncio.run(process_node(arf_data))
        
        # Save
        if not asyncio.run(save_arf_data(enriched_data, ARF_OUTPUT_PATH)):
            sys.exit(1)
        
        # Generate Report
        report = {
            "script_version": SCRIPT_VERSION,
            "date": DATE_STAMP,
            "input_file": ARF_INPUT_PATH,
            "output_file": ARF_OUTPUT_PATH,
            "statistics": stats,
            "safety_levels": SAFETY_LEVELS,
            "note": "Tools tagged 'High' safety are recommended for field use in conflict zones."
        }
        
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        logger.info("="*50)
        logger.info("ENRICHMENT COMPLETE")
        logger.info(f"Total Processed: {stats['processed_nodes']}")
        logger.info(f"Humanitarian Relevant: {stats['tagged_humanitarian']}")
        logger.info(f"Non-API Tools: {stats['non_api_tools']}")
        logger.info(f"API Tools: {stats['api_tools']}")
        logger.info(f"Report saved to: {REPORT_PATH}")
        logger.info("="*50)
        
    except Exception as e:
        asyncio.run(handle_error(e, "main_execution"))
        sys.exit(1)

# ALWAYS at bottom — entry point
if __name__ == "__main__":
    main()
