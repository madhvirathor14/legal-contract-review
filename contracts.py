"""
Synthetic legal contract templates for all 3 tasks.
Realistic but fictional contracts used for agent evaluation.
3+ contracts per task for variety and reproducible seeding.
"""

from typing import List, Dict, Any


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1: FIND MISSING CLAUSES — Easy
# Contracts intentionally missing 2-4 standard clauses.
# ─────────────────────────────────────────────────────────────────────────────

FIND_MISSING_CONTRACTS: List[Dict[str, Any]] = [
    {
        "contract_id": "FM-001",
        "contract_title": "Software Development Services Agreement",
        "contract_text": """SOFTWARE DEVELOPMENT SERVICES AGREEMENT

This Agreement is entered into as of January 1, 2025, between TechCorp Solutions Inc.
("Client") and DevStudio Ltd. ("Developer").

1. SCOPE OF WORK
Developer agrees to design, develop, and deliver a web-based inventory management system
as described in Exhibit A attached hereto. Developer shall complete the work within 90 days.

2. PAYMENT TERMS
Client shall pay Developer a total of $50,000 USD. An initial payment of $20,000 is due upon
signing. The remaining $30,000 is due upon final delivery and acceptance of the software.

3. CONFIDENTIALITY
Each party agrees to maintain in confidence all Confidential Information received from the other
party and to use such information solely for purposes of this Agreement. This obligation shall
survive for 3 years after termination of this Agreement.

4. OWNERSHIP OF DELIVERABLES
All software, code, and documentation created under this Agreement shall be the exclusive
property of Client upon full payment. Developer retains no rights to the deliverables.

5. WARRANTIES
Developer warrants that the software will perform substantially in accordance with specifications
for a period of 90 days following delivery.""".strip(),
        "clauses": [
            {"clause_id": "clause_1", "title": "Scope of Work", "clause_type": "payment_terms",
             "text": "Developer agrees to design, develop, and deliver a web-based inventory management system within 90 days.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_2", "title": "Payment Terms", "clause_type": "payment_terms",
             "text": "Client shall pay Developer $50,000 USD. $20,000 due on signing, $30,000 due on final delivery.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_3", "title": "Confidentiality", "clause_type": "confidentiality",
             "text": "Each party maintains confidence of received information for 3 years post-termination.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_4", "title": "Ownership", "clause_type": "intellectual_property",
             "text": "All deliverables are Client's property upon full payment.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_5", "title": "Warranties", "clause_type": "payment_terms",
             "text": "Software will perform per specifications for 90 days post delivery.", "is_ambiguous": False, "flagged_for_analysis": False},
        ],
        "missing_clauses": ["termination", "dispute_resolution", "limitation_of_liability", "governing_law"],
        "task_description": (
            "EASY TASK: This Software Development Agreement is missing several standard protective clauses. "
            "Review the contract carefully and identify ALL missing clause types from the standard list: "
            "termination, confidentiality, indemnification, dispute_resolution, payment_terms, "
            "intellectual_property, limitation_of_liability, governing_law."
        ),
    },
    {
        "contract_id": "FM-002",
        "contract_title": "Commercial Lease Agreement",
        "contract_text": """COMMERCIAL LEASE AGREEMENT

This Lease Agreement is made on March 15, 2025 between Sunrise Properties LLC ("Landlord")
and RetailMax Inc. ("Tenant").

1. PREMISES AND TERM
Landlord leases to Tenant the commercial space at 45 Business Park Drive, Suite 200.
The lease term is 24 months, commencing April 1, 2025 and ending March 31, 2027.

2. RENT
Monthly rent is $8,500 USD, due on the 1st of each month. A security deposit of $17,000
(two months' rent) is due at signing.

3. USE OF PREMISES
Tenant shall use the premises solely for retail clothing sales. Any change in use requires
prior written consent from Landlord.

4. MAINTENANCE AND REPAIRS
Tenant is responsible for routine maintenance of the interior. Landlord is responsible for
structural repairs, roof, and HVAC systems.

5. GOVERNING LAW
This Agreement shall be governed by the laws of the State of California.""".strip(),
        "clauses": [
            {"clause_id": "clause_1", "title": "Premises and Term", "clause_type": "payment_terms",
             "text": "Leases Suite 200 for 24 months from April 1 2025.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_2", "title": "Rent", "clause_type": "payment_terms",
             "text": "Monthly rent $8,500 due 1st of month. $17,000 security deposit.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_3", "title": "Use of Premises", "clause_type": "payment_terms",
             "text": "Premises for retail clothing only. Change needs written consent.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_4", "title": "Maintenance", "clause_type": "payment_terms",
             "text": "Tenant maintains interior; Landlord maintains structure/HVAC.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_5", "title": "Governing Law", "clause_type": "governing_law",
             "text": "Governed by California law.", "is_ambiguous": False, "flagged_for_analysis": False},
        ],
        "missing_clauses": ["termination", "indemnification", "dispute_resolution"],
        "task_description": (
            "EASY TASK: This Commercial Lease Agreement is missing critical protective clauses. "
            "Review the contract carefully and identify ALL missing clause types from the standard list: "
            "termination, confidentiality, indemnification, dispute_resolution, payment_terms, "
            "intellectual_property, limitation_of_liability, governing_law."
        ),
    },
    {
        "contract_id": "FM-003",
        "contract_title": "Marketing Agency Services Agreement",
        "contract_text": """MARKETING AGENCY SERVICES AGREEMENT

This Agreement is entered into as of June 1, 2025, between BrandBoost Inc. ("Agency")
and FreshFoods Co. ("Client").

1. SERVICES
Agency shall provide digital marketing services including SEO, social media management,
and content creation as detailed in the attached Service Schedule.

2. FEES
Client shall pay Agency a monthly retainer of $12,000, due on the 1st of each month.
Additional project fees as quoted and approved in writing.

3. TERMINATION
Either party may terminate this Agreement upon 30 days written notice. Client shall pay
for all services rendered up to the termination date.

4. INDEMNIFICATION
Each party shall indemnify and hold harmless the other party from claims arising from
its own negligent acts or omissions in the performance of this Agreement.

5. GOVERNING LAW
This Agreement is governed by the laws of the State of New York.""".strip(),
        "clauses": [
            {"clause_id": "clause_1", "title": "Services", "clause_type": "payment_terms",
             "text": "Agency provides SEO, social media, and content creation services.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_2", "title": "Fees", "clause_type": "payment_terms",
             "text": "Monthly retainer $12,000 due 1st of month. Additional project fees quoted separately.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_3", "title": "Termination", "clause_type": "termination",
             "text": "30 days written notice to terminate. Client pays for services rendered.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_4", "title": "Indemnification", "clause_type": "indemnification",
             "text": "Each party indemnifies the other for its own negligent acts.", "is_ambiguous": False, "flagged_for_analysis": False},
            {"clause_id": "clause_5", "title": "Governing Law", "clause_type": "governing_law",
             "text": "Governed by New York law.", "is_ambiguous": False, "flagged_for_analysis": False},
        ],
        "missing_clauses": ["confidentiality", "intellectual_property", "dispute_resolution", "limitation_of_liability"],
        "task_description": (
            "EASY TASK: This Marketing Agency Agreement is missing several standard clauses. "
            "Review the contract carefully and identify ALL missing clause types from the standard list: "
            "termination, confidentiality, indemnification, dispute_resolution, payment_terms, "
            "intellectual_property, limitation_of_liability, governing_law."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2: IDENTIFY RISKY PARTY — Medium
# Contracts with clearly one-sided clauses.
# ─────────────────────────────────────────────────────────────────────────────

IDENTIFY_RISKY_CONTRACTS: List[Dict[str, Any]] = [
    {
        "contract_id": "IR-001",
        "contract_title": "Freelance Content Creation Agreement",
        "contract_text": """FREELANCE CONTENT CREATION AGREEMENT

Agreement between MediaHouse Corp. ("Client" / Party A) and Jane Smith ("Freelancer" / Party B),
dated Feb 1, 2025.

1. SERVICES
Freelancer will produce 20 blog articles per month on topics assigned by Client.

2. PAYMENT
Client will pay $500 per month, payable at Client's discretion within 90 days of invoice.
Client may withhold payment if it deems the content unsatisfactory, with no obligation to
specify reasons or provide revision opportunity.

3. REVISIONS
Freelancer shall provide unlimited revisions at no extra cost for as long as Client requests,
including revisions requested 6 months after original delivery.

4. INTELLECTUAL PROPERTY
All content created by Freelancer, including unpublished drafts, becomes the exclusive
property of Client immediately upon creation, without additional compensation.

5. NON-COMPETE
Freelancer shall not create content for any competitor of Client, as defined solely by Client,
for a period of 5 years following termination of this Agreement.

6. TERMINATION
Client may terminate this Agreement at any time without notice and without obligation to pay
for work in progress. Freelancer may not terminate without 180 days written notice.

7. DISPUTE RESOLUTION
All disputes shall be resolved through binding arbitration in Client's home city,
with all arbitration costs borne entirely by Freelancer.""".strip(),
        "clauses": [
            {"clause_id": "clause_2", "title": "Payment", "clause_type": "payment_terms",
             "text": "Client pays $500/month at Client's discretion within 90 days. May withhold without reason.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_3", "title": "Revisions", "clause_type": "payment_terms",
             "text": "Freelancer provides unlimited revisions including 6 months after delivery.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_5", "title": "Non-Compete", "clause_type": "payment_terms",
             "text": "No competing content for 5 years post-termination, competitor defined by Client alone.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_6", "title": "Termination", "clause_type": "termination",
             "text": "Client may terminate immediately with no pay. Freelancer needs 180 days notice.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_7", "title": "Dispute Resolution", "clause_type": "dispute_resolution",
             "text": "All disputes in Client's city. All arbitration costs paid by Freelancer.",
             "is_ambiguous": False, "flagged_for_analysis": True},
        ],
        "risky_clauses": {
            "clause_2": "Party B",
            "clause_3": "Party B",
            "clause_5": "Party B",
            "clause_6": "Party B",
            "clause_7": "Party B",
        },
        "party_a": "MediaHouse Corp. (Client)",
        "party_b": "Jane Smith (Freelancer)",
        "task_description": (
            "MEDIUM TASK: Analyze this Freelance Agreement. Clause 6 (Termination) has been flagged. "
            "Which party is disadvantaged by this termination clause: "
            "'Party A' (MediaHouse Corp.) or 'Party B' (Jane Smith / Freelancer)? "
            "Provide your legal reasoning explaining the imbalance."
        ),
        "target_clause_id": "clause_6",
        "target_answer": "Party B",
    },
    {
        "contract_id": "IR-002",
        "contract_title": "SaaS Platform Subscription Agreement",
        "contract_text": """SAAS PLATFORM SUBSCRIPTION AGREEMENT

Between CloudBase Inc. ("Provider" / Party A) and StartupXYZ Ltd. ("Customer" / Party B),
effective January 1, 2025.

1. SUBSCRIPTION SERVICES
Provider grants Customer access to the CloudBase analytics platform under the selected plan.

2. FEES AND PAYMENT
Provider may increase subscription fees at any time upon 7 days notice. Customer has no right
to dispute fee increases and must pay the revised fee or lose access immediately.

3. DATA OWNERSHIP
Customer data uploaded to the platform becomes joint property of both parties upon upload.
Provider may use Customer's data for AI model training, product improvement, and marketing
without additional consent or compensation.

4. UPTIME AND SLA
Provider targets 95% uptime but this is aspirational only and creates no legal obligation.
Customer's sole remedy for downtime is a service credit of $10, regardless of actual losses.

5. TERMINATION
Customer may cancel with 12 months advance notice. Provider may terminate immediately for any
reason. No refunds are provided upon termination under any circumstances.""".strip(),
        "clauses": [
            {"clause_id": "clause_2", "title": "Fees and Payment", "clause_type": "payment_terms",
             "text": "Provider may increase fees anytime with 7 days notice. Customer cannot dispute.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_3", "title": "Data Ownership", "clause_type": "intellectual_property",
             "text": "Customer data becomes joint property. Provider uses it for AI training without consent.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_4", "title": "Uptime SLA", "clause_type": "payment_terms",
             "text": "95% uptime is aspirational only. Remedy is $10 credit regardless of losses.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_5", "title": "Termination", "clause_type": "termination",
             "text": "Customer needs 12 months notice. Provider can terminate immediately. No refunds.",
             "is_ambiguous": False, "flagged_for_analysis": True},
        ],
        "risky_clauses": {
            "clause_2": "Party B",
            "clause_3": "Party B",
            "clause_4": "Party B",
            "clause_5": "Party B",
        },
        "party_a": "CloudBase Inc. (Provider)",
        "party_b": "StartupXYZ Ltd. (Customer)",
        "task_description": (
            "MEDIUM TASK: Analyze this SaaS Agreement. Clause 3 (Data Ownership) has been flagged. "
            "Which party is disadvantaged by this data ownership clause: "
            "'Party A' (CloudBase Inc.) or 'Party B' (StartupXYZ Ltd.)? "
            "Provide your legal reasoning."
        ),
        "target_clause_id": "clause_3",
        "target_answer": "Party B",
    },
    {
        "contract_id": "IR-003",
        "contract_title": "Construction Subcontractor Agreement",
        "contract_text": """CONSTRUCTION SUBCONTRACTOR AGREEMENT

Between BuildRight Construction LLC ("General Contractor" / Party A) and IronWorks Ltd.
("Subcontractor" / Party B), dated March 1, 2025.

1. SCOPE OF WORK
Subcontractor shall perform all steel fabrication and installation work as per project specs.

2. PAYMENT
General Contractor shall pay Subcontractor within 90 days of invoice submission.
Payment is conditional on General Contractor receiving payment from the project owner.
If the owner does not pay General Contractor, General Contractor has no obligation to pay
Subcontractor, regardless of work completed.

3. CHANGES
General Contractor may direct changes to the scope at any time. Subcontractor must comply
immediately. Compensation for changes is at General Contractor's sole discretion.

4. LIABILITY
Subcontractor assumes full liability for any project delays, defects, or claims arising from
the project, including delays caused by General Contractor or third parties.

5. INSURANCE
Subcontractor shall maintain $5,000,000 in liability insurance and name General Contractor
as additional insured at Subcontractor's expense. General Contractor carries no insurance.""".strip(),
        "clauses": [
            {"clause_id": "clause_2", "title": "Payment", "clause_type": "payment_terms",
             "text": "Payment conditional on owner paying GC. No payment to Subcontractor if owner doesn't pay.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_3", "title": "Changes", "clause_type": "payment_terms",
             "text": "GC may change scope anytime. Subcontractor must comply. Compensation at GC's discretion.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_4", "title": "Liability", "clause_type": "indemnification",
             "text": "Subcontractor assumes full liability including for delays caused by others.",
             "is_ambiguous": False, "flagged_for_analysis": True},
            {"clause_id": "clause_5", "title": "Insurance", "clause_type": "indemnification",
             "text": "Subcontractor carries $5M insurance at own expense. GC carries none.",
             "is_ambiguous": False, "flagged_for_analysis": True},
        ],
        "risky_clauses": {
            "clause_2": "Party B",
            "clause_3": "Party B",
            "clause_4": "Party B",
            "clause_5": "Party B",
        },
        "party_a": "BuildRight Construction LLC (General Contractor)",
        "party_b": "IronWorks Ltd. (Subcontractor)",
        "task_description": (
            "MEDIUM TASK: Analyze this Subcontractor Agreement. Clause 4 (Liability) has been flagged. "
            "Which party is disadvantaged by this liability clause: "
            "'Party A' (BuildRight Construction) or 'Party B' (IronWorks Ltd.)? "
            "Provide your legal reasoning."
        ),
        "target_clause_id": "clause_4",
        "target_answer": "Party B",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3: REWRITE AMBIGUOUS CLAUSE — Hard
# Clauses that are vague, contradictory, or legally unsound.
# ─────────────────────────────────────────────────────────────────────────────

REWRITE_CONTRACTS: List[Dict[str, Any]] = [
    {
        "contract_id": "RW-001",
        "contract_title": "Partnership Agreement",
        "contract_text": """PARTNERSHIP AGREEMENT

This agreement is between Alpha Ventures ("Partner A") and Beta Holdings ("Partner B").

1. PROFIT SHARING
Profits will be split fairly between the partners based on contribution.
Each partner's contribution will be assessed periodically.

2. DECISION MAKING
Important decisions will require agreement. Routine decisions can be made by either partner.

3. TERMINATION
Either partner can leave when they want. The remaining partner will handle outstanding matters
in a reasonable timeframe.

4. INTELLECTUAL PROPERTY
Any inventions or ideas developed during the partnership may belong to the partnership
or to the individual partner, depending on circumstances.""".strip(),
        "ambiguous_clauses": [
            {
                "clause_id": "clause_1",
                "title": "Profit Sharing",
                "text": "Profits will be split fairly between the partners based on contribution. Each partner's contribution will be assessed periodically.",
                "issues": ["'fairly' is undefined", "'periodically' is undefined", "no formula specified", "no dispute mechanism"],
                "flagged_for_analysis": True,
                "is_ambiguous": True,
                "clause_type": "payment_terms",
            },
        ],
        "target_clause_id": "clause_1",
        "task_description": (
            "HARD TASK: Clause 1 (Profit Sharing) of this Partnership Agreement is dangerously ambiguous. "
            "The terms 'fairly' and 'periodically' are undefined, and there is no formula or dispute mechanism. "
            "Rewrite this clause to be legally precise and enforceable, including: "
            "specific split percentages or formula, assessment schedule, and dispute resolution mechanism."
        ),
        "evaluation_keywords": [
            "percent", "%", "60", "50", "40",
            "quarterly", "annually", "monthly", "review",
            "dispute", "arbitration", "mediation", "accountant",
            "contribution", "capital", "hours", "revenue",
        ],
        "min_word_count": 50,
    },
    {
        "contract_id": "RW-002",
        "contract_title": "Employment Contract — Non-Disclosure",
        "contract_text": """EMPLOYMENT CONTRACT

Between NovaTech Inc. ("Employer") and the Employee.

1. COMPENSATION
Employee will receive competitive market compensation reviewed regularly.

2. TERMINATION
Either party may end this agreement with reasonable notice.

3. NON-DISCLOSURE
Employee shall not disclose sensitive information to competitors or the general public
for an appropriate period after employment ends.

4. REMOTE WORK
Employee may work remotely sometimes, subject to business needs and manager approval.""".strip(),
        "ambiguous_clauses": [
            {
                "clause_id": "clause_3",
                "title": "Non-Disclosure",
                "text": "Employee shall not disclose sensitive information to competitors or the general public for an appropriate period after employment ends.",
                "issues": ["'sensitive information' undefined", "'appropriate period' undefined", "no carve-outs for public knowledge", "no geographic scope"],
                "flagged_for_analysis": True,
                "is_ambiguous": True,
                "clause_type": "confidentiality",
            },
        ],
        "target_clause_id": "clause_3",
        "task_description": (
            "HARD TASK: Clause 3 (Non-Disclosure) of this Employment Contract is legally unenforceable. "
            "'Sensitive information' and 'appropriate period' are completely undefined. "
            "Rewrite this clause to be legally enforceable, specifying: "
            "exact definition of confidential information, specific duration (years), "
            "carve-outs for public domain info, and permitted disclosures (e.g., court orders)."
        ),
        "evaluation_keywords": [
            "year", "month", "2 year", "1 year", "24 month",
            "confidential information", "trade secret", "proprietary",
            "publicly available", "public domain", "prior to",
            "written", "disclosed", "shall not",
        ],
        "min_word_count": 60,
    },
    {
        "contract_id": "RW-003",
        "contract_title": "Consulting Services Agreement",
        "contract_text": """CONSULTING SERVICES AGREEMENT

Between Apex Consulting Group ("Consultant") and MegaCorp Inc. ("Client").

1. SERVICES
Consultant will provide strategic advisory services on an as-needed basis.

2. COMPENSATION
Client will pay Consultant a reasonable fee for services rendered. Payment will be made
in a timely manner after receipt of Consultant's invoice.

3. INTELLECTUAL PROPERTY
Work product created by Consultant during the engagement may be used by Client.
Ownership of such work product will depend on the nature of the work.

4. TERMINATION
Either party may end this agreement when appropriate.""".strip(),
        "ambiguous_clauses": [
            {
                "clause_id": "clause_2",
                "title": "Compensation",
                "text": "Client will pay Consultant a reasonable fee for services rendered. Payment will be made in a timely manner after receipt of Consultant's invoice.",
                "issues": ["'reasonable fee' undefined", "'timely manner' undefined", "no late payment penalty", "no invoice dispute process"],
                "flagged_for_analysis": True,
                "is_ambiguous": True,
                "clause_type": "payment_terms",
            },
        ],
        "target_clause_id": "clause_2",
        "task_description": (
            "HARD TASK: Clause 2 (Compensation) of this Consulting Agreement is dangerously vague. "
            "'Reasonable fee' and 'timely manner' create no enforceable obligation. "
            "Rewrite this clause to be legally precise, including: "
            "specific hourly/project rate or calculation formula, exact payment deadline (days), "
            "late payment interest rate, and invoice dispute process."
        ),
        "evaluation_keywords": [
            "per hour", "per day", "hourly", "rate", "$",
            "days", "30 days", "net 30", "net 15",
            "interest", "late payment", "penalty",
            "invoice", "dispute", "written notice", "shall",
        ],
        "min_word_count": 55,
    },
]
