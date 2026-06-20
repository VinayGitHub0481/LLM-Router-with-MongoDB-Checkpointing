

from typing_extensions import TypedDict 
from langgraph.graph import StateGraph,START,END 
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field
import os

load_dotenv()

llm1=ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    api_key=os.getenv("GOOGLE_API_KEY")
)

llm2=ChatOpenAI(
    model='gpt-4.1-mini',
    api_key=os.getenv("OPENAI_API_KEY")
)


class Score(BaseModel):
    score:float=Field(...,ge=0,le=10)

class State(TypedDict):
    user_query:str 
    response:list
    final_response:str 
    score:float  

    #first node 
def first_model(state:State):
    print(f"Gemini node invoked")
    resp=llm1.invoke(state['user_query'])
    return {"response":[resp.content],"final_response":resp} 


    #Score Evaluator node 
def score_evaluator(state:State):
        print(f"Score evaluator invoked")

        structured_score=llm2.with_structured_output(Score)   #here referring to the base model  Score
    
        PROMPT=f"""

    Hey AI assistant you are a Score Evaluator Agent where you should rate the response from (0-10.0)  

    User Query:
    {state["user_query"]}

    Response:
    {state["response"]}

    NOTE: you should give the score according to the response output ONLY and ONLY from (0-10) scale

    """
        result=structured_score.invoke(PROMPT)              # so now works as score evaluator 

        obtained_score=result.score if result else 0.0      #here the response score from the llm obtained 
        
        print(obtained_score)
        
        return {"score":obtained_score,"response":state['response']}


    #conditional edge [here routing takes place based on the Score evaluator node]
def route(state:State):
        print(f"Routing based on score...")
        if (state['score']<8.5):
            return "chat-gpt"
        return END    #return to end edge if score is satisfied  


    #third node
def conditional_model(state:State):
        print(f"GPT fallback node...")
        resp=llm2.invoke(state['user_query'])

        return {"response":[resp.content],"final_response":resp,"score":state['score']}


graph=StateGraph(State)   #this object carries the state through the nodes 

#nodes 
graph.add_node("gemini",first_model)
graph.add_node("score-evaluator",score_evaluator)
graph.add_node("chat-gpt",conditional_model)

#edges
graph.add_edge(START,"gemini") #edges starts and goes to gemini 
graph.add_edge("gemini","score-evaluator")
graph.add_conditional_edges("score-evaluator",route,{

    "chat-gpt":"chat-gpt",   #here from the route return type:node 
    END:END

})
graph.add_edge("chat-gpt",END)   #so here after the routing it comes to the gpt and goes to end 



#MongoDB checkpointer
URL='mongodb://admin:admin@localhost:27017'

with MongoDBSaver.from_conn_string(URL) as checkpoint:
        persistent_data=graph.compile(checkpointer=checkpoint)  #here state management persistantly takes place using checkpointer(mongodb saver)

        config={
            "configurable":{
                "thread_id":"A123"
            }
        }

        while True:
            Query=input("Ask your query:")

            if Query.lower()=="exit":
                break

            for chunk in persistent_data.stream({"user_query": Query}
                                                ,config=config,stream_mode="values"):
                if "final_response" in chunk :
                 print(chunk["response"][-1])

































