def save_students(students, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for student in students:
            line = f"{student['name']},{student['score']}\n"
            file.write(line)
            
students= [
    {"name":"민수","score":85},
    {"name":"지수","score":92},
    {"name":"영희","score":55}
]

save_students(students,"students.txt")


def load_students(filename):
    students = []

    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        data = line.strip().split(",")

        student = {
            "name": data[0],
            "score": int(data[1])
        }

        students.append(student)

    return students
students=load_students("students.txt")

print(students)