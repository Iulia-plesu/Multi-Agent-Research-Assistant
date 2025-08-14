from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.graph import MermaidDrawMethod
from dotenv import load_dotenv
import os

# Multi-agent research assistant with four specialized agents:
# Agent 1: Research Agent - Gathers information on shaorma places
# Agent 2: Supervisor Agent - Validates research completeness (price, ingredients, location)
# Agent 3: Writing Agent - Creates structured markdown reports
# Agent 4: Food Critic Agent - Reviews for BIO ingredients, fresh produce, and local meat sourcing

class ResearchState(TypedDict):
    messages: Annotated[List[HumanMessage | AIMessage], "The messages in the conversation"]
    country: str
    interests: List[str]
    research_findings: str
    report: str
    research_approved: bool
    research_attempts: int
    critic_review: str
    final_report: str

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY")
)

# Define prompts for research, supervisor, and writing agents
research_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful research assistant. Gather information about the best shaorma in {country} based on the user's interests: {interests}. Provide detailed reviews for each result with specific restaurant names, locations, prices, and ingredients. Make sure to include PRICE, INGREDIENTS, and LOCATION for each restaurant."),
    ("human", "Research the best shaorma places in {country} focusing on these interests: {interests}. Provide comprehensive information including price, ingredients, and location for each restaurant."),
])

supervisor_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a quality control supervisor. Review the research findings and check if they only contain the required compact information for each restaurant: PRICE, INGREDIENTS, and LOCATION. Respond with 'APPROVED' if all restaurants have these three details, or 'REJECTED' if any restaurant is missing price, ingredients, or location information or contains extraneous details. Only essential information, without any additional commentary or explanations.    "),
    ("human", "Review these research findings and check if they contain price, ingredients, and location for each restaurant: {research_findings}"),
])

writing_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional writing assistant. Create a well-structured markdown report based on the research findings provided. Include headings, bullet points, and organize the information clearly."),
    ("human", "Write a comprehensive markdown report based on these research findings: {research_findings}"),
])

food_critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the food critic Gordon Ramsay with expertise in sustainable and organic dining. Review the shaorma report and provide a critical analysis focusing on: 1) Whether ingredients are BIO/organic and fresh, 2) Whether meat is sourced locally, 3) Overall quality and sustainability standards. Rate each restaurant and provide recommendations for improvement. Be thorough and professional in your critique. Give it a rating out of 5 stars."),
    ("human", " Please review this shaorma research report and provide your expert food critic analysis focusing on BIO ingredients, fresh produce, and local meat sourcing: {report}"),
])

def input_country(state: ResearchState) -> ResearchState:
    """Agent function to collect country input from user"""
    print("Please enter the country you want to find the best shaorma in:")
    user_message = input("Your input: ")
    return {
        **state,
        "country": user_message,
        "messages": state['messages'] + [HumanMessage(content=user_message)],
    }

def input_interests(state: ResearchState) -> ResearchState:
    """Agent function to collect interests input from user"""
    print(f"Please enter your interests for shaorma in {state['country']} (comma-separated):")
    user_message = input("Your input: ")
    interests = [interest.strip() for interest in user_message.split(",")]
    return {
        **state,
        "interests": interests,
        "messages": state['messages'] + [HumanMessage(content=user_message)],
    }

def research_agent(state: ResearchState) -> ResearchState:
    """Research Agent: Gathers information about shaorma places"""
    attempt = state.get('research_attempts', 0) + 1
    
    if attempt > 1:
        print(f"🔍 Research Agent: Re-gathering information (attempt {attempt}) with more focus on price, ingredients, and location...")
    else:
        print(f"🔍 Research Agent: Gathering information about shaorma in {state['country']}...")
    
    response = llm.invoke(research_prompt.format_messages(
        country=state['country'],
        interests=", ".join(state['interests'])
    ))
    print("✅ Research completed!")
    return {
        **state,
        "research_findings": response.content,
        "research_attempts": attempt,
        "research_approved": False,  # Reset approval status
        "messages": state['messages'] + [AIMessage(content=response.content)],
    }

def supervisor_agent(state: ResearchState) -> ResearchState:
    """Supervisor Agent: Validates research output for required compact information"""
    print("🧑‍💼 Supervisor Agent: Reviewing research findings for completeness...")
    
    response = llm.invoke(supervisor_prompt.format_messages(
        research_findings=state['research_findings']
    ))
    
    approval_decision = "APPROVED" in response.content.upper()
    
    if approval_decision:
        print("✅ Supervisor: Research findings approved - contains price, ingredients, and location")
    else:
        print("❌ Supervisor: Research findings rejected - missing price, ingredients, or location details")
        print("🔄 Requesting more compact research...")
    
    return {
        **state,
        "research_approved": approval_decision,
        "messages": state['messages'] + [AIMessage(content=f"Supervisor review: {response.content}")],
    }

