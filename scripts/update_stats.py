# scripts/update_stats.py
import urllib.request
import json
import re
import os
import math

def fetch_github_stats(username):
    # Fetch public user info
    user_url = f"https://api.github.com/users/{username}"
    req = urllib.request.Request(user_url, headers={"User-Agent": "Stats-Updater"})
    try:
        with urllib.request.urlopen(req) as res:
            user_data = json.loads(res.read().decode())
    except Exception as e:
        print("Error fetching GitHub user details:", e)
        user_data = {}

    # Fetch total contributions using GraphQL
    token = os.getenv("GITHUB_TOKEN")
    contributions = 0
    total_stars = 0
    prs = 0
    issues = 0

    if token:
        # Use GraphQL API
        graphql_url = "https://api.github.com/graphql"
        query = {
            "query": f"""
            query {{
              user(login: "{username}") {{
                contributionsCollection {{
                  contributionCalendar {{
                    totalContributions
                  }}
                }}
                repositories(first: 100, ownerAffiliations: OWNER) {{
                  nodes {{
                    stargazers {{
                      totalCount
                    }}
                  }}
                }}
              }}
            }}
            """
        }
        req = urllib.request.Request(
            graphql_url,
            data=json.dumps(query).encode(),
            headers={
                "Authorization": f"bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "Stats-Updater"
            }
        )
        try:
            with urllib.request.urlopen(req) as res:
                gql_res = json.loads(res.read().decode())
                user_node = gql_res.get("data", {}).get("user", {})
                if user_node:
                    contributions = user_node.get("contributionsCollection", {}).get("contributionCalendar", {}).get("totalContributions", 0)
                    repos = user_node.get("repositories", {}).get("nodes", [])
                    total_stars = sum(repo.get("stargazers", {}).get("totalCount", 0) for repo in repos)
        except Exception as e:
            print("Error calling GitHub GraphQL API:", e)

        # Fetch PRs count via Search API
        pr_url = f"https://api.github.com/search/issues?q=author:{username}+type:pr"
        req = urllib.request.Request(pr_url, headers={"Authorization": f"token {token}", "User-Agent": "Stats-Updater"})
        try:
            with urllib.request.urlopen(req) as res:
                prs = json.loads(res.read().decode()).get("total_count", 0)
        except Exception as e:
            print("Error fetching PR count:", e)

        # Fetch Issues count via Search API
        issue_url = f"https://api.github.com/search/issues?q=author:{username}+type:issue"
        req = urllib.request.Request(issue_url, headers={"Authorization": f"token {token}", "User-Agent": "Stats-Updater"})
        try:
            with urllib.request.urlopen(req) as res:
                issues = json.loads(res.read().decode()).get("total_count", 0)
        except Exception as e:
            print("Error fetching Issue count:", e)
    else:
        # Fallback values for local testing or when token is missing
        print("GITHUB_TOKEN not found, using fallback REST API or simulated stats")
        contributions = 200 # simulated for C-Rank level 34
        total_stars = 2     # simulated
        prs = 5             # simulated
        issues = 3          # simulated

    # Compile all stats
    stats = {
        "repos": user_data.get("public_repos", 20),
        "followers": user_data.get("followers", 6),
        "contributions": contributions,
        "stars": total_stars,
        "prs": prs,
        "issues": issues,
        "total_commits": max(0, contributions - prs - issues)
    }
    return stats

def fetch_leetcode_stats(username):
    url = "https://leetcode.com/graphql"
    query = {
        "query": """
        query userProblemsSolved($username: String!) {
          allQuestionsCount {
            difficulty
            count
          }
          matchedUser(username: $username) {
            submitStatsGlobal {
              acSubmissionNum {
                difficulty
                count
              }
            }
            profile {
              ranking
            }
          }
        }
        """,
        "variables": {"username": username}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(query).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode())
            user_data = data.get("data", {})
            
            all_questions = user_data.get("allQuestionsCount", [])
            matched_user = user_data.get("matchedUser", {})
            submit_stats = matched_user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
            profile = matched_user.get("profile", {})
            
            ranking = profile.get("ranking", 1965340)
            
            total_counts = {item["difficulty"]: item["count"] for item in all_questions}
            solved_counts = {item["difficulty"]: item["count"] for item in submit_stats}
            
            return {
                "solved_total": solved_counts.get("All", 76),
                "total_questions": total_counts.get("All", 3299),
                "solved_easy": solved_counts.get("Easy", 36),
                "total_easy": total_counts.get("Easy", 830),
                "solved_medium": solved_counts.get("Medium", 37),
                "total_medium": total_counts.get("Medium", 1723),
                "solved_hard": solved_counts.get("Hard", 3),
                "total_hard": total_counts.get("Hard", 744),
                "ranking": ranking
            }
    except Exception as e:
        print("Error fetching LeetCode stats:", e)
        # Fallbacks
        return {
            "solved_total": 76,
            "total_questions": 3299,
            "solved_easy": 36,
            "total_easy": 830,
            "solved_medium": 37,
            "total_medium": 1723,
            "solved_hard": 3,
            "total_hard": 744,
            "ranking": 1965340
        }

