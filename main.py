import asyncio
import logging
import sys
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger("apple-notes-mcp")

# Initialize FastMCP server
mcp = FastMCP("apple-notes-mcp")

# Check if debug mode is enabled via environment variable
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
if DEBUG_MODE:
    logging.getLogger().setLevel(logging.DEBUG)
    logger.debug("Debug mode enabled")

@mcp.tool()
def list_notes(limit: int = 50) -> Dict[str, Any]:
    """
    List all accessible notes from Apple Notes.app
    
    Args:
        limit: Maximum number of notes to return (default: 50, max: 1000)
    
    Returns:
        Dictionary containing notes list and metadata
    """
    try:
        # Import here to handle cases where macnotesapp isn't available
        from macnotesapp import NotesApp
        
        # Validate limit parameter
        if limit < 1:
            limit = 1
        elif limit > 1000:
            limit = 1000
            
        logger.info(f"Fetching up to {limit} notes from Apple Notes")
        
        # Initialize Notes app connection
        notes_app = NotesApp()
        
        # Get all notes
        all_notes = notes_app.notes()
        
        if not all_notes:
            logger.info("No notes found in Apple Notes")
            return {
                "notes": [],
                "total_count": 0,
                "returned_count": 0,
                "message": "No notes found in Apple Notes"
            }
        
        # Limit the results
        limited_notes = all_notes[:limit]
        
        # Convert notes to serializable format
        notes_data = []
        for note in limited_notes:
            try:
                # Get basic note information
                note_info = {
                    "name": note.name or "Untitled",
                    "body_preview": (note.body or "")[:200] + ("..." if len(note.body or "") > 200 else ""),
                    "creation_date": note.creation_date.isoformat() if note.creation_date else None,
                    "modification_date": note.modification_date.isoformat() if note.modification_date else None,
                    "account": note.account.name if note.account else "Unknown",
                    "folder": note.folder.name if note.folder else "Unknown"
                }
                notes_data.append(note_info)
                logger.debug(f"Processed note: {note_info['name']}")
                
            except Exception as note_error:
                logger.warning(f"Error processing individual note: {note_error}")
                # Add placeholder for failed note
                notes_data.append({
                    "name": "Error reading note",
                    "body_preview": "Unable to read note content",
                    "creation_date": None,
                    "modification_date": None,
                    "account": "Unknown",
                    "folder": "Unknown",
                    "error": str(note_error)
                })
        
        result = {
            "notes": notes_data,
            "total_count": len(all_notes),
            "returned_count": len(notes_data),
            "message": f"Successfully retrieved {len(notes_data)} of {len(all_notes)} notes"
        }
        
        logger.info(f"Successfully returned {len(notes_data)} notes")
        return result
        
    except ImportError as e:
        error_msg = "macnotesapp package not available. Please install it with: pip install macnotesapp"
        logger.error(error_msg)
        return {
            "notes": [],
            "total_count": 0,
            "returned_count": 0,
            "error": error_msg,
            "message": "Failed to import required dependencies"
        }
        
    except Exception as e:
        error_msg = f"Error accessing Apple Notes: {str(e)}"
        logger.error(error_msg)
        return {
            "notes": [],
            "total_count": 0,
            "returned_count": 0,
            "error": error_msg,
            "message": "Failed to access Apple Notes. Please ensure Notes.app is accessible and you have proper permissions."
        }

if __name__ == "__main__":
    logger.info("Starting Apple Notes MCP Server")
    
    try:
        # Use FastMCP's run method which handles the event loop properly
        mcp.run("stdio")
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
