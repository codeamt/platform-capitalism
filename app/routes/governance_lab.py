from fasthtml import APIRouter
from app.ui.pages.governance_lab import GovernanceLabPage

rt = APIRouter()

@rt("/governance-lab")
def governance_lab_page():
    return GovernanceLabPage()