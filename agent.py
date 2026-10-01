from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url
from tools import web_search, scrape_url
import os 
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(
    model="openai/gpt-oss-safeguard-20b",  
    temperature=0
)

#first agent 
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

#second agent
def buuild_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="You are a specialized search agent. Your job is to find the best relevant URLs and summaries for a topic."
    )

# writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert research writer.

Create clear, structured, factual, and professional research reports.

Use the provided research and critic feedback.
Do not invent information.
"""
    ),
    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Previous Draft:
{draft}

Critic Feedback:
{critique}

Structure the final report as:

# Introduction

# Key Findings
- Finding 1
- Finding 2
- Finding 3

# Detailed Analysis

# Conclusion

# Sources

Include all relevant source URLs available in the research.

Requirements:
- Be factual and professional.
- Explain important points clearly.
- Use the research provided.
- Address the critic's feedback.
- Do not mention the AI agents or internal pipeline.
"""
    )
])

writer_chain = writer_prompt | llm | StrOutputParser()


#critic_chain 
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a senior research editor and fact-checker.

Your task is to critically evaluate the research report.

Review the report for:
- Accuracy
- Completeness
- Logical flow
- Clarity
- Depth of explanation
- Missing information
- Grammar and readability
- Proper use of sources

Do not rewrite the report.

Provide constructive feedback and actionable suggestions.
"""
    ),
    (
        "human",
        """

Research Report:
{report}

Evaluate the report using the following format:

## Overall Score
(Give a score out of 10)

## Strengths
- ...

## Weaknesses
- ...

## Missing Information
- ...

## Suggestions for Improvement
- ...

## Final Verdict
(State whether the report is Ready to Publish or Needs Revision.)
"""
    )
])

critic_chain = critic_prompt | llm | StrOutputParser()


