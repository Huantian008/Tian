def add_student(students: dict) -> None:
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("ID cannot be empty.")
        return
    if student_id in students:
        print("Student ID already exists.")
        return
    name = input("Name: ").strip()
    gender = input("Gender: ").strip()
    students[student_id] = {"name": name, "gender": gender}
    print("Student added.\n")


def delete_student(students: dict) -> None:
    student_id = input("Student ID to delete: ").strip()
    if student_id in students:
        del students[student_id]
        print("Student deleted.\n")
    else:
        print("Student not found.\n")


def view_students(students: dict) -> None:
    if not students:
        print("No students recorded.\n")
        return
    print("ID\tName\tGender")
    for student_id in sorted(students):
        info = students[student_id]
        print(f"{student_id}\t{info['name']}\t{info['gender']}")
    print()


def main() -> None:
    students: dict[str, dict[str, str]] = {}
    menu = (
        "1. Add student\n"
        "2. Delete student\n"
        "3. View students\n"
        "4. Exit\n"
    )
    actions = {
        "1": add_student,
        "2": delete_student,
        "3": view_students,
    }

    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        if choice == "4":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action:
            action(students)
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()
