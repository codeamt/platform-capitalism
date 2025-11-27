from fasthtml.common import APIRouter
from simulation.environment import GLOBAL_ENVIRONMENT
import json
import csv
from io import StringIO
from fasthtml.common import Response

rt = APIRouter()

@rt("/export/json")
def export_json():
    data = [a.history for a in GLOBAL_ENVIRONMENT.agents]
    return Response(json.dumps(data), media_type="application/json")

@rt("/export/csv")
def export_csv():
    """Export comprehensive simulation data as downloadable CSV."""
    output = StringIO()
    writer = csv.writer(output)
    
    # Comprehensive header with all key metrics
    writer.writerow([
        "agent_id",
        "tick",
        "state",
        "strategy",
        "final_reward",
        "cpm_earnings",
        "posts_generated",
        "burnout",
        "addiction_drive",
        "emotional_resilience",
        "arousal_level",
        "quality",
        "diversity",
        "consistency",
        "action_taken"
    ])

    # Export all agent history
    for agent in GLOBAL_ENVIRONMENT.agents:
        for entry in agent.history:
            writer.writerow([
                agent.profile.id,
                entry.get("tick", 0),
                entry.get("state", "UNKNOWN"),
                entry.get("strategy", "unknown"),
                entry.get("final_reward", 0),
                entry.get("cpm_earnings", 0),
                entry.get("posts_generated", 0),
                entry.get("burnout", 0),
                entry.get("addiction_drive", 0),
                entry.get("emotional_resilience", 0),
                entry.get("arousal_level", 0),
                entry.get("quality", 0),
                entry.get("diversity", 0),
                entry.get("consistency", 0),
                entry.get("action_taken", "")
            ])

    # Return with proper download headers
    csv_data = output.getvalue()
    return Response(
        csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=platform_capitalism_data.csv"
        }
    )