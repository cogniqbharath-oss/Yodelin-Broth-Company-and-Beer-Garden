export async function onRequestPost(context) {
    try {
        // Force rebuild comment
        const { request, env } = context;
        const { message } = await request.json();

        if (!message) {
            return new Response(JSON.stringify({ error: "No message provided" }), {
                status: 400,
                headers: { "Content-Type": "application/json" },
            });
        }

        const apiKey = env.GEMINI_API_KEY || "AIzaSyAU2_OXsU1nZ0A9q15w9fhaBYv2MBdz1UU";
        if (!apiKey) {
            return new Response(JSON.stringify({ error: "Configuration Error: GEMINI_API_KEY missing" }), {
                status: 500,
                headers: { "Content-Type": "application/json" },
            });
        }

        const contextPrompt = `
    You are the helpful AI assistant for Yodelin Broth Company & Beer Garden in Leavenworth, WA. 
    We are a stylish, rustic joint offering bone broth, burgers, salads, and craft beer with mountain views.
    Location: 633 Front St #1346, Leavenworth, WA.
    Hours: Mon-Thu 11am-9pm, Fri-Sun 11am-9pm.
    We do takeout (ToastTab) and have a beer garden.
    We specialize in Bone Broth (healing, 24hr simmer) and Craft Beer interactions (inventory varies).
    Tone: Friendly, rustic, helpful, slightly hipster/outdoorsy but professional.
    Keep answers concise (under 50 words usually).
    `;

        const fullPrompt = `${contextPrompt}\nUser asked: ${message}`;

        // Models to try in order
        const modelsToTry = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro"
        ];

        let errors = [];

        for (const model of modelsToTry) {
            try {
                const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

                const response = await fetch(apiUrl, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        contents: [{ parts: [{ text: fullPrompt }] }]
                    }),
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Model ${model} failed: ${response.status} ${errorText}`);
                }

                const data = await response.json();
                // Check if candidate exists
                if (!data.candidates || !data.candidates[0] || !data.candidates[0].content) {
                    throw new Error(`Model ${model} returned no candidates: ${JSON.stringify(data)}`);
                }
                const reply = data.candidates[0].content.parts[0].text;

                return new Response(JSON.stringify({ reply }), {
                    headers: { "Content-Type": "application/json" },
                });

            } catch (error) {
                console.error(error);
                errors.push(error.message);
                // Continue to next model
            }
        }

        throw new Error("All models failed. Details: " + errors.join("; "));

    } catch (error) {
        return new Response(JSON.stringify({ error: `AI Service Error: ${error.message}` }), {
            status: 502,
            headers: { "Content-Type": "application/json" },
        });
    }
}
