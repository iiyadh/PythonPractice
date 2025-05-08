from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()


class Movie(BaseModel):
    title: str = Field(description="The title of the movie.")
    genre: List[str] = Field(description="The genre(s) of the movie.")
    year: int = Field(description="The year the movie was released.")

class MovieList(BaseModel):
    movies: List[Movie]

    
# Model setup
parser = PydanticOutputParser(pydantic_object=MovieList)

prompt_template_text = """
You are a movie expert. Provide a list of 3 recommended movies in JSON format that match the user query.

{format_instructions}

User query: {query}
"""

format_instructions = parser.get_format_instructions()

prompt_template = PromptTemplate(
    template=prompt_template_text,
    input_variables=["query"],
    partial_variables={"format_instructions": format_instructions},
)

query = "Recommend 3 science fiction movies from the 2000s."
formatted_prompt = prompt_template.format(query=query)

chat_model = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model="llama3-70b-8192",
    temperature=0.7,
    max_tokens=800,
)

response = chat_model.invoke(formatted_prompt)

print("Raw response:\n", response.content)

parsed_output = parser.parse(response.content)

print("\nParsed movies:")
for movie in parsed_output.movies:
    print(f"- {movie.title} ({movie.year}) - Genres: {', '.join(movie.genre)}")
