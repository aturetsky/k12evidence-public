# Human-AI K-12 Evidence Project - Website Architecture & Content Outline

## Site Architecture

The website will be a clean, academic, and accessible static site deployed on Cloudflare Pages (k12evidence.org).

### Navigation Menu
- Home
- Clusters (Dropdown or Overview page linking to 10 cluster pages)
- Replications
- Bibliography
- About

---

## Page Content Outlines

### 1. Home Page
- **Hero Section**: 
  - Title: Human-AI K-12 Evidence Project
  - Mission Statement: A systematic, AI-assisted evidence synthesis of K-12 education research.
- **Methodology Note**: Brief explanation of the systematic AI-assisted evidence synthesis process.
- **High-Level Summary**: 
  - Overview of the 10 clusters of research.
  - Key takeaways: Areas of strong consensus (e.g., high-dosage tutoring, systematic phonics), areas of methodological debate (VAMs, early childhood fadeout), and the persistence of selection bias.

### 2. Clusters Section
*This section will have an overview page and individual pages/sections for each of the 10 clusters. Content extracted from the Markdown literature review.*

- **Cluster 1: Teacher Quality and Value-Added Models**
  - Core finding: Teacher quality is the most important school-based determinant of student achievement.
  - Debate: Validity of Value-Added Models (VAMs) and non-random sorting.
  - Expanded view: Non-cognitive teacher effects (attendance, behavior).
- **Cluster 2: Early Childhood Education**
  - Core finding: High return on investment from intensive early programs (Perry, Abecedarian).
  - Debate: The fadeout problem in modern, scaled-up public pre-K programs.
- **Cluster 3: Class Size Reduction**
  - Core finding: Positive effects in early grades (STAR experiment), but expensive.
  - Debate: General equilibrium effects (e.g., California's scale-up diluting teacher quality).
- **Cluster 4: School Funding and Resources**
  - Core finding: Targeted funding increases improve long-run outcomes, especially for low-income students.
  - Debate: How money is spent matters more than just increasing block grants.
- **Cluster 5: Charter Schools and Vouchers**
  - Core finding: Urban "No Excuses" charters show robust positive effects.
  - Debate: Non-urban/virtual charters and large-scale voucher programs often show null or negative effects.
- **Cluster 6: Reading Instruction**
  - Core finding: Unambiguous scientific consensus on systematic phonics instruction.
  - Debate: Sustaining gains (e.g., Reading Recovery fadeout) requires strong Tier 1 instruction.
- **Cluster 7: High-Dosage Tutoring**
  - Core finding: Highly effective and replicable (effect sizes ~0.37), especially during the school day.
  - Debate: Cost-effectiveness and scaling challenges.
- **Cluster 8: Social-Emotional Learning and Non-Cognitive Skills**
  - Core finding: Universal SEL programs improve achievement and behavior.
  - Debate: Targeted psychological interventions (grit, growth mindset) show weak or context-dependent effects at scale.
- **Cluster 9: Out-of-School Factors**
  - Core finding: Family background and neighborhood poverty are primary drivers of inequality.
  - Debate: The summer learning gap and the limits of school-based interventions.
- **Cluster 10: International Systems**
  - Core finding: High-performing systems share selective teacher prep, equitable funding, and centralized curricula.
  - Debate: Translating these features to the decentralized US context.

### 3. Replications Section
- **Overview**: Explanation of the replication agenda.
- **Featured Replication: Jackson, Johnson & Persico (2016)**
  - Summary of the original paper (school finance reforms).
  - Explanation of the replication constraints (state-level approximation due to restricted geocode data).
  - Findings: First-stage confirmation of spending increases, but inconclusive reduced-form and IV results due to instrument weakness at the state level.
  - Out-of-sample extension: Inconclusive SEDA test score analysis.
  - Links: Download the Replication Note PDF, link to Zenodo/GitHub repository.

### 4. Bibliography Section
- **Overview**: List of all 124 reviewed papers (based on the `k12_references.bib` and `access_classification.md` registry).
- **Organization**: Grouped by cluster or alphabetically, clearly indicating the 61 directly cited papers.
- **PDF Hosting Policy**: 
  - Direct PDF links for Open Access and Government Reports.
  - Links to legal preprints (NBER, SSRN, author sites) where available.
  - DOI links only for paywalled papers.
  - Direct download links for our own compiled literature review PDF and replication note PDF.

### 5. About Page
- **Methodology**: Detailed description of the systematic AI-assisted evidence synthesis.
- **Human-AI Collaboration Model**: 
  - Human Author: Avi Turetsky
  - AI Assistants: Manus (execution), Claude (audit/verification), Perplexity (fact-checking).
- **Contact/Links**: GitHub repository link, author LinkedIn.
