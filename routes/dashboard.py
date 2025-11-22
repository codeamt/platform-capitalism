from fasthtml.common import APIRouter
from ui.pages.dashboard import DashboardPage
from ui.components import page_layout

rt = APIRouter()

@rt("/")
def dashboard_page():
    return page_layout(DashboardPage(), current_path="/")