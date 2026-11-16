"""Optional RAG integration blueprint.

Provision Azure AI Search and an approved embedding/chat model first.
Index policy documents, not raw loan rows. Configure secrets via managed identity
or environment/Key Vault. This module intentionally does not fabricate credentials
or pretend that a cloud index exists.
"""

def retrieve_policy_context(question: str, top_k: int = 5):
    """Implement Azure AI Search hybrid/vector retrieval here.

    Expected steps:
      1. Embed question with configured embedding deployment.
      2. Run hybrid/vector search against approved policy index.
      3. Return top-k text chunks with document title, page, and URI metadata.
      4. Pass retrieved context to LLM with an instruction to cite sources.
    """
    raise NotImplementedError(
        "Provision Azure AI Search + embedding/chat deployments and implement "
        "the tenant-specific SDK integration before enabling policy Q&A."
    )
