class Prompt:
    @staticmethod
    def simple_rag(question, context):
        return f"""
        You're a health specialist. Based on the question below, provide an answer using the context provided. You should answer the questions based on the context given. Also answer with the same language as the question.

        Only answer in markdown format.

        Question: 
        ```{question}```

        Context: 
        ```{context}```
        """

    @staticmethod
    def search_query(question, previous_question=None):
        if previous_question is None:
            return f"""
            What is the required information in order to answer this question. Only answer with the search query in Bahasa Indonesia. For example: "Obat Batuk Anak" or "Gejala Tipes".

            Question: 
            ```{question}```
            """
        else:
            prev_q = '\n'.join(previous_question)
            return f"""
            What is the required information in order to answer this question. Only answer with the search query in Bahasa Indonesia. For example: "Obat Batuk Anak" or "Gejala Tipes".

            Also please consider this previous question:
            ```{prev_q}```

            Question: 
            ```{question}```
            """
