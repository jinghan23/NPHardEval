# ref: https://github.com/composable-models/llm_multiagent_debate/tree/main

from data import Data
from models import *
from experiement import * # this will later becomes games.py
from prompts import reasoningPrompts as r, feedbackPrompts as f
import wikipediaapi

# Helpers
def Game():
    return "Describe the solution to a quadratic equation."

def Model(model_name):
    if model_name == "GPT-3.5":
        return AzureGPT()
    # elif model_name == "GPT-4":
    #     return GPT4()
    elif model_name == "AzureFalcon":
        return AzureFalconDeployment('40b')
    elif model_name == "GooglePaLM":
        return GooglePaLM()
    # elif model_name == "Claude":
    #     return Claude()
    # elif model_name == "LLaMa":
    #     return LLaMa()
    else:
        return "Model not found."


def Wiki(prompt):
    # Search on Wikipedia api
    # Create a Wikipedia object for the specified language
    wiki_wiki = wikipediaapi.Wikipedia('en')

    # Search for the query
    page = wiki_wiki.page(prompt)

    # Check if the page exists
    if not page.exists():
        return "No relevant information found on Wikipedia for query: " + prompt
    
    return page.summary

def Check(game, result):
    correct_answer = "x = (-b ± √(b^2-4ac)) / 2a" # TBD
    return result == correct_answer

### Agents
def peerMentor(llm_model, wrong_answer, main_player_question):
    mentor_prompt = f['Mentor'] + wrong_answer + main_player_question
    return llm_model(mentor_prompt)

def peerLearner(llm_model, wrong_answer, main_player_question):
    learner_prompt = f['Learner'] + wrong_answer + main_player_question
    return llm_model(learner_prompt)

def peerWiki(llm_model, main_player_question):
    wiki_result = Wiki(main_player_question)
    wiki_prompt = f['Wiki'] + wiki_result
    return llm_model(wiki_prompt)

def mainPlayerReasoning(llm_model, game_description, r):
    # should set different version for different tasks
    prompt_text = r['Intro'] + '\n' \
            + r['Initial_question'].format(max_vertices=number_of_vertices,max_colors=chromatic_number) + '\n' \
            + r['Output_content'] + '\n' \
            + r['Option_with_reasoning'] + \
            '\n The data is below: \n'
    m = llm_model(game_description, prompt_text) # main player response
    return m

def mainPlayerQuestion(game_description, wrong_answer, question_to):
    if question_to == "mentor":
        prompt = f['Main_q_mentor']
    elif question_to == "learner":
        prompt = f['Main_q_learner']
    elif question_to == "wiki":
        prompt = f['Main_q_wiki']
    main_player_prompt = wrong_answer + prompt
    q =  Model(game_description, main_player_prompt)
    return q


### Main
def main():
    llm_model = Model("GPT-3.5")

    game_description = Game()

    number_of_rounds = 3
    records = []

    for i in range(number_of_rounds):
        m = mainPlayerReasoning(llm_model, game_description, r)
        
        if i == number_of_rounds - 1:
            records.append({"main_player": m})
        else:
            # if correct
            if Check(game_description, m):
                records.append({"main_player": m})
                exit()
            # if incorrect, ask question to peers
            wrong_answer = m
            peer_mentor_advice = peerMentor(llm_model, m, mainPlayerQuestion(game_description, wrong_answer, "mentor"))
            peer_learner_discuss = peerLearner(llm_model, m, mainPlayerQuestion(game_description, wrong_answer, "learner"))
            wiki_info = peerWiki(mainPlayerQuestion(llm_model, game_description, wrong_answer, "wiki"))
            records.append({
                "main_player": m,
                "peer_mentor": peer_mentor_advice,
                "peer_learner": peer_learner_discuss,
                "peer_wiki": wiki_info
            })

    return records

if __name__ == "__main__":
    results = main()
    print(results)

