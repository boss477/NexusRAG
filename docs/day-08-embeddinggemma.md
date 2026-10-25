# Day 8 — Local EmbeddingGemma 2

## Completed

- Added a lazy `EmbeddingGemmaProvider` using the local `google/embeddinggemma-2` checkpoint.
- Added retrieval-specific `SearchQuery` and `Document` prompts for text.
- Added model-native media input for image, audio, video, or interleaved content, with independently selectable vision and audio encoders. Video uses the vision encoder.
- Added 768/512/256/128-dimensional output with truncation and L2 normalization.
- Added mocked tests for prompts, encoder selection, dimensions, normalization, and invalid output.

## Use

Install the optional dependency with `pip install -e ".[embeddinggemma]"`, then:

```python
from app.embeddings import EmbeddingGemmaProvider

provider = EmbeddingGemmaProvider()  # text-only, 768 dimensions
query = provider.embed_query("How does hybrid retrieval work?")
documents = provider.embed_documents(["Hybrid retrieval combines dense and sparse search."])

media_provider = EmbeddingGemmaProvider(load_vision=True)
image = media_provider.embed_media({"image": "diagram.png"})
```

The model is downloaded lazily on first use. A real-model integration run was **not** performed on Day 8; tests use a fake model so CI needs no checkpoint or GPU. Production use should verify checkpoint access, hardware memory, library compatibility, and retrieval quality against the actual model before indexing. Do not mix output dimensions within a Qdrant collection. The adapter uses float32 on CPU or bfloat16 on a compatible CUDA GPU; float16 is deliberately avoided.

References: [Google model card](https://ai.google.dev/gemma/docs/embeddinggemma/model_card_2), [Hugging Face checkpoint](https://huggingface.co/google/embeddinggemma-2).

## Next day

Day 9: Qdrant indexing and semantic retrieval.
