from fasthtml import APIRouter
from fasthtml.common import Redirect
from app.simulation.environment import GLOBAL_ENVIRONMENT
from app.simulation.policy_engine.config import PolicyConfig

rt = APIRouter()

@rt("/api/update-policy", methods=["POST"])
def update_policy(request):
    form = request.form
    cfg = GLOBAL_ENVIRONMENT.policy_engine.config

    cfg.quality_weight = float(form.get("quality_weight", cfg.quality_weight))
    cfg.diversity_weight = float(form.get("diversity_weight", cfg.diversity_weight))
    cfg.consistency_weight = float(form.get("consistency_weight", cfg.consistency_weight))
    cfg.break_reward = float(form.get("break_reward", cfg.break_reward))

    GLOBAL_ENVIRONMENT.policy_engine.config = cfg
    return Redirect("/governance-lab")