from agent import (
    build_search_agent,
    buuild_reader_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:

    print("\n" + "=" * 60)
    print("MULTI-AGENT RESEARCH PIPELINE")
    print("=" * 60)

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    state = {
        "topic": topic,
        "search_result": None,
        "sources": [],
        "research_content": "",
        "draft": "",
        "critique": "",
        "answer": ""
    }

    # =========================================================
    # STEP 1 - SEARCH AGENT
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 1 - SEARCH AGENT")
    print("=" * 60)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Research the following topic:

{topic}

Find reliable and relevant information.
Return useful sources and important information that
can be used by another agent for writing the final report.
"""
            )
        ]
    })

    state["search_result"] = search_result

    print("\nSearch agent completed.")

    # ---------------------------------------------------------
    # Extract search content
    # ---------------------------------------------------------

    if isinstance(search_result, dict):

        messages = search_result.get("messages", [])

        if messages:
            search_content = messages[-1].content

        else:
            search_content = str(search_result)

    else:
        search_content = str(search_result)

    state["research_content"] = search_content

    # ---------------------------------------------------------
    # Sources
    # ---------------------------------------------------------

    sources = []

    if isinstance(search_result, dict):

        # If your search agent returns sources
        sources = search_result.get("sources", [])

        # If sources are inside another key
        if not sources:
            sources = search_result.get("urls", [])

    state["sources"] = sources

    print(f"Sources found: {len(sources)}")

    # =========================================================
    # STEP 2 - READER AGENT
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 2 - READER AGENT")
    print("=" * 60)

    reader_agent = buuild_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Topic:

{topic}

Here is the information collected by the Search Agent:

{search_content}

Read and analyze this information carefully.

Extract:
- Important facts
- Key points
- Relevant evidence
- Important statistics
- Useful information for the final report

Do not add unsupported information.
"""
            )
        ]
    })

    print("\nReader agent completed.")

    # ---------------------------------------------------------
    # Extract reader output
    # ---------------------------------------------------------

    if isinstance(reader_result, dict):

        messages = reader_result.get("messages", [])

        if messages:
            reader_content = messages[-1].content

        else:
            reader_content = str(reader_result)

    else:
        reader_content = str(reader_result)

    state["research_content"] = reader_content

    # =========================================================
    # STEP 3 - WRITER
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 3 - WRITER AGENT")
    print("=" * 60)

    writer_result = writer_chain.invoke({
        "topic": topic,
        "research": reader_content
    })

    print("\nWriter completed.")

    # ---------------------------------------------------------
    # Extract writer output
    # ---------------------------------------------------------

    if hasattr(writer_result, "content"):
        draft = writer_result.content

    elif isinstance(writer_result, dict):

        if "text" in writer_result:
            draft = writer_result["text"]

        elif "content" in writer_result:
            draft = writer_result["content"]

        else:
            draft = str(writer_result)

    else:
        draft = str(writer_result)

    state["draft"] = draft

    # =========================================================
    # STEP 4 - CRITIC
    # =========================================================

    print("\n" + "=" * 50)
    print("Step 4 - Critic Agent is working...")
    print("=" * 50)

    critic_result = critic_chain.invoke({
        "report": draft
    })

    critique = critic_result   

    print("\nCritic feedback generated successfully.")

    # ---------------------------------------------------------
    # Extract critic output
    # ---------------------------------------------------------

    if hasattr(critic_result, "content"):
        critique = critic_result.content

    elif isinstance(critic_result, dict):

        if "text" in critic_result:
            critique = critic_result["text"]

        elif "content" in critic_result:
            critique = critic_result["content"]

        else:
            critique = str(critic_result)

    else:
        critique = str(critic_result)

    state["critique"] = critique

    # =========================================================
    # STEP 5 - FINAL ANSWER
    # =========================================================

    print("\n" + "=" * 60)
    print("STEP 5 - FINAL REPORT")
    print("=" * 60)

    final_result = writer_chain.invoke({
        "topic": topic,
        "research": f"""
Research:

{reader_content}

Original Draft:

{draft}

Critic Feedback:

{critique}

Rewrite the report using the critic's feedback.

Requirements:
- Answer the user's topic directly
- Use the research information
- Correct issues identified by the critic
- Do not invent facts
- Keep the answer clear and structured
- Include important sources when available
"""
    })

    # ---------------------------------------------------------
    # Extract final answer
    # ---------------------------------------------------------

    if hasattr(final_result, "content"):
        final_answer = final_result.content

    elif isinstance(final_result, dict):

        if "text" in final_result:
            final_answer = final_result["text"]

        elif "content" in final_result:
            final_answer = final_result["content"]

        else:
            final_answer = str(final_result)

    else:
        final_answer = str(final_result)

    state["answer"] = final_answer

    print("\nFinal report generated successfully.")

    # =========================================================
    # RETURN RESULT
    # =========================================================

    return {
        "topic": topic,
        "answer": final_answer,
        "sources": sources,
        "research": reader_content,
        "draft": draft,
        "critique": critique
    }