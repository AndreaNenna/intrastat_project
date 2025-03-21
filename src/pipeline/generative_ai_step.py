
from pydantic import BaseModel, Field, ConfigDict
from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import AzureChatOpenAI

from src.pipeline.pipeline import PipelineStep, PipelineInput

    

class GenerativeAIStep(PipelineStep):
    def __init__(self, azure_openai_client: AzureChatOpenAI):
        self.azure_openai_client = azure_openai_client
        self.chain = self.get_prompt() | azure_openai_client | JsonOutputParser()

    def process(self, data: PipelineInput):
        
        result_list = []
        for file in data.document_pdf_markdowns:
            formatted_json = self.chain.invoke({"markdown_input": file.markdown})
            result_list.append({"file_name": file.file_name, "result": formatted_json})
        
        return result_list
    

    def get_prompt(self):
        prompt = ChatPromptTemplate.from_messages([("user", 
        """Estrarre i seguenti dati da una fattura rappresentata in formato markdown (estratta da Azure Document Intelligence Layout):

        1. **HS code**: Elenca tutti i codici HS trovati nella fattura, rispettando il formato standard internazionale con eventuali estensioni specifiche. Di seguito ulteriori indicazioni per questo codice:
                        - Il codice viene solitamente inserito con diversi acronimo o nomi, tra questi: TARIFFA DOGANALE ,CUSTOMS NOMENCLATURE, NOMENCLATURA COMBINATA, CUSTOMS CLASSIFICATION, CUSTOMS TARIFF, HTS code
                        - È sempre e solo numerico, mai alfanumerico
                        - potresti trovare fatture dove il numero è scritto tutto unito 84186900 o fatture dove usano punti o spazi per suddividere 8418.69.00 o 84 18 69 00
                        - Le prime due cifre rappresentano il CAPITOLO SA per lo standard degli HS code, se vedi più codici, per decidere quale estrarre,  verifica che il nome del prodotto in fattura sia coerente con il capitolo SA corrispettivo.
        2. **Peso totale**: Indica il peso complessivo della merce descritta nella fattura, incluso il valore dell'unità di misura. Se nella fattura trovi sia peso netto che peso lordo, inseriscili nel JSON separatamente.
        3. **Country of Origin**: Elenca tutti i paesi di origine associati ai prodotti nella fattura è un'informazione che si trova nella riga del prodotto, se non è presente, riempi con stringa vuota.
        4. **Prezzo della fattura**: Fornisci il totale della fattura in euro o nella valuta indicata.
        5. **Dati del mittente**: Estrarre i seguenti dettagli del mittente:
           - Nome
           - Indirizzo completo
           - Contatti (telefono, email, fax, ecc.)
           - Partita IVA o identificativo equivalente (se presente)

        Restituisci un JSON strutturato con questo schema:

        ```json
        {{{{
          "HS_Codes": ["<HS_code_1>", "<HS_code_2>", "..."],
          "Net_Weight": "<weight_value> <unit>",
          "Gross_Weight": "<weight_value> <unit>",
          "Countries_of_Origin": ["<country_1>", "<country_2>", "..."],
          "Invoice_Total": "<amount> <currency>",
          "Sender_Details": {{{{
            "Name": "<sender_name>",
            "Address": "<sender_address>",
            "Contacts": {{{{
              "Phone": "<phone_number>",
              "Email": "<email>",
              "Fax": "<fax>"
            }}}},
            "VAT_ID": "<VAT_number>"
          }}}}
        }}}}
        ```

        Leggi attentamente il markdown per individuare i dati richiesti, anche se il layout della fattura varia. Se un dato non è presente, lascia il campo vuoto o con un valore nullo.

        Input: {markdown_input}
        JSON: 
        """)])

        return prompt