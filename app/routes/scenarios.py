from fasthtml import APIRouter
from app.ui.pages.scenarios import ScenariosPage

rt = APIRouter()

@rt("/scenarios")
def scenarios_page():
    return ScenariosPage()