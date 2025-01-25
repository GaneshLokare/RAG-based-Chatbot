from langchain_text_splitters import RecursiveCharacterTextSplitter


class Splitter:
    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )

    def split_text(self, text):
        return self.text_splitter.split_documents(text)
    
