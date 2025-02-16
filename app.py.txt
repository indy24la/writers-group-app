from flask import Flask, render_template, request
import random

app = Flask(__name__)

roster = ["Chris", "James", "Sarah", "Gene", "Barry", "Erin", "Josh", "Jeremy", "Julie", "Jim", "Jill", "Gus", "Kai", "Rebecca", "David", "Kelly"]

def randomize_groups(attendees, group_count):
    readers = [name for name, role in attendees.items() if role == "reader"]
    nonreaders = [name for name, role in attendees.items() if role == "nonreader"]
    
    random.shuffle(readers)
    random.shuffle(nonreaders)
    
    new_groups = [[] for _ in range(group_count)]
    
    for index, person in enumerate(readers):
        new_groups[index % group_count].append(f"{person} (R)")
    for index, person in enumerate(nonreaders):
        new_groups[index % group_count].append(f"{person} (NR)")
    
    return new_groups

@app.route('/', methods=['GET', 'POST'])
def index():
    groups = []
    if request.method == 'POST':
        attendees = {}
        for name in roster:
            role = request.form.get(name, None)
            if role:
                attendees[name] = role
        group_count = int(request.form.get("group_count", 2))
        groups = randomize_groups(attendees, group_count)
    return render_template('index.html', roster=roster, groups=groups)

if __name__ == "__main__":
    app.run(debug=True)
