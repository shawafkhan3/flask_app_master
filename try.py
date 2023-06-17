history=[{'role':'user','content':nquestion},{'role':'assistant','content':g[0]}]

def create_search_prompt(chat_history, query):
  return f'''Your task is to take into consideration two things, one is the chat history that has happend between the User and AI and other is the question. Now you need to 
modify the question if only it is needed according to chat history and generate  a new question that can searched upon. You have to handle follow up questions and take into 
considerations the previous responses of the AI if necessary. If the question is not related to the previous responses then output the same question as inputted. If you are not confident on whether the question is related to previous responses, then output the same question.

Example 1:
------------
Chat History:
User: When is MG University established?
AI: 1998

Given question: then what about Rao University?
Rephrased question: When is Rao University established?
------------

Example 2:
------------
Chat History:
User: When is the Republic day of India?
AI: January 26

Given question: Who is Pawan Kalyan?
Rephrased question: Who is Pawan Kalyan?
------------

Example 3:
------------
Chat History:


Given question: What is water made up of?
Rephrased question: What is water made up of?
------------


Chat history:
{chat_history}

Given question: {query}
Rephrased question: 
'''

def create_prompt(context, query):
  return f'''Your task is to extract the answer from the context for the question. You will be given a context and question. Answer the question as truthfully as possible and if the
answer does not lie in the context then say "I don't know".

Context
----------
{context}
----------

Question: {query}
Answer: 
'''



def get_formatted_history(history):
  chat_history=''
  for message in history:
    if(message['role']=='user'):
      chat_history+='User: '+message['content']+'\n'
    elif(message['role']=='assistant'):
      chat_history+='AI: '+message['content']+'\n'
  return chat_history.strip()

search_prompt = create_search_prompt(get_formatted_history(history), "What was my previous question")



response = openai.Completion.create(
                      engine="text-davinci-003",
                      prompt=search_prompt,
                      temperature=0,
                      max_tokens=400,
                    #   top_p=0,
                      frequency_penalty=0.0,
                      presence_penalty=0.0,
                    #   stop=["\n"]
                    )



response['choices'][0]["text"]


def num_tokens_from_messages(messages, encoding):
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += len(encoding.encode(message['content'])) + 1 # 1 is added to take into consideration the role
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

encoding = tiktoken.encoding_for_model("text-davinci-003")
num_tokens_from_messages(history,encoding)
