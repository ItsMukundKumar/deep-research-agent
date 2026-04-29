from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage, AIMessage


def run_research_pipeline(topic: str) -> dict:

    state = {}
    # search agent working
    print("\n" + "=" * 50)
    print("Step 1 - search agent is Working....")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"Find recent, reliable and detailed information about: {topic}"
                )
            ]
        }
    )
    state["search_results"] = search_result["messages"][-1].content

    print("\nsearch result : \n", state["search_results"])

    # reader Agent
    print("\n" + "=" * 50)
    print("Step 2 - Reader Agent is scraping top recources ....")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    f'Based on the following search result about "{topic}",\nPick the most relevent URL and scrabe it for deeper content.\n\nSearch Result : \n{state['search_results'][:1000]}'
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScaped Content : \n", state["scraped_content"])

    # Writer Chain
    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report ....")
    print("=" * 50)
    
    research_combined = (
        f'SEARCH RESULT : \n {state['search_results']} \n\n'
        f'DETAILED SCRAPED CONTENT : \n {state['scraped_content']}'
    )
    
    writer_result = writer_chain.invoke(
        {
            'topic' : topic,
            'research' : research_combined
        }
    )
    
    state['report'] = writer_result
    
    print('\n Final Report\n',state['report'])
    
    # critic report 
    print("\n" + "=" * 50)
    print("Step 4 - critic is reviewing the report ....")
    print("=" * 50)

    critic_result = critic_chain.invoke(
        {
            'report' : state['report']
        }
    )
    
    state['feedback'] = critic_result
    
    print('\n Critic Report : \n', state['feedback'])
    
    return state

if __name__ == "__main__":
    topic = input('\nEnter a research topic : ')
    run_research_pipeline(topic=topic)
    