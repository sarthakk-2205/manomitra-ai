
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel, Field

from app.chatbot import generate_reply,generate_rag_reply
from app.sentiment import analyze_sentiment
from app.safety import check_safety
from app.emotion import analyze_emotion
from app.chatbot import generate_memory_reply
from app.chatbot import generate_memory_rag_reply


app = FastAPI(
    title="ManoMitra AI",
    description="AI service for student mental wellness",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "project": "ManoMitra-AI",
        "message": "AI service is running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)

class MemoryChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=4000)


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    try:
        reply = generate_reply(message)
        return {"reply": reply}
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Chatbot temporarily unavailable.",
        )


@app.post("/sentiment")
def sentiment(request: ChatRequest):
    try:
        return analyze_sentiment(request.message)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Sentiment analysis is temporarily unavailable."
        )


@app.post("/emotion")
def emotion(request: ChatRequest):
    try:
        return analyze_emotion(request.message)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Emotion detection is temporarily unavailable."
        )



    




    

@app.post("/wellness-chat")
def wellness_chat(request: ChatRequest):
    try:
        # Screen for possible risk before calling the LLM.
        safety_result = check_safety(request.message)

        if safety_result["possible_risk"]:
            return {
                "reply": safety_result["message"],
                "sources": [],
                "safety": {
                    "possible_risk": True,
                    "resources": safety_result["resources"]
                }
            }

        # Continue with RAG only when no screening phrase matches.
        result = generate_rag_reply(request.message)

        result["safety"] = {
            "possible_risk": False,
            "resources": []
        }

        return result

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="The wellness assistant is temporarily unavailable."
        )




@app.post("/memory-chat")
def memory_chat(request: MemoryChatRequest):
    try:
        reply = generate_memory_reply(
            message=request.message,
            session_id=request.session_id
        )

        return {
            "session_id": request.session_id,
            "reply": reply
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/memory-rag-chat")
def memory_rag_chat(request: MemoryChatRequest):
    try:
        message = request.message.strip()

        if not message:
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty."
            )

        # Step 1: Screen for possible safety risk
        safety_result = check_safety(message)

        # Step 2: If possible risk is detected, don't call the LLM
        if safety_result["possible_risk"]:
            return {
                "session_id": request.session_id,
                "reply": safety_result["message"],
                "sources": [],
                "safety": {
                    "possible_risk": True,
                    "resources": safety_result["resources"]
                }
            }

        # Step 3: Continue with memory + RAG
        result = generate_memory_rag_reply(
            message=message,
            session_id=request.session_id
        )

        return {
            "session_id": request.session_id,
            "reply": result["reply"],
            "sources": result["sources"],
            "safety": {
                "possible_risk": False,
                "resources": []
            }
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="The wellness assistant is temporarily unavailable."
        )






