# 🌍 Travel Advisor — GenAI-Powered CLI Application

A simple, modular command-line application that generates structured travel advisories for any city worldwide using real-time weather, language, and tourism data — enhanced with retrieval-augmented generation (RAG) and a local LLM.

---

## Features

-  Accepts user input for city and country
-  Uses GeoNames API to fetch location coordinates
-  Pulls 3-day weather forecast from OpenWeather API
-  Retrieves spoken languages via GeoNames
-  Gets top tourist attractions using Geoapify API
-  Builds or loads a **local vector-based knowledge base**
  - Scraped from [travel.state.gov](https://travel.state.gov)
  - Indexed with `all-MiniLM-L6-v2` embeddings and **Chroma**
-  Uses `Qwen1.5-1.8B-Chat` LLM to generate professional-grade advisories
-  Outputs final advisory as a `.txt` file in `generated_advisories/`

---

By default, the project uses a prebuilt KnowledgeBase.txt and a persistent chroma_store/ for faster startup.

You can delete both files and run the script to build your own knowledge base — just know it will take a few minutes (scraping & indexing ~60 countries).
