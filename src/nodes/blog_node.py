from src.states.blogstate import BlogState

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