def should_continue_research(state: ResearchState) -> str:
    """Conditional edge function to determine next step after supervisor review"""
    if state['research_approved']:
        return "writing_agent"
    else:
        # Prevent infinite loops - max 3 attempts
        if state.get('research_attempts', 0) >= 3:
            print("⚠️ Maximum research attempts reached, proceeding to writing agent...")
            return "writing_agent"
        return "research_agent"

def writing_agent(state: ResearchState) -> ResearchState:
    """Writing Agent: Creates markdown report from research findings"""
    print("📝 Writing Agent: Creating markdown report...")
    response = llm.invoke(writing_prompt.format_messages(
        research_findings=state['research_findings']
    ))
    print("✅ Report completed!")
    return {
        **state,
        "report": response.content,
        "messages": state['messages'] + [AIMessage(content=response.content)],
    }

def food_critic_agent(state: ResearchState) -> ResearchState:
    """Food Critic Agent: Reviews report for BIO ingredients, fresh produce, and local meat sourcing"""
    print("👨‍🍳 Food Critic Agent: Analyzing report for quality standards...")
    print("   🌱 Checking for BIO/organic ingredients")
    print("   🥩 Verifying local meat sourcing")
    print("   🥬 Assessing freshness standards")
    
    response = llm.invoke(food_critic_prompt.format_messages(
        report=state['report']
    ))
    
    print("✅ Food critic analysis completed!")
    
    # Combine original report with critic review
    final_report = f"{state['report']}\n\n---\n\n## 👨‍🍳 Food Critic Review\n\n{response.content}"
    
    return {
        **state,
        "critic_review": response.content,
        "final_report": final_report,
        "messages": state['messages'] + [AIMessage(content=f"Food Critic Review: {response.content}")],
    }

def display_results(state: ResearchState) -> ResearchState:
    """Display the final report with critic review and save to file"""
    print("\n" + "="*60)
    print("📄 FINAL REPORT WITH FOOD CRITIC ANALYSIS")
    print("="*60)
    print(state['final_report'])
    print("\n" + "="*60)
    
    # Save final report to file
    with open("shaorma_research_report.md", "w", encoding="utf-8") as f:
        f.write(state['final_report'])
    print("💾 Final report with critic review saved to 'shaorma_research_report.md'")
    
    # Also save just the critic review separately
    with open("food_critic_review.md", "w", encoding="utf-8") as f:
        f.write(f"# Food Critic Review\n\n{state['critic_review']}")
    print("👨‍🍳 Food critic review saved separately to 'food_critic_review.md'")
    
    return state

def visualize_graph(workflow_app):
    """Function to visualize the workflow graph and save as PNG"""
    try:
        # Generate the graph visualization
        graph_png = workflow_app.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        
        # Save the graph to a file
        with open("workflow_graph.png", "wb") as f:
            f.write(graph_png)
        
        print("📊 Workflow graph saved as 'workflow_graph.png'")
        return graph_png
        
    except Exception as e:
        print(f"⚠️ Could not generate graph visualization: {e}")
        return None

# Create the workflow
def create_workflow():
    """Create and compile the LangGraph workflow"""
    workflow = StateGraph(ResearchState)
    
    # Add nodes (agents)
    workflow.add_node("input_country", input_country)
    workflow.add_node("input_interests", input_interests)
    workflow.add_node("research_agent", research_agent)
    workflow.add_node("supervisor_agent", supervisor_agent)
    workflow.add_node("writing_agent", writing_agent)
    workflow.add_node("food_critic_agent", food_critic_agent)
    workflow.add_node("display_results", display_results)
    
    # Set entry point
    workflow.set_entry_point("input_country")
    
    # Add edges (flow)
    workflow.add_edge("input_country", "input_interests")
    workflow.add_edge("input_interests", "research_agent")
    workflow.add_edge("research_agent", "supervisor_agent")
    
    # Add conditional edge from supervisor
    workflow.add_conditional_edges(
        "supervisor_agent",
        should_continue_research,
        {
            "research_agent": "research_agent",
            "writing_agent": "writing_agent"
        }
    )
    
    workflow.add_edge("writing_agent", "food_critic_agent")
    workflow.add_edge("food_critic_agent", "display_results")
    workflow.add_edge("display_results", END)
    
    return workflow.compile()

def run_research_assistant(user_request: str = "I want to find the best shaorma places"):
    """Main function to run the research assistant"""
    print(f"🚀 Starting Multi-Agent Research Assistant")
    print(f"📋 Initial Request: {user_request}\n")
    
    # Initialize state
    initial_state = {
        "messages": [HumanMessage(content=user_request)],
        "country": "",
        "interests": [],
        "research_findings": "",
        "report": "",
        "research_approved": False,
        "research_attempts": 0,
        "critic_review": "",
        "final_report": "",
    }
    
    # Create and visualize the workflow
    app = create_workflow()
    
    # Generate and save workflow visualization
    visualize_graph(app)
    
    # Run the workflow
    print("🔄 Executing workflow...\n")
    for output in app.stream(initial_state):
        pass  # The nodes handle their own printing
    
    print("\n✅ Research Assistant workflow completed!")

if __name__ == "__main__":
    # Run the research assistant
    run_research_assistant()
