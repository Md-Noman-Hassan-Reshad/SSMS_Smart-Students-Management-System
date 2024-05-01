import os
from datetime import datetime
import segno
import cv2

now = datetime.now()
date_str = now.strftime("%d-%m-%Y")
time_str = now.strftime(f"%I:%M:%S %p")


class Student:
    """
    To know more about this project visit the link below: https://docs.google.com/document/d/15Jlvn0-xKT-_ZMqudkQOWtevGir5iBXuGcFI_JjFtmg/edit?fbclid=IwAR1JR-L270UUtpKBtpzmATg9vXDzTVUX6WAvLfnytufHC3hlQku1kxfvr24

    This is a class definition for Student. It contains attributes such as unique_id,
    name, roll, semester, department, college, and digital_balance. college is a class
    attribute shared by all instances of the class.
    """

    def __init__(self, unique_id=None, name=None, roll=None, semester=None, department=None, college=None, digital_balance=0, password=None):
        self.unique_id = unique_id
        self.name = name
        self.roll = roll
        self.semester = semester
        self.department = department
        self.college = college
        self.digital_balance = float(digital_balance)
        self.__password = password

    def __str__(self):
        """This method defines how the Student object should be represented."""
        return f"Unique ID: {self.unique_id}, Name: {self.name}, Roll: {self.roll}, Semester: {self.semester}, Department: {self.department}, College: {self.college}, Digital Balance: {self.digital_balance}, Password: {self.__password}"


