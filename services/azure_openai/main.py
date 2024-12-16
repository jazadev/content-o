import json
import datetime
from functools import wraps

#import openai
from openai import AzureOpenAI  # New import style

from tenacity import retry, wait_random_exponential, stop_after_attempt
from services.azure_openai.utils import read_csv, parse_json_safely
#from settings.config import AZURE_STORAGE_ACCOUNT_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_DATA_NAME, AZURE_STORAGE_CSV
#from services.azure_storage import StorageAccount
from langchain_openai import AzureChatOpenAI

from settings.config import (
    AZURE_OPENAI_API_BASE,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
)
from services.azure_openai.utils import (
    get_prompt,
    get_tools,
    get_usage_tokens,
)


ENGINE_MODEL_VERSION = "gpt-4o-mini"


def measure_time(stage_name):
    def decorator(func):
        @wraps(func)
        def wrapper(cls, *args, **kwargs):
            t1 = datetime.datetime.now()
            result = func(cls, *args, **kwargs)
            elapsed_time = (datetime.datetime.now() - t1).total_seconds()
            cls.stage_duration.append({stage_name: elapsed_time})
            return result
        return wrapper
    return decorator


class ChatGPTService:

    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_API_BASE
        )
        
        self.stages_engine_version = ENGINE_MODEL_VERSION
        self.stage_duration = []
        self.stage_token_usage = []
        self.conversation_history = []
        self.current_role = None

    def start_conversation(self, role):
        """Initialize conversation with role-specific system prompt"""
        self.current_role = role
        if role != None:
            prompt = get_prompt(role)
        else:
            prompt = get_prompt("external-user")
        self.conversation_history = [
            {"role": "system", "content": prompt}
        ]

    @retry(wait=wait_random_exponential(min=2, max=60), stop=stop_after_attempt(3), reraise=True)
    def run_query_chatgpt(self, query, role=None):
        try:
            # If role changes or conversation not started, initialize with new role
            if role != self.current_role or not self.conversation_history:
                self.start_conversation(role)

            #tools = get_tools(role)
            engine_version = "gpt-4o-mini"

           

             # Add user message while maintaining the system prompt
            self.conversation_history.append({"role": "user", "content": query})



            completion = self.client.chat.completions.create(
                model=engine_version,
                messages=self.conversation_history,
                temperature=0,
                max_tokens=3000,
                top_p=0.9,
                #tool_choice="auto",
            )

            assistant_message = completion.choices[0].message
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content if assistant_message.content else "",
                "tool_calls": assistant_message.tool_calls
            })
            print(assistant_message.content)




            token_consumed = {role: get_usage_tokens(completion)}
            self.stage_token_usage.append(token_consumed)
        except Exception as e:
            # TODO: delete after testing, and logging
            print(f"Error in ChatGPT request. Detail: {e}")
            completion = {}

        return completion

    @measure_time("identifier")
    def get_identifier(self, files, subject, content, origin_date):
        options = {
            "stage": 'identifier',
        }

        engine_version = ENGINE_MODEL_VERSION

        response_list = []

        if len(files) == 0:
            file_txt = 'Asunto del correo: ' + subject + 'Cuerpo:' + content
            completion = self.run_query_chatgpt(source_text=file_txt, options=options)
            try:
                message = completion.choices[0].message
                tool_calls = message.tool_calls
                result = tool_calls[0].function.arguments

                result = json.loads(result) if isinstance(result, str) else result

                result['attachments']=False
                result['with_term']=False

                response_list.append(result)

            except Exception as e:
                print(f'Error stage identifier. Detail: {e}')
                raise



        #response_list = []
        for file_path in files:
            with open(file_path, 'r', encoding="utf-8") as f:
                file_txt = f.read()
                file_txt = 'Asunto del correo: ' + subject +'  '+ file_txt 

            if len(file_txt) == 0:
                file_txt = 'Asunto del correo: ' + subject + 'Cuerpo:' + content

            completion = self.run_query_chatgpt(source_text=file_txt, options=options)

            try:
                #message = completion["choices"][0]["message"]
                #tool_calls = message["tool_calls"]
                message = completion.choices[0].message
                tool_calls = message.tool_calls

                #result=tool_calls[0]["function"]["arguments"]
                result = tool_calls[0].function.arguments

                result = json.loads(result) if isinstance(result, str) else result

                #response_list.append(tool_calls[0]["function"]["arguments"])
                response_list.append(result)

            except Exception as e:
                print(f'Error stage identifier. Detail: {e}')
                continue
        return response_list
    
    @measure_time("regional")
    def get_region(self, jurisdiccion):
        options = {
            "stage": 'regional',
        }
        csv_key = AZURE_STORAGE_CSV

        # Se accede al archivo CSV con la data puntual que necesitamos consultar para obtener el dato que necesitamos
        store_service_csv = StorageAccount(AZURE_STORAGE_ACCOUNT_CONNECTION_STRING, AZURE_STORAGE_CONTAINER_DATA_NAME)
        data_csv = store_service_csv.get_data_csv(blob=csv_key)

        
        header, data = read_csv(data_csv)
        #key_data=search_word(jurisdiccion, header, data)

        completion = self.run_query_chatgpt(source_text=str(header), options=options)
        try:
            message =  completion.choices[0].message
            tool_calls = message.tool_calls
            arguments = json.loads(tool_calls[0].function.arguments)
            return arguments["regional"].upper()
        except Exception as e:
            print(f'Error stage regional. Detail: {e}')
            raise
       

    @measure_time("important_feature")
    def get_extract_important_feature(self, source_txt, stage):
        options = {
            "stage": stage,
        }

        completion = self.run_query_chatgpt(source_txt, options)
        tool_calls = completion.choices[0].message.tool_calls
        arguments = tool_calls[0].function.arguments
        return arguments
    
    @measure_time("classification")
    def get_classification(self, important_feature):
        options = {
            "stage": 'classification',
        }
        completion = self.run_query_chatgpt(source_text=important_feature, options=options)
        tool_calls = completion["choices"][0]["message"]["tool_calls"]
        return tool_calls[0]["function"]["arguments"]

    def stage_based_on_process(self, answer):
        proceso = answer.get("proceso")
        process_function_map = {
            "Otro": "extract_eif_written",
            "Proceso completo es Escrito de tutela": "extract_eif_written",
            "Proceso completo es Admision": "extract_eif_admision",
            "Proceso completo es Fallo": "extract_eif_fallo",
            "Proceso completo es Incidente": "extract_important_feature"
        }
        function_to_call = process_function_map.get(proceso, "extract_important_feature")
        return function_to_call

    def get_engine_version(self, stage):
        #engine_version = self.stages_engine_version.get(stage)
        stage_key = str(stage) if not isinstance(stage, str) else stage
        engine_version = self.stages_engine_version.get(stage_key)
        return ENGINE_MODEL_VERSION.get(engine_version, ENGINE_MODEL_VERSION)

    def process(self, role, query):
        try:

            #filter_documents = [doc for doc in file_source_list if doc.endswith('.pdf.txt')]
            #file_source_list = filter_documents if len(filter_documents) > 0 else []

            response_data = self.run_query_chatgpt(query=query, role=role)
            
            print(response_data)


        #except openai.error.InvalidRequestError as e:
        #   return {"error": "Maximum token length exceeded. Please reduce the length of the input text."}
        except Exception as e:
            print(f"Error processing the request. Detail: {e}")
            return {"error": f"Error processing the request {e}"}

        try:
            messages = {
                "stage_duration": self.stage_duration,
                "stage_token_usage": self.stage_token_usage,
                "role": role,
                "response_data": response_data,
            }
        except Exception as e:
            print(f"JSON encoding error. Detail: {e}")
            messages = {
                "error": "JSON encoding error"
            }

        return messages
    
    def process_anon(self, query):
        try:

            #filter_documents = [doc for doc in file_source_list if doc.endswith('.pdf.txt')]
            #file_source_list = filter_documents if len(filter_documents) > 0 else []

            response_data = self.run_query_chatgpt(query=query)
            
            print(response_data)


        #except openai.error.InvalidRequestError as e:
        #   return {"error": "Maximum token length exceeded. Please reduce the length of the input text."}
        except Exception as e:
            print(f"Error processing the request. Detail: {e}")
            return {"error": f"Error processing the request {e}"}

        try:
            messages = {
                "stage_duration": self.stage_duration,
                "stage_token_usage": self.stage_token_usage,
                "role": "not user",
                "response_data": response_data,
            }
        except Exception as e:
            print(f"JSON encoding error. Detail: {e}")
            messages = {
                "error": "JSON encoding error"
            }

        return messages