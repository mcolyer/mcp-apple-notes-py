import asyncio
import logging
import sys
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
import os
import re
import markdown

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
def list_notes(limit: int = 50) -> List[Dict[str, str]]:
    """
    List all accessible notes from Apple Notes.app
    
    Args:
        limit: Maximum number of notes to return (default: 50, max: 1000)
    
    Returns:
        List of dictionaries with note titles and IDs
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
            return []
        
        # Limit the results
        limited_notes = all_notes[:limit]
        
        # Extract note titles and IDs
        note_data = []
        for note in limited_notes:
            try:
                title = getattr(note, 'name', None) or "Untitled"
                note_id = getattr(note, 'id', None) or "unknown"
                note_data.append({"title": title, "id": note_id})
                logger.debug(f"Added note: {title} (ID: {note_id})")
                
            except Exception as note_error:
                logger.warning(f"Error processing individual note: {note_error}")
                note_data.append({"title": "Error reading note", "id": "error"})
        
        # Return the array of title/ID pairs
        logger.info(f"Successfully returned {len(note_data)} notes with titles and IDs")
        return note_data
        
    except ImportError as e:
        error_msg = "macnotesapp package not available. Please install it with: pip install macnotesapp"
        logger.error(error_msg)
        return []
        
    except Exception as e:
        error_msg = f"Error accessing Apple Notes: {str(e)}"
        logger.error(error_msg)
        return []

@mcp.tool()
def get_notes(ids: List[str]) -> Dict[str, Any]:
    """
    Retrieve specific notes by their IDs
    
    Args:
        ids: List of note IDs to retrieve
    
    Returns:
        Dictionary containing successfully retrieved notes and list of not found IDs
    """
    try:
        from macnotesapp import NotesApp
        
        if not ids:
            return {
                "notes": [],
                "found_count": 0,
                "not_found": [],
                "message": "No IDs provided"
            }
        
        logger.info(f"Retrieving {len(ids)} notes by ID")
        
        notes_app = NotesApp()
        all_notes = notes_app.notes()
        
        # Create a mapping of note IDs to note objects
        notes_by_id = {note.id: note for note in all_notes if hasattr(note, 'id') and note.id}
        
        found_notes = []
        not_found = []
        
        for note_id in ids:
            if note_id in notes_by_id:
                note = notes_by_id[note_id]
                try:
                    # Handle folder name properly
                    folder_name = "Unknown"
                    try:
                        if hasattr(note.folder, 'name'):
                            folder_name = note.folder.name
                        else:
                            folder_name = str(note.folder)
                    except:
                        folder_name = "Unknown"
                    
                    note_info = {
                        "name": note.name or "Untitled",
                        "body": note.body or "",
                        "plaintext": note.plaintext or "",
                        "creation_date": note.creation_date.isoformat() if note.creation_date else None,
                        "modification_date": note.modification_date.isoformat() if note.modification_date else None,
                        "account": note.account.name if note.account else "Unknown",
                        "folder": folder_name,
                        "id": note.id,
                        "password_protected": note.password_protected
                    }
                    found_notes.append(note_info)
                    logger.debug(f"Retrieved note with ID: {note_id}")
                except Exception as note_error:
                    logger.warning(f"Error processing note with ID '{note_id}': {note_error}")
                    not_found.append(note_id)
            else:
                not_found.append(note_id)
        
        result = {
            "notes": found_notes,
            "found_count": len(found_notes),
            "not_found": not_found,
            "message": f"Found {len(found_notes)} of {len(ids)} requested notes"
        }
        
        logger.info(f"Retrieved {len(found_notes)} notes, {len(not_found)} IDs not found")
        return result
        
    except ImportError as e:
        error_msg = "macnotesapp package not available. Please install it with: pip install macnotesapp"
        logger.error(error_msg)
        return {
            "notes": [],
            "found_count": 0,
            "not_found": ids,
            "error": error_msg,
            "message": "Failed to import required dependencies"
        }
        
    except Exception as e:
        error_msg = f"Error retrieving notes: {str(e)}"
        logger.error(error_msg)
        return {
            "notes": [],
            "found_count": 0,
            "not_found": ids,
            "error": error_msg,
            "message": "Failed to retrieve notes"
        }

@mcp.tool()
def search_notes(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search notes by text content or tags
    
    Args:
        query: Search term or tag (use #tag format for tag search)
        limit: Maximum number of results to return (default: 10, max: 100)
    
    Returns:
        Dictionary containing matching notes with titles and IDs
    """
    try:
        from macnotesapp import NotesApp
        
        if not query.strip():
            return {
                "notes": [],
                "found_count": 0,
                "query": query,
                "search_type": "empty",
                "message": "Empty search query provided"
            }
        
        # Validate limit parameter
        if limit < 1:
            limit = 1
        elif limit > 100:
            limit = 100
            
        logger.info(f"Searching notes for: '{query}' (limit: {limit})")
        
        notes_app = NotesApp()
        
        # Determine search type and prepare search terms
        is_tag_search = query.strip().startswith('#')
        search_type = "tag" if is_tag_search else "content"
        
        if is_tag_search:
            # For tag search, look for the hashtag in the text
            tag = query.strip()
            search_terms = [tag]
        else:
            # For content search, split query into words for better matching
            search_terms = [query.strip()]
        
        # Use built-in search functionality for much better performance
        try:
            # Use the library's built-in text search
            matching_note_objects = notes_app.notes(text=search_terms)
            logger.debug(f"Built-in search found {len(matching_note_objects)} notes")
            
            # Convert to our format and apply limit
            matching_notes = []
            for note in matching_note_objects[:limit]:
                try:
                    note_info = {
                        "title": note.name or "Untitled",
                        "id": getattr(note, 'id', 'unknown')
                    }
                    matching_notes.append(note_info)
                except Exception as note_error:
                    logger.debug(f"Error processing search result: {note_error}")
                    continue
            
            logger.info(f"Search completed: found {len(matching_notes)} matches using built-in search")
            
        except Exception as search_error:
            logger.warning(f"Built-in search failed: {search_error}, falling back to manual search")
            
            # Fallback to title-only search if built-in search fails
            all_notes = notes_app.notes()
            matching_notes = []
            
            for note in all_notes:
                if len(matching_notes) >= limit:
                    break
                    
                try:
                    note_title = (note.name or "").lower()
                    for term in search_terms:
                        if term.lower() in note_title:
                            note_info = {
                                "title": note.name or "Untitled",
                                "id": getattr(note, 'id', 'unknown')
                            }
                            matching_notes.append(note_info)
                            break
                except Exception:
                    continue
            
            logger.info(f"Fallback search completed: found {len(matching_notes)} matches in titles")
        
        result = {
            "notes": matching_notes,
            "found_count": len(matching_notes),
            "query": query,
            "search_type": search_type,
            "message": f"Found {len(matching_notes)} notes matching '{query}'"
        }
        
        logger.info(f"Search completed: {len(matching_notes)} results for '{query}'")
        return result
        
    except ImportError as e:
        error_msg = "macnotesapp package not available. Please install it with: pip install macnotesapp"
        logger.error(error_msg)
        return {
            "notes": [],
            "found_count": 0,
            "query": query,
            "search_type": "error",
            "error": error_msg,
            "message": "Failed to import required dependencies"
        }
        
    except Exception as e:
        error_msg = f"Error searching notes: {str(e)}"
        logger.error(error_msg)
        return {
            "notes": [],
            "found_count": 0,
            "query": query,
            "search_type": "error",
            "error": error_msg,
            "message": "Failed to search notes"
        }

