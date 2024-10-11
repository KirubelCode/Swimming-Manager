#Student number: C00260396
#Name: Kirubel Temesgen

from flask import Flask, render_template, request
import os
import webbrowser
import hfpy_utils
import swim_utils


app = Flask(__name__)


current_name = None
selected_files = []


@app.route("/")

@app.get("/getswimmers")
def select_swimmer():
    global selected_files

    if request.method == "POST":
        current_name = request.form["swimmer"]
        selected_files = [
            filename
            for filename in os.listdir(swim_utils.FOLDER)
            if filename.startswith(current_name)
        ]
        return render_template(
            "select.html",
            title="Select a swimmer to chart",
            data=sorted(set(current_name)),
        )

    names = set()
    for filename in os.listdir(swim_utils.FOLDER):
        if filename.endswith(".txt"):
            name, *_ = filename.removesuffix(".txt").split("-")
            names.add(name)

    return render_template(
        "select.html", title="Select a swimmer to chart", data=sorted(names)
    )


@app.post("/displayevents")
def get_swimmer_events():
    global selected_files

    name = request.form["swimmer"]
    selected_files = [
        filename.removesuffix(".txt")
        for filename in os.listdir(swim_utils.FOLDER)
        if filename.startswith(name)        
    ]

    
    return render_template(
        "swimmersFiles.html",
        title="Select a swimmer to chart",
        fileData=sorted(selected_files),
    )


@app.post("/chart")
def display_chart():
    filename = request.form["filenames"] + ".txt"
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(filename)

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html", title=the_title, average=the_average, data=the_data
    )


if __name__ == "__main__":
    app.run(debug=True)
