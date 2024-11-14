import abc
import os

from langchain.schema import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models import EmbeddingsModel


class BaseVectorDatabase(abc.ABC):
    """Base class for vector databases."""

    def get_default_collection_name(self) -> str:
        """Get the default collection name for the vector database."""

        return os.environ.get('DEFAULT_VECTOR_DB_COLLECTION_NAME', 'MyRAGApp')

    def get_embedding_function(self) -> Embeddings:
        """Get the embedding function for the vector database."""

        # TODO: Add more options such as `Voyage`, `Gemini`.
        return EmbeddingsModel()
    
    async def split_and_store_text(
        self,
        text: str,
        metadata: dict,
        chunk_size: int = 1_000,
        chunk_overlap: int = 200,
    ) -> list[int]:
        """Store the embeddings for the given text in the vector database."""

        # Split the text into chunks.
        docs = [Document(page_content=text, metadata=metadata)]
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        splits = text_splitter.split_documents(docs)

        # Store the embeddings for each chunk.
        return self.add_documents(documents=splits)
    
    @abc.abstractmethod
    def __init__(self, collection_name: str = None, **kwargs):
        """Initialize the vector database."""
        pass

    @abc.abstractmethod
    async def delete_embeddings(self, source_id: str) -> dict:
        """Delete the embeddings for the given text from the vector database.
        
        :param source_id: The `source_id` metadata parameter to delete.
            This is not the same as the ID in the vector database, but rather the ID
            we use to identify the source, that the chunk of text came from.

        :return: A dictionary with the results of the deletion.
        """
        pass

    @abc.abstractmethod
    async def drop_collection(self, collection_name: str, ignore_non_exist: bool = False) -> None:
        """Drop the collection from the vector database.
        
        :param collection_name: The name of the collection to drop.
        :param ignore_non_exist: If `True`, no error will be raised if the collection does not exist.
        """
        pass
