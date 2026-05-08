import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import itertools

API_KEY = "YOUR_API_KEY"

colors = itertools.cycle([
    "#ff4d4d", "#ff9f1a", "#f1c40f",
    "#2ecc71", "#1abc9c", "#3498db",
    "#9b59b6"
])


def search_food():

    food = entry.get().strip().lower()

    if not food:
        result_label.config(
            text="Please enter a food name",
            fg="white"
        )
        return

    btn.config(text="Searching...", state="disabled")
    root.update_idletasks()

    try:

        url = "https://api.nal.usda.gov/fdc/v1/foods/search"

        params = {
            "query": food,
            "api_key": API_KEY,
            "pageSize": 10
        }

        data = requests.get(
            url,
            params=params,
            timeout=10
        ).json()

        foods = data.get("foods", [])

        if not foods:
            result_label.config(
                text="Food not found",
                fg="white"
            )
            btn.config(text="Search", state="normal")
            return

        item = foods[0]

        food_text = item.get(
            "description",
            ""
        ).lower()

        protein = carbs = fat = calories = 0
        fiber = vitamins = minerals = 0
        sugar = sodium = 0

        for n in item.get("foodNutrients", []):

            name = (
                n.get("nutrientName") or ""
            ).lower()

            value = n.get("value")

            if value is None:
                value = 0

            try:
                value = float(value)

            except:
                value = 0

            if (
                "energy" in name or
                "calorie" in name or
                "kcal" in name
            ):
                calories = value

            elif "protein" in name:
                protein = value

            elif "carbohydrate" in name:
                carbs = value

            elif (
                "lipid" in name or
                "fat" in name
            ):
                fat = value

            elif "fiber" in name:
                fiber += value

            elif "sugar" in name:
                sugar += value

            elif "sodium" in name:
                sodium += value

            elif "vitamin" in name:
                vitamins += value

            elif any(
                x in name for x in
                [
                    "calcium",
                    "iron",
                    "magnesium",
                    "potassium"
                ]
            ):
                minerals += value

        fruit_keywords = [
            "apple", "banana", "orange",
            "mango", "grape", "pear",
            "pineapple", "watermelon"
        ]

        veg_keywords = [
            "spinach", "broccoli",
            "carrot", "lettuce",
            "tomato", "cucumber"
        ]

        junk_keywords = [
            "burger", "pizza",
            "fries", "cake",
            "cookie", "chips"
        ]

        processed_keywords = [
            "instant",
            "processed",
            "packaged",
            "frozen"
        ]

        is_fruit = any(
            x in food_text
            for x in fruit_keywords
        )

        is_veg = any(
            x in food_text
            for x in veg_keywords
        )

        is_junk = any(
            x in food_text
            for x in junk_keywords
        )

        is_processed = any(
            x in food_text
            for x in processed_keywords
        )

        healthy_score = 0
        junk_score = 0

        if protein >= 8:
            healthy_score += 15

        if fiber >= 5:
            healthy_score += 25

        if vitamins > 0:
            healthy_score += 10

        if minerals > 0:
            healthy_score += 10

        if calories < 150:
            healthy_score += 15

        if is_fruit:
            healthy_score += 35

        if is_veg:
            healthy_score += 40

        if sugar >= 20:
            junk_score += 30

        if fat >= 25:
            junk_score += 25

        if sodium >= 600:
            junk_score += 25

        if calories >= 700:
            junk_score += 20

        if is_junk:
            junk_score += 50

        if is_processed:
            junk_score += 30

        final_score = max(
            0,
            min(
                100,
                healthy_score - junk_score + 45
            )
        )

        if final_score >= 80:
            health = "🥗 Very Healthy"
            color = "#2ecc71"

        elif final_score >= 60:
            health = "💪 Healthy"
            color = "#7CFC00"

        elif final_score >= 40:
            health = "⚠️ Moderate"
            color = "#f1c40f"

        else:
            health = "🍔 Unhealthy"
            color = "#e74c3c"

        result_label.config(
            text=
            f"{item['description']}\n\n"
            f"Calories : {calories:.1f}\n"
            f"Protein : {protein:.1f}g\n"
            f"Carbs : {carbs:.1f}g\n"
            f"Fat : {fat:.1f}g\n"
            f"Sugar : {sugar:.1f}g\n\n"
            f"Score : {final_score}/100\n\n"
            f"{health}",
            fg=color,
            justify="center",
            anchor="center"
        )

        calories_bar["value"] = min(
            (calories / 800) * 100,
            100
        )

        protein_bar["value"] = min(
            (protein / 50) * 100,
            100
        )

        carbs_bar["value"] = min(
            (carbs / 100) * 100,
            100
        )

        fat_bar["value"] = min(
            (fat / 70) * 100,
            100
        )

    except Exception as e:

        result_label.config(
            text="API Error",
            fg="white"
        )

        print(e)

    btn.config(
        text="Search",
        state="normal"
    )


