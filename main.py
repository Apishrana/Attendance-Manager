import pandas as pd
import datetime
from tabulate import tabulate
import os


class Manager:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATA_PATH = os.path.join(self.BASE_DIR, "Data")
        self.attendanceOverall = pd.DataFrame
        self.attendanceSub = {}

    def initializeDataFiles(self):
        os.makedirs(os.path.join(self.DATA_PATH, "Sub"), exist_ok=True)

        overall_file = os.path.join(self.DATA_PATH, "Overall.csv")

        if not os.path.exists(overall_file):
            pd.DataFrame(
                [
                    {
                        "Subject": "Overall",
                        "Present": 0,
                        "Total Classes": 0,
                        "Attendance Percentage": 0.0,
                        "Last Updated": datetime.datetime.now().strftime("%a %b %d %Y"),
                    }
                ]
            ).to_csv(overall_file, index=False)

    def getData(self):
        try:
            self.attendanceOverall = pd.read_csv(
                os.path.join(self.DATA_PATH, "Overall.csv")
            )
            for i in os.listdir(os.path.join(self.DATA_PATH, "Sub/")):
                self.attendanceSub[i[:-4]] = pd.read_csv(
                    os.path.join(self.DATA_PATH, "Sub", i)
                )
        except:
            self.initializeDataFiles()
            self.getData()

    def writeData(self):
        self.attendanceOverall.to_csv(
            os.path.join(self.DATA_PATH, "Overall.csv"), index=False
        )
        for i in self.attendanceSub:
            self.attendanceSub[i].to_csv(
                os.path.join(self.DATA_PATH, "Sub/", f"{i}.csv"), index=False
            )

    def addSub(self):
        sub = input("Enter subject name: ").upper()
        self.attendanceSub[sub] = pd.DataFrame(columns=["Lec_Date", "Status"])

        newRow = pd.DataFrame(
            [
                {
                    "Subject": sub,
                    "Present": 0,
                    "Total Classes": 0,
                    "Attendance Percentage": 0.0,
                    "Last Updated": datetime.datetime.now().strftime("%a %b %d %Y"),
                }
            ]
        )

        self.attendanceOverall = pd.concat(
            [self.attendanceOverall, newRow], ignore_index=True
        )

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

        self.attendanceOverall.loc[
            self.attendanceOverall["Subject"] == "Overall", "Last Updated"
        ] = datetime.datetime.now().strftime("%a %b %d %Y")

        self.attendanceOverall.loc[
            self.attendanceOverall["Subject"] == sub, "Last Updated"
        ] = datetime.datetime.now().strftime("%a %b %d %Y")

        if status:
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Present"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Total Classes"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Total Classes"
                ]
                * 100
            )

            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Present"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Total Classes"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Total Classes"
                ]
                * 100
            )
        else:
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Total Classes"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Total Classes"
                ]
                * 100
            )
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Total Classes"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Total Classes"
                ]
                * 100
            )

    def toggleAttendance(self, sub, date):
        subDF = self.attendanceSub[sub]
        if date not in subDF["Lec_Date"].values:
            print("Invalid date")
            return

        status = subDF.loc[subDF["Lec_Date"] == date, "Status"].values[0]

        self.attendanceSub[sub].loc[
            self.attendanceSub[sub]["Lec_Date"] == date, "Status"
        ] = not status

        if status:
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Present"
            ] -= 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Total Classes"
                ]
                * 100
            )
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Present"
            ] -= 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Total Classes"
                ]
                * 100
            )
        else:
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Present"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == "Overall", "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == "Overall", "Total Classes"
                ]
                * 100
            )
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Present"
            ] += 1
            self.attendanceOverall.loc[
                self.attendanceOverall["Subject"] == sub, "Attendance Percentage"
            ] = (
                self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Present"
                ]
                / self.attendanceOverall.loc[
                    self.attendanceOverall["Subject"] == sub, "Total Classes"
                ]
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
                subjectList.remove("Overall")

                print("Subjects:")
                print(
                    tabulate(
                        enumerate(subjectList),
                        headers=["Index", "Subject"],
                        tablefmt="simple_outline",
                    )
                )

                sub = input("Enter subject Index:")
                status = input("Enter status (P/A): ")
                self.addAttendance(subjectList[int(sub)], status)

            case "2":
                subjectList = self.attendanceOverall["Subject"].tolist()
                subjectList.remove("Overall")

                print("Subjects:")
                print(
                    tabulate(
                        enumerate(subjectList),
                        headers=["Index", "Subject"],
                        tablefmt="simple_outline",
                    )
                )

                sub = input("Enter subject Index:")
                sub = subjectList[int(sub)]
                print(sub)
                print(
                    tabulate(
                        self.attendanceSub[sub],
                        headers="keys",
                        tablefmt="simple_outline",
                    )
                )
                date = input("Enter date (e.g. Wed May 06 2026): ")

                self.toggleAttendance(sub, date)

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
