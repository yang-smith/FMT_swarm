from swarm import Swarm, Agent
from src.utils.api_client_factory import get_client
from src.utils.reader import get_file_previews, get_file_list
from src.utils.prompts import recognize_filename_patterns_prompt, rename_files_prompt

files = get_file_list("./example")
prompt = recognize_filename_patterns_prompt(files)
# print(prompt)

client = get_client()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
)
print(response.choices[0].message.content)

rule = response.choices[0].message.content
files = get_file_previews("./example")

prompt = rename_files_prompt(files, rule)
print(prompt)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
)
print(response.choices[0].message.content)

# client = Swarm(get_client())

# def transfer_to_agent_b():
#     return agent_b


# agent_a = Agent(
#     name="Agent A",
#     instructions="You are a helpful agent.",
#     functions=[transfer_to_agent_b],
# )

# agent_b = Agent(
#     name="Agent B",
#     instructions="Only speak in Haikus.",
# )

# response = client.run(
#     agent=agent_a,
#     messages=[{"role": "user", "content": "I want to talk to agent B."}],
# )

# print(response.messages[-1]["content"])