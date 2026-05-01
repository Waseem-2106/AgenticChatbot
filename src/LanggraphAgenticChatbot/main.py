import streamlit as st
from src.LanggraphAgenticChatbot.ui.streamlit.loadui import LoadStreamlitUI
from src.LanggraphAgenticChatbot.LLMs.groqllm import GroqLLM
from src.LanggraphAgenticChatbot.graph.graph_builder import GraphBuilder
from src.LanggraphAgenticChatbot.ui.streamlit.display_result import DisplayResultStreamlit




def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph Agentic Ai application with streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph bases on the selected use case, and display the output while
    implementing exception handling for rebustness
    
    
    """
    ##Load UI
    ui=LoadStreamlitUI()
    user_input=ui.load_streamlit_ui()

    if not user_input:
        st.error("Enter: failed to load user input from The UI.")
        return
    
    ##Text input for user message
    if st.session_state.IsFetchButtonClicked:
        user_message=st.session_state.timeframe
    else:
        user_message=st.chat_input("Enter Your message:")

    if user_message:
        try:
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized")
                return
            
            ##Initialize and set up the graph based on use case
            usecase=user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No use case selected.")
                return
            
            ##Graph Builder
            graph_builder=GraphBuilder(model)
            try:
                graph=graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: Graph set up failed. {e}")
                return


        except Exception as e:
            st.error(f"Error: Graph set up failed. {e}")
            return