def animate_title():

    canvas.itemconfig(
        title,
        fill=next(colors)
    )

    root.after(
        400,
        animate_title
    )


root = tk.Tk()

root.title("Food Nutrition Analyzer")

root.geometry("900x650")

root.resizable(False, False)

canvas = tk.Canvas(
    root,
    width=900,
    height=650,
    highlightthickness=0
)

canvas.pack()

bg = Image.open(
    "food.jpg"
).resize((900, 650))

bg_img = ImageTk.PhotoImage(bg)

canvas.bg_img = bg_img

canvas.create_image(
    0,
    0,
    image=bg_img,
    anchor="nw"
)

title = canvas.create_text(
    450,
    50,
    text="Food Nutrition Analyzer",
    font=("Segoe UI", 28, "bold"),
    fill="white"
)

animate_title()

canvas.create_text(
    450,
    95,
    text="Smart nutrition + health scoring system",
    font=("Segoe UI", 13),
    fill="#064E3B"
)

canvas.create_text(
    830,
    20,
    text="Made by GDGPSD",
    font=("Segoe UI", 9, "italic"),
    fill="white"
)

frame = tk.Frame(
    root,
    bg="#000000"
)

entry = tk.Entry(
    frame,
    font=("Segoe UI", 15),
    width=30,
    justify="center"
)

entry.pack(
    side="left",
    ipady=6
)

btn = tk.Button(
    frame,
    text="Search",
    font=("Segoe UI", 11, "bold"),
    bg="#2ecc71",
    fg="white",
    bd=0,
    padx=15,
    pady=6,
    command=search_food
)

btn.pack(side="left")

canvas.create_window(
    450,
    150,
    window=frame
)

main_result_frame = tk.Frame(
    root,
    bg="#000000"
)

canvas.create_window(
    450,
    390,
    window=main_result_frame
)

card = tk.Frame(
    main_result_frame,
    bg="#1a1a1a"
)

card.pack(
    side="left",
    padx=20
)

result_label = tk.Label(
    card,
    text="Search food",
    font=("Segoe UI", 11, "bold"),
    bg="#1a1a1a",
    fg="white",
    justify="center",
    width=22,
    padx=20,
    pady=20
)

result_label.pack()

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TProgressbar",
    troughcolor="#2b2b2b",
    background="#2ecc71",
    thickness=14
)

bars_frame = tk.Frame(
    main_result_frame,
    bg="#000000"
)

bars_frame.pack(
    side="left",
    padx=15
)

def make_bar(name):

    container = tk.Frame(
        bars_frame,
        bg="#000000"
    )

    container.pack(
        pady=10,
        anchor="w"
    )

    tk.Label(
        container,
        text=name,
        font=("Segoe UI", 10, "bold"),
        bg="#000000",
        fg="white"
    ).pack(anchor="w")

    bar = ttk.Progressbar(
        container,
        length=220,
        mode="determinate"
    )

    bar.pack(pady=4)

    return bar


calories_bar = make_bar("Calories")
protein_bar = make_bar("Protein")
carbs_bar = make_bar("Carbs")
fat_bar = make_bar("Fat")

root.mainloop()
