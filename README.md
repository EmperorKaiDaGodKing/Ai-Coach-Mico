# Ai-Coach-Mico
AI-powered captioning and tagging coach for mature media — built with privacy, moderation, and expressive freedom at its core.

## Memory bank (mood + journal)
- `AssistantState.update_engagement_profile(mood, style, flow, instructions)` lets you tell the AI how to match your energy.
- `AssistantState.log_moment(note, mood?, tags?, share=True/False)` records moments into a journal, with `share=True` marking entries safe to surface in chat.
- `AssistantState.recall_journal(limit, shared_only=True/False)` retrieves recent journal context for responses.
