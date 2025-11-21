from fasthtml import APIRouter
from app.ui.pages.network import NetworkPage

rt = APIRouter()

@rt("/network")
def network_page():
    return NetworkPage()