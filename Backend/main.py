from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import re

app = FastAPI()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "Your_openAi_API_key")
client = OpenAI(api_key=OPENAI_API_KEY)

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5

class WebResult(BaseModel):
    title: str
    url: str
    content: str
    summary: str

@app.post("/search/")
async def search_task(request: SearchRequest):
    try:
        # Step 1: Simulate web search (replace with actual API in production)
        search_results = simulate_web_search(request.query, request.max_results)
        
        # Step 2: Process results with AI
        enriched_results = []
        for result in search_results:
            summary = generate_ai_summary(
                content=result['content'],
                query=request.query,
                url=result['url']
            )
            enriched_results.append(WebResult(
                title=result['title'],
                url=result['url'],
                content=result['content'],
                summary=summary
            ))
        
        return {
            "query": request.query,
            "results": enriched_results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def simulate_web_search(query: str, max_results: int) -> List[dict]:
    """Simulate web search results (replace with real API in production)"""
    # This is a placeholder - in production, use:
    # - Google Custom Search API
    # - SerpAPI
    # - Or a headless browser like Playwright
    
    # Example simulated results
    return [
        {
            "title": f"Research about {query}",
            "url": f"https://example.com/research/{query.replace(' ', '-')}",
            "content": f"This is simulated content about {query}. In a real implementation, this would be scraped from actual web pages or fetched from an API. The content would contain relevant information about the search query."
        },
        {
            "title": f"Recent studies on {query}",
            "url": f"https://research.org/{query.replace(' ', '_')}",
            "content": f"Another simulated result for {query}. The AI would analyze this content to extract key insights and generate a summary. The real version would process actual web content."
        }
    ][:max_results]

def generate_ai_summary(content: str, query: str, url: str) -> str:
    """Generate an AI-powered summary of web content"""
    try:
        prompt = f"""
        Analyze this web content for relevance to: {query}
        Source URL: {url}
        
        Content:
        {content[:12000]}  # Truncate to avoid token limits
        
        Instructions:
        1. Extract key information most relevant to the query
        2. Identify the 3-5 most important points
        3. Provide a concise summary in academic tone
        4. Include any statistics or notable findings
        5. Keep under 200 words
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a scientific research assistant. Provide clear, accurate summaries with academic rigor."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Summary unavailable due to error: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)