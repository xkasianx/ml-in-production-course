# Design Doc

## https://eugeneyan.com/writing/ml-design-docs/
### Motivation
- risk of building the wrong thing and redoing it from scratch

### Whys and Whats
- **Why** should we solve this problem? **Why now**? 
- What are the **success criteria**? (increased customer engagement, revenue, or reduced cost)
- What are the **requirements and constraints**?(throughput, latency, security, data privacy, costs, etc.)
- What is **in-scope vs out-of-scope**?
- What are our **assumptions**? (how many products and users do you have? What is the expected number of requests per second? This guides how you frame the problem.)

### How
- **Problem statement** (If it’s a recommender system, are you taking a content or collaboration-based approach? Will it be an item-to-item or user-to-item recommender?)
- **Data**
- **Techniques** (Outline the machine learning techniques you’ll try/tried)
- **Validation and experimentation** (Explain how you’ll evaluate models)

### Implementation
- **Diagram** (System-context diagrams and data-flow diagrams)
- **Infra + scalability** (Briefly list the infra options and your final choice)
- **Performance (throughput + latency)** (throughput (i.e., requests per second) and latency (e.g., x ms @ p99))
- **Security**
- **Data privacy**
- **Monitoring + alarms**
- **Cost**
- **Integration points** (Define how downstream services will use and interact with your endpoint)
- **Risks and uncertainties** (Risks are the known unknowns; uncertainties are the unknown unknowns)

### (Optional) Alternatives considered and rejected