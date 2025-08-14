## Project Title: Build a Multi-Agent Research Assistant

**Collaborators:**

- [vld2405](https://github.com/vld2405)
- [Mantelgen](https://github.com/Mantelgen)

**Description:**

This project aims to develop a multi-agent system using LangGraph and Gemini. The system will consist of four specialized agents:

* **Researcher Agent:** This agent will be responsible for gathering information on a specified topic using a search tool.
* **Supervisor Agent:** This agent validates research output to ensure it contains required compact information (price, ingredients, location).
* **Writer Agent:** This agent will synthesize the findings from the Researcher Agent into a structured summary, which can be formatted as a markdown report or a JSON object.
* **Food Critic Agent:** This specialized agent reviews the final report focusing on BIO/organic ingredients, fresh produce, and local meat sourcing standards.

Additional components will be integrated throughout the development process.

**Requirements:**

The project requires the use of **LangChain** and **LangGraph**. For the Language Model, you can choose a **Gemini model** from the available options. Using **Ollama** for the LLM will earn bonus points.

**Main Steps for Guidance:**

1.  **Architectural Design:** Begin by conceptualizing the application's flow and identifying the necessary nodes for the graph.
2.  **State Object Creation:** Define the state object that will manage information across the agents.
3.  **Function Development:** Write the individual functions that will interact with your chosen initialized LLM.
4.  **Graph Construction:** Connect these functions to form the LangGraph, with each function serving as a distinct node.

## Features

### Graph Visualization 📊
The project includes graph visualization functionality that generates a visual representation of the workflow:

```python
# Generate workflow graph visualization
graph_png = app.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API,
)

# Save to file
with open("workflow_graph.png", "wb") as f:
    f.write(graph_png)
```

This creates a Mermaid diagram showing:
- All workflow nodes (agents)
- Connections between nodes
- Flow direction
- Entry and exit points

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Iulia-plesu/Multi-Agent-Research-Assistant
   cd Multi-Agent-Research-Assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **View workflow visualization:**
   ```bash
   python graph_visualizer.py
   ```

## Project Structure

```
Multi-Agent-Research-Assistant/
├── main.py                      # Main application with 4-agent workflow
├── graph_visualizer.py          # Graph visualization utilities
├── requirements.txt             # Project dependencies
├── .env.example                # Environment variables template
├── README.md                   # Project documentation
├── workflow_graph.png          # Generated workflow visualization
├── shaorma_research_report.md  # Complete report with critic analysis
└── food_critic_review.md       # Separate food critic review
```

## Usage

The application will:
1. Ask for a country to research
2. Collect your interests
3. **Research Agent** gathers information about shaorma places
4. **Supervisor Agent** validates the research for completeness:
   - Checks if each restaurant has: **Price**, **Ingredients**, **Location**
   - If incomplete, sends back to Research Agent (max 3 attempts)
   - If complete, approves and sends to Writing Agent
5. **Writing Agent** creates a markdown report
6. **Food Critic Agent** reviews the report with focus on:
   - 🌱 **BIO/Organic ingredients**
   - 🥬 **Fresh produce standards**
   - 🥩 **Local meat sourcing**
   - 📊 **Overall sustainability ratings**
7. Save the enhanced report and generate workflow visualization

### Supervisor Agent Features 🧑‍💼
- **Quality Control**: Ensures research contains essential details
- **Validation Criteria**: Price, Ingredients, Location for each restaurant
- **Feedback Loop**: Can request more compact research if needed
- **Safety Mechanism**: Maximum 3 research attempts to prevent infinite loops

### Food Critic Agent Features 👨‍🍳
- **Sustainability Focus**: Reviews for organic and local sourcing
- **Quality Standards**: Evaluates BIO ingredients and freshness
- **Professional Analysis**: Provides expert food critic perspective
- **Ratings & Recommendations**: Scores restaurants and suggests improvements

Generated files:
- `shaorma_research_report.md` - Complete report with critic analysis
- `food_critic_review.md` - Separate food critic review
- `workflow_graph.png` - Visual workflow diagram


