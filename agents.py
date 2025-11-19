import openai

# -------------------------------------------------
# 1. SETUP
# -------------------------------------------------
openai.api_key = "sk-proj-qXig_Pr7-m_sfwHW5RLkRiO9hPs8u9mANNIAaCJRME7GiAx3CEvJzcym7VZi4ESKjwBhbLBGN1T3BlbkFJ3rqNbQUYdMh-yi4zQVAJnQwFUvnHJBsMFpMwdOpOWLIHaYiB2jSNC3SAKScd6nm6nggatxixQAAnalyze customer purchasing behavior and group customers into meaningful segments such as high-value, frequent shoppers, and new users."

def ask_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]


# -------------------------------------------------
# 2. AGENTS
# -------------------------------------------------

# PLANNER AGENT
def planner_agent(user_request):
    prompt = f"""
    You are a Planner Agent. Break the following request into 3–4 clear steps.
    Return steps line by line.

    Request: {user_request}
    """
    result = ask_llm(prompt)
    steps = result.split("\n")
    steps = [s.strip() for s in steps if s.strip()]
    return steps


# DATA AGENT
def data_agent(step):
    prompt = f"""
    You are a Data Agent. Explain what data is needed for this step:

    Step: {step}
    """
    return ask_llm(prompt)


# ANALYSIS AGENT
def analysis_agent(step, data_info):
    prompt = f"""
    You are an Analysis Agent.
    Based on this step and available data info, produce a short analysis.

    Step: {step}
    Data Info: {data_info}
    """
    return ask_llm(prompt)


# REPORT AGENT
def report_agent(user_request, steps, analysis_results):
    prompt = f"""
    You are a Report Agent. Create a clean professional report.

    User Request: {user_request}

    Steps:
    {steps}

    Analysis:
    {analysis_results}

    Write the final summary in bullet points + final conclusion.
    """
    return ask_llm(prompt)


# -------------------------------------------------
# 3. ORCHESTRATOR – RUN ALL AGENTS
# -------------------------------------------------

def run_enterprise_agents(user_request):
    print("\n=== ENTERPRISE AI AGENT SYSTEM ===\n")

    print("📌 User Request:")
    print(user_request)
    print("\n----------------------------------")

    # 1. Planning
    print("\n📌 Planner Agent:")
    steps = planner_agent(user_request)
    for i, step in enumerate(steps, 1):
        print(f"Step {i}: {step}")

    # 2. Data + Analysis
    analysis_results = []
    for step in steps:
        print("\n📌 Data Agent:")
        data_info = data_agent(step)
        print("Data Needed:", data_info)

        print("\n📌 Analysis Agent:")
        analysis = analysis_agent(step, data_info)
        print("Analysis:", analysis)
        analysis_results.append(f"Step: {step}\nAnalysis: {analysis}")

    # 3. Final Report
    print("\n📌 Report Agent: Generating final report...\n")
    final_report = report_agent(user_request, steps, analysis_results)

    print("\n===== FINAL REPORT =====\n")
    print(final_report)
    print("\n=========================\n")

    return final_report


# -------------------------------------------------
# 4. MAIN – RUN THE PROGRAM
# -------------------------------------------------

if __name__ == "__main__":
    print("Enter your enterprise task:")
    user_request = input("> ")

    run_enterprise_agents(user_request)
