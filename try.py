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




The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"response_back_to_user": {"title": "Response Back To User", "description": "Answer in polite tone, if there is no answer in above chunks/information provided the answer is could not find,  provide justification from which document and how answer is relevant to question ", "type": "string"}, "is_there_answer_in_context": {"title": "Is There Answer In Context", "description": "True if  answer was from pdf/chunk data provided below else False", "type": "boolean"}, "document_id": {"title": "Document Id", "description": "List of document_ids sorted from most relevance only if there was answer, empty list if no answer", "type": "array", "items": {"type": "string"}}}, "required": ["is_there_answer_in_context"]}
```


"Human: Context: You are an AI assistant of Celebal Technology company. Your job is to help user chat with pdf file data, where you can only answer from pdf information.\nThe output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {\"properties\": {\"foo\": {\"title\": \"Foo\", \"description\": \"a list of strings\", \"type\": \"array\", \"items\": {\"type\": \"string\"}}}, \"required\": [\"foo\"]}}\nthe object {\"foo\": [\"bar\", \"baz\"]} is a well-formatted instance of the schema. The object {\"properties\": {\"foo\": [\"bar\", \"baz\"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{\"properties\": {\"response_back_to_user\": {\"title\": \"Response Back To User\", \"description\": \"Answer in polite tone, if there is no answer in above chunks/information provided the answer is could not find,  provide justification from which document and how answer is relevant to question \", \"type\": \"string\"}, \"is_there_answer_in_context\": {\"title\": \"Is There Answer In Context\", \"description\": \"True if  answer was from pdf/chunk data provided below else False\", \"type\": \"boolean\"}, \"document_id\": {\"title\": \"Document Id\", \"description\": \"List of document_ids sorted from most relevance only if there was answer, empty list if no answer\", \"type\": \"array\", \"items\": {\"type\": \"string\"}}}, \"required\": [\"is_there_answer_in_context\"]}\n```\n\nContext: You are an assistant in question answering assistant at Celabal Technologies Company.\n        you will be provided with information from pdf file and your task is to answer \n        the user question.\n        While answering you have to make sure you are answering from given pdf information only\n        You have to give a reason or the answer which explain your answer\n        If answer is there in pdf, you have to return the SOURCE of the information\n\nUser Question: whoem should I report in case of money laundering are the policy on money laundering at celebal\n\n=========\nInformation from : POLICY ON Anti Money Laundering.pdf\nCTPL - POLICY ON Anti Money Laundering 3.1 The relevant member(s) of Compliance and HR are responsible for monitoring and enforcing compliance with the AML Policy and the final responsibility for developing and executing mitigation actions in case ofissues. The relevant member(s) of Compliance and HR are responsible for compliance with all relevant laws, regulations, rules and professional standards applicable to Celebal, whereunder those with respect to AML. 4. DEFINITIONS OF MONEY LAUNDERING AND TERRORISM FINANCING 4.1 Money Laundering is the process by which it attempts to hide and disguise the true origin and ownership ofthe proceeds from criminal activities, thereby avoiding prosecution, conviction and confiscation of criminal funds. 4.2 Terrorism Financing means: the provision or collection of funds, by any means, directly or indirectly, with the intention that they be used orin the knowledge that they are to be used, in full or in part, in order to carryout any terrorist act. 5. OBLIGATIONS 5.1 The main obligations for Celebal and its Personnel under this AML Policy are as follows: A. perform a risk assessment on overall activities, including contemplated activities; B. perform an individualized counterparty due diligence on a risk-sensitive basis; and C. report to and cooperate with the competent authorities (if required). 5.2 Celebal complies with all applicable laws and regulations wherever the company conducts business, enters into, or maintains business relationships. 6. RISK ASSESSMENT 6.1 Celebal takes a risk-based approach to prevent, manage and mitigate AML offences, including (but not limited to): A. identification of the risk of AML to which it could be exposed; B. categorizing such risk in accordance with its internal risk categorization methodology; and C. defining and implementing appropriate measures to mitigate the identified risk. CT\n ,\nsource: \n    Document ID : 7df11169-d281-4feb-914d-86b6b7d5d70a \n=========\n=========\nInformation from : POLICY ON Anti Money Laundering.pdf\nCTPL - POLICY ON Anti Money Laundering 6.2 In the risk-based approach, Celebal takes into account the nature and the size of its activities and the risk factors related to: A. types of counterparties and/or (ultimate) beneficial owners; B. types of (envisaged) products with the counterparties; C. types of (envisaged) services with the counterparties; D. the delivery channels; E. type of business activities of Celebal; and F. the countries and geographical locations of Celebal’s operations. 6.3 Celebal examines, as far as reasonably possible, the background and purpose of all complex and unusually large transactions, and all unusual patterns of transactions, which have no apparent economic or lawful purpose. The company increases its degree and nature of monitoring of the business relationship, in order to determine whether those transactions or activities appear suspicious. 7. COUNTERPARTY DUE DILIGENCE (“CDD”) 7.1 Consistent with a risk-based approach, Celebal will, before the establishment of a business relationshipor the carrying-out of a transaction, as part of all due diligence measures that are applied to such business relationship or transaction: A. identify and verify the identity of its counterparty and the (ultimate) beneficial owner(s); B. assess the level of AML risk such counterparty could present; and C. decide the intensity (i.e.simplified,standard or enhanced) of the AML Counterparty Due Diligence.\n ,\nsource: \n    Document ID : 7df11169-d281-4feb-914d-86b6b7d5d70a \n=========\n=========\nInformation from : POLICY ON Anti Money Laundering.pdf\n9. MONITORING AND REPORTING 9.1. As part of the ongoing relationship with the counterparty, ongoing AML monitoring will be carried out on a risk-based approach and where needed orotherwise required. In case unusualtransactions, such as data changes, payments or withdraws, or activities potentially linked to money laundering, are identified, further investigation will take place. Transactions/ activities not consistent with the initiallydeclared purpose or nature of the relationship may also be further investigated. 9.2. All Employees will endeavor to avoid carrying out a transaction which they know or suspect or have reasonable grounds to suspect to be related to money laundering. Unusual transactions shall be escalated. CT\n ,\nsource: \n    Document ID : 7df11169-d281-4feb-914d-86b6b7d5d70a \n=========\n=========\nInformation from : POLICY ON Anti Money Laundering.pdf\n10. COOPERATION WITH AUTHORITIES 10.1. All Employees are obliged to cooperate fully with the appropriate governmental authorities responsiblefor combating AML, if required. If needed, this could include reporting suspicious transactions and cooperating with the authorities, or inform promptly, on their own initiative, the appropriate authoritywhen they know, suspect or have reasonable grounds to suspect that money laundering, an associatedpredicate offence, or terrorist financing is being committed or has been committed or attempted, in particular in consideration of the person concerned, its development, the origin of the funds, the purpose, nature and procedure of the operation. 10.2. The identity of the Employees or authorized representatives having provided such information is keptconfidential by the aforementioned authorities, unless disclosure is essential to ensure the regularity of legal proceedings or to establish proof of the facts forming the basis of these proceedings.\n ,\nsource: \n    Document ID : 7df11169-d281-4feb-914d-86b6b7d5d70a \n=========\n=========\nInformation from : POLICY ON Anti Money Laundering.pdf\nCTPL - POLICY ON Anti Money Laundering 1. INTRODUCTION 1.1 The meaning of certain capitalized or uncapitalized terms used in this AML Policy is set forth in the List ofDefinitions attached as Annex 1. 2. APPLICATION 2.1 The Anti-Money Laundering Policy (“AML Policy”) applies to Celebal Technologies, its subsidiaries (within and outside India) and affiliates, and its and their respective directors, officers, full-time, part-time and seconded employees, and anyone working on Celebal’s behalf, e.g. consultants and representatives (collectively “Personnel”, or the “Employees”). Personnel are expected to act in a manner that will enhanceCelebal’s reputation for honesty, integrity, and reliability. The AML Policy applies in all countries in whichCelebal operates or conducts business. When the laws of those countries require a higher standard, such standard shall apply. Adherence to this AML Policy is a condition of employment and/or engagement with the Company, and therefore the Employees must acknowledge on an annual basisthatthey have understoodthe AML Policy and have disclosed any suspected and actual violations through appropriate channels. 2.2 TheAMLPolicywillnot giveanswersforevery ethicalorlegalsituation. IfEmployees haveanydoubts aboutthe right thing to do, they should seek advice from the relevant member(s) of Compliance or the HR Team. 2.3 If Employees violate Celebal’s policies and procedures or any of the laws that govern Celebal’s business,thecompany will take immediate and appropriate action up to and including termination of employment. 2.4 The purpose of this AML Policy is to substantially prevent, manage and mitigate the risk that Celebal and their Employees become directly or indirectly involved in actual or potential money laundering activities, or terrorist financing activities. 2.5 This AML Policy sets out the key principles and obligations in relation to the AML Framework in order to identify and assess the Money Laundering (“ML”)/Terrorism Financing (“TF”) risks to which Celebal is exposed to (\"ML/TF\", respectively the \"AML\" measures, or more broadly \"AML\"), as defined below. 2.6 For the purpose of this AML Policy, a counterparty comprises of: Celebal’s shareholders, Employees, financial institutions, service providers and any business relationship. A ‘business relationship’ means a business, professional or commercial relationship which is connected with the professional activities of the institutions and persons covered by such law, and which is expected, at the time when the contact is established, to have an element of duration. 3. GOVERNANCE CT\n ,\nsource: \n    Document ID : 7df11169-d281-4feb-914d-86b6b7d5d70a \n=========\n=========\nInformation from : CTPL- HR Manual.pdf\nFor details, kindly refer the Policy on Anti Money Laundering_23.0 on Zoho.\n ,\nsource: \n    Document ID : 8c5e5593-e0bd-45bc-9dca-0501d160a3c7 \n=========\n=========\nInformation from : POLICY ON Anti Money Laundering.pdf\n12. In this AML Policy, the following terms have the following meanings: 12.1. AML means anti-money laundering. 12.2. 12.3. AML Policy means the Anti-Money Laundering Policy at Celebal. CDD means Counterparty Due Diligence. 12.4. Company means Celebal Technologies Pvt. Ltd. 12.5. Employee means any director, officer, full-time, part-time and seconded employee including any third- party contractor, who receives or is entitled to receive remuneration for goods or services from Celebal. 12.6. Enhanced Counterparty Due Diligence means the Enhanced Counterparty Due Diligence process. 12.7. Celebal means Celebal Technologies Pvt. Ltd. 12.8. ML means Money Laundering. 12.9. Personnel means the directors, officers, full-time, part-time and seconded employees of Celebal, and anyone working on Celebal’s behalf, e.g. consultants and representatives. 12.10. Simplified CDD means the Simplified Counterparty Due Diligence. 12.11. Standard CDD means Standard Counterparty Due Diligence. 12.12. TF means Terrorist Financing. 12.13. a. Save where the context dictates otherwise, in this AML Policy: unless a different intention clearly appears, a reference to a Clause or Annex is a reference to a clause or annex of this AML Policy; b. words and expressions expressed in the singular form also include the plural form, and vice versa; c. words and expressions expressed in the masculine form also include the feminine form; and d. a reference to a statutory provision counts as a reference to this statutory provision including all amendments, additions and replacing legislation that may apply from time to time. e. Headings of clauses and other headings in this AML Policy are inserted for ease of reference and do not form part of this AML Policy for the purpose of interpretation. CT\n ,\nsource: \n    Document ID : 7df11169-d281-4feb-914d-86b6b7d5d70a \n=========\n=========\nInformation from : POLICY ON Anti Money Laundering.pdf\n7.3 The following is a non-exhaustive list of risk variablesthat Celebal considers when determining to whatextent it shall apply counterparty due diligence measures: A. the purpose of the account or relationship; B. the (intended) regularity or duration of the business relationship; C. the risk profile; and D. the results of financial sanctions/Politically Exposed Person (“PEP”)/negative media screening.\n ,\nsource: \n    Document ID : 7df11169-d281-4feb-914d-86b6b7d5d70a \n========="

initial_prompt = f"""
Context: You are an assistant in question answering assistant at Celabal Technologies Company.
        you will be provided with information from pdf file and your task is to answer 
        the user question.
        While answering you have to make sure you are answering from given pdf information only
        You have to give a reason or the answer which explain your answer
        If answer is there in pdf, you have to return the SOURCE of the information

User Question: {query}

"""
template_chunk_information =  initial_prompt
chunk_information =  """=========
Information from : {file_name}
{chunk_data},
source: 
    Document ID : {document_id} 
=========
"""
