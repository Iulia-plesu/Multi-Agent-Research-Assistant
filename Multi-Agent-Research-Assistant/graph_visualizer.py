"""
Graph Visualization Utility for LangGraph Workflows
This module demonstrates how to visualize LangGraph workflows using Mermaid diagrams.
"""

from langgraph.graph import StateGraph, END
from langchain_core.runnables.graph import MermaidDrawMethod
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage
import os

class ExampleState(TypedDict):
    """Example state for demonstration purposes"""
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    step: str

def step_1(state: ExampleState) -> ExampleState:
    """Example step 1"""
    return {**state, "step": "completed_step_1"}

def step_2(state: ExampleState) -> ExampleState:
    """Example step 2"""
    return {**state, "step": "completed_step_2"}

def step_3(state: ExampleState) -> ExampleState:
    """Example step 3"""
    return {**state, "step": "completed_step_3"}

def create_example_workflow():
    """Create an example workflow for demonstration"""
    workflow = StateGraph(ExampleState)
    
    # Add nodes
    workflow.add_node("step_1", step_1)
    workflow.add_node("step_2", step_2)
    workflow.add_node("step_3", step_3)
    
    # Set entry point
    workflow.set_entry_point("step_1")
    
    # Add edges
    workflow.add_edge("step_1", "step_2")
    workflow.add_edge("step_2", "step_3")
    workflow.add_edge("step_3", END)
    
    return workflow.compile()

def visualize_workflow_graph(workflow_app, output_filename="workflow_graph.png"):
    """
    Visualize a LangGraph workflow and save as PNG
    
    This function replicates the functionality from your Jupyter notebook:
    display(
        Image(
            app.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )
        )
    )
    
    Args:
        workflow_app: Compiled LangGraph workflow
        output_filename: Name of the output PNG file
    
    Returns:
        bytes: PNG image data if successful, None if failed
    """
    try:
        # Generate the Mermaid PNG using the API method
        graph_png = workflow_app.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        
        # Save to file
        with open(output_filename, "wb") as f:
            f.write(graph_png)
        
        print(f"✅ Graph visualization saved as '{output_filename}'")
        print(f"📊 Graph shows the workflow structure with nodes and edges")
        
        return graph_png
        
    except Exception as e:
        print(f"❌ Failed to generate graph visualization: {e}")
        print("💡 Make sure you have internet connection for MermaidDrawMethod.API")
        return None

def display_graph_info(workflow_app):
    """Display information about the workflow graph"""
    graph = workflow_app.get_graph()
    
    print("🔍 WORKFLOW GRAPH INFORMATION")
    print("=" * 40)
    print(f"Number of nodes: {len(graph.nodes)}")
    print(f"Number of edges: {len(graph.edges)}")
    
    print("\n📋 Nodes:")
    for node_id in graph.nodes:
        print(f"  - {node_id}")
    
    print("\n🔗 Edges:")
    for edge in graph.edges:
        print(f"  - {edge}")
    
    print("\n🧑‍💼 Supervisor Agent Features:")
    print("  - Validates research output for completeness")
    print("  - Checks for: Price, Ingredients, Location")
    print("  - Can redirect back to research agent if needed")
    print("  - Prevents infinite loops with max 3 attempts")

def demo_graph_visualization():
    """Demonstrate the graph visualization functionality"""
    print("🚀 LangGraph Workflow Visualization Demo")
    print("=" * 50)
    
    # Create example workflow
    app = create_example_workflow()
    
    # Display graph information
    display_graph_info(app)
    
    # Generate and save visualization
    print("\n📊 Generating graph visualization...")
    visualize_workflow_graph(app, "demo_workflow.png")
    
    print("\n✨ Demo completed!")
    print("💡 You can now integrate this visualization code into your main workflow!")

if __name__ == "__main__":
    demo_graph_visualization()
