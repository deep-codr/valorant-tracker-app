import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter

# ---------------------- DATA LOADER ----------------------

def load_data(path):
    return pd.read_csv(path)

# ---------------------- BASIC SUMMARY ----------------------

def basic_summary(df):
    total_matches = len(df)
    avg_kills = df['Kills'].mean()
    avg_deaths = df['Deaths'].mean()
    kd_ratio = df['Kills'].sum() / df['Deaths'].sum() if df['Deaths'].sum() > 0 else 0
    win_rate = (df['Result'].str.lower() == 'win').mean() * 100

    summary = {
        'Total Matches': int(total_matches),
        'Average Kills': round(avg_kills, 2),
        'Average Deaths': round(avg_deaths, 2),
        'K/D Ratio': round(kd_ratio, 2),
        'Win Rate (%)': round(win_rate, 2)
    }
    return summary

def save_summary(summary_dict, path):
    df_summary = pd.DataFrame([summary_dict])
    df_summary.to_csv(path, index=False)

# ---------------------- AGENT-WISE SUMMARY ----------------------

def agent_wise_summary(df):
    agents = df['Agent'].unique()
    result = []

    for agent in agents:
        agent_df = df[df['Agent'] == agent]
        total_matches = len(agent_df)
        avg_kills = agent_df['Kills'].mean()
        avg_deaths = agent_df['Deaths'].mean()
        kd_ratio = agent_df['Kills'].sum() / agent_df['Deaths'].sum() if agent_df['Deaths'].sum() > 0 else 0
        win_rate = (agent_df['Result'].str.lower() == 'win').mean() * 100

        result.append({
            'Agent': agent,
            'Matches': total_matches,
            'Avg Kills': round(avg_kills, 2),
            'Avg Deaths': round(avg_deaths, 2),
            'K/D Ratio': round(kd_ratio, 2),
            'Win Rate (%)': round(win_rate, 2)
        })

    return pd.DataFrame(result)

# ---------------------- MAP-WISE SUMMARY ----------------------

def map_wise_summary(df):
    maps = df['Map'].unique()
    result = []

    for map_name in maps:
        map_df = df[df['Map'] == map_name]
        total_matches = len(map_df)
        avg_kills = map_df['Kills'].mean()
        avg_deaths = map_df['Deaths'].mean()
        kd_ratio = map_df['Kills'].sum() / map_df['Deaths'].sum() if map_df['Deaths'].sum() > 0 else 0
        win_rate = (map_df['Result'].str.lower() == 'win').mean() * 100

        result.append({
            'Map': map_name,
            'Matches': total_matches,
            'Avg Kills': round(avg_kills, 2),
            'Avg Deaths': round(avg_deaths, 2),
            'K/D Ratio': round(kd_ratio, 2),
            'Win Rate (%)': round(win_rate, 2)
        })

    return pd.DataFrame(result)

# ---------------------- BEST AGENT SUGGESTION ----------------------

def suggest_best_agent(agent_df):
    top_winrate = agent_df.sort_values(by='Win Rate (%)', ascending=False).iloc[0]
    top_kd = agent_df.sort_values(by='K/D Ratio', ascending=False).iloc[0]
    most_played = agent_df.sort_values(by='Matches', ascending=False).iloc[0]

    votes = [top_winrate['Agent'], top_kd['Agent'], most_played['Agent']]
    final_vote = Counter(votes).most_common(1)[0][0]

    return {
        'Best Winrate Agent': top_winrate['Agent'],
        'Best K/D Agent': top_kd['Agent'],
        'Most Played Agent': most_played['Agent'],
        'Recommended Agent': final_vote
    }

# ---------------------- CHARTS ----------------------

def plot_kills_line_chart(df, save_path='output/kills_line_chart.png'):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Kills'], marker='o', linestyle='-', color='skyblue', label='Kills per Match')
    plt.title('Kills per Match')
    plt.xlabel('Match Number')
    plt.ylabel('Kills')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_agent_winrate(agent_df, save_path='output/agent_winrate_chart.png'):
    plt.figure(figsize=(10, 6))
    plt.bar(agent_df['Agent'], agent_df['Win Rate (%)'], color='orchid')
    plt.title('Agent-wise Win Rate')
    plt.xlabel('Agent')
    plt.ylabel('Win Rate (%)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    for index, value in enumerate(agent_df['Win Rate (%)']):
        plt.text(index, value + 1, f'{value:.1f}%', ha='center')

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# ---------------------- MATCH REPORT ----------------------

def generate_match_report(df):
    report = df.copy()
    report['K/D Ratio'] = (report['Kills'] / report['Deaths']).round(2)

    def get_grade(kills):
        if kills >= 25:
            return 'S'
        elif kills >= 20:
            return 'A'
        elif kills >= 15:
            return 'B'
        elif kills >= 10:
            return 'C'
        else:
            return 'D'

    report['Grade'] = report['Kills'].apply(get_grade)
    report['Win'] = report['Result'].str.lower().apply(lambda x: 1 if x == 'win' else 0)

    return report

# ---------------------- MATCH FETCH (SAMPLE) ----------------------

def fetch_match_data(riot_id):
    try:
        with open("data/sample_data.json", "r") as file:
            data = json.load(file)
            return data
    except Exception as e:
        return {"error": str(e)}

# ---------------------- SUMMARY STATS FROM JSON ----------------------

def get_summary_stats(data):
    kills = [m['kills'] for m in data['matches']]
    deaths = [m['deaths'] for m in data['matches']]

    total_kills = sum(kills)
    total_deaths = sum(deaths)

    return {
        "avg_kills": round(total_kills / len(kills), 2),
        "avg_deaths": round(total_deaths / len(deaths), 2),
        "kd_ratio": total_kills / total_deaths if total_deaths != 0 else 0
    }
