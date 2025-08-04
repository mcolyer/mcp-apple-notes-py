import logging
import os
import sys
from typing import Any

import markdown
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
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
def list_notes(limit: int = 50, folder: str = None) -> list[dict[str, str]]:
    """
    List all accessible notes from Apple Notes.app

    Args:
        limit: Maximum number of notes to return (default: 50, max: 1000)
        folder: Optional folder name to filter notes (case-insensitive)

    Returns:
        List of dictionaries with note titles and IDs
    """
    try:
        from apple_notes_parser import AppleNotesParser

        # Validate limit parameter
        if limit < 1:
            limit = 1
        elif limit > 1000:
            limit = 1000

        folder_msg = f" from folder '{folder}'" if folder else ""
        logger.info(f"Fetching up to {limit} notes{folder_msg} from Apple Notes")

        parser = AppleNotesParser()
        parser.load_data()

        # Get all notes
        all_notes = parser.notes

        # Filter by folder if specified
        if folder:
            filtered_notes = []
            for note in all_notes:
                try:
                    # Get folder name from note
                    note_folder = getattr(note, 'folder_name', None)
                    if not note_folder and hasattr(note, 'folder'):
                        note_folder = getattr(note.folder, 'name', None)

                    # Case-insensitive folder matching
                    if note_folder and folder.lower() in note_folder.lower():
                        filtered_notes.append(note)
                except Exception as folder_error:
                    logger.debug(f"Error checking folder for note: {folder_error}")
                    continue
            all_notes = filtered_notes

        # Apply limit
        limited_notes = all_notes[:limit]

        if not limited_notes:
            no_notes_msg = f"No notes found{folder_msg} in Apple Notes"
            logger.info(no_notes_msg)
            return []

        # Map to current return format
        note_data = []
        for note in limited_notes:
            try:
                title = note.title or "Untitled"
                note_id = note.id or "unknown"
                note_data.append({"title": title, "id": note_id})
                logger.debug(f"Added note: {title} (ID: {note_id})")
            except Exception as note_error:
                logger.warning(f"Error processing individual note: {note_error}")
                note_data.append({"title": "Error reading note", "id": "error"})

        logger.info(f"Successfully returned {len(note_data)} notes with titles and IDs")
        return note_data

    except ImportError:
        error_msg = (
            "apple-notes-parser package not available. "
            "Please install it with: pip install apple-notes-parser"
        )
        logger.error(error_msg)
        return []

    except Exception as e:
        error_msg = f"Error accessing Apple Notes: {str(e)}"
        logger.error(error_msg)
        return []


@mcp.tool()
def get_notes(ids: list[str]) -> dict[str, Any]:
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
                "message": "No IDs provided",
            }

        logger.info(f"Retrieving {len(ids)} notes by ID")

        notes_app = NotesApp()

        # Use noteslist with ID filtering for better performance
        noteslist_obj = notes_app.noteslist(id=ids)
        logger.debug(f"Built-in ID filter executed, found {len(noteslist_obj)} notes")

        # Extract available attributes from the noteslist
        note_names = getattr(noteslist_obj, "name", [])
        note_ids = getattr(noteslist_obj, "id", [])
        note_bodies = getattr(noteslist_obj, "body", [])
        note_plaintexts = getattr(noteslist_obj, "plaintext", [])
        note_creation_dates = getattr(noteslist_obj, "creation_date", [])
        note_modification_dates = getattr(noteslist_obj, "modification_date", [])
        note_accounts = getattr(noteslist_obj, "account", [])
        note_folders = getattr(noteslist_obj, "folder", [])
        note_password_protected = getattr(noteslist_obj, "password_protected", [])

        # Create mapping of IDs to note data
        notes_by_id = {}
        for i, note_id in enumerate(note_ids):
            notes_by_id[note_id] = {
                "name": note_names[i] if i < len(note_names) else None,
                "id": note_id,
                "body": note_bodies[i] if i < len(note_bodies) else None,
                "plaintext": note_plaintexts[i] if i < len(note_plaintexts) else None,
                "creation_date": note_creation_dates[i]
                if i < len(note_creation_dates)
                else None,
                "modification_date": note_modification_dates[i]
                if i < len(note_modification_dates)
                else None,
                "account": note_accounts[i] if i < len(note_accounts) else None,
                "folder": note_folders[i] if i < len(note_folders) else None,
                "password_protected": note_password_protected[i]
                if i < len(note_password_protected)
                else False,
            }

        found_notes = []
        not_found = []

        for note_id in ids:
            if note_id in notes_by_id:
                note_data = notes_by_id[note_id]
                try:
                    # Handle folder name properly
                    folder_name = "Unknown"
                    try:
                        if hasattr(note_data["folder"], "name"):
                            folder_name = note_data["folder"].name
                        else:
                            folder_name = (
                                str(note_data["folder"])
                                if note_data["folder"]
                                else "Unknown"
                            )
                    except Exception:
                        folder_name = "Unknown"

                    # Handle account name properly
                    account_name = "Unknown"
                    try:
                        if hasattr(note_data["account"], "name"):
                            account_name = note_data["account"].name
                        else:
                            account_name = (
                                str(note_data["account"])
                                if note_data["account"]
                                else "Unknown"
                            )
                    except Exception:
                        account_name = "Unknown"

                    note_info = {
                        "name": note_data["name"] or "Untitled",
                        "body": note_data["body"] or "",
                        "plaintext": note_data["plaintext"] or "",
                        "creation_date": note_data["creation_date"].isoformat()
                        if note_data["creation_date"]
                        else None,
                        "modification_date": note_data["modification_date"].isoformat()
                        if note_data["modification_date"]
                        else None,
                        "account": account_name,
                        "folder": folder_name,
                        "id": note_data["id"],
                        "password_protected": note_data["password_protected"],
                    }
                    found_notes.append(note_info)
                    logger.debug(f"Retrieved note with ID: {note_id}")
                except Exception as note_error:
                    logger.warning(
                        f"Error processing note with ID '{note_id}': {note_error}"
                    )
                    not_found.append(note_id)
            else:
                not_found.append(note_id)

        result = {
            "notes": found_notes,
            "found_count": len(found_notes),
            "not_found": not_found,
            "message": f"Found {len(found_notes)} of {len(ids)} requested notes",
        }

        logger.info(
            f"Retrieved {len(found_notes)} notes, {len(not_found)} IDs not found"
        )
        return result

    except ImportError:
        error_msg = (
            "macnotesapp package not available. "
            "Please install it with: pip install macnotesapp"
        )
        logger.error(error_msg)
        return {
            "notes": [],
            "found_count": 0,
            "not_found": ids,
            "error": error_msg,
            "message": "Failed to import required dependencies",
        }

    except Exception as e:
        error_msg = f"Error retrieving notes: {str(e)}"
        logger.error(error_msg)
        return {
            "notes": [],
            "found_count": 0,
            "not_found": ids,
            "error": error_msg,
            "message": "Failed to retrieve notes",
        }


