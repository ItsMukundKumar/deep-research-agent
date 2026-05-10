from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage, AIMessage


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # Step 1 - Search Agent
    print("\n" + "=" * 50)
    print("Step 1 - Search Agent is Working....")
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
    print("\nSearch Result:\n", state["search_results"])

    # Step 2 - Reader Agent
    print("\n" + "=" * 50)
    print("Step 2 - Reader Agent is scraping top resources ....")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        f'Based on the following search result about "{topic}",\n'
                        f'Pick the most relevant URL and scrape it for deeper content.\n\n'
                        f'Search Result:\n{state["search_results"][:2000]}'   # increased from 1000 to 2000
                    )
                )
            ]
        }
    )

    state["scraped_content"] = reader_result["messages"][-1].content
    print("\nScraped Content:\n", state["scraped_content"])

    # Step 3 - Writer Chain
    print("\n" + "=" * 50)
    print("Step 3 - Writer is drafting the report ....")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULT:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    writer_result = writer_chain.invoke(
        {
            "topic": topic,
            "research": research_combined,
        }
    )

    state["report"] = writer_result
    print("\nFinal Report:\n", state["report"])

    # Step 4 - Critic Chain
    print("\n" + "=" * 50)
    print("Step 4 - Critic is reviewing the report ....")
    print("=" * 50)

    critic_result = critic_chain.invoke(
        {
            "report": state["report"],
        }
    )

    state["feedback"] = critic_result
    print("\nCritic Report:\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic=topic)
