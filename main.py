@app.get("/quote")
def quote_page():
    return Title("Instant Quote – "+COMPANY), Html(Head(style), Body(
        nav(),
        Div(cls="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-20 px-4")(
            Div(cls="max-w-3xl mx-auto bg-white/95 backdrop-blur rounded-3xl shadow-2xl p-10 md:p-16")(
                H1("Your Price in 5 Seconds", cls="text-5xl md:text-6xl font-black text-center mb-6 text-gray-800"),
                P("Our AI gives you an accurate range instantly – no waiting, no forms", cls="text-center text-xl text-gray-600 mb-12"),

                Form(
                    # Address (for personalization only – no scraping)
                    Input(name="address", placeholder="123 Oak Street, Austin, TX", required=True,
                          cls="w-full p-5 text-xl rounded-xl border-2 mb-5 focus:border-blue-600 outline-none"),

                    # Optional sqft – 90 % of homeowners know this or can guess
                    Input(name="sqft", type="number", placeholder="Home size in sqft (optional – e.g. 2200)",
                          cls="w-full p-5 text-xl rounded-xl border-2 mb-5 focus:border-blue-600 outline-none"),

                    # Service picker
                    Select(name="service", required=True, cls="w-full p-5 text-xl rounded-xl border-2 mb-8")(
                        Option("— Choose Your Service —", value="", disabled=True, selected=True),
                        Option("House Soft Wash", value="house"),
                        Option("Driveway + Walkways", value="driveway"),
                        Option("Roof Cleaning", value="roof"),
                        Option("Deck / Fence", value="deck"),
                        Option("Exterior Painting", value="painting"),
                    ),

                    Button("Show My Price →", cls="w-full bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white font-black text-2xl py-6 rounded-2xl shadow-2xl transform hover:scale-105 transition"),
                    hx_post="/ethical-quote", hx_target="#result", hx_swap="innerHTML"
                ),
                Div(id="result", cls="mt-12")
            )
        ),
        trust_badges(),
        footer()
    ))

@app.post("/ethical-quote")
async def ethical_quote(address: str, service: str, sqft: str = ""):
    # Clean human-readable names
    names = {
        "house": "House Soft Wash",
        "driveway": "Driveway + Walkways",
        "roof": "Roof Cleaning",
        "deck": "Deck / Fence Restoration",
        "painting": "Exterior Painting"
    }
    service_name = names.get(service, service.title())

    # Use provided sqft or smart fallback
    size_text = f"{sqft} sqft home" if sqft else "average-sized home in your area"

    prompt = f"""
    You are the friendliest, most accurate pressure-washing & painting estimator in {CITY}.
    Customer just entered: {address}
    Home size: {size_text}
    Service requested: {service_name}

    Give a realistic price RANGE only (example: $279 – $399).
    Add 2 short bullets explaining what affects the final price.
    End with: “Call {PHONE} now – we answer 7 days a week!”
    Keep total response under 4 lines.
    """

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": "Bearer sk-ant-xai-public-key-2025"},
                json={"model": "grok-beta", "messages": [{"role":"user","content":prompt}], "temperature":0.4}
            )
            ai_response = r.json()["choices"][0]["message"]["content"]
    except:
        ai_response = f"{service_name}: $249 – $499\n• Price depends on home size & condition\n• Call {PHONE} now – we answer 7 days a week!"

    return Div(cls="text-center p-10 bg-gradient-to-b from-green-50 to-white rounded-3xl shadow-2xl")(
        H2("Your Instant Quote", cls="text-4xl font-black mb-6 text-green-700"),
        P(f"For {size_text} at {address}:", cls="text-xl text-gray-700 mb-4"),
        P(ai_response, cls="text-2xl md:text-3xl leading-relaxed whitespace-pre-line font-medium text-gray-800"),
        Div(cls="mt-8 space-x-4")(
            A("Call Now – Book It!", href=f"tel:{PHONE.replace(' ','')}",
              cls="inline-block bg-green-600 hover:bg-green-700 text-white font-bold text-xl px-10 py-5 rounded-2xl shadow-xl"),
            A("See Before & After", href="/gallery",
              cls="inline-block border-4 border-blue-600 hover:bg-blue-600 hover:text-white text-xl px-10 py-5 rounded-2xl font-bold transition")
        )
    )
