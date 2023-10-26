reasoningPrompts = {
    "Intro":"Graph coloring refers to the problem of coloring vertices of a graph in such a way that no two adjacent vertices have the same color. ",
    "Initial_question":"There are {max_vertices} vertices 1 to {max_vertices} in a graph. You may use {max_colors} colors A, B, and C to color the graph.",
    "Output_content":"Please label every vertex, even if it is disconnected from the rest of the graph. Please provide each vertex's color. Do not skip any vertices. Each color must be provided on a new line in the response and should be formatted as '{VERTEX NUMBER}:{VERTEX COLOR ASSIGNMENT}'.",
    "Option_no_reasoning":"You should not provide anything beyond the answer. You output should be in the format '{'Answer': a list of '{VERTEX NUMBER}:{VERTEX COLOR ASSIGNMENT}'.",
    "Option_with_reasoning":"You should also provide your step by step reasoning. You output should be in the format '{'Answer': a list of '{VERTEX NUMBER}:{VERTEX COLOR ASSIGNMENT}','Reasoning: a step by step walk through'}'.",
    "Wrong_answer":"This is incorrect. Using the feedback, please try again."
}

feedbackPrompts = {
    "Mentor":"Provide feedback for what and why the result is wrong. Can also provide high-level methodology guidence.", # simulated teacher feedback [a novel contribution]
    "Learner":"Discuss about the wrong answer", # traditional self correction
    "Wiki":"Share external knowledge without sharing the correct answer.", # tool
    "Main_q_mentor":"",
    "Main_q_learner":"",
    "Main_q_wiki":"",
}

# RQ: pattern - check which and where is the dominaent strategy discovered.
# RQ: pattern - check if more communication quantity lead to more correct answer or easier discovery of dominent strategy.
