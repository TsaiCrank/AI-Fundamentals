"""Connecting Nodes with Edges - Building your first graph"""

import os
import time
from typing import TypedDict
from langgraph.graph import StateGraph, END

# ┌──────────────────────────────────────┐
# │   Building Your First Graph          │
# └──────────────────────────────────────┘
#
#  Step 1: Create Graph Container
#  ┌──────────────────────────────┐
#  │     StateGraph(State)        │
#  │  Container for your workflow │
#  └──────────────────────────────┘
#                │
#  Step 2: Register Functions as Nodes
#     ┌──────────┴──────────┐
#     │   add_node()        │
#     │  "greet" → func     │
#     │  "enhance" → func   │
#     └─────────────────────┘
#
#  Step 3: Connect with Edges
#  ╔═══════════════════════════╗
#  ║    Execution Flow:        ║
#  ╟───────────────────────────╢
#  ║      [START]              ║
#  ║         │                 ║
#  ║         ▼                 ║
#  ║   ┌─────────────┐         ║
#  ║   │    greet    │         ║
#  ║   │ (greet_node)│         ║
#  ║   └──────┬──────┘         ║
#  ║          │ add_edge       ║
#  ║          ▼                ║
#  ║   ┌─────────────┐         ║
#  ║   │   enhance   │         ║
#  ║   │(enhance_node)│        ║
#  ║   └──────┬──────┘         ║
#  ║          │                ║
#  ║          ▼                ║
#  ║       [END]               ║
#  ╚═══════════════════════════╝
#
# KEY CONCEPT: add_node() registers functions
# add_edge() defines execution order

# Define our state
class State(TypedDict):
    name: str
    greeting: str

# Our nodes from node_creation.py (now with timing)
def greet_node(state: State):
    """Creates initial greeting"""
    print("  🔄 Processing in greet_node...")
    time.sleep(2)  # Helps visualize execution flow
    greeting = f"Hello, {state['name']}!"
    return {"greeting": greeting}

def enhance_node(state: State):
    """Enhances the greeting"""
    print("  🔄 Processing in enhance_node...")
    time.sleep(2)  # Helps visualize execution flow
    enhanced = state["greeting"] + " Welcome to LangGraph!"
    return {"greeting": enhanced}

# NOW we build a graph!
print("Building your first graph:\n")

# Create a StateGraph with our State
workflow = StateGraph(State)

# Add nodes to the graph
# Hint: Use add_node method
workflow.add_node("greet", greet_node)
workflow.add_node("enhance", enhance_node)

# Connect nodes with edges
workflow.set_entry_point("greet")
workflow.add_edge("greet", "enhance")
workflow.add_edge("enhance", END)

# Compile the graph
print("Compiling graph...")
app = workflow.compile()
print("✅ Graph compiled successfully!\n")

# Run the graph!
print("Running the graph:")
result = app.invoke({"name": "Bob", "greeting": ""})

print(f"\nFinal result: {result}")

print("💡 KEY CONCEPTS:")
print("- StateGraph: Container for your workflow")
print("- add_node: Registers a function as a node")
print("- set_entry_point: Where execution starts")
print("- add_edge: Connects nodes (A → B)")
print("- END: Special marker for final node")
print("- compile: Converts graph to executable app")