def calculate_rpg_level(contributions):
    if contributions <= 0:
        return 1, 0, 1000, 0.0
    
    # Square root progression model: hits exactly Level 34 at 200 contributions!
    level = min(99, int(math.sqrt(contributions) * 2.4) + 1)
    
    c_curr = ((level - 1) / 2.4) ** 2
    c_next = (level / 2.4) ** 2
    
    total_in_level = c_next - c_curr
    progress_in_level = contributions - c_curr
    
    frac = progress_in_level / total_in_level if total_in_level > 0 else 0.0
    frac = max(0.0, min(1.0, frac))
    
    max_xp = level * 1000
    current_xp = int(frac * max_xp)
    xp_percent = frac * 100
    
    return level, current_xp, max_xp, xp_percent

def get_rank(level):
    if level < 10:
        return "E-RANK (NOVICE)"
    elif level < 20:
        return "D-RANK (SCOUT)"
    elif level < 35:
        return "C-RANK (MID-TIER)"
    elif level < 50:
        return "B-RANK (ELITE)"
    elif level < 80:
        return "A-RANK (RAIDER)"
    else:
        return "S-RANK (MONARCH)"

def generate_tiers_tspan(rank):
    tiers = ['E', 'D', 'C', 'B', 'A', 'S']
    output_parts = []
    for t in tiers:
        if t == rank[0]: # Highlight matching rank letter
            output_parts.append(f'<tspan fill="#00f2fe" font-weight="800">[{t}]</tspan>')
        else:
            output_parts.append(t)
    return " ➔ ".join(output_parts) + " (MAX)"

