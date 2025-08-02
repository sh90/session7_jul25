from crewai_tools import ScrapeWebsiteTool, FileWriterTool, TXTSearchTool
import os
import data_info
from crewai import Agent, Task, Crew

# Initialize the tool, potentially passing the session
tool = ScrapeWebsiteTool(website_url='https://en.wikipedia.org/wiki/Artificial_intelligence')

# Extract the text
text = tool.run()
# Ensure the file is written to the current working directory.
file_writer_tool = FileWriterTool()
filename = 'ai.txt'
if  isinstance(text, str):
    print("yes")
    result = file_writer_tool._run(filename=filename, content=text, directory='', overwrite=True)
else:
    result = file_writer_tool._run(filename=filename, content="dummy text", directory='', overwrite=True)
print(result)

os.environ['OPENAI_API_KEY'] = data_info.open_ai_key

# Initialize the tool with a specific text file, so the agent can search within the given text file's content
tool = TXTSearchTool(txt=filename)

# Get the context from the text file.
context = tool.run('What is natural language processing?')

# Create the agent with the context string.
data_analyst = Agent(
    role='Educator',
    goal=f'Based on the context provided, answer the question - What is Natural Language Processing? Context - {context}',
    backstory='You are a data expert',
    verbose=True,
    allow_delegation=False,
    tools=[tool]
)

# Create the task.
test_task = Task(
    description="Understand the topic and give the correct response",
    tools=[tool],
    agent=data_analyst,
    expected_output='Give a correct response'
)

# Create the crew.
crew = Crew(
    agents=[data_analyst],
    tasks=[test_task]
)

# Run the crew.
output = crew.kickoff()
print(output)
