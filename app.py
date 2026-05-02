import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="db",
        database="localgigs",
        user="postgres",
        password="postgres"
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS concerts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            city TEXT NOT NULL,
            venue TEXT DEFAULT '',
            genre TEXT NOT NULL,
            price TEXT NOT NULL,
            event_date TEXT DEFAULT '',
            image_url TEXT DEFAULT '',
            contact_url TEXT DEFAULT '',
            description TEXT NOT NULL,
            is_featured BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("ALTER TABLE concerts ADD COLUMN IF NOT EXISTS venue TEXT DEFAULT '';")
    cur.execute("ALTER TABLE concerts ADD COLUMN IF NOT EXISTS event_date TEXT DEFAULT '';")
    cur.execute("ALTER TABLE concerts ADD COLUMN IF NOT EXISTS image_url TEXT DEFAULT '';")
    cur.execute("ALTER TABLE concerts ADD COLUMN IF NOT EXISTS contact_url TEXT DEFAULT '';")
    cur.execute("ALTER TABLE concerts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
    cur.execute("ALTER TABLE concerts ADD COLUMN IF NOT EXISTS is_featured BOOLEAN NOT NULL DEFAULT FALSE;")

    conn.commit()
    cur.close()
    conn.close()

def seed_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM concerts;")
    cur.execute("ALTER SEQUENCE concerts_id_seq RESTART WITH 1;")

    concerts = [
        ("Jazz Night", "Dnipro", "Blue Note Club", "Jazz", "$10", "2026-05-10", "https://images.unsplash.com/photo-1511192336575-5a79af67a629", "https://example.com/jazz-night", "Живий джаз у центрі міста з місцевим квартетом.", True),
        ("Rock Evening", "Kyiv", "Atlas Club", "Rock", "$15", "2026-05-12", "https://images.unsplash.com/photo-1501386761578-eac5c94b800a", "https://example.com/rock-evening", "Локальні рок-гурти, гітари, драйв і вечірня атмосфера.", False),
        ("Indie Vibes", "Lviv", "Dzyga Art Center", "Indie", "$12", "2026-05-14", "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f", "https://example.com/indie-vibes", "Атмосферний інді-концерт для тих, хто любить камерні виступи.", True),
        ("Hip-Hop Night", "Kharkiv", "Urban Stage", "Hip-Hop", "$8", "2026-05-16", "https://img.redbull.com/images/q_auto,f_auto/redbullcom/2023/12/5/xdaxjmwkryffxwc5yy9l/hip-hop-for-hopw-showcase", "https://example.com/hip-hop-night", "Батли, лайв-виступи та молоді локальні артисти.", False),
        ("Acoustic Evening", "Odesa", "Sea View Bar", "Acoustic", "$7", "2026-05-18", "https://images.unsplash.com/photo-1510915361894-db8b60106cb1", "https://example.com/acoustic-evening", "Спокійна акустична музика біля моря на заході сонця.", False),
        ("Electronic Party", "Kyiv", "Module Club", "Electronic", "$20", "2026-05-20", "https://images.unsplash.com/photo-1571266028243-d220c6a7edbf", "https://example.com/electronic-party", "Ніч електронної музики з локальними DJ-сетами.", True),
        ("Blues Night", "Lviv", "Old Tram Pub", "Blues", "$9", "2026-05-22", "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4", "https://example.com/blues-night", "Класичний блюз у живому виконанні в маленькому пабі.", False),
        ("Pop Hits Live", "Dnipro", "Rooftop Stage", "Pop", "$11", "2026-05-24", "https://images.unsplash.com/photo-1501612780327-45045538702b", "https://example.com/pop-hits-live", "Популярні хіти наживо від молодих місцевих вокалістів.", False),
        ("Folk Stories Live", "Ivano-Frankivsk", "Warm Hall", "Folk", "$6", "2026-05-26", "https://i.pinimg.com/1200x/4f/53/22/4f532239270021cff178cb053b437897.jpg", "https://example.com/folk-stories-live", "Сучасний український фолк у теплому камерному просторі.", False),
        ("Garage Band Session", "Ternopil", "Garage 21", "Alternative", "$9", "2026-05-28", "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b", "https://example.com/garage-band-session", "Виступ молодих альтернативних гуртів у камерному клубі.", False)
    ]

    cur.executemany("""
        INSERT INTO concerts
        (title, city, venue, genre, price, event_date, image_url, contact_url, description, is_featured)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, concerts)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    city = request.args.get("city")

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if city:
        cur.execute("""
            SELECT * FROM concerts
            WHERE city = %s
            ORDER BY is_featured DESC, created_at DESC;
        """, (city,))
    else:
        cur.execute("""
            SELECT * FROM concerts
            ORDER BY is_featured DESC, created_at DESC;
        """)

    concerts = cur.fetchall()

    cur.execute("SELECT DISTINCT city FROM concerts ORDER BY city;")
    cities = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "index.html",
        concerts=concerts,
        cities=cities,
        selected_city=city
    )

@app.route("/items/<int:concert_id>")
def concert_details(concert_id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM concerts WHERE id = %s;", (concert_id,))
    concert = cur.fetchone()

    cur.close()
    conn.close()

    if concert is None:
        return "Концерт не знайдено", 404

    return render_template("details.html", concert=concert)

@app.route("/admin")
def admin():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT * FROM concerts
        ORDER BY created_at DESC;
    """)

    concerts = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin.html", concerts=concerts)

if __name__ == "__main__":
    create_table()
    seed_data()
    app.run(host="0.0.0.0", port=5000, debug=True)