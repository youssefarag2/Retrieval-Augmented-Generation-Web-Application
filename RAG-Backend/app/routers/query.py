# app/routers/query.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from ..services import rag_service
# --- MODIFIED: Import the new dependency ---
from ..dependencies import get_user_query_context, UserQueryContext
from ..db import schemas # Import request/response schemas

router = APIRouter(
    prefix="/query",
    tags=["Query RAG"] # Updated tag
    # No global dependency here, as auth is optional for this endpoint
)
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.RagQueryResponse)
async def handle_query(
    request: schemas.RagQueryRequest,
    # --- MODIFIED: Use the new user context dependency ---
    user_context: UserQueryContext = Depends(get_user_query_context)
):
    """
    Receives a user query, processes it using the RAG chain,
    applying access control based on the user's role and level.
    Accessible by guests, students, and admins.
    """
    if not request.query or not request.query.strip():
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty."
         )

    try:
        logger.info(f"Received query: '{request.query}' from user with context: Role='{user_context.role}', Level='{user_context.level}'")
        
        # --- MODIFIED: Pass user_context to the RAG service ---
        answer, sources = rag_service.get_rag_answer(request.query, user_context)

        if answer.startswith("Error:"): # Check for specific error from rag_service
             # Determine appropriate status code based on error type
             if "not available" in answer or "configuration issue" in answer:
                 status_code = status.HTTP_503_SERVICE_UNAVAILABLE
             else:
                 status_code = status.HTTP_400_BAD_REQUEST # Or other relevant error
             raise HTTPException(
                status_code=status_code,
                detail=answer
            )

        return schemas.RagQueryResponse(answer=answer, sources=sources)

    except Exception as e:
        logger.exception(f"Unexpected error processing query '{request.query}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your query."
        )
