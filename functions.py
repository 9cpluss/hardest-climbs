grade_map = {
    "9c": "5.15d",
    "9b/c": "5.15c/d",
    "9b+": "5.15c",
    "9b/+": "5.15b/c",
    "9b": "5.15b",
    "9a+": "5.15a",
    # Bouldering ---
    "9A": "V17",
    "8C+/9A": "V16/V17",
    "8C+": "V16",
    "8C/+": "V15/16",
    "8C": "V15",
}


def map_grades(grade):
    return grade_map.get(grade)


def create_video_list(x):
    links = []
    for name, link in x.items():
        links.append(
            f'<a href="{link}" class="link-warning" target="_blank">{name}</a>'
        )

    return ", ".join(links)


def create_repeat_list(x, category):
    return ", ".join([create_name_link(n, category) for n in x])


def create_title(title):
    return f'<h4>{title}</h4>'


def create_name_link(name, category):
    first_name = " ".join(name.split(" ")[0:-1])
    last_name = name.split(" ")[-1]

    return f'{first_name} <a href="/{category}/{last_name.lower()}" class="link-light">{last_name}</a>'


def create_html_from_json_element(x: dict, category: str, bg="secondary"):
    title = x.get("name")
    grade = x.get("grade")
    fa = x.get("fa")
    repeats = x.get("repeat")
    videos = x.get("videos")

    return f'\
        <div class="col-6">\
            <div class="p-3 bg-{bg} text-white rounded">\
                {create_title(title)}\
                Grade: {grade} / {map_grades(grade)}<br>\
                First Ascent: {create_name_link(fa, category)}<br>\
                Repeated by: {create_repeat_list(repeats, category)}<br>\
                Videos: {create_video_list(videos)}\
            </div>\
        </div>'


def create_html_columns(x: list, category: str):
    columns = []

    for i, climb in enumerate(x):
        if i % 2 == 0:
            html = create_html_from_json_element(climb, category)
        else:
            html = create_html_from_json_element(climb, category, bg="dark")

        columns.append(html)

    return "".join(columns)

