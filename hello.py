import numpy as np

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
    def set_state(state):
        self.state = state


def get_schedule_with_hill_climbing(current_state):
    current_state.state
    i = 1
    while i < 10:
        nextState = find_next_state(current_state)
        i += 1
        if nextState is None:
            current_state.set_state(nextState)

def find_next_state(current_state):
    return current_state


def read_file(file_name,exams,periods,rooms):
    lineType = ""
    with open(file_name) as f:
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


def main():
    exams = []
    periods = []
    rooms = []
    read_file("test.exam",exams,periods,rooms)

    print(np.random.randint(5,size=(len(exams),2)))
    state = State(np.random.randint(5,size=(len(exams),2)),1)

    get_schedule_with_hill_climbing(state)

    print(exams[0].studentAmount)

    print(periods[0].date)

    print(rooms[0].penalty)



main()
