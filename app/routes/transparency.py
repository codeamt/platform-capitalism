from fasthtml import APIRouter
from app.ui.pages.transparency import TransparencyPage

rt = APIRouter()

@rt("/transparency")
def transparency_page():
    return TransparencyPage()