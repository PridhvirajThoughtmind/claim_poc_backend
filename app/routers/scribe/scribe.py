import assemblyai as aai
import tempfile
import os
from app.schemas import scribe
from app.core.settings import settings
from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.utills.openai_utils import get_openai_llm
from app.utills.prompts import EHR_PROMPT , CONVERSATION_FORMATER_PROMPT


router = APIRouter()

aai.settings.api_key=settings.ASSEMBLY_AI_API_KEY
async def transcribe_audio_from_bytes(audio_bytes: bytes, filename: str) -> dict:
    """
    Transcribe audio from bytes using AssemblyAI
    
    Args:
        audio_bytes: Raw audio file bytes
        filename: Original filename (for extension detection)
        
    Returns:
        dict with transcribed_text and status
    """
    try:
        
        # Transcribe using AssemblyAI
        config = aai.TranscriptionConfig(speech_models=["universal"])
        transcript = aai.Transcriber(config=config).transcribe(audio_bytes)
        llm_client = get_openai_llm()
        if transcript.status == "error":
            return {
                "transcript": "",
                "status": "error",
                "error": transcript.error
            }
        prompt = CONVERSATION_FORMATER_PROMPT.format(doc_patient_conversation=transcript.text)
        response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
        )
        llm_response = response.choices[0].message.content
        return {
            "transcript": llm_response,
            "status": "completed",
            "error": None
        }
    except Exception as e:
        return {
            "transcript": "",
            "status": "error",
            "error": str(e)
        }

async def generate_ehr(transcribed_text:str) -> dict:
    llm_client = get_openai_llm()
    prompt = EHR_PROMPT.format(transcribed_text=transcribed_text)
    response = llm_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
    )
    llm_response = response.choices[0].message.content
    return llm_response


@router.post("/scribe", response_model=scribe.ScribeResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file received as bytes
    
    Args:
        file: Audio file upload (mp3, wav, m4a, etc.)
        
    Returns:
        TranscriptionResponse with transcribed text
    """
    
    # Validate file type
    allowed_types = {"audio/mpeg", "audio/wav", "audio/m4a", "audio/mp4", "audio/ogg"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {allowed_types}"
        )
    
    try:
        # Read audio bytes from uploaded file
        audio_bytes = await file.read()
        
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Transcribe audio
        transcribe_text = await transcribe_audio_from_bytes(audio_bytes, file.filename)
        result = await generate_ehr(transcribed_text=transcribe_text)
        print("===========",jsonable_encoder(result))
        return scribe.ScribeResponse(doc_patient_conversation=transcribe_text['transcript'], scribe=result, status="success")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription failed: {str(e)}"
        )