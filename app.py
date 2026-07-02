import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Multi-Agent Research Assistant")
st.markdown("Research any topic using Search Agent → Reader Agent → Writer → Critic")

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Artificial Intelligence in Healthcare"
)

if st.button("Start Research", use_container_width=True):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

    with st.spinner("Running Multi-Agent Research..."):
        result = run_research_pipeline(topic)

    st.success("Research Completed!")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Search Results",
            "Scraped Content",
            "Final Report",
            "Critic Feedback"
        ]
    )

    with tab1:
        st.subheader("🔍 Search Agent")
        st.write(result["search_results"])

    with tab2:
        st.subheader("📄 Reader Agent")
        st.write(result["scraped_content"])

    with tab3:
        st.subheader("📝 Writer Agent")
        st.markdown(result["report"])

    with tab4:
        st.subheader("✅ Critic Agent")
        st.markdown(result["feedback"])

    st.download_button(
        "⬇ Download Report",
        data=result["report"],
        file_name="research_report.md",
        mime="text/markdown",
    )