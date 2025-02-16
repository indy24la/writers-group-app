from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Initial roster of members
roster = ["Chris", "James", "Sarah", "Gene", "Barry", "Erin", "Josh", "Jeremy", "Julie", "Jim", "Jill", "Gus", "Kai", "Rebecca", "David", "Kelly"]

def randomize_groups(attendees, group_count):
    readers = [name for name, role in attendees.items() if role == "reader"]
    nonreaders = [name for name, role in attendees.items() if role == "nonreader"]
    
    random.shuffle(readers)
    random.shuffle(nonreaders)
    
    new_groups = [[] for _ in range(group_count)]
    
    # Evenly distribute readers
    for index, person in enumerate(readers):
        new_groups[index % group_count].append(f"{person} (R)")
    
    # Evenly distribute nonreaders
    for index, person in enumerate(nonreaders):
        new_groups[index % group_count].append(f"{person} (NR)")
    
    return new_groups

@app.route('/', methods=['GET', 'POST'])
def index():
    global roster  # Allows updating the roster list

    groups = []
    if request.method == 'POST':
        # Add a new member if entered
        new_member = request.form.get("new_member")
        if new_member and new_member.strip() and new_member not in roster:
            roster.append(new_member.strip())

        # Remove a member if the remove button was clicked
        remove_member = request.form.get("remove_member")
        if remove_member and remove_member in roster:
            roster.remove(remove_member)

        attendees = {}
        for name in roster:
            role = request.form.get(name, None)
            if role:
                attendees[name] = role

        # Get the number of groups (default to 2 if not provided)
        group_count = int(request.form.get("group_count", 2))

        # Generate groups based on selection
        if attendees:
            groups = randomize_groups(attendees, group_count)

    return render_template('index.html', roster=roster, groups=groups)

if __name__ == "__main__":
    app.run(debug=True)