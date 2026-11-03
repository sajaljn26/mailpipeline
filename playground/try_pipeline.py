import sys
from pathlib import Path
import nest_asyncio

# Force UTF-8 for Windows consoles to avoid 'charmap' encoding errors
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(str(Path(__file__).resolve().parents[1]))
nest_asyncio.apply()

from app.ai.decide import decide

question = "Panel 4 of my HP-S3 is cracked. Order 112-4839201-5528341"

try:
    decision = decide(question)
    print("--- DECISION ---")
    # Use model_dump_json and ensure it's printed as utf-8
    print(decision.model_dump_json(indent=2))
except Exception as e:
    print(f"Error occurred: {e}")
