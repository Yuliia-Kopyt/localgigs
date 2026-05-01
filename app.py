from flask import Flask, render_template

app = Flask(__name__)

concerts = [
    {
        "id": 1,
        "title": "Jazz Night",
        "city": "Dnipro",
        "genre": "Jazz",
        "price": "$10",
        "description": "Живий джаз у центрі міста"
    },
    {
        "id": 2,
        "title": "Rock Evening",
        "city": "Kyiv",
        "genre": "Rock",
        "price": "$15",
        "description": "Локальні рок-гурти"
    },
    {
        "id": 3,
        "title": "Indie Vibes",
        "city": "Lviv",
        "genre": "Indie",
        "price": "$12",
        "description": "Атмосферний інді-концерт"
    },
    {
        "id": 4,
        "title": "Hip-Hop Night",
        "city": "Kharkiv",
        "genre": "Hip-Hop",
        "price": "$8",
        "description": "Батли та лайв виступи"
    },
    {
        "id": 5,
        "title": "Acoustic Evening",
        "city": "Odesa",
        "genre": "Acoustic",
        "price": "$7",
        "description": "Спокійна музика на заході сонця"
    },
    {
        "id": 6,
        "title": "Electronic Party",
        "city": "Kyiv",
        "genre": "Electronic",
        "price": "$20",
        "description": "DJ сети всю ніч"
    },
    {
        "id": 7,
        "title": "Blues Night",
        "city": "Lviv",
        "genre": "Blues",
        "price": "$9",
        "description": "Класичний блюз у живому виконанні"
    },
    {
        "id": 8,
        "title": "Pop Hits Live",
        "city": "Dnipro",
        "genre": "Pop",
        "price": "$11",
        "description": "Популярні хіти наживо"
    },
        {
        "id": 9,
        "title": "Folk Stories Live",
        "city": "Ivano-Frankivsk",
        "genre": "Folk",
        "price": "$6",
        "description": "Локальні музиканти виконують сучасні фолк-пісні"
    },
    {
        "id": 10,
        "title": "Garage Band Session",
        "city": "Ternopil",
        "genre": "Alternative",
        "price": "$9",
        "description": "Виступ молодих альтернативних гуртів у камерному клубі"
    }
]


@app.route("/")
def home():
    return render_template("index.html", concerts=concerts)

@app.route("/items/<int:concert_id>")
def concert_details(concert_id):
    concert = next((item for item in concerts if item["id"] == concert_id), None)

    if concert is None:
        return "Концерт не знайдено", 404

    return render_template("details.html", concert=concert)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)