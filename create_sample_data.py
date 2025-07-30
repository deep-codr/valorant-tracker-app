import pandas as pd

data = {
    'match_id': ['M1', 'M2', 'M3', 'M4', 'M5'],
    'agent': ['Jett', 'Reyna', 'Sage', 'Sova', 'Phoenix'],
    'map': ['Haven', 'Ascent', 'Bind', 'Split', 'Breeze'],
    'kills': [18, 22, 10, 15, 17],
    'deaths': [12, 14, 8, 10, 9],
    'assists': [3, 5, 9, 2, 4],
    'win': [True, False, True, False, True]
}

df = pd.DataFrame(data)
df.to_csv("data/match_history.csv", index=False)
print("✅ match_history.csv created successfully!")