@mcp.tool()
def create_note(title: str, body: str) -> Dict[str, Any]:
    """
    Create a new note with Markdown formatted body
    
    Args:
        title: Title for the new note
        body: Body content in Markdown format
    
    Returns:
        Dictionary containing created note details and status
    """
    try:
        from macnotesapp import NotesApp
        
        if not title.strip():
            return {
                "success": False,
                "error": "Note title cannot be empty",
                "message": "Please provide a valid note title"
            }
        
        logger.info(f"Creating note: '{title}' in default folder")
        
        notes_app = NotesApp()
        account = notes_app.account()
        
        # Create note in default folder
        
        # Convert Markdown to HTML for Apple Notes
        try:
            # Configure markdown with extensions for better HTML output
            md = markdown.Markdown(extensions=['extra', 'codehilite'])
            html_body = md.convert(body) if body.strip() else ""
        except Exception as md_error:
            logger.warning(f"Markdown conversion failed, using plain text: {md_error}")
            # Fallback to plain text with basic HTML formatting
            html_body = body.replace('\\n', '<br>')
        
        # Create the note in default folder
        try:
            new_note = account.make_note(
                name=title.strip(),
                body=html_body
            )
            
            # Return note details
            result = {
                "success": True,
                "note": {
                    "name": new_note.name,
                    "id": new_note.id,
                    "body_preview": (new_note.plaintext or "")[:200] + ("..." if len(new_note.plaintext or "") > 200 else ""),
                    "creation_date": new_note.creation_date.isoformat() if new_note.creation_date else None,
                    "account": new_note.account.name if new_note.account else "Unknown",
                    "folder": new_note.folder.name if new_note.folder else "Unknown"
                },
                "message": f"Successfully created note '{title}' in default folder"
            }
            
            logger.info(f"Successfully created note: {title}")
            return result
            
        except Exception as create_error:
            error_msg = f"Failed to create note: {str(create_error)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "message": "Failed to create note in Apple Notes"
            }
        
    except ImportError as e:
        error_msg = "macnotesapp package not available. Please install it with: pip install macnotesapp"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "message": "Failed to import required dependencies"
        }
        
    except Exception as e:
        error_msg = f"Error creating note: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "message": "Failed to create note"
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
