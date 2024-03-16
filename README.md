# chat-with-files

Started out as wanting to generate code using code not learned by a LLM without having to train or fine-tune a model.

This should be easy to modify for other use cases.

# Configuration

The following environment variables need to be set in your `.env` file:

| Variable | Required | Description | Example |
| --- | --- | --- | --- |
| EMBEDDING_PROVIDER | Yes | Provider for embeddings. Can be either voyageai or openai. | voyageai |
| ANTHROPIC_API_KEY | No* | API key for Anthropic. | sk-ant-... |
| VOYAGE_API_KEY | No* | API key for VoyageAI. | pa-... |
| OPENAI_API_KEY | No* | API key for OpenAI. | sk-... |
| ACTIVELOOP_TOKEN | Yes | JWT token for ActiveLoop. | JWT |
| ACTIVELOOP_USERNAME | Yes | Username for ActiveLoop. | username |
| GIT_REPO | Yes | URL of the Git repository to clone. | "https://github.com/username/repo" |
| VECTORDB_NAME | Yes | Name of the Vector Database. | chat-with-files |
| LLM_PROVIDER | Yes | Provider for the QA Chat. Can be either anthropic or openai. | anthropic |
- *Keys are required for chosen providers.