class SmartStudentsManagementSystem:
    """
    This is a class definition for SmartStudentsManagementSystem. It contains a list
    students to store instances of the Student class.
    """

    def __init__(self):
        self.students = []

    @staticmethod
    def define_students_file(students_file="students-demo.csv"):
        return students_file

    def add_student(self, student):
        # if student.unique_id not in self.students:
        self.students.append(student)
        # print("Account created successfully.")
        # else:
        #     print("Student with that unique id already exists!")

    def delete_student_by_roll(self, roll):
        for student in self.students:
            if student.roll == roll:
                self.students.remove(student)
                return True
        return False

    def get_student_by_roll(self, roll):
        for student in self.students:
            if student.roll == roll:
                return student
        return None

    def get_student_by_id(self, unique_id):
        for student in self.students:
            if student.unique_id == unique_id:
                return student
        return None

    def save_students_in_students_csv(self, students_file=None):
        """
        data_list = []
        for line in data:
            split_line = line.split(",")
            first_column = split_line[0]
            data_list.append(first_column)
        """
        if students_file is None:
            students_file = self.define_students_file()
        with open(students_file, mode="r+") as file:
            data = file.readlines()
            data_list = [line.split(",")[0] for line in data]
            for student in self.students:
                if student.unique_id not in data_list:
                    file.writelines(
                        f"\n{student.unique_id},{student.name.title()},{student.roll},{student.semester},{student.department},{student.college},{student.digital_balance},{student._Student__password}")
                    # print("Account created successfully.")
                # else:
                # print("Student already exists")

    def load_students_csv(self, students_file=None):
        """
        Here, the *data syntax unpacks the elements of the `data` list and passes them as separate arguments to the Student constructor. So, it's essentially the same as manually providing each element of data as an argument to the Student constructor.
        """
        if students_file is None:
            students_file = self.define_students_file()
        with open(students_file, mode='r+') as file:
            header = file.readline().strip().split(",")  # Read the header row
            if header:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) == len(header):  # Ensure number of columns match
                        student = Student(*data)
                        self.students.append(student)
                    # else:
                    #     print("Skipping malformed row:", line)
            if os.path.getsize(students_file) == 0:
                file.write("Unique ID,Name,Roll,Semester,Department,College,Digital Balance,Password")

    def pay_fees_expenses(self, roll, amount, account, students_file=None, is_course=False, course_name=""):
        if students_file is None:
            students_file = self.define_students_file()
        amount = float(amount)
        student = self.get_student_by_roll(roll)
        if student:
            if student.digital_balance >= amount:
                with open(students_file, "r") as file:
                    lines = file.readlines()

                # Find the line corresponding to the student
                for index, line in enumerate(lines):
                    if student.roll in line:
                        parts = line.strip().split(",")
                        if parts[2] == roll:
                            if float(parts[-2]) > 0:
                                parts[-2] = str(float(parts[-2]) - amount)
                                lines[index] = ",".join(parts) + "\n"
                                with open(students_file, "w") as file:
                                    file.writelines(lines)
                                break
                            else:
                                print("Your balance is 0")

                accounts_folder = "Accounts"
                account_file = f"{accounts_folder}/{account}"

                if not os.path.exists(accounts_folder):
                    os.mkdir(accounts_folder)
                if not os.path.exists(account_file):
                    with open(account_file, "x") as _:
                        pass

                if is_course:
                    if os.path.getsize(account_file) == 0:
                        with open(account_file, mode="w") as file:
                            file.write("Date,Time,Roll,Amount,Course")
                            file.write(f"\n{date_str},{time_str},{roll},{amount},{course_name}")
                            print("Completed.")
                            return True
                    else:
                        with open(account_file, mode="a") as file:
                            file.write(f"\n{date_str},{time_str},{roll},{amount},{course_name}")
                            print("Completed.")
                            return True

                else:
                    if os.path.getsize(account_file) == 0:
                        with open(account_file, mode="w") as file:
                            file.write("Date,Time,Roll,Amount")
                            file.write(f"\n{date_str},{time_str},{roll},{amount}")
                            print("Transaction completed.")
                            return True
                    else:
                        with open(account_file, mode="a") as file:
                            file.write(f"\n{date_str},{time_str},{roll},{amount}")
                            print("Transaction completed.")
                            return True
            else:
                print("Insufficient balance or too low!")
                return False
        else:
            print("Student not found")
            return False

    def add_balance(self, roll, amount, students_file=None):
        student = self.get_student_by_roll(roll)
        amount = float(amount)
        if students_file is None:
            students_file = self.define_students_file()
        if student:
            with open(students_file, "r") as f:
                lines = f.readlines()
            for index, line in enumerate(lines):
                if student.roll in line:
                    parts = line.strip().split(",")
                    if parts[2] == roll:
                        parts[-2] = str(float(parts[-2]) + amount)
                        lines[index] = ",".join(parts) + "\n"
                        with open(students_file, "w") as f:
                            f.writelines(lines)
                            print("Digital Balance or Money added successfully!")
                            # print("Do not added Balance.")
                        break

    def scan_qr_code(self, roll, show=False):
        student = self.get_student_by_roll(roll)
        qrFolder = "QRCode"
        if student:
            qr_data = f"Name: {student.name}\nRoll: {student.roll}\nSemester: {student.semester}\nDepartment: {student.department}\nCollege: {student.college}"
            qr = segno.make(qr_data, micro=False)
            if not os.path.exists(qrFolder):
                os.mkdir(qrFolder)
            qr.save(f"{qrFolder}/{student.roll}.png", dark="darkred", light="lightblue")
            if show:
                # qr.show(dark="darkred", light="lightblue", scale=30)
                w, h, resizedQuality = 300, 300, cv2.INTER_AREA
                imgQr = cv2.imread(f"{qrFolder}/{student.roll}.png")
                resizedImg = cv2.resize(imgQr, (w, h), interpolation=resizedQuality)
                cv2.imshow("QR Code", resizedImg)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return qr_data
        else:
            print("Student not found.")
            return None


# Example usage:
if __name__ == '__main__':
    # Initialize the student management system
    ssms = SmartStudentsManagementSystem()

    # Load students from CSV file
    # if want to change file name then give parameter file_name
    fileName = ssms.define_students_file()
    ssms.load_students_csv(fileName)

    # Add a new student
    new_student = Student("127", "John Doe", "207", "6th", "CST", "NIIST", 500, "123456")
    ssms.add_student(new_student)

    # Save students to CSV file
    ssms.save_students_in_students_csv(fileName)

    # Pay college fees , canteen expenses & buy a course
    ssms.pay_fees_expenses("207", 10, "college.csv", fileName)
    # ssms.pay_fees_expenses("207", 10, "canteen.csv")

    ssms.pay_fees_expenses("207", 10, "course.csv", fileName, True, "Python Course")

    # Scan qr code to know students information
    ssms.scan_qr_code("207", False)
