#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A simple script to process user memos and task histories,
extract key themes/skills/economic goals, and produce a
JSON-formatted matching score matrix.

Dependencies:
- Python 3.x (no external libraries required, but can expand with nltk/spacy if desired)

Usage:
python matchmaking.py
"""

import json
import re

# ------------------------------
# SAMPLE DATA
# ------------------------------
USER_MEMOS = {
    "userA": "Focusing on AI trading strategies and cross-chain arbitrage. Interested in collaborating on NFT-lending initiatives.",
    "userB": "Looking for marketing experts and data analysts for future metaverse expansions. Keen on stablecoin yield farming.",
    "userC": "Passionate about DeFi governance and on-chain treasury management. Also open to cross-network collaborations."
}

TASK_HISTORIES = {
    "userA": [
        "Completed a short analysis on high-frequency XRPL trading",
        "Participated in NFT aggregator experiment"
    ],
    "userB": [
        "Developed marketing strategy for new token listing",
        "Researched stablecoin yield optimization"
    ],
    "userC": [
        "Launched governance proposal for a treasury pilot project",
        "Coordinated a cross-chain partnership with side networks"
    ]
}

# Example dictionary to store user 'skills' or 'goals' extracted from memos:
# This is the simplest approach - we’ll just store extracted keywords per user.
user_profiles = {}

# ------------------------------
# SIMPLE NLP UTILS
# ------------------------------
def simple_tokenize(text):
    """
    Basic text normalization:
      - Lowercase
      - Remove non-alphanumeric chars
      - Split on whitespace
    Returns a set of tokens for easier matching.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    return set(tokens)

def build_user_profiles():
    """
    Extract key tokens from user memos and tasks,
    storing them in a dictionary: user_profiles[user] = { 'tokens': set([...]) }
    """
    for user, memo in USER_MEMOS.items():
        # Start with memo tokens
        memo_tokens = simple_tokenize(memo)

        # Also gather tokens from task history
        task_tokens = set()
        if user in TASK_HISTORIES:
            for task_desc in TASK_HISTORIES[user]:
                task_tokens.update(simple_tokenize(task_desc))

        # Combine sets for a user profile
        combined_tokens = memo_tokens.union(task_tokens)

        user_profiles[user] = {
            "tokens": combined_tokens
        }

def compute_match_scores():
    """
    Create a matrix of user-to-user matching scores based on token overlap.
    Also suitable for user-to-task matching if tasks were kept separate.
    
    Score method: Jaccard similarity = (overlap) / (union)
    Output: A dict that maps { (userX, userY): score }
    """
    users = list(user_profiles.keys())
    results = {}

    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            user_i = users[i]
            user_j = users[j]

            set_i = user_profiles[user_i]["tokens"]
            set_j = user_profiles[user_j]["tokens"]

            overlap = set_i.intersection(set_j)
            union = set_i.union(set_j)
            if len(union) > 0:
                score = len(overlap) / len(union)
            else:
                score = 0.0

            # Store bidirectional or symmetrical
            pair_key_1 = f"{user_i} -> {user_j}"
            pair_key_2 = f"{user_j} -> {user_i}"

            results[pair_key_1] = round(score, 3)
            results[pair_key_2] = round(score, 3)

    return results


# ------------------------------
# MAIN SCRIPT
# ------------------------------
def main():
    print("Building user profiles...")
    build_user_profiles()

    print("Computing matching scores...")
    match_scores = compute_match_scores()

    print("Generated matching score matrix (JSON):")
    print(json.dumps(match_scores, indent=2))


if __name__ == "__main__":
    main()