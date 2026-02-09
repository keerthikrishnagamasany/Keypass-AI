main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import uuid

app = FastAPI(title="Keypass AI", version="0.1")

# -----------------------------
# DATA MODELS
# -----------------------------

class Process(BaseModel):
    process_id: str
    description: str
    avg_time_minutes: int
    volume_per_day: int

class EnterpriseContext(BaseModel):
    enterprise_id: str
    industry: str
    processes: List[Process]
    constraints: Dict

class TaskSubmission(BaseModel):
    enterprise_id: str
    process_id: str
    task_type: str
    input: Dict
    preferences: Dict

class ProjectSubmission(BaseModel):
    enterprise_id: str
    project_name: str
    description: str
    constraints: Dict

# -----------------------------
# IN-MEMORY STORAGE (V1 ONLY)
# -----------------------------

ENTERPRISES = {}
TASKS = {}
PROJECTS = {}

# -----------------------------
# HEALTH CHECK
# -----------------------------

@app.get("/")
def health():
    return {"status": "Keypass AI running"}

# -----------------------------
# ENTERPRISE CONTEXT INGESTION
# -----------------------------

@app.post("/enterprise/context")
def register_enterprise(context: EnterpriseContext):
    ENTERPRISES[context.enterprise_id] = context
    return {
        "message": "Enterprise context registered",
        "enterprise_id": context.enterprise_id
    }

# -----------------------------
# TASK SUBMISSION (CORE API)
# -----------------------------

@app.post("/tasks/submit")
def submit_task(task: TaskSubmission):
    task_id = str(uuid.uuid4())

    # Very simple capability inference (v1)
    if "email" in task.task_type.lower():
        capability = "text_generation"
    elif "extract" in task.task_type.lower():
        capability = "classification"
    else:
        capability = "general_ai"

    # Mock routing decision
    provider_selected = "mock-ai-low-cost"

    cost_usd = 0.01

    TASKS[task_id] = {
        "enterprise_id": task.enterprise_id,
        "process_id": task.process_id,
        "capability": capability,
        "provider": provider_selected,
        "cost": cost_usd
    }

    return {
        "task_id": task_id,
        "capability": capability,
        "provider_used": provider_selected,
        "cost_usd": cost_usd,
        "output": "This is a simulated AI response"
    }

# -----------------------------
# PROJECT FEASIBILITY & SCORING
# -----------------------------

@app.post("/projects/submit")
def submit_project(project: ProjectSubmission):
    project_id = str(uuid.uuid4())

    # Mock scoring of multiple AIs
    scores = [
        {
            "ai_model": "Model_A",
            "overall_score": 88,
            "notes": "High accuracy, moderate cost"
        },
        {
            "ai_model": "Model_B",
            "overall_score": 74,
            "notes": "Low cost, lower reasoning"
        }
    ]

    PROJECTS[project_id] = project

    return {
        "project_id": project_id,
        "scores": scores,
        "recommended_model": "Model_A",
        "next_step": "Run simulation or proceed to implementation"
    }

# -----------------------------
# ROI & REPORTING
# -----------------------------

@app.get("/reports/roi/{enterprise_id}")
def roi_report(enterprise_id: str):
    tasks = [
        t for t in TASKS.values()
        if t["enterprise_id"] == enterprise_id
    ]

    total_cost = sum(t["cost"] for t in tasks)
    estimated_time_saved_hours = len(tasks) * 0.2
    value_created = estimated_time_saved_hours * 50

    return {
        "enterprise_id": enterprise_id,
        "tasks_processed": len(tasks),
        "ai_spend_usd": total_cost,
        "time_saved_hours": estimated_time_saved_hours,
        "value_created_usd": value_created,
        "net_roi_usd": value_created - total_cost
    }
