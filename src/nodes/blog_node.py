from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.states.blogstate import Blog

class BlogNode:
    """"
    A Class to represent a blog node 
    """
    def __init__(self,llm):
        self.llm=llm

    def title_creation(self,state:BlogState):
        """
        Create a tile for a blog
        """
        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog for the {topic}. This title should be creatie and SEO friendly
                   """
            
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        """
        Generate content for the blog based on the title
        """
        if "topic" in state and state["topic"]:
            sysytem_prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a detailed blog content with detailed breakdown for the {topic}.
                   """
            
            system_message = sysytem_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog":{"title":state['blog']['title'],"content":response.content}}
        
    def translation(self, state:BlogState):
        """
        Translate the content to the specified language.
        """

        translation_prompt = """
        Translate the following blog post into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.
        - Return the result as a JSON object with the following fields: 'title' and 'content'.
        - 'title' should be the translated title, and 'content' should be the translated blog content.

        ORIGINAL BLOG:
        Title: {blog_title}
        Content: {blog_content}

        Your response must be a valid JSON object with 'title' and 'content'.
        """

        blog_title = state["blog"]["title"]
        blog_content = state["blog"]["content"]
        message = [
            HumanMessage(
                translation_prompt.format(
                    current_language=state["current_language"],
                    blog_title=blog_title,
                    blog_content=blog_content
                )
            )
        ]

        try:
            translation_content = self.llm.with_structured_output(Blog).invoke(message)
            return {"blog": {"title": translation_content.title, "content": translation_content.content}}
        except Exception as e:
            print("[DEBUG] Structured output parsing failed. Exception:", e)
            raw_response = self.llm.invoke(message)
            print("[DEBUG] Raw LLM response:\n", raw_response)
            raise

    def route(self,state:BlogState):
        return {"current_language":state["current_language"]}
    
    def route_decision(self, state:BlogState):
        """"
        Route the content to the respective translation function.
        """
        if state["current_language"]=="hindi":
            return "hindi"
        elif state["current_language"]=="french":
            return "french"
        else:
            return state["current_language"]