from app.runtime import init_graph, run_question

g = init_graph()
route_label, result = run_question(g, "Plot revenue_millions from 2010 to 2024.")

print("ROUTE:", route_label)
print("OUTPUT:", result["output"])
print("IMAGE:", result["image_path"])