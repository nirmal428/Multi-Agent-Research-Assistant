from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url
import os 
from dotenv import load_dotenv

load_dotenv()

llm=ChatGroq(
    model="llama-3.3-70b-versatile",  
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
        tools=[scrape_url]
    )

# writer chain 
writer_prompt=ChatPromptTemplate.from_messages([
    ("system","you are an expert research writer. write clear, structured and insightful reports."),
    ("human","""write a detailed research report on the topic below
     
     Topic :{topic}

     research Gathered: {research}


     Structure of the report as:
     - Introduction
     - key Finding (minimum 3 well-explained points)
     -Conclusion
     -Sources (list all urls )


     Be detailed, factual and professional.
     """)
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