from fasthtml.common import APIRouter
from ui.pages.governance_lab import GovernanceLabPage
from ui.components import page_layout

rt = APIRouter()

@rt("/governance-lab")
def governance_lab_page():
    return page_layout(GovernanceLabPage(), current_path="/governance-lab")