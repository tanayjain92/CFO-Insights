from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_classic.chains import LLMChain

# RAG glossary agent
def create_glossary_agent(tools):
    llm = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature = 0.1
        )
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You are a finance glossary tutor for Apple financial metrics. "
        "Use the glossary tool to look up definitions and explanations. "
        "Base your answer ONLY on the retrieved glossary content, and do not invent new facts. "
        "Explain concepts clearly and concisely in plain language."),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
        ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent = agent, tools = tools, verbose = True, return_intermediate_steps=True)
    return executor
        
# Analyst agent
def create_analyst_agent(tools):
    llm = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0.1
        )
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an expert Apple financial analyst. "
         "Use the tools to fetch accurate historical data from the horizon presented in the data. "
         "Prefer metric tools for standard trends and the SQL tool for complex filters. "
         "Always explain your reasoning in clear, logical CFO-friendly language."),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
        ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent = agent, tools = tools, verbose = True, return_intermediate_steps=True)
    return executor

# Charting agent
def create_chart_agent(tools):
    llm = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature = 0.2
        )  
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a data visualization expert. "
         "Create clear charts and briefly explain insights. "
         "Use plotting tools to generate charts whenever prompted by the user for visuals. "
         "Use metric tools to fetch data if/when needed. "
         "Keep explanations concise and focus attention on what the chart(s) show."),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad")
        ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent = agent, tools = tools, verbose = True, return_intermediate_steps=True)
    return executor

# Router chain logic
def create_router_chain():
    llm = ChatAnthropic(
        model = "claude-sonnet-4-5-20250929",    ## revert to older model (verfify this)
        temperature = 0.0
        )
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a router for an Apple financial assistant. "
         "Your job is to choose ONE route label. "
         "Respond with ONLY one of: analysis, analysis_with_chart, definition, other."),
        ("human", "{input}")
        ])
    chain = LLMChain(llm = llm, prompt = prompt)
    return chain