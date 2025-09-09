import logging
import traceback
from fastapi import APIRouter, HTTPException
from .models import Query, AnswerResponse, ErrorResponse
from .settings import settings
from .client import client

logger = logging.getLogger("HRPolicyAssistant")
router = APIRouter()

@router.get("/")
async def health():
    return {"message": "Welcome to the HR Policy Assistant API. Use the /ask endpoint to ask questions."}

@router.post("/ask", response_model=AnswerResponse, responses={500: {"model": ErrorResponse}})
async def ask(query: Query):
    logger.info(f"Received question: {query.question}")
    try:
        extension_config = {
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": settings.azure_search_endpoint,
                        "index_name": settings.azure_search_index,
                        "authentication": {
                            "type": "api_key",
                            "key": settings.azure_search_key
                        }
                    }
                }
            ]
        }

        response = client.chat.completions.create(
            model=settings.azure_oai_deployment,
            temperature=0.0,
            max_tokens=800,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an HR assistant for employees of the company. "
                        "You must strictly use information from company HR policies and guidelines "
                        "retrieved from the documents. "
                        "If the information is not available in the company policies, "
                        "reply: 'I could not find that in the company policies.'"
                    )
                },
                {"role": "user", "content": query.question}
            ],
            extra_body=extension_config
        )

        answer = response.choices[0].message.content.strip()
        citations = []
        if hasattr(response.choices[0].message, "context"):
            context_data = getattr(response.choices[0].message, "context", {})
            if isinstance(context_data, dict):
                citations = context_data.get("citations", [])

        return AnswerResponse(answer=answer, citations=citations)

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request."
        )
