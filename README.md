================================================================================
README: AUTONOMOUS MULTI-AGENT SUPPORT ORCHESTRATOR
Quickstart & Evaluation Guide
================================================================================

PROJECT OVERVIEW
----------------
An enterprise customer support engine utilizing domain-specialized AI agents
(Billing, Logistics, Technical Diagnostics, Account Security) backed by hardcoded
deterministic Python guardrails (₹3,500.00 ceiling) and real-time supervisory
Human-in-the-Loop escalation.

 
--------------------------------------------------------------------------------
1. PREREQUISITES
--------------------------------------------------------------------------------
- Python 3.10 or higher installed.
- A free Google Gemini API Key (obtain from: https://aistudio.google.com/).
- Git (for cloning the repository).
--------------------------------------------------------------------------------
2. INSTALLATION & ENVIRONMENT SETUP
--------------------------------------------------------------------------------
Step 1: Clone the repository and enter the folder
   git clone https://github.com/<your-username>/autonomous-support-agent.git
   cd autonomous-support-agent

Step 2: Create a virtual environment
   - On macOS/Linux:
     python3 -m venv venv
     source venv/bin/activate

   - On Windows (Command Prompt):
     python -m venv venv
     venv\Scripts\activate.bat

   - On Windows (PowerShell):
     python -m venv venv
     venv\Scripts\Activate.ps1

Step 3: Install dependencies
   pip install -r requirements.txt

   (Direct installation alternative: pip install streamlit google-genai pandas python-dotenv)

Step 4: Configure environment variables
   Create a file named ".env" in the root directory:
   GEMINI_API_KEY="your_actual_gemini_api_key_here"


--------------------------------------------------------------------------------
3. LAUNCHING THE APPLICATION
--------------------------------------------------------------------------------
Run the Streamlit app from your terminal:
   streamlit run app.py

Access the live web dashboard in your browser:
   http://localhost:8501


--------------------------------------------------------------------------------
4. INTERFACE LAYOUT
--------------------------------------------------------------------------------
- Left Panel (Customer Experience Portal):
  Interactive chat interface where users submit requests for refunds,
  order tracking, diagnostics, or account recovery.

- Right Panel (Governance & Supervisor Engine):
  * Tab 1 (Live Telemetry Stream): Real-time audit log of agent selection,
    tool arguments, execution results, and latency traces.
  * Tab 2 (Escalation Queue): Displays high-risk incident cards halted by
    safety guardrails with 1-Click "Approve" or "Reject" supervisor actions.
  * Tab 3 (In-Memory DB): Live ledger and database status updates.


--------------------------------------------------------------------------------
5. STEP-BY-STEP DEMO TEST PROMPTS (COPY & PASTE)
--------------------------------------------------------------------------------

TEST CASE 1: Autonomous In-Policy Refund (Safe Execution)
--------------------------------------------------------
- Concept: Verifies autonomous database ledger mutation when request is under
  the policy limit (₹2,000 <= ₹3,500).
- Paste in Customer Chat (Left):
  I noticed an accidental duplicate charge of ₹2,000 on my account for order ORD-101 (Mechanical Keyboard). Please check the ledger and refund it.
- Expected Behavior:
  * Left Panel: Generates an instant refund receipt (REF-ORD-101-SUCCESS) in sub-3s.
  * Right Panel -> Tab 1 (Telemetry): Billing Agent executes with AUTONOMOUS_SUCCESS.
  * Right Panel -> Tab 3 (DB): Order ORD-101 status mutates to "Refunded".


TEST CASE 2: Deterministic Safety Guardrail (₹2.5 Lakh Breach & Damage)
-----------------------------------------------------------------------
- Concept: Verifies that physical damage claims and transactions exceeding
  the threshold (₹2,50,000 > ₹3,500) halt autonomy and force supervisory review.
- Paste in Customer Chat (Left):
  My Pro Studio Display monitor in order ORD-202 (₹2,50,000) arrived with a completely cracked and shattered display panel. I demand an immediate refund right now.
- Expected Behavior:
  * Left Panel: Autonomy halts immediately. System informs customer that
    physical damage and values exceeding ₹3,500 require management sign-off.
  * Right Panel -> Tab 2 (Escalations): A high-priority red incident card appears
    showing Ticket #ESC-001, ₹250,000.00 amount, and physical damage trigger.
  * Action: Click "✅ 1-Click Approve" button on the card to execute the
    supervisor override and update the ledger.
================================================================================
