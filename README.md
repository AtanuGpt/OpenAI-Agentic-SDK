# OpenAI-Agentic-SDK

# 🧠 Multi-Agent DEMO with OpenAI Agent SDK

This repository demonstrates a modular, multi-agent proof-of-concept (POC) using the **OpenAI Agent SDK**. The system showcases how specialized agents can collaborate to solve domain-specific tasks such as retrieving a cricketer's birthplace, suggesting sightseeing spots, and generating budget-friendly travel itineraries.

---

## 🚀 Project Overview

The goal of this project is to illustrate the power of agentic architectures using OpenAI's Agent SDK. It features:

- A **triage agent** that intelligently routes user queries.
- Three specialized agents:
  - `CricketerPlaceOfBirth`: Fetches the city and country of birth of a cricket player.
  - `SightSeeingPlaces`: Suggests top sightseeing spots in a given city.
  - `TravelItineraryAdvisor`: Generates a budget-friendly travel itinerary.

Each agent is powered by `gpt-4o-mini` and designed with a focused instruction set.

---

## ✨ Features

- Modular agent definitions
- Intelligent handoff and orchestration
- Real-time streaming of responses
- Asynchronous execution
- Easily extensible architecture
- Agent workflow graph (Download GraphViz from https://graphviz.org/download/)

---

## 🧠 Architecture
User Query │ ▼ Triage Agent (Router) ├──> CricketerPlaceOfBirth Agent ├──> SightSeeingPlaces Agent └──> TravelItineraryAdvisor Agent
