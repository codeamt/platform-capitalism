from fasthtml import APIRouter
from app.ui.pages.creator_studio import CreatorStudioPage

rt = APIRouter()

@rt("/creator-studio")
def creator_studio_page():
    return CreatorStudioPage()