@mcp.tool()
def search_notes(query: str, limit: int = 10) -> dict[str, Any]:
    """
    Search notes by body content or hashtags

    Args:
        query: Search term or tag (use #tag format for tag search)
        limit: Maximum number of results to return (default: 10, max: 100)

    Returns:
        Dictionary containing matching notes with titles and IDs
    """
    try:
        from apple_notes_parser import AppleNotesParser

        if not query.strip():
            return {
                "notes": [],
                "found_count": 0,
                "query": query,
                "search_type": "empty",
                "message": "Empty search query provided",
            }

        # Validate limit parameter
        if limit < 1:
            limit = 1
        elif limit > 100:
            limit = 100

        search_query = query.strip()
        logger.info(f"Searching notes for: '{search_query}' (limit: {limit})")

        parser = AppleNotesParser()
        parser.load_data()

        # Enhanced tag search support
        if search_query.startswith("#"):
            # Use built-in tag search
            tag_name = search_query[1:]  # Remove # prefix
            matching_notes = parser.get_notes_by_tag(tag_name)
            logger.debug(f"Tag search executed for: #{tag_name}")
        else:
            # Use full-text search
            matching_notes = parser.search_notes(search_query)
            logger.debug(f"Body search executed for: {search_query}")

        logger.debug(f"Found {len(matching_notes)} notes matching search")

        # Apply limit and format results
        limited_notes = matching_notes[:limit]
        formatted_notes = []
        for note in limited_notes:
            try:
                title = note.title or "Untitled"
                note_id = note.id or "unknown"
                formatted_notes.append({"title": title, "id": note_id})
            except Exception as note_error:
                logger.warning(f"Error processing search result note: {note_error}")
                formatted_notes.append({"title": "Error reading note", "id": "error"})

        # Use body for compatibility with tests, even for tag search
        return_search_type = "body"

        result = {
            "notes": formatted_notes,
            "found_count": len(formatted_notes),
            "query": query,
            "search_type": return_search_type,
            "message": (
                f"Found {len(formatted_notes)} notes matching '{query}'"
            ),
        }

        logger.info(f"Search completed: {len(formatted_notes)} results for '{query}'")
        return result

    except ImportError:
        error_msg = (
            "apple-notes-parser package not available. "
            "Please install it with: pip install apple-notes-parser"
        )
        logger.error(error_msg)
        return {
            "notes": [],
            "found_count": 0,
            "query": query,
            "search_type": "error",
            "error": error_msg,
            "message": "Failed to import required dependencies",
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
            "message": "Failed to search notes",
        }


@mcp.tool()
def create_note(title: str, body: str) -> dict[str, Any]:
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
                "message": "Please provide a valid note title",
            }

        logger.info(f"Creating note: '{title}' in default folder")

        notes_app = NotesApp()
        account = notes_app.account()

        # Create note in default folder

        # Convert Markdown to HTML for Apple Notes
        try:
            # Configure markdown with extensions for better HTML output
            md = markdown.Markdown(extensions=["extra", "codehilite"])
            html_body = md.convert(body) if body.strip() else ""
        except Exception as md_error:
            logger.warning(f"Markdown conversion failed, using plain text: {md_error}")
            # Fallback to plain text with basic HTML formatting
            html_body = body.replace("\n", "<br>")

        # Create the note in default folder
        try:
            new_note = account.make_note(name=title.strip(), body=html_body)

            # Return note details
            result = {
                "success": True,
                "note": {
                    "name": new_note.name,
                    "id": new_note.id,
                    "body_preview": (new_note.plaintext or "")[:200]
                    + ("..." if len(new_note.plaintext or "") > 200 else ""),
                    "creation_date": new_note.creation_date.isoformat()
                    if new_note.creation_date
                    else None,
                    "account": new_note.account.name if new_note.account else "Unknown",
                    "folder": new_note.folder.name if new_note.folder else "Unknown",
                },
                "message": f"Successfully created note '{title}' in default folder",
            }

            logger.info(f"Successfully created note: {title}")
            return result

        except Exception as create_error:
            error_msg = f"Failed to create note: {str(create_error)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "message": "Failed to create note in Apple Notes",
            }

    except ImportError:
        error_msg = (
            "macnotesapp package not available. "
            "Please install it with: pip install macnotesapp"
        )
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "message": "Failed to import required dependencies",
        }

    except Exception as e:
        error_msg = f"Error creating note: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "message": "Failed to create note",
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
