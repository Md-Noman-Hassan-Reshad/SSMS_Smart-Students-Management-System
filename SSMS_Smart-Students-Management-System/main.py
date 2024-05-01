import ssmsModule
from time import sleep
import re

ssms = ssmsModule.SmartStudentsManagementSystem()
csvFile = ssms.define_students_file("students-info.csv")
ssms.load_students_csv(csvFile)

colleges = ["NIIST", "BUET", "DUET"]
departments = ["Computer Science & Technology", "Automobile Technology", "Electrical Technology", "Mechanical Technology"]
semesters = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]
courses = ["Python Course(Beginner to Advance) --> only BDT 300TK",
           "Java Course(Beginner to Advance) --> only BDT 300TK",
           "Android App Development Course in Java(Beginner to Advance) --> only BDT 500TK",
           "Android App Development Course in Kotlin(Beginner to Advance) --> only BDT 600TK",
           "Web Development Course(Beginner to Advance) --> only BDT 480TK"]

print("\n\t\t\t\t\t\t\t\t\t\t\t Python Programming Project-2\n\t\t\t\t\t\t\t\t\t\t\tSmart Student Management System\n\t\t\t\t\t\t\t\t\t\t\t\t\t3rd Semester\n\t\t\t\t\t\t\t\t\t\t\t Computer Science & Technology\n\t\t\t\t\t\t\t" + "-" * 63)


def decorateFooter(func):
    def decorator():
        func()
        print("\nProject, Smart Student Management System - developed by me-Reshad & team members who touch their hand a little bit - Jahidul, Sujon, Fahim")

    return decorator


def printInfo(infoList, alignment="\t\t"):
    for i, content in enumerate(infoList):
        print(f"{i + 1}. {content}", end=alignment)
    if alignment != "\n":
        print()


def signin():
    print()
    inputId = input("Unique ID: ")
    inputPass = input("Password: ")

    student = ssms.get_student_by_id(inputId)

    sleep(1)
    if inputId != "" and inputPass != "":
        if student:
            if inputId == student.unique_id and inputPass == student._Student__password:
                print("Login successful!")
                print("Welcome", student.name + "!")
                main()
                return True
            else:
                print("Wrong Password. Login unsuccessful!")
                return False
        else:
            print("Student not found with that ID!")
    else:
        print("Enter all the information!")


def signup():
    print()
    uniqueId = input("Unique ID: ")
    name = input("Name: ")
    roll = input("Roll: ")

    printInfo(semesters)
    semester = ""
    try:
        smst = int(input("Semester: "))
        if smst != 0:
            semester += semesters[smst - 1]
    except ValueError:
        print("Select given number of semester!")
    except IndexError:
        print("Select given number of semester!")

    printInfo(departments)
    department = ""
    try:
        dpt = int(input("Department: "))
        if dpt != 0:
            department += departments[dpt - 1]
    except ValueError:
        print("Select given number of department!")
    except IndexError:
        print("Select given number of department!")

    printInfo(colleges)
    college = ""
    try:
        clg = int(input("College: "))
        if clg != 0:
            college += colleges[clg - 1]
    except ValueError:
        print("Select given number of college!")
    except IndexError:
        print("Select given number of college!")

    balance = float(0)
    try:
        balance += float(input("Digital Balance(at least 500 Tk): "))
    except ValueError:
        pass
    password = input("Password(must be at least 8 characters): ")

    if uniqueId != "" and name != "" and roll != "" and semester != "" and department != "" and college != "" and password != "":
        if len(password) >= 8:
            newStudent = ssmsModule.Student(uniqueId, name, roll, semester, department, college, balance, password)
            ssms.add_student(newStudent)
            ssms.save_students_in_students_csv(csvFile)
            sleep(1)
            print("Account created successfully.")
            main()
        else:
            print("Password must be at least 8 characters")
    else:
        print("Enter all the information!")
    if balance < float(500):
        print("Digital balance is too low(must be at least 500 Tk)")


