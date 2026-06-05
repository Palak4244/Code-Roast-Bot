import os
from github import Github
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Groq client - free wala ChatGPT
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
g = Github(os.getenv("GITHUB_TOKEN"))

def roast_pr(repo_name, pr_number):
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    
    # PR ka code nikalo
    files = pr.get_files()
    code = ""
    for file in files:
        if file.filename.endswith('.py'):
            code += file.patch + "\n"
    
    if not code:
        return "Bhai Python file hi nahi hai PR me. Kya roast karu? 😭"
    
    # Fix: Triple quotes ke andar ``` use nahi kar sakte
    # Isliye code ko alag se jod rahe hain
    prompt = f"""
Tu ek savage FAANG senior engineer hai jiska naam "Code Chacha" hai. 
Tera kaam junior devs ke PR roast karna hai. 

Rules:
1. Hinglish me bol. Tapori Mumbai style. 
2. Gali mat de. Sirf dosti wala mazak.
3. Structure aisa rakhna:
   **Roast:** [2-3 line ka solid punch. Code ki sabse badi beizzati kar, lekin hasi aani chahiye,ek stand up comadian ki trh jaise harsh gujral ya zakir khan ki trh]
   **Rating:** [X/10 aur ek line me reason]
   **Tip by Senior SDE:** [1 coorect approach batao jo uuse help kare code likhne mein]

Code ye raha:
{code}

Yaad rakh: Cringe mat karna. Funny means inshan padh ke hasne se rok na paye khid ko aisa hona  hona chahiye. Samajh aana chahiye.
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Ye wala smart hai
        messages=[{"role": "user", "content": prompt}]
    )
    
    roast = response.choices[0].message.content
    return roast

# Test ke liye
if __name__ == "__main__":
    roast = roast_pr("Palak4244/Test---Roast", 1)
    print(roast)