from traceback import print_list

import pandas as pd
import datetime
from tabulate import tabulate
import os


class Manager:
    def __init__(self):
        self.DATA_PATH = "./Data/"
        self.attendanceOverall = pd.DataFrame
        self.attendanceSub = {}

    def getData(self):
        self.attendanceOverall = pd.read_csv(
            os.path.join(self.DATA_PATH, "Overall.csv")
        )
        for i in os.listdir(os.path.join(self.DATA_PATH, "Sub/")):
            self.attendanceSub[i[:-4]] = pd.read_csv(
                os.path.join(self.DATA_PATH, "Sub", i)
            )

    def writeData(self):
        self.attendanceOverall.to_csv(os.path.join(self.DATA_PATH, "Overall.csv"))
        for i in self.attendanceSub:
            self.attendanceSub[i].to_csv(
                os.path.join(self.DATA_PATH, "Sub/", f"{i}.csv")
            )

    def addSub(self):
        self.attendanceSub[input("Enter subject name: ")] = pd.DataFrame(
            columns=["Date", "Status"]
        )
        self.attendanceOverall

    def printAtt(self):
        print("OVERALL")
        print(
            tabulate(self.attendanceOverall, headers="keys", tablefmt="simple_outline")
        )
        for i in self.attendanceSub:
            print(i)
            print(
                tabulate(
                    self.attendanceSub[i], headers="keys", tablefmt="simple_outline"
                )
            )

    def addAttendance(self, sub, status):
        subDF = self.attendanceSub[sub]
        status = status.upper() == "P"
        newRow = pd.DataFrame(
            [
                {
                    "Lec_Date": datetime.datetime.now().strftime("%a %b %d %Y"),
                    "Status": status,
                }
            ]
        )
        subDF = pd.concat([subDF, newRow], ignore_index=True)
        self.attendanceSub[sub] = subDF

        if status:
            self.attendanceOverall["Overall"]["Present"] += 1
            self.attendanceOverall["Overall"]["Total Classes"] += 1
            self.attendanceOverall["Overall"]["Attendance Percentage"] = (
                self.attendanceOverall["Overall"]["Present"]
                / self.attendanceOverall["Overall"]["Total Classes"]
                * 100
            )
        else:
            self.attendanceOverall["Overall"]["Total Classes"] += 1
            self.attendanceOverall["Overall"]["Attendance Percentage"] = (
                self.attendanceOverall["Overall"]["Present"]
                / self.attendanceOverall["Overall"]["Total Classes"]
                * 100
            )

    def run(self):
        self.getData()
        self.printAtt()
        print("\n")
        print("What do you want to do?")
        print("1. Add Attendance")
        print("2. Toggle Attendance")
        print("3. Add Sub")
        print("4. Exit")
        print("\n")

        match input("Enter your choice: "):
            case "1":
                subjectList = self.attendanceOverall["Subject"].tolist()
                # subjectList.remove("Overall")

                print("Subjects:")
                print(
                    tabulate(
                        subjectList,
                        headers=["Index", "Subject"],
                        showindex=True,
                        tablefmt="simple_outline",
                    )
                )

                sub = input("Enter subject Index:")
                status = input("Enter status (P/A): ")
                self.addAttendance(subjectList[sub], status)

            case "2":
                sub = input("Enter subject name: ")
                date = input("Enter date (dd-mm-yyyy): ")
                self.attendanceSub[sub].loc[
                    self.attendanceSub[sub]["Date"] == date, "Status"
                ] = (
                    "P"
                    if self.attendanceSub[sub]
                    .loc[self.attendanceSub[sub]["Date"] == date, "Status"]
                    .values[0]
                    == "A"
                    else "A"
                )
            case "3":
                self.addSub()
            case "4":
                self.writeData()
                quit()

        self.writeData()
        self.run()


if __name__ == "__main__":
    man = Manager()
    man.run()
