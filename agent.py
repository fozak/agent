import subprocess
import json
import uuid
import openai

# Set your OpenAI API key
openai.api_key = 'your-api-key'

def query_llm(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # or use the appropriate model
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()

class AutonomousAgent:
    def __init__(self, memory_file='memory.json'):
        self.memory_file = memory_file
        self.history = self.load_memory()

    def load_memory(self):
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def run_command(self, command):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=20)
            return output.decode().strip()
        except subprocess.CalledProcessError as e:
            return e.output.decode().strip()
        except Exception as e:
            return f"ERROR: {e}"

    def generate_next_action(self):
        goal = """
Your task is to identify 1–2 major applications installed or running on this Linux machine.
Examples: Discourse, Nocodb, ERPnext etc. They use Redis, MongoDB, Docker, Nginx, PostgreSQL, etc.

Determine:
- Whether it is installed
- Whether it is running
- If it seems healthy

Only return a single Linux shell command per step. Do not explain anything.
"""
        context = "\n".join([f"Step {i+1}:\nAction: {item['action']}\nResult: {item['result'][:300]}" for i, item in enumerate(self.history[-5:])])
        prompt = f"""
{goal}

--- Recent History ---
{context}

What is the next best Linux command to run?
"""
        return query_llm(prompt)

    def execute_and_record(self, action):
        print("\n🔧 Running command...")
        result = self.run_command(action)
        print(f"\n📄 Output (truncated):\n{result[:1000]}\n")
        self.history.append({
            "id": str(uuid.uuid4()),
            "action": action,
            "result": result
        })
        self.save_memory()

    def goal_achieved(self):
        summary = "\n".join([f"Action: {h['action']}\nResult: {h['result'][:200]}" for h in self.history])
        prompt = f"""
Has the following investigation identified at least one major app (e.g., mysql, redis, nginx, etc.) and checked whether it is running and healthy?

Respond only "yes" or "no".

{summary}
"""
        result = query_llm(prompt).lower()
        return "yes" in result

def main():
    agent = AutonomousAgent()

    print("🤖 Autonomous Linux App Detector (Manual Review Mode)\n")

    while not agent.goal_achieved():
        action = agent.generate_next_action()
        print(f"\n🧠 Next Command: {action}")

        choice = input("\nPress:\n[1] to run it\n[2] to skip it\n[3] to exit\n> ").strip()

        if choice == "1":
            agent.execute_and_record(action)
        elif choice == "2":
            print("⏭️ Skipped.\n")
            continue
        elif choice == "3":
            print("👋 Exiting.")
            break
        else:
            print("⚠️ Invalid input. Try again.")

    if agent.goal_achieved():
        print("✅ Goal complete: major app(s) identified and evaluated.")

if __name__ == "__main__":
    main()
