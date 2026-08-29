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
    days = []

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
                    weeks {{
                      contributionDays {{
                        contributionCount
                        date
                      }}
                    }}
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
                    calendar = user_node.get("contributionsCollection", {}).get("contributionCalendar", {})
                    contributions = calendar.get("totalContributions", 0)
                    
                    # Flatten days
                    weeks = calendar.get("weeks", [])
                    for week in weeks:
                        days.extend(week.get("contributionDays", []))

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
        contributions = 346 
        total_stars = 2     
        prs = 56             
        issues = 2          
        
        # Simulated days for testing
        import datetime
        today = datetime.date.today()
        days = []
        for i in range(365):
            date_str = (today - datetime.timedelta(days=365 - i)).strftime("%Y-%m-%d")
            count = 0
            if i % 3 == 0:
                count = (i % 7) + 1
            if i > 360 and i % 4 != 0: # Create active streak near the end
                count = 4
            days.append({"contributionCount": count, "date": date_str})

    # Compile all stats
    stats = {
        "repos": user_data.get("public_repos", 20),
        "followers": user_data.get("followers", 6),
        "contributions": contributions,
        "stars": total_stars,
        "prs": prs,
        "issues": issues,
        "total_commits": max(0, contributions - prs - issues),
        "days": days
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
            
            ranking = profile.get("ranking", 1852009)
            
            total_counts = {item["difficulty"]: item["count"] for item in all_questions}
            solved_counts = {item["difficulty"]: item["count"] for item in submit_stats}
            
            return {
                "solved_total": solved_counts.get("All", 86),
                "total_questions": total_counts.get("All", 4033),
                "solved_easy": solved_counts.get("Easy", 42),
                "total_easy": total_counts.get("Easy", 961),
                "solved_medium": solved_counts.get("Medium", 41),
                "total_medium": total_counts.get("Medium", 2105),
                "solved_hard": solved_counts.get("Hard", 3),
                "total_hard": total_counts.get("Hard", 967),
                "ranking": ranking
            }
    except Exception as e:
        print("Error fetching LeetCode stats:", e)
        # Fallbacks
        return {
            "solved_total": 86,
            "total_questions": 4033,
            "solved_easy": 42,
            "total_easy": 961,
            "solved_medium": 41,
            "total_medium": 2105,
            "solved_hard": 3,
            "total_hard": 967,
            "ranking": 1852009
        }

def calculate_streaks(days):
    longest = 0
    current = 0
    
    # Calculate longest streak
    temp_streak = 0
    for d in days:
        if d.get("contributionCount", 0) > 0:
            temp_streak += 1
            if temp_streak > longest:
                longest = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak (scan backwards from today/yesterday)
    if not days:
        return 0, 0
        
    n = len(days)
    start_idx = -1
    
    # Check if today has contributions
    if days[-1].get("contributionCount", 0) > 0:
        start_idx = n - 1
    # Or check if yesterday did (active streak)
    elif n > 1 and days[-2].get("contributionCount", 0) > 0:
        start_idx = n - 2
        
    if start_idx != -1:
        for i in range(start_idx, -1, -1):
            if days[i].get("contributionCount", 0) > 0:
                current += 1
            else:
                break
    else:
        current = 0
        
    return current, longest

def calculate_rpg_level(contributions):
    if contributions <= 0:
        return 1, 0, 1000, 0.0
    
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
        return "JUN-II (NOVICE)"
    elif level < 20:
        return "JUN-I (DEVELOPER)"
    elif level < 35:
        return "MID-II (PROGRAMMER)"
    elif level < 50:
        return "MID-I (ENGINEER)"
    elif level < 80:
        return "SEN (ARCHITECT)"
    else:
        return "PRIN (MONARCH)"

def generate_tiers_tspan(rank):
    tiers = ['JUN-II', 'JUN-I', 'MID-II', 'MID-I', 'SEN', 'PRIN']
    output_parts = []
    for t in tiers:
        if t in rank:
            output_parts.append(f'<tspan fill="#00f2fe" font-weight="800">[{t}]</tspan>')
        else:
            output_parts.append(t)
    return " ➔ ".join(output_parts)

def generate_github_dashboard_svg(stats, current_streak, longest_streak, days):
    # Slice last 30 days
    last_30 = days[-30:] if len(days) >= 30 else days
    while len(last_30) < 30:
        last_30.insert(0, {"contributionCount": 0, "date": ""})
        
    squares_svg = ""
    for i, d in enumerate(last_30):
        count = d.get("contributionCount", 0)
        if count == 0:
            color = "#05070f"
            stroke = "#1e293b"
        elif count <= 2:
            color = "#0d5c75"
            stroke = "#00f2fe"
        elif count <= 5:
            color = "#008f9f"
            stroke = "#00f2fe"
        elif count <= 9:
            color = "#00f2fe"
            stroke = "#00f2fe"
        else:
            color = "#bd00ff"
            stroke = "#d946ef"
            
        x_pos = 340 + i * 13.5
        y_pos = 103
        squares_svg += f'      <rect x="{x_pos}" y="{y_pos}" width="9" height="9" rx="0" fill="{color}" stroke="{stroke}" stroke-width="0.5" />\n'

    circumference = 56.5
    dash = min(circumference, (current_streak / 10) * circumference)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 140" width="100%" height="100%">
  <defs>
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&amp;family=Fira+Code:wght@400;500&amp;display=swap');
      
      .status-card {{
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
      }}
      
      .mono-text {{
        font-family: 'Fira Code', monospace;
      }}

      .glow-neon-blue {{
        filter: drop-shadow(0 0 3px #00f2fe) drop-shadow(0 0 6px rgba(0, 242, 254, 0.2));
      }}
      
      @keyframes scan-line {{
        0% {{ transform: translateY(0); opacity: 0; }}
        5% {{ opacity: 0.8; }}
        95% {{ opacity: 0.8; }}
        100% {{ transform: translateY(130px); opacity: 0; }}
      }}

      .scanner-line {{
        animation: scan-line 6s linear infinite;
      }}
      
      @keyframes flame-pulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.8; }}
        50% {{ transform: scale(1.15); opacity: 1; }}
      }}
      
      .flame {{
        transform-origin: 618px 42px;
        animation: flame-pulse 2s ease-in-out infinite;
      }}
    </style>
    
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#0e1322" stroke-width="0.8" />
    </pattern>

    <linearGradient id="card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#04060c" />
      <stop offset="100%" stop-color="#080c16" />
    </linearGradient>

    <filter id="scan-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="850" height="140" rx="2" fill="url(#card-bg)" stroke="#1e293b" stroke-width="1.5" />
  <rect width="850" height="140" rx="0" fill="url(#grid)" />
  
  <rect x="6" y="6" width="838" height="128" fill="none" stroke="#1e293b" stroke-width="1" />
  <line x1="7" y1="7" x2="843" y2="7" stroke="#00f2fe" stroke-width="1.5" class="scanner-line" filter="url(#scan-glow)" />

  <g class="status-card">
    <!-- Left Panel: Core Stats -->
    <g transform="translate(20, 15)">
      <!-- Border Box -->
      <rect width="300" height="110" fill="#05070f" stroke="#1e293b" stroke-width="1" />
      <polygon points="2,2 8,2 2,8" fill="#00f2fe" />
      <polygon points="298,2 292,2 298,8" fill="#00f2fe" />
      <polygon points="2,108 8,108 2,102" fill="#00f2fe" />
      <polygon points="298,108 292,108 298,102" fill="#00f2fe" />
      
      <text x="15" y="20" font-size="11" font-weight="800" fill="#f1f5f9" letter-spacing="1.5">GITHUB LOGISTICS PROFILE</text>
      
      <!-- Stats Col 1 -->
      <text x="15" y="45" font-size="10" font-weight="600" fill="#475569">TOTAL COMMITS:</text>
      <text x="125" y="45" font-size="11" font-weight="700" fill="#3b82f6" class="mono-text">{stats['total_commits']}</text>

      <text x="15" y="65" font-size="10" font-weight="600" fill="#475569">PULL REQUESTS:</text>
      <text x="125" y="65" font-size="11" font-weight="700" fill="#00f2fe" class="mono-text">{stats['prs']}</text>

      <text x="15" y="85" font-size="10" font-weight="600" fill="#475569">TOTAL ISSUES:</text>
      <text x="125" y="85" font-size="11" font-weight="700" fill="#fb923c" class="mono-text">{stats['issues']}</text>

      <!-- Stats Col 2 -->
      <text x="160" y="45" font-size="10" font-weight="600" fill="#475569">TOTAL STARS:</text>
      <text x="250" y="45" font-size="11" font-weight="700" fill="#eab308" class="mono-text">{stats['stars']}</text>

      <text x="160" y="65" font-size="10" font-weight="600" fill="#475569">PUBLIC REPOS:</text>
      <text x="250" y="65" font-size="11" font-weight="700" fill="#a855f7" class="mono-text">{stats['repos']}</text>

      <text x="160" y="85" font-size="10" font-weight="600" fill="#475569">FOLLOWERS:</text>
      <text x="250" y="85" font-size="11" font-weight="700" fill="#10b981" class="mono-text">{stats['followers']}</text>
    </g>

    <!-- Right Section: Streak Metrics -->
    <!-- Card 1: Total Contributions -->
    <g transform="translate(340, 15)">
      <rect width="145" height="55" fill="#05070f" stroke="#1e293b" stroke-width="1" />
      <text x="15" y="20" font-size="8" font-weight="700" fill="#475569" letter-spacing="1">TOTAL CONTRIBUTIONS</text>
      <text x="15" y="42" font-size="20" font-weight="800" fill="#f1f5f9" class="mono-text">{stats['contributions']}</text>
    </g>

    <!-- Card 2: Current Streak -->
    <g transform="translate(500, 15)">
      <rect width="155" height="55" fill="#05070f" stroke="#1e293b" stroke-width="1" />
      <text x="15" y="20" font-size="8" font-weight="700" fill="#475569" letter-spacing="1">CURRENT STREAK</text>
      <text x="15" y="42" font-size="20" font-weight="800" fill="#00f2fe" class="mono-text">{current_streak}</text>
      
      <!-- Flame Gauge Circle -->
      <circle cx="125" cy="28" r="9" fill="none" stroke="#1c2538" stroke-width="2" />
      <circle cx="125" cy="28" r="9" fill="none" stroke="#00f2fe" stroke-width="2" stroke-linecap="butt" stroke-dasharray="{dash:.2f} 57" stroke-dashoffset="0" class="glow-neon-blue" />
      <!-- Tiny Flame SVG inside circle -->
      <path class="flame" d="M 125 22 C 122.5 25.5 122 28 123.5 31.5 C 125 33 126.5 32.5 127 30.5 C 127.5 28.5 126 26.5 125 22 Z" fill="#ff4500" />
    </g>

    <!-- Card 3: Longest Streak -->
    <g transform="translate(670, 15)">
      <rect width="160" height="55" fill="#05070f" stroke="#1e293b" stroke-width="1" />
      <text x="15" y="20" font-size="8" font-weight="700" fill="#475569" letter-spacing="1">LONGEST STREAK</text>
      <text x="15" y="42" font-size="20" font-weight="800" fill="#fb923c" class="mono-text">{longest_streak}</text>
      <text x="95" y="38" font-size="8" font-weight="700" fill="#10b981">DAYS PEAK</text>
    </g>

    <!-- Bottom Row: Recent Activity Sync -->
    <g transform="translate(0, 0)">
      <text x="340" y="93" font-size="9" font-weight="800" fill="#475569" letter-spacing="1.5">RECENT ACTIVITY SYNC (30 DAYS)</text>
      
      <!-- Grid Squares -->
{squares_svg}      
      <!-- Legend -->
      <text x="750" y="110" font-size="7" font-weight="600" fill="#475569">Less</text>
      <rect x="772" y="103" width="8" height="8" rx="0" fill="#05070f" stroke="#1e293b" stroke-width="0.5" />
      <rect x="782" y="103" width="8" height="8" rx="0" fill="#0d5c75" stroke="#00f2fe" stroke-width="0.5" />
      <rect x="792" y="103" width="8" height="8" rx="0" fill="#008f9f" stroke="#00f2fe" stroke-width="0.5" />
      <rect x="802" y="103" width="8" height="8" rx="0" fill="#00f2fe" stroke="#00f2fe" stroke-width="0.5" />
      <rect x="812" y="103" width="8" height="8" rx="0" fill="#bd00ff" stroke="#d946ef" stroke-width="0.5" />
      <text x="825" y="110" font-size="7" font-weight="600" fill="#475569">More</text>
    </g>
  </g>
</svg>"""
    return svg

def update_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    stats_path = os.path.join(base_dir, "..", "assets", "stats.svg")
    leetcode_path = os.path.join(base_dir, "..", "assets", "leetcode.svg")
    github_dashboard_path = os.path.join(base_dir, "..", "assets", "github_dashboard.svg")

    print("Fetching GitHub metrics...")
    github_stats = fetch_github_stats("anshulsharma200817-svg")
    print("GitHub stats:", {k: v for k, v in github_stats.items() if k != 'days'})

    print("Fetching LeetCode metrics...")
    leetcode_stats = fetch_leetcode_stats("anshulsharma200817-svg")
    print("LeetCode stats:", leetcode_stats)

    # Compute Streaks
    current_streak, longest_streak = calculate_streaks(github_stats["days"])
    print(f"Computed Streaks -> Current: {current_streak}, Longest: {longest_streak}")

    # 1. Update stats.svg
    if os.path.exists(stats_path):
        with open(stats_path, "r", encoding="utf-8") as f:
            stats_content = f.read()

        level, curr_xp, max_xp, xp_percent = calculate_rpg_level(github_stats["contributions"])
        rank = get_rank(level)
        tiers_html = generate_tiers_tspan(rank)

        stats_content = re.sub(r'(<text id="val-level"[^>]*>).*?(</text>)', rf'\g<1>{level}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-rank"[^>]*>).*?(</text>)', rf'\g<1>{rank}\2', stats_content)
        stats_content = re.sub(r'(<text id="val-tiers"[^>]*>).*?(</text>)', rf'\g<1>{tiers_html}\2', stats_content)

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

        int_w = min(180, int((int_val / 50) * 180))
        str_w = min(180, int((str_val / 500) * 180))
        sen_w = min(180, int((sen_val / 30) * 180))
        agi_w = min(180, int((agi_val / 40) * 180))
        vit_w = min(180, int((vit_val / 30) * 180))
        xp_w = min(420, int((xp_percent / 100) * 420))

        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!int_width\s*\*/)', rf'\g<1>{int_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!str_width\s*\*/)', rf'\g<1>{str_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!sen_width\s*\*/)', rf'\g<1>{sen_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!agi_width\s*\*/)', rf'\g<1>{agi_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!vit_width\s*\*/)', rf'\g<1>{vit_w}px\2', stats_content)
        stats_content = re.sub(r'(to\s*\{\s*width:\s*)\d+px(;?\s*\}\s*/\*\s*!xp_width\s*\*/)', rf'\g<1>{xp_w}px\2', stats_content)

        with open(stats_path, "w", encoding="utf-8") as f:
            f.write(stats_content)
        print("Updated stats.svg successfully.")

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

        if ranking < 50000:
            lc_solver = "ELITE ARCHITECT"
        elif ranking < 250000:
            lc_solver = "STAFF ENGINEER"
        elif ranking < 1000000:
            lc_solver = "SENIOR DEVELOPER"
        elif ranking < 2500000:
            lc_solver = "MID-TIER CODER"
        elif ranking < 5000000:
            lc_solver = "ASSOCIATE CODER"
        else:
            lc_solver = "APPRENTICE"

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

        goal = 300
        easy_dash = min(179.0, (easy_s / goal) * 179.0)
        medium_dash = min(179.0 - easy_dash, (medium_s / goal) * 179.0)
        hard_dash = min(179.0 - easy_dash - medium_dash, (hard_s / goal) * 179.0)

        lc_content = re.sub(r'(to\s*\{\s*stroke-dasharray:\s*)\d+(?:\.\d+)?(\s+200;\s*\}\s*/\*\s*!lc_easy_dash\s*\*/)', rf'\g<1>{easy_dash:.2f}\2', lc_content)
        lc_content = re.sub(r'(to\s*\{\s*stroke-dasharray:\s*)\d+(?:\.\d+)?(\s+200;\s*\}\s*/\*\s*!lc_medium_dash\s*\*/)', rf'\g<1>{medium_dash:.2f}\2', lc_content)
        lc_content = re.sub(r'(to\s*\{\s*stroke-dasharray:\s*)\d+(?:\.\d+)?(\s+200;\s*\}\s*/\*\s*!lc_hard_dash\s*\*/)', rf'\g<1>{hard_dash:.2f}\2', lc_content)

        medium_offset = -int(easy_dash)
        hard_offset = -int(easy_dash + medium_dash)

        lc_content = re.sub(r'(<path id="lc-medium-arc"[^>]*stroke-dashoffset=").*?(")', rf'\g<1>{medium_offset}\2', lc_content)
        lc_content = re.sub(r'(<path id="lc-hard-arc"[^>]*stroke-dashoffset=").*?(")', rf'\g<1>{hard_offset}\2', lc_content)

        with open(leetcode_path, "w", encoding="utf-8") as f:
            f.write(lc_content)
        print("Updated leetcode.svg successfully.")

    # 3. Generate github_dashboard.svg
    dashboard_svg = generate_github_dashboard_svg(github_stats, current_streak, longest_streak, github_stats["days"])
    with open(github_dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_svg)
    print("Generated github_dashboard.svg successfully.")

if __name__ == "__main__":
    update_files()
