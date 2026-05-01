import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template

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
            genre TEXT NOT NULL,
            price TEXT NOT NULL,
            description TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def seed_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM concerts;")
    count = cur.fetchone()[0]

    if count == 0:
        concerts = [
            ("Jazz Night", "Dnipro", "Jazz", "$10", "Живий джаз у центрі міста"),
            ("Rock Evening", "Kyiv", "Rock", "$15", "Локальні рок-гурти"),
            ("Indie Vibes", "Lviv", "Indie", "$12", "Атмосферний інді-концерт"),
            ("Hip-Hop Night", "Kharkiv", "Hip-Hop", "$8", "Батли та лайв виступи"),
            ("Acoustic Evening", "Odesa", "Acoustic", "$7", "Спокійна музика на заході сонця"),
            ("Electronic Party", "Kyiv", "Electronic", "$20", "DJ сети всю ніч"),
            ("Blues Night", "Lviv", "Blues", "$9", "Класичний блюз у живому виконанні"),
            ("Pop Hits Live", "Dnipro", "Pop", "$11", "Популярні хіти наживо"),
            ("Folk Stories Live", "Ivano-Frankivsk", "Folk", "$6", "Локальні музиканти виконують сучасні фолк-пісні"),
            ("Garage Band Session", "Ternopil", "Alternative", "$9", "Виступ молодих альтернативних гуртів у камерному клубі")
        ]

        cur.executemany("""
            INSERT INTO concerts (title, city, genre, price, description)
            VALUES (%s, %s, %s, %s, %s);
        """, concerts)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM concerts ORDER BY id;")
    concerts = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", concerts=concerts)

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

if __name__ == "__main__":
    create_table()
    seed_data()
    app.run(host="0.0.0.0", port=5000, debug=True)