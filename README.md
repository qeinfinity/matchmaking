# AI-Powered Collaboration Matching Prototype

This project provides a **simple reference implementation** for identifying collaboration opportunities among Post Fiat network participants. It processes **user memos** and **task histories**, extracting skills and economic goals using a minimal NLP approach, then outputs a **JSON-formatted matching score matrix**.

## Table of Contents
- [Introduction](#introduction)
- [Algorithm Overview](#algorithm-overview)
- [Scaling & Future Enhancements](#scaling--future-enhancements)
- [Usage](#usage)

---

## Introduction

In Post Fiat's ecosystem, participants often share memos reflecting their skills, economic goals, and prior successes. This prototype merges those memos with **task history** to discover potential synergy between users. The script:

1. **Tokenizes** user text (lowercasing, alphanumeric filtering).
2. **Builds user profiles** based on combined tokens (memo + tasks).
3. **Computes Jaccard similarity** for user-to-user matching.
4. **Outputs** a JSON object where each key is a user-pair, and the value is a numeric match score (0.0 to 1.0).

This approach can also be extended to **user-to-task** or **user-to-node** matching.

---

## Algorithm Overview

1. **Token Extraction**  
   Each user memo and task description is normalized:  
   - Lowercased to ensure consistency.  
   - Non-alphanumeric characters removed.  
   - Split into simple tokens.  
   This yields a **set** of keywords representing each user's focus or experience.

2. **Profile Construction**  
   A user's combined profile is the union of tokens from their memos and task histories. For example, if userA has `"ai"`, `"trading"`, and `"nft"` in their memo, plus `"analysis"`, `"xrpl"` in tasks, their profile becomes:  
   ```json
   {
     "tokens": {"ai", "trading", "nft", "analysis", "xrpl"}
   }
   ```

3. **Similarity Calculation (Jaccard)**  
   - A score close to 1.0 indicates very similar skill sets/interests.
   - A score near 0.0 means little common ground.

4. **JSON Output**  
   Each user pair is stored in a dictionary with a matching score (rounded to 3 decimals for readability). Example:
   ```json
   {
     "userA -> userB": 0.333,
     "userB -> userA": 0.333,
     "userA -> userC": 0.125,
     "userC -> userA": 0.125,
   }
   ```
