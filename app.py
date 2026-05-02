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
            genre TEXT NOT NULL,
            price TEXT NOT NULL,
            description TEXT NOT NULL,
            is_featured BOOLEAN NOT NULL DEFAULT FALSE
        );
    """)

    cur.execute("""
        ALTER TABLE concerts
        ADD COLUMN IF NOT EXISTS is_featured BOOLEAN NOT NULL DEFAULT FALSE;
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
            ("Jazz Night", "Dnipro", "Jazz", "$10", "Живий джаз у центрі міста", True),
            ("Rock Evening", "Kyiv", "Rock", "$15", "Локальні рок-гурти", False),
            ("Indie Vibes", "Lviv", "Indie", "$12", "Атмосферний інді-концерт", True),
            ("Hip-Hop Night", "Kharkiv", "Hip-Hop", "$8", "Батли та лайв виступи", False),
            ("Acoustic Evening", "Odesa", "Acoustic", "$7", "Спокійна музика на заході сонця", False),
            ("Electronic Party", "Kyiv", "Electronic", "$20", "DJ сети всю ніч", True),
            ("Blues Night", "Lviv", "Blues", "$9", "Класичний блюз у живому виконанні", False),
            ("Pop Hits Live", "Dnipro", "Pop", "$11", "Популярні хіти наживо", False),
            ("Folk Stories Live", "Ivano-Frankivsk", "Folk", "$6", "Локальні музиканти виконують сучасні фолк-пісні", False),
            ("Garage Band Session", "Ternopil", "Alternative", "$9", "Виступ молодих альтернативних гуртів у камерному клубі", False)
        ]

        cur.executemany("""
            INSERT INTO concerts (title, city, genre, price, description, is_featured)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, concerts)

    cur.execute("UPDATE concerts SET is_featured = FALSE;")

    cur.execute("""
        UPDATE concerts
        SET is_featured = TRUE
        WHERE title IN ('Jazz Night', 'Indie Vibes', 'Electronic Party');
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    city = request.args.get("city")

    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if city:
        cur.execute(
            """
            SELECT * FROM concerts
            WHERE city = %s
            ORDER BY is_featured DESC, id DESC;
            """,
            (city,)
        )
    else:
        cur.execute("""
            SELECT * FROM concerts
            ORDER BY is_featured DESC, id DESC;
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

if __name__ == "__main__":
    create_table()
    seed_data()
    app.run(host="0.0.0.0", port=5000, debug=True)