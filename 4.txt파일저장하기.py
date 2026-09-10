students= [
    {"name":"민수","score":85},
    {"name":"지수","score":92},
    {"name":"영희","score":55}
]

with open("students.txt","w",encoding="utf-8")as file:
	for student in students:
		file.write(f"{student['name']},{student['score']}\n")