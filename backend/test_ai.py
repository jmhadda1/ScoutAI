import ollama

response = ollama.chat(

    model="qwen2.5vl",

    messages=[

        {

            "role":"user",

            "content":"Say hello from Scout AI."

        }

    ]

)

print(response["message"]["content"])