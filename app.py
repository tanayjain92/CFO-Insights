import os
import streamlit as st
from app.runtime import init_graph, run_question

@st.cache_resource      #cache graph / session because this is taking too much time and memory
def get_graph():
    return init_graph()

def extract_chart_paths(result):
    paths = []
    seen = set()
    image_path = result.get("image_path")
    if image_path and os.path.exists(image_path):
        paths.append(image_path)
        seen.add(image_path)
    steps = result.get("intermediate_steps", [])
    for action, observation in steps:
        tool_name = getattr(action, "tool", "")
        if tool_name in {"plot_metric_over_time_tool", "plot_multi_metrics_over_time_tool"}:
            if isinstance(observation, dict):
                img_path = observation.get("image_path")
                if img_path and os.path.exists(img_path) and img_path not in seen:
                    paths.append(img_path)
                    seen.add(img_path)
    return paths

def main():
    st.title("CFO Insights Apple Financials - Multi-Agent Demo")
    graph = get_graph()
    question = st.text_area(
        "Ask a question about Apple's financials:",
        placeholder="Example: Compare revenue and net income trends from 2010 to 2024, or get charts, or ask for definitions like 'what is net profit margin?'.",
        height=120,
    )
    
    if st.button("Run analysis") and question.strip():
        with st.spinner("Thinking..."):
            route, result = run_question(graph, question.strip())
        st.markdown(f"**Route selected:** `{route}`")
        output = result.get("output") or result.get("answer") or str(result)            #from agent executor? (verify this + return should be a dictionary)
        st.markdown("### Answer")
        st.write(output)
        if route == "analysis_with_chart":
            chart_paths = extract_chart_paths(result)
            if chart_paths:
                st.markdown("### Chart(s)")
                for p in chart_paths:
                    st.image(p, caption=os.path.basename(p))
            else:
                st.info("No chart images found in tool outputs.")

if __name__ == "__main__":
    main()