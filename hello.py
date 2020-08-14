import numpy as np
exams = []
periods = []
rooms = []

class Exam:
    def __init__(self, duration, studentAmount):
        self.duration = duration
        self.studentAmount = studentAmount

class ScheduledExam:
    def __init__(self, period, room):
        self.period = period
        self.room = room

class Room:
    def __init__(self, number, penalty):
        self.number = number
        self.penalty = penalty

class Period:
    def __init__(self, date, time,duration,penalty):
        self.date = date
        self.time = time
        self.duration = duration
        self.penalty = penalty

class State:
    def __init__(self, state, heuristic):
        self.state = state
        self.heuristic = heuristic


# def get_schedule_with_hill_climbing():
#     while():

def read_file():
    lineType = ""
    with open("test.exam") as f:
        for line in f:
            if "Exams" in line:
                line = f.readline()
                lineType = "Exams"
            if "Periods" in line:
                line = f.readline()
                lineType = "Periods"
            if "Rooms" in line:
                line = f.readline()
                lineType = "Rooms"
            if "PeriodHardConstraints" in line:
                line = f.readline()
                lineType = "PeriodHardConstraints"
                line = f.readline()
            if "RoomHardConstraints" in line:
                line = f.readline()
                lineType = "RoomHardConstraints"
            if "InstitutionalWeightings" in line:
                line = f.readline()
                lineType = "InstitutionalWeightings"
             
            if(lineType == 'Exams'):
                arr = line.split(',')
                e1 = Exam(arr[0],len(arr))
                exams.append(e1)

            
            if(lineType == 'Periods'):
                arr = line.split(',')
                p1 = Period(arr[0],arr[1],arr[2],arr[3])
                periods.append(p1)

            
            if(lineType == 'Rooms'):
                arr = line.split(',')
                r1 = Room(arr[0],arr[1])
                rooms.append(r1)




read_file()

print(exams[0].studentAmount)

print(periods[0].date)

print(rooms[0].penalty)


def main():
    random_start_state = np.random.randint(5,size=(len(exams),2))
    print(random_start_state)

main()