def update_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stats_path = os.path.join(base_dir, "..", "assets", "stats.svg")
    leetcode_path = os.path.join(base_dir, "..", "assets", "leetcode.svg")

    print("Fetching GitHub metrics...")
    github_stats = fetch_github_stats("anshulsharma200817-svg")
    print("GitHub stats:", github_stats)

    print("Fetching LeetCode metrics...")
    leetcode_stats = fetch_leetcode_stats("anshulsharma200817-svg")
    print("LeetCode stats:", leetcode_stats)

    # 1. Update stats.svg
    if os.path.exists(stats_path):
        with open(stats_path, "r", encoding="utf-8") as f:
            stats_content = f.read()

        level, curr_xp, max_xp, xp_percent = calculate_rpg_level(github_stats["contributions"])
        rank = get_rank(level)
        tiers_html = generate_tiers_tspan(rank)

        # Replace info
        stats_content = re.sub(r'(<text id="val-level"[^>]*>).*?(</text>)', rf'\g<1>{level}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-rank"[^>]*>).*?(</text>)', rf'\g<1>{rank}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-tiers"[^>]*>).*?(</text>)', rf'\g<1>{tiers_html}\2', stats_content)

        # Replace attributes
        int_val = github_stats["prs"] + github_stats["issues"]
        str_val = github_stats["total_commits"]
        sen_val = github_stats["stars"]
        agi_val = github_stats["repos"]
        vit_val = github_stats["followers"]

        stats_content = re.sub(r'(<text id="val-int"[^>]*>).*?(</text>)', rf'\g<1>{int_val}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-str"[^>]*>).*?(</text>)', rf'\g<1>{str_val}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-sen"[^>]*>).*?(</text>)', rf'\g<1>{sen_val}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-agi"[^>]*>).*?(</text>)', rf'\g<1>{agi_val}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-vit"[^>]*>).*?(</text>)', rf'\g<1>{vit_val}\2', stats_content)

        xp_str = f"XP: {curr_xp:,} / {max_xp:,} ({xp_percent:.2f}%)"
        stats_content = re.sub(r'(<text id="val-xp-text"[^>]*>).*?(</text>)', rf'\g<1>{xp_str}\2', stats_content)

        # Bar widths (scale out of 180px max)
        int_w = min(180, int((int_val / 50) * 180))
        str_w = min(180, int((str_val / 500) * 180))
        sen_w = min(180, int((sen_val / 30) * 180))
        agi_w = min(180, int((agi_val / 40) * 180))
        vit_w = min(180, int((vit_val / 30) * 180))
        xp_w = min(420, int((xp_percent / 100) * 420))

        # Replace style keyframes
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!int_width\s*\*/)', rf'\g<1>{int_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!str_width\s*\*/)', rf'\g<1>{str_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!sen_width\s*\*/)', rf'\g<1>{sen_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!agi_width\s*\*/)', rf'\g<1>{agi_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!vit_width\s*\*/)', rf'\g<1>{vit_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!xp_width\s*\*/)', rf'\g<1>{xp_w}px\2', stats_content)

        with open(stats_path, "w", encoding="utf-8") as f:
            f.write(stats_content)
        print("Updated stats.svg successfully.")
    else:
        print("stats.svg not found at path:", stats_path)

    # 2. Update leetcode.svg
    if os.path.exists(leetcode_path):
        with open(leetcode_path, "r", encoding="utf-8") as f:
            lc_content = f.read()

        solved = leetcode_stats["solved_total"]
        total = leetcode_stats["total_questions"]
        ranking = leetcode_stats["ranking"]

        easy_s = leetcode_stats["solved_easy"]
        easy_t = leetcode_stats["total_easy"]
        medium_s = leetcode_stats["solved_medium"]
        medium_t = leetcode_stats["total_medium"]
        hard_s = leetcode_stats["solved_hard"]
        hard_t = leetcode_stats["total_hard"]

        lc_rank_str = f"#{ranking:,}"

        # Solver rank logic
        if ranking < 50000:
            lc_solver = "S-RANK COMPETITOR"
        elif ranking < 250000:
            lc_solver = "A-RANK COMPETITOR"
        elif ranking < 1000000:
            lc_solver = "B-RANK COMPETITOR"
        elif ranking < 2500000:
            lc_solver = "C-RANK COMPETITOR"
        elif ranking < 5000000:
            lc_solver = "D-RANK COMPETITOR"
        else:
            lc_solver = "E-RANK COMPETITOR"

        lc_content = re.sub(r'(<text id="lc-rank"[^>]*>).*?(</text>)', rf'\g<1>{lc_rank_str}\2', lc_content)
        lc_content = re.sub(r'(<text id="lc-solver"[^>]*>).*?(</text>)', rf'\g<1>{lc_solver}\2', lc_content)
        lc_content = re.sub(r'(<tspan id="lc-solved"[^>]*>).*?(</tspan>)', rf'\g<1>{solved}\2', lc_content)
        lc_content = re.sub(r'(<tspan id="lc-total"[^>]*>).*?(</tspan>)', rf'\g<1>/{total}\2', lc_content)

        easy_str = f"{easy_s} <tspan fill=\"#475569\" font-size=\"10\">/ {easy_t}</tspan>"
        medium_str = f"{medium_s} <tspan fill=\"#475569\" font-size=\"10\">/ {medium_t}</tspan>"
        hard_str = f"{hard_s} <tspan fill=\"#475569\" font-size=\"10\">/ {hard_t}</tspan>"

        lc_content = re.sub(r'(<text id="lc-easy-count"[^>]*>).*?(</text>)', rf'\g<1>{easy_str}\2', lc_content)
        lc_content = re.sub(r'(<text id="lc-medium-count"[^>]*>).*?(</text>)', rf'\g<1>{medium_str}\2', lc_content)
        lc_content = re.sub(r'(<text id="lc-hard-count"[^>]*>).*?(</text>)', rf'\g<1>{hard_str}\2', lc_content)

        # Scale rings (target solved = 300)
        goal = 300
        easy_dash = min(179.0, (easy_s / goal) * 179.0)
        medium_dash = min(179.0 - easy_dash, (medium_s / goal) * 179.0)
        hard_dash = min(179.0 - easy_dash - medium_dash, (hard_s / goal) * 179.0)

        # Style dash arrays
        lc_content = re.sub(r'(to\s*\{\s*stroke-dasharray:\s*)\d+(?:\.\d+)?(\s+200;\s*\}\s*/\*\s*!lc_easy_dash\s*\*/)', rf'\g<1>{easy_dash:.2f}\2', lc_content)
        lc_content = re.sub(r'(to\s*\{\s*stroke-dasharray:\s*)\d+(?:\.\d+)?(\s+200;\s*\}\s*/\*\s*!lc_medium_dash\s*\*/)', rf'\g<1>{medium_dash:.2f}\2', lc_content)
        lc_content = re.sub(r'(to\s*\{\s*stroke-dasharray:\s*)\d+(?:\.\d+)?(\s+200;\s*\}\s*/\*\s*!lc_hard_dash\s*\*/)', rf'\g<1>{hard_dash:.2f}\2', lc_content)

        # Path stroke offsets
        medium_offset = -int(easy_dash)
        hard_offset = -int(easy_dash + medium_dash)

        lc_content = re.sub(r'(<path id="lc-medium-arc"[^>]*stroke-dashoffset=").*?(")', rf'\g<1>{medium_offset}\2', lc_content)
        lc_content = re.sub(r'(<path id="lc-hard-arc"[^>]*stroke-dashoffset=").*?(")', rf'\g<1>{hard_offset}\2', lc_content)

        with open(leetcode_path, "w", encoding="utf-8") as f:
            f.write(lc_content)
        print("Updated leetcode.svg successfully.")
    else:
        print("leetcode.svg not found at path:", leetcode_path)

if __name__ == "__main__":
    update_files()
