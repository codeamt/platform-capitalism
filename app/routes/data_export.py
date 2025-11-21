from fasthtml import APIRouter
from app.simulation.environment import GLOBAL_ENVIRONMENT
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
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["agent_id", "tick", "state", "final_reward"])

    for agent in GLOBAL_ENVIRONMENT.agents:
        for idx, entry in enumerate(agent.history):
            writer.writerow([
                agent.profile.id,
                idx,
                entry.get("state"),
                entry.get("final_reward")
            ])

    return Response(output.getvalue(), media_type="text/csv")