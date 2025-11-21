from fasthtml import APIRouter
from app.ui.pages.dashboard import DashboardPage


rt = APIRouter()

@rt("/")
def dashboard_page():
    return DashboardPage()