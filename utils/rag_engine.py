import os
import math
import re

class LocalPythonVectoriser:
    """A zero-dependency text vectorizer that processes text matching locally."""
    def __init__(self):
        pass

    def get_words(self, text):
        """Tokenize text into lowercase words."""
        return re.findall(r'\w+', text.lower())

    def compute_vector(self, text, vocabulary):
        """Creates a frequency count vector based on a global vocabulary list."""
        words = self.get_words(text)
        vector = [0] * len(vocabulary)
        for word in words:
            if word in vocabulary:
                idx = vocabulary[word]
                vector[idx] += 1
        return vector

class PurePythonVectorStore:
    """A zero-dependency in-memory Vector Database that runs completely offline."""
    def __init__(self):
        self.vectoriser = LocalPythonVectoriser()
        self.documents = []
        self.vocabulary = {}
        self.vectors = []

    def build_vocabulary(self):
        """Builds a unique word index tracking map across all documents."""
        unique_words = set()
        for doc in self.documents:
            unique_words.update(self.vectoriser.get_words(doc))
        
        self.vocabulary = {word: idx for idx, word in enumerate(unique_words)}
        
        # Re-vectorize existing entries with the updated vocabulary map
        self.vectors = []
        for doc in self.documents:
            self.vectors.append(self.vectoriser.compute_vector(doc, self.vocabulary))

    def add_texts(self, texts):
        if not texts:
            return
        self.documents.extend(texts)
        self.build_vocabulary()

    def cosine_similarity(self, vec1, vec2):
        """Mathematical formula calculating similarity scores between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def similarity_search(self, query, k=2):
        if not self.vectors or not self.vocabulary:
            return []
        
        # Vectorize the search query using our current local vocabulary mapping
        query_vector = self.vectoriser.compute_vector(query, self.vocabulary)
        
        # Calculate similarity scores against all database entries
        scored_docs = []
        for doc, doc_vector in zip(self.documents, self.vectors):
            score = self.cosine_similarity(query_vector, doc_vector)
            scored_docs.append((doc, score))
        
        # Sort documents highest matching score first
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in scored_docs[:k]]

def initialize_vector_store():
    """Initializes our bulletproof local vector storage layer."""
    return PurePythonVectorStore()

def seed_academic_glossary(vector_store):
    """Seeds sample foundational curriculum terminology framework values."""
    if len(vector_store.documents) > 0:
        return
        
    sample_glossary = [
        "Glossary Reference: 'Machine Learning' should be translated as 'मशीन शिक्षण' in Marathi academic contexts to align with engineering frameworks.",
        "Glossary Reference: 'Artificial Intelligence' maps to 'कृत्रिम बुद्धिमत्ता' in standard pedagogical glossaries.",
        "Glossary Reference: 'Subset' means an instructional component or sub-classification, translated as 'उपवर्ग' or 'उपसंच'."
    ]
    vector_store.add_texts(sample_glossary)

def retrieve_academic_context(query, vector_store, k=2):
    """Retrieves relevant background terminology context for a given prompt."""
    try:
        matched_docs = vector_store.similarity_search(query, k=k)
        return "\n".join(matched_docs)
    except Exception:
        return ""