@decorateFooter
def main():
    while True:
        print(
            "\n1.Pay Fees or Expenses\n2.Add Digital Balance or Money\n3.Scan QR Code\n4.Digital Content/Courses\n5.Change Password\n6.Sign out\n7.Exit")

        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            roll = input("Roll: ")
            amount = float(input("Amount: "))
            print("1.College Fees\t\t2.Canteen Expenses")
            transactionType = input("Enter your choice: ")
            sleep(1)
            match transactionType:
                case "1":
                    ssms.pay_fees_expenses(roll, amount, "college.csv", csvFile)
                    ssms.save_students_in_students_csv(csvFile)
                case "2":
                    ssms.pay_fees_expenses(roll, amount, "canteen.csv", csvFile)
                    ssms.save_students_in_students_csv(csvFile)
                case _:
                    print("Invalid choice!")

        # elif choice == "2":
        #     roll = input("Roll: ")
        #     deletedStudent = ssms.delete_student_by_roll(roll)
        #     if deletedStudent:
        #         print("Student deleted successfully.")
        #         ssms.save_students_to_csv(csvFile)
        #     else:
        #         print("Student not found.")
        #     sleep(1)

        elif choice == "2":
            roll = input("Roll: ")
            amount = float(input("Balance: "))
            ssms.add_balance(roll, amount, csvFile)
            ssms.save_students_in_students_csv(csvFile)
            # print("Digital Balance added successfully!")
            # print("Do not added.")
            sleep(1)

        elif choice == "3":
            roll = input("Roll: ")
            ssms.scan_qr_code(roll, True)

        elif choice == "4":
            printInfo(courses, "\n")
            course = ""
            global crs
            try:
                crs = int(input("Enter: "))
                if crs != 0:
                    course += courses[crs - 1]
            except ValueError:
                print("Select given number of course!")
            except IndexError:
                print("Select given number of course!")
            price = re.findall(r"\d+", course)
            price = float(*price)

            roll = input("Roll: ")
            amount = float(input("Amount: "))
            sleep(1)
            if crs:
                if price == amount:
                    ssms.pay_fees_expenses(roll, amount, "course.csv", csvFile, True, course)
                    ssms.save_students_in_students_csv(csvFile)
            else:
                print("Invalid choice!")
            print("All Course designed by Md. Noman Hassan Reshad")

        elif choice == "5":
            inputId = input("Unique ID: ")
            oldPass = input("Old Password: ")

            student = ssms.get_student_by_id(inputId)

            if student:
                if inputId == student.unique_id and oldPass == student._Student__password:
                    newPass = input("New Password: ")
                    confNewPass = input("Confirm New Password: ")
                    if newPass == confNewPass:
                        with open(csvFile, "r") as file:
                            lines = file.readlines()

                        # Find the line corresponding to the student
                        for index, line in enumerate(lines):
                            if student.roll in line:
                                parts = line.strip().split(",")
                                parts[-1] = str(parts[-1].replace(parts[-1], confNewPass))
                                lines[index] = ",".join(parts) + "\n"
                                with open(csvFile, "w") as file:
                                    file.writelines(lines)
                                break
                        sleep(1)
                        print("Password changed successful!")
                        main()
                    else:
                        print("Confirm new password, do not match!")
                else:
                    print("Wrong old Password. Password unchanged!")
            else:
                print("Student not found with that ID!")

        elif choice == "6":
            signOut = input("Do you want to Sign out? (y/n): ").lower()
            if signOut == "y":
                startUp()
                break

        elif choice == "7":
            exitProgram = input("Do you want to Exit? (y/n): ").lower()
            if exitProgram == "y":
                break

        else:
            print("Invalid Choice. Please try again!")


@decorateFooter
def startUp():
    while True:
        print("\n1. Create an Account, Sign Up\t\t2. Already have an account? Sign in\t\t3. Exit")
        accountDecision = input("Enter: ")
        match accountDecision:
            case "1":
                signup()
                break
            case "2":
                signin()
                break
            case "3":
                exitProgram = input("Do you want to Exit? (y/n): ").lower()
                if exitProgram == "y":
                    break
            case _:
                print("Invalid Choice. Please try again!")


startUp()
