import streamlit as st
from camel.agents import ChatAgent


from typing import Optional

from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.models import BaseModelBackend
from camel.types import RoleType, ModelPlatformType, ModelType
from camel.models import ModelFactory

text_prompt = """
You're a help assistant to rewtire the post from original language into another language

===== TASK =====
please rewrite the content below.

{task}
"""


class PostTranslationAgent(ChatAgent):
    r"""An agent that can extract node and relationship information for
    different entities from given `Element` content.

    Attributes:
        original_post (TextPrompt): A prompt for the agent to extract node and
            relationship information for different entities.
        output_language (str, optional): The language to be output by the
            agent. (default: :obj:`None`)
    """

    def __init__(
        self,
        api_key: str,
        output_language: str = "Chinese",
        model: Optional[BaseModelBackend] = None
    ) -> None:
        r"""Initialize the `KnowledgeGraphAgent`.

        Args:
            model (BaseModelBackend, optional): The model backend to use for
                generating responses. (default: :obj:`OpenAIModel` with
                `GPT_4O`)
            api_key
        """
        if model is None:
            model = ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI,
                model_type=ModelType.GPT_4O,
                model_config_dict={"temperature":0.6},
                api_key=api_key)
        system_message = BaseMessage(
            role_name="Post Translator",
            role_type=RoleType.ASSISTANT,
            meta_dict=None,
            content="Your mission is to transter the given post into another language, make sure the content is in high quality"
        )
        super().__init__(system_message, model=model, api_key=api_key, output_language=output_language)

    def run(
        self,
        original_post: str,
    ) -> str:
        r"""Run the agent to extract node and relationship information.

        Args:
            original_post (str): Whether to parse into
                `GraphElement`. Defaults to `False`.

        Returns:
            str
        """
        self.reset()

        post_translation_msg = BaseMessage.make_user_message(
            role_name="CAMEL User", content=original_post
        )

        response = self.step(input_message=post_translation_msg)

        content = response.msg.content

        return content


st.set_page_config(page_title="🐫 Post Translate App")
st.title('🐫 Post Translate App')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

def generate_response(input_text):
  agent = PostTranslationAgent(api_key=openai_api_key)
  st.info(agent.run(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What post content you would like to translate?')
  submitted = st.form_submit_button('Submit')
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    generate_response(text)