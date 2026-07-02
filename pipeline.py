from agent import build_search_agent, buuild_reader_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str)->dict:

    state={}

    #search agent working 
    print("\n"+" ="*50)
    print("Step 1 - seach agent is working....")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[("user",f"Find recent, reliable and detailed information about : {topic}")]
    })

    state["search_results"] = search_result['messages'][-1].content

    print("\n Search Result ",state['search_results'])

    #step 2 Reader agent
    print("\n"+" ="*50)
    print("Step 2 - Reader agent is scraping resources .....")
    print("="*50)

    reader_agent = buuild_reader_agent()
    reader_result = reader_agent.invoke({
        "messages":[("user",
        f"base on the following search resluts about'{topic}',"
        f"pick the most relevent URL and scrape it for deeper content.\n\n"
        f"Search Result:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n Scraped content",state['scraped_content'])

    #step 3 writer chain
    print("\n"+" ="*50)
    print("Step 3 Writer is draftig the report.....")
    print("="*50)

    research_combine = (
        f"Search Result : \n {state['search_results']}\n\n"
        f"Detailed Scraped Content : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combine
    })

    print("\n Final Report \n ", state["report"])

    #critic report 
    print("\n"+" ="*50)
    print("Step 4 critic is review the report.....")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state["report"]
    })
    print("\n Critic Report \n",state["feedback"])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a reseach topic : ")
    run_research_pipeline(topic)
