import os
import warnings

from transformers import AutoTokenizer, AutoModelForCausalLM

import knowlege_base
from coodinates import Coordinates
from languages import Languages
from locations import Locations
from weather import Weather

# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# User input
city = input("Enter the city's name: ")
country = input("Enter the country: ").title()
print("Please wait....\n\n")

# API Key
WEATHER_API_KEY = "ENTER YOUR OPENWEATHERMAP API KEY HERE"
LOC_API_KEY = "ENTER YOUR GEOAPIFY API KEY HERE"
GEONAMES_USERNAME = 'ENTER YOUR GEONAMES USERNAME HERE'

# -------------------------------------------- API USAGE ---------------------------------------------------------------

# Get the coordinates
c = Coordinates(city=city, country=country)
lat, lon = c.get_coordinates(api=WEATHER_API_KEY)

# Get weather
w = Weather(latitude=lat, longitude=lon)
weather = w.get_weather(api=WEATHER_API_KEY)

# Get languages
lang = Languages(country=country)
languages = lang.get_languages(username=GEONAMES_USERNAME)

# Get tourist locations
loc = Locations()
locations = loc.get_locations(latitude=lat, longitude=lon, api=LOC_API_KEY)

# -------------------------------------------- UPDATING KNOWLEDGE BASE -------------------------------------------------

# Working with the knowledge
confirmation = input("Do you want to update the knowledge base? (Y/N): ").upper()
if confirmation == "Y":
    knowlege_base.generate(confirmation=confirmation)
else:
    knowlege_base.load_and_index()

print("Please wait as we generate the advisory.... ")

# Retrieving knowledge base
results = knowlege_base.retrieve(country=country)

advisory_text = results[0].page_content.strip()

# -------------------------------------------------- AI MODEL ----------------------------------------------------------

# Model setup
MODEL_NAME = "Qwen/Qwen1.5-1.8B-Chat"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto", trust_remote_code=True)


def build_chat_messages(city, country, weather, languages, locations, advisory_text):
    system_msg = {
        "role": "system",
        "content": "You are a helpful and professional travel advisory assistant. Always follow the instructions exactly."
    }

    user_msg = {
        "role": "user",
        "content": (
            f"Generate a full travel advisory for {city}, {country}. "
            "The format must include the following sections in this order:\n\n"

            "--- Travel Advisory ---\n"
            "[City], [Country] Travel Advisory\n\n"

            "1. CSR (Country Security Report):\n"
            "- Summarize crime risks, terrorism, cybersecurity, and other relevant concerns.\n\n"

            "2. Local Weather Forecast (3-day):\n"
            f"- Use this weather data:\n{weather}\n\n"

            "3. Languages Spoken:\n"
            f"- Use this info to describe main and regional languages:\n{languages}\n\n"

            "4. Popular Tourist Attractions:\n"
            f"- Use this list to describe 5–7 locations:\n{locations}\n\n"

            "5. Final Tips and Conclusion:\n"
            "- Add short bullet points with safety tips.\n"
            "- End with a warm, professional closing.\n\n"

            "You must include **all 5 sections** in the final output, with the section headers exactly as shown above. "
            "Use a professional tone, avoid repetition, and do not invent extra headings. Do not skip the weather, language, or locations sections."
        )
    }

    return [system_msg, user_msg]


def generate_text(city, country, weather, languages, locations, advisory_text):
    messages = build_chat_messages(city, country, weather, languages, locations, advisory_text)
    encoded = tokenizer.apply_chat_template(messages, return_tensors="pt", padding=True)
    input_ids = encoded.to(model.device)
    attention_mask = (input_ids != tokenizer.pad_token_id).long().to(model.device)

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=1000,
        temperature=0.5,
        top_k=30,
        top_p=0.80,
        do_sample=True
    )
    new_tokens = output[0][input_ids.shape[-1]:]
    decoded_output = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return decoded_output.strip()


result = generate_text(city, country, weather, languages, locations, advisory_text)

os.makedirs("generated_advisories", exist_ok=True)
filename = os.path.join("generated_advisories", f"{city}_{country}.txt")
with open(filename, 'w', encoding='utf-8') as file:
    file.write(result)

print(result)
