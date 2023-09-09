from langchain.llms import OpenAI
from langchain import  LLMChain
from langchain.chat_models import ChatOpenAI
from magiccommits.src.utils.prompt import generate_prompt
from langchain.prompts import (SystemMessagePromptTemplate,HumanMessagePromptTemplate,ChatPromptTemplate)
from langchain.schema import (HumanMessage,SystemMessage)

test_diff = """
diff --git a/app/main.py b/app/main.py
index e5f1a12..4c8a2f7 100644
--- a/app/main.py
+++ b/app/main.py
@@ -1,5 +1,9 @@
 # MyApp - Main Application
 
 import requests
+from my_new_feature import process_new_data
 
 def fetch_data(url):
     response = requests.get(url)
     data = response.json()
     return data
 
 def main():
     data = fetch_data("https://api.example.com/data")
+    processed_data = process_new_data(data)
+    if processed_data:
+        print("New feature result:", processed_data)
+
 if __name__ == "__main__":
     main()
"""
test_api_key = "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"
test_locale = "en"
test_completions = 4
test_max_length = 80
test_type = "conventional"
test_timeout = 600
def generateCommitMessage(api_key,model,locale,diff,completions,max_length,type,timeout):
    template = generate_prompt(locale=locale,max_length=max_length,commit_type=type,emoji_type=type)
    llm = ChatOpenAI(openai_api_key=api_key,request_timeout=timeout,n=completions,streaming=False,max_tokens=200)
    system_prompt = SystemMessage(content=template)
    human_prompt = HumanMessage(content=f" Based on this code diff generate 4 commit: {diff}")
    return llm([system_prompt,human_prompt])
    # human_prompt = HumanMessagePromptTemplate(human_template,["diff"])

    # chat_prompt_template = ChatPromptTemplate.from_messages([system_prompt,human_prompt])

    # llm_chain = LLMChain(prompt=chat_prompt_template,llm=llm)
    





# apiKey: string,
# 	model: TiktokenModel,
# 	locale: string,
# 	diff: string,
# 	completions: number,
# 	maxLength: number,
# 	type: CommitType,
# 	timeout: number,
# 	proxy?: string,

commit = generateCommitMessage(test_api_key,"gpt-3.5-turbo",test_locale,test_diff,test_completions,test_max_length,test_type,test_timeout)
print(commit.content)