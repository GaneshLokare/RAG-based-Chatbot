import asyncio
from langchain_community.document_loaders import PyPDFLoader

    
class PdfLoader:
    def __init__(self, path):
        self.loader = PyPDFLoader(path)
        self.pages = []

    async def load_pages(self):
        async for page in self.loader.alazy_load():
            self.pages.append(page)
        return self.pages

    def load_pages_sync(self):
        return asyncio.run(self.load_pages())
    
