import pandas as pd

# Load dataset
file_path = "dataset.csv"
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error reading {file_path}: {e}")
    exit()

# Define keyword-based categorization
def assign_category(row):
    text = (str(row['title']) + " " + str(row['description'])).lower()
    
    if any(x in text for x in ['python', 'react', 'java', 'sql', 'php', 'node', 'code', 'html', 'css', 'javascript', 'algorithm', 'git', 'excel', 'word', 'powerpoint', 'figma', 'canva', 'photoshop', 'illustrator', 'seo', 'machine learning', 'data science', 'ai']):
        return "Teknologi"
    elif any(x in text for x in ['mukbang', 'makan', 'kuliner', 'food', 'pedas', 'enak', 'restoran', 'kue', 'roti', 'pizza', 'burger', 'sushi', 'ramen', 'seafood']):
        return "Kuliner"
    elif any(x in text for x in ['vlog', 'liburan', 'travel', 'pantai', 'gunung', 'alam', 'kota', 'daily', 'hari', 'seru', 'pengalaman']):
        return "Vlog"
    elif any(x in text for x in ['belajar', 'tutorial', 'panduan', 'edukasi', 'matematika', 'fisika', 'kimia', 'biologi', 'sejarah', 'ekonomi', 'bahasa', 'statistik', 'rumit', 'sulit', 'kompleks']):
        return "Edukasi"
    elif any(x in text for x in ['drama', 'film', 'musik', 'lagu', 'lucu', 'menghibur', 'seram', 'horor', 'hantu', 'menakutkan', 'kekerasan']):
        return "Hiburan"
    else:
        return "Umum"

# Apply mapping
df['category'] = df.apply(assign_category, axis=1)

# Save back to CSV
df.to_csv(file_path, index=False)
print("Dataset successfully upgraded with 'category' column!")
print(df.head())
