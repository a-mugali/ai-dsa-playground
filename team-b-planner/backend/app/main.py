import json
import logging
import os
from typing import Dict, List

from app.core.difficulty import update_difficulty
from app.core.loader import load_problems
from app.core.scheduler import generate_plan
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ---------------------------------
# App Setup
# ---------------------------------

app = FastAPI(title="AI Practice Planner")

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
PROBLEM_FILE = os.path.join(DATA_DIR, "problems.json")
DIFF_FILE = os.path.join(DATA_DIR, "difficulty.json")


# ---------------------------------
# Request Models
# ---------------------------------


class PlanRequest(BaseModel):
    time: int
    min_d: int
    max_d: int


class FeedbackItem(BaseModel):
    problem_id: int
    feedback: str


class FeedbackRequest(BaseModel):
    feedback: List[FeedbackItem]


# ---------------------------------
# Helper Functions
# ---------------------------------


def load_difficulty() -> Dict[str, int]:

    if not os.path.exists(DIFF_FILE):
        return {}

    with open(DIFF_FILE, "r") as f:
        return json.load(f)


def save_difficulty(data: Dict[str, int]) -> None:

    with open(DIFF_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ---------------------------------
# API Routes
# ---------------------------------


@app.get("/")
def health_check():
    return {"status": "Planner backend running"}


@app.post("/generate_plan")
def generate(req: PlanRequest):

    logging.info("Generate plan request received")

    if req.min_d > req.max_d:
        raise HTTPException(
            status_code=400, detail="min_d cannot be greater than max_d"
        )

    try:
        problems = load_problems(PROBLEM_FILE)

        plan = generate_plan(problems, req.time, req.min_d, req.max_d)

        logging.info(f"Generated plan with {len(plan)} problems")

        return plan

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(status_code=500, detail="Failed to generate plan")


@app.post("/feedback")
def submit_feedback(req: FeedbackRequest):

    logging.info("Feedback received")

    try:
        difficulty_map = load_difficulty()

        for item in req.feedback:

            pid = str(item.problem_id)

            old = difficulty_map.get(pid, 5)

            new = update_difficulty(old, item.feedback)

            difficulty_map[pid] = new

        save_difficulty(difficulty_map)

        logging.info("Difficulty updated")

        return {"message": "Feedback saved successfully"}

    except Exception as e:

        logging.error(str(e))

        raise HTTPException(status_code=500, detail="Failed to save feedback")
