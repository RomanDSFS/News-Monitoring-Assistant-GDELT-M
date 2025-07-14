# nlp/topic_classification_en.py

import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

for res in ["punkt", "wordnet", "omw-1.4"]:
    try:
        nltk.data.find(f"tokenizers/{res}") if res == "punkt" else nltk.data.find(f"corpora/{res}")
    except LookupError:
        nltk.download(res)

lemmatizer = WordNetLemmatizer()

TOPIC_KEYWORDS = {
    "military": [
        "armed forces", "military base", "special forces", "warfare", "combat", "battle", 
        "conflict", "war", "operation", "mission", "deployment", "weapons", 
        "firearms", "artillery", "tank", "aircraft", "drone", "missile", "ammunition", 
        "naval", "armor", "soldier", "commander", "officer", "unit", "division", "platoon", 
        "brigade", "general", "intelligence", "attack", "defense", "invasion", 
        "siege", "reconnaissance", "patrol", "strike", "ambush", "retreat", "engagement", 
        "strategy", "tactics", "training", "logistics", "casualties", "resistance", "occupation", 
        "base", "conflict zone", "rules of engagement"
    ],
    "politics": [
        "law", "government", "parliament", "congress", "senate", "president", "prime minister", 
        "chancellor", "minister", "governor", "mayor", "cabinet", "administration", "bureaucracy", 
        "election", "vote", "voting", "campaign", "referendum", "legislation", "policy", "diplomacy", 
        "negotiation", "sanctions", "lobbying", "governance", "law-making", "impeachment", "democracy", 
        "republic", "autocracy", "dictatorship", "monarchy", "federalism", "separation of powers", 
        "checks and balances", "rule of law", "civil rights", "human rights", "freedom", "corruption", 
        "propaganda", "censorship", "opposition", "activism", "liberalism", "conservatism", "socialism", 
        "communism", "nationalism", "populism", "capitalism", "anarchism", "fascism", "progressivism", 
        "centrism", "left-wing", "right-wing", "green politics", "united nations", "nato", "european union", 
        "g7", "g20", "oecd", "imf", "world bank", "state", "nation", "sovereignty", "embassy",
        "foreign affairs", "international relations", "protest", "coup", "revolution", "scandal", "speech", 
        "summit", "debate", "policy reform", "civil unrest", "public opinion", "approval rating", "campaign trail"
    ],
    "disasters": [
        "natural disaster", "man-made disaster", "emergency response", "search and rescue", "first responders",
        "emergency", "accident", "crash", "explosion", "fire", "flood", "earthquake", "disaster", "tsunami", "hurricane", "tornado", 
        "storm", "cyclone", "volcano", "eruption", "landslide", "avalanche", "drought", "heatwave", "wildfire", 
        "blizzard", "hailstorm", "rescue", "evacuation", "hazard", 
        "crisis", "catastrophe", "aftershock", "warning", "alert", "relief", "damage", 
        "casualties", "aid", "shelter", "environmental disaster", 
        "nuclear accident", "chemical spill", "oil spill", "radioactive", "blackout", "infrastructure collapse", 
        "risk assessment", "disaster preparedness", "early warning system"
    ],
    "economy": [
        "economic indicators", "housing market", "real estate", "economic development", "emerging markets", "inflation rate",
        "funding", "crisis", "inflation", "market", "oil", "currency", "bank", "interest rate", "unemployment", 
        "recession", "growth", "gdp", "budget", "deficit", "surplus", "stock", "stock market", "investment", 
        "trade", "exports", "imports", "tariff", "tax", "fiscal policy", "monetary policy", "central bank", "debt", 
        "public debt", "credit", "bonds", "financial", "capital", "income", "wages", "productivity",
        "commodities", "exchange rate", "business", "industry", "enterprise", "consumer", 
        "spending", "savings", "economic reform", 
        "economic stability", "subsidy", "regulation", "economic policy"
    ],
    "social": [
        "education reform", "social assistance", "higher education", "child care",
        "population", "education", "pension", "unemployment", "housing", "medicine",
        "school", "university", "children", "youth", "reform", "family", "migration",
        "minorities", "inequality", "poverty", "discrimination", "community"
    ],
    "health": [
        "mental health", "public health", "health care", "healthcare system", "chronic disease", "infectious disease", 
        "disease outbreak", "disease prevention", "medical research", "health insurance",
        "virus", "vaccine", "epidemic", "health", "doctor", "treat", "disease", "illness", "infection", "pandemic",
        "symptom", "diagnosis", "treatment", "medicine", "medication", "hospital", "clinic", "nurse", "patient",
        "physical health", "chronic", "acute", "prevention", "immunity", 
        "immune system", "outbreak", "medical", "surgery", "first aid", "telemedicine", "quarantine", "isolation", "contagious", "recovery", "mortality", 
        "morbidity", "wellness", "nutrition", "fitness", "exercise", "obesity", "diabetes", "cancer", 
        "cardiovascular", "respiratory", "therapy", "psychology", "psychiatry", "vital signs", "check-up",
        "screening", "side effects", "prescription", "pharmacy"
    ],
    "ecology": [
        "climate change", "global warming", "carbon footprint", "greenhouse gases", "sea level rise", "environmental policy", 
        "renewable energy", "solar energy", "wind energy", "environmental protection", "sustainable development", 
        "biodiversity", "ozone layer", "soil degradation", "environmental awareness", "environmental movement", "ecological balance",
        "ecology", "climate", "emission", "nature", "pollution", "environment", "sustainability", 
        "deforestation", "reforestation", "recycling", "ecosystem", "conservation", "wildlife", "endangered species", "habitat", 
        "air quality", "water quality", "waste", "toxic", "contamination", "green energy", "organic", 
        "climate action", "carbon neutral", "natural resources", "overconsumption", 
        "environmental impact", "acid rain", "climate crisis", "carbon emissions", "environmental degradation"
    ],
    "tech": [
        "artificial intelligence", "machine learning", "data science", "cloud computing", "big data", "cyber security", 
        "blockchain", "virtual reality", "augmented reality", "internet of things", "quantum computing", "digital transformation", 
        "mobile application", "user interface", "user experience", "automation tools", "nanotechnology", "it infrastructure", 
        "ai", "internet", "cyberattack", "technology", "robot", "digitalization", "automation", 
        "algorithm", "software", "hardware", "programming", "coding", "cybersecurity", "encryption", "network", 
        "server", "database", "iot", "smartphone", "mobile", "app", "platform", "social media", "digital", 
        "5g", "wireless", "satellite", "semiconductor", "tech industry", "start-up", "innovation", "tech company", 
        "hacking", "malware", "firewall", "biometrics", "cloud", "smart technology", "wearable"
    ],
}

def normalize(text):
    text = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()

def lemmatize(text):
    words = word_tokenize(text)
    return [lemmatizer.lemmatize(word) for word in words]

def classify_topic_en(text: str) -> str:
    if not text or len(text.strip()) < 20:
        return "other"
    text_norm = normalize(text)
    words = [lemmatizer.lemmatize(w) for w in word_tokenize(text_norm)]
    bigrams = set(" ".join([words[i], words[i+1]]) for i in range(len(words)-1))
    lemmas = set(words)

    topic_scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            kw_norm = normalize(kw)
            if " " in kw_norm:
                if kw_norm in text_norm or kw_norm in bigrams:
                    score += 1
            else:
                if kw_norm in lemmas:
                    score += 1
        topic_scores[topic] = score
    best_topic = max(topic_scores, key=topic_scores.get)
    if topic_scores[best_topic] == 0:
        return "other"
    return best_topic
