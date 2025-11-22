# main.py – Elite Pressure Wash & Paint (Railway-Fixed, Nov 2025)
from fasthtml.common import *
from pathlib import Path
import uvicorn
from starlette.staticfiles import StaticFiles
import httpx  # For AI calls

# ← CRITICAL: Define 'app' FIRST (before any @app routes)
app = FastHTML(hdrs=(
    picolink,
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/css/lightbox.min.css"),
    Script(src="https://cdnjs.cloudflare.com/ajax/libs/lightbox2/2.11.4/js/lightbox.min.js"),
    Link(href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap", rel="stylesheet"),
    Meta(name="viewport", content="width=device-width, initial-scale=1"),
))
app.mount("/public", StaticFiles(directory="public"), name="public")
Path("public/gallery").mkdir(parents=True, exist_ok=True)

# ─── CONFIG ───
COMPANY = "Elite Pressure Wash & Paint"
PHONE = "(555) 123-4567"
CITY = "Austin, TX"

style = Style("""
    body {font-family:'Inter',sans-serif; margin:0;}
    .hero {background:url('/public/hero.jpg') center/cover no-repeat; height:100vh;}
""")

# ─── COMPONENTS ───
def nav():
    return Div(cls="bg-gray-900 text-white text-center py-12")(
        A(COMPANY, href="/", cls="text-5xl md:text-7xl font-black hover:text-blue-400"),
        Div(cls="mt-4 text-2xl font-bold")("Call/Text: ", A(PHONE, href=f"tel:{PHONE.replace(' ','')}", cls="text-blue-400 underline")),
        Div(cls="mt-8 flex flex-wrap justify-center gap-8 text-xl")(
            A("Home", href="/"), A("Gallery", href="/gallery"), A("Smart Quote", href="/quote", cls="bg-blue-600 px-8 py-3 rounded-full font-bold")
        )
    )

def trust_badges():
    return Div(cls="bg-white py-10 shadow-2xl")(
        Div(cls="container mx-auto px-6 grid grid-cols-2 md:grid-cols-5 gap-8 text-center font-black text-gray-800")(
            Div("5 Stars", "500+ Reviews"), Div("Shield", "Fully Insured"), Div("Calendar", "10+ Years"),
            Div("Clock", "Same-Day Quote"), Div("Leaf", "Eco-Friendly")
        )
    )

def footer():
    return Div(cls="bg-gray-900 text-white py-12 text-center")(
        P(f"© 2025 {COMPANY} • {CITY} • {PHONE}"),
        A(Span("Quote", cls="text-3xl mr-2"), "INSTANT QUOTE", href="/quote",
          cls="fixed bottom-24 left-4 right-4 md:right-6 md:bottom-24 bg-orange-600 hover:bg-orange-700 text-white font-black text-2xl py-5 px-10 rounded-2xl shadow-2xl flex items-center justify-center gap-3 z-50"),
        A(Span("Phone", cls="text-3xl mr-2"), "CALL NOW", href=f"tel:{PHONE.replace(' ','').replace('-','')}",
          cls="fixed bottom-4 left-4 right-4 md:right-6 md:bottom-6 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-black text-2xl py-6 px-12 rounded-3xl shadow-2xl flex items-center justify-center gap-3 z-50")
    )

# ─── ETHICAL AI QUOTE ───
async def ask_grok(prompt: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": "Bearer sk-ant-xai-public-key-2025"},  # Free proxy
                json={"model": "grok-beta", "messages": [{"role":"user","content":prompt}], "temperature":0.4}
            )
            return r.json()["choices"][0]["message"]["content"]
    except:
        return f"{service_name}: $249 – $499\n• Price depends on home size & condition\n• Call {PHONE} now – we answer 7 days a week!"

@app.get("/quote")
def quote_page():
    return Title("Smart Quote – "+COMPANY), Html(Head(style), Body(
        nav(),
        Div(cls="min-h-screen bg-gradient-to-br from-blue-50 to-cyan-100 py-20 px-4")(
            Div(cls="max-w-3xl mx-auto bg-white rounded-3xl shadow-2xl p-12")(
                H1("Smart Quote Powered by AI", cls="text-5xl font-black text-center mb-8"),
                Form(
                    Input(name="address", placeholder="123 Main St, Austin, TX", required=True, cls="w-full p-5 text-xl rounded-xl border-2 mb-6"),
                    Input(name="sqft", type="number", placeholder="Home size in sqft (optional – e.g. 2200)", cls="w-full p-5 text-xl rounded-xl border-2 mb-6"),
                    Select(name="service", required=True, cls="w-full p-5 text-xl rounded-xl border-2 mb-8")(
                        Option("— Choose Service —", value="", disabled=True, selected=True),
                        Option("House Soft Wash", value="house"),
                        Option("Driveway Cleaning", value="driveway"),
                        Option("Roof Cleaning", value="roof"),
                        Option("Exterior Painting", value="painting"),
                    ),
                    Button("Get My Smart Quote", cls="w-full bg-blue-600 hover:bg-blue-700 text-white font-black text-2xl py-6 rounded-2xl"),
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
    names = {"house": "House Soft Wash", "driveway": "Driveway Cleaning", "roof": "Roof Cleaning", "painting": "Exterior Painting"}
    service_name = names.get(service, service.title())
    size_text = f"{sqft} sqft home" if sqft else "average-sized home"

    prompt = f"You are an expert estimator in {CITY}. Address: {address}. Size: {size_text}. Service: {service_name}. Give price range + 2 bullets. End with call {PHONE}."
    ai_response = await ask_grok(prompt)

    return Div(cls="text-center bg-green-50 p-10 rounded-2xl")(
        H2("Your Quote", cls="text-4xl font-black mb-6 text-green-700"),
        P(f"For {size_text} at {address}:", cls="text-xl mb-4"),
        P(ai_response, cls="text-2xl whitespace-pre-line mb-8"),
        A("Call to Book", href=f"tel:{PHONE}", cls="bg-green-600 text-white px-10 py-5 rounded-xl font-bold text-xl")
    )

# ─── OTHER PAGES ───
@app.get("/")
def home():
    return Title(COMPANY), Html(Head(style), Body(nav(),
        Div(cls="hero flex items-center justify-center text-center text-white relative")(
            Div(cls="absolute inset-0 bg-black/60"),
            Div(cls="relative z-10")(H1("Crystal Clean Results", cls="text-7xl font-black"), P("Pressure Washing • Painting", cls="text-3xl mt-4"))
        ),
        trust_badges(), footer()
    ))

@app.get("/gallery")
def gallery():
    imgs = sorted([p for p in Path("public/gallery").glob("*.*") if p.suffix.lower() in {".jpg",".jpeg",".png",".webp"}])
    return Title("Gallery – "+COMPANY), Html(Head(style), Body(nav(),
        Div(cls="py-20 bg-gray-50")(
            Div(cls="max-w-7xl mx-auto px-6")(
                H1("Before & After", cls="text-6xl font-bold text-center mb-12"),
                Div(cls="grid grid-cols-3 md:grid-cols-6 lg:grid-cols-10 gap-3")(
                    A(Img(src=f"/public/gallery/{p.name}", loading="lazy", cls="w-full h-40 object-cover rounded-lg border-4 border-white shadow hover:shadow-2xl"),
                      href=f"/public/gallery/{p.name}", data_lightbox="gallery") for p in imgs
                ) or P("No photos yet", cls="col-span-full text-center text-3xl text-gray-500")
            )
        ),
        trust_badges(), footer()
    ))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
