"""
Q&A Engine Module
Retrieves relevant documents and generates answers using LLM
"""
import logging
from typing import List, Dict, Tuple

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QAEngine:
    """
    Retrieval Augmented Generation Q&A Engine
    """
    
    def __init__(self, api_key: str, vector_db, embedding_generator, model: str = "gpt-3.5-turbo"):
        """
        Initialize Q&A Engine
        
        Args:
            api_key: OpenAI API key
            vector_db: Vector database instance
            embedding_generator: Embeddings generator instance
            model: LLM model to use
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed")
        
        self.client = OpenAI(api_key=api_key)
        self.vector_db = vector_db
        self.embedding_generator = embedding_generator
        self.model = model
    
    def retrieve_context(self, query: str, top_k: int = 5) -> Tuple[List[Dict], str]:
        """
        Retrieve relevant documents for the query
        
        Args:
            query: User question
            top_k: Number of top results to return
            
        Returns:
            Tuple of (documents, formatted context string)
        """
        try:
            # Generate embedding for query
            query_embedding = self.embedding_generator.generate_embedding(query)
            
            # Search for similar documents
            documents = self.vector_db.search(query_embedding, top_k=top_k)
            
            # Format context
            context = self._format_context(documents)
            
            return documents, context
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            raise
    
    def _format_context(self, documents: List[Dict]) -> str:
        """
        Format retrieved documents as context string
        
        Args:
            documents: Retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, doc in enumerate(documents, 1):
            part = f"Source {i} ({doc.get('title', 'Unknown')}):\n{doc['content']}\nURL: {doc['url']}\n"
            context_parts.append(part)
        
        return "\n".join(context_parts)
    
    def generate_answer(self, query: str, context: str, temperature: float = 0.7) -> str:
        """
        Generate answer using LLM based on context
        
        Args:
            query: User question
            context: Retrieved context
            temperature: Temperature for generation
            
        Returns:
            Generated answer
        """
        try:
            system_prompt = """You are a helpful Q&A assistant. Answer questions based only on the provided context.
If the information is not available in the context, say "I don't have enough information to answer this question."
Be concise and accurate in your responses."""
            
            user_message = f"""Context:
{context}

Question: {query}

Answer:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise
    
    def answer_question(self, query: str, top_k: int = 5, temperature: float = 0.7) -> Dict:
        """
        Answer a question using RAG
        
        Args:
            query: User question
            top_k: Number of context documents to retrieve
            temperature: Temperature for generation
            
        Returns:
            Dictionary with answer and sources
        """
        try:
            # Retrieve context
            documents, context = self.retrieve_context(query, top_k)
            
            # Generate answer
            answer = self.generate_answer(query, context, temperature)
            
            # Format response
            return {
                'query': query,
                'answer': answer,
                'sources': [
                    {
                        'url': doc['url'],
                        'title': doc['title'],
                        'score': doc.get('score', 0)
                    }
                    for doc in documents
                ]
            }
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
