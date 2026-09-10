students = []

with open("students.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    data = line.strip().split(",")

    student = {
        "name": data[0],
        "score": int(data[1])
    }

    students.append(student)

print(students)