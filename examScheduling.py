import sqlalchemy as db
import pandas as pd
from sqlalchemy import Column, Integer, Text, ForeignKey, String, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
from IPython.display import clear_output
import numpy as np


class Constraint:
    def __init__(self, ctype, name, periods):
        self.ctype = ctype
        self.name = name
        self.periods = periods


class SoftConstraint:
    def __init__(self, name, params):
        self.name = name
        self.params = params


def createModels(Base, engine):
    association_table = Table(
        "exam_student",
        Base.metadata,
        Column("id", db.Integer, primary_key=True),
        Column("exam_id", Integer, ForeignKey("exam.id", ondelete="cascade")),
        Column("student_id", Integer, ForeignKey("student.id", ondelete="cascade")),
    )

    association_two = Table(
        "exam_period",
        Base.metadata,
        Column("id", db.Integer, primary_key=True),
        Column("exam_id", Integer, ForeignKey("exam.id", ondelete="cascade")),
        Column("period_id", Integer, ForeignKey("period.id", ondelete="cascade")),
    )

    association_three = Table(
        "exam_room",
        Base.metadata,
        Column("id", db.Integer, primary_key=True),
        Column("exam_id", Integer, ForeignKey("exam.id", ondelete="cascade")),
        Column("room_id", Integer, ForeignKey("room.id", ondelete="cascade")),
    )

    class Exam(Base):
        __tablename__ = "exam"

        id = Column(Integer, primary_key=True)
        duration = Column(Integer)
        students = relationship(
            "Student",
            secondary=association_table,
            back_populates="exams",
            cascade="all, delete",
            passive_deletes=True,
        )
        periods = relationship(
            "Period",
            secondary=association_two,
            back_populates="exams",
            cascade="all, delete",
            passive_deletes=True,
        )
        rooms = relationship(
            "Room",
            secondary=association_three,
            back_populates="exams",
            cascade="all, delete",
            passive_deletes=True,
        )

    class Student(Base):
        __tablename__ = "student"

        id = Column(Integer, primary_key=True)
        #    examid = Column(Integer, ForeignKey('exams.id'))
        number = Column(Integer)
        #    exams = relationship(Exam,secondary='link')
        exams = relationship(
            "Exam",
            secondary=association_table,
            back_populates="students",
            cascade="all, delete",
            passive_deletes=True,
        )

    class Room(Base):
        __tablename__ = "room"

        id = Column(Integer, primary_key=True)
        capacity = Column(Integer)
        penalty = Column(Integer)
        exams = relationship(
            "Exam",
            secondary=association_three,
            back_populates="rooms",
            cascade="all, delete",
            passive_deletes=True,
        )

    class Period(Base):
        __tablename__ = "period"
        id = Column(Integer, primary_key=True)
        time = Column(DateTime)
        duration = Column(Integer)
        penalty = Column(Integer)
        exams = relationship(
            "Exam",
            secondary=association_two,
            back_populates="periods",
            cascade="all, delete",
            passive_deletes=True,
        )

    Base.metadata.create_all(engine)

    # for tbl in reversed(Base.metadata.sorted_tables):
    #     print(tbl.name)
    #     truncate_table = db.text(
    #         "TRUNCATE TABLE " + tbl.name + " RESTART IDENTITY CASCADE"
    #     )
    #     engine.execute(truncate_table)
    # print("hey model")
    return Period, Room, Student, Exam


def readRoomsFromFile(file, roomRows, session, Room):
    with open(file) as f:
        for line in f:
            if "Exams" in line:
                line = f.next()
                lineType = "Exams"
            if "Periods" in line:
                line = f.readline()
                lineType = "Periods"
            if "Rooms" in line:
                line = f.readline()
                lineType = "Rooms"
            if "PeriodHardConstraints" in line:
                lineType = "PeriodHardConstraints"
                line = f.readline()
            if "RoomHardConstraints" in line:
                line = f.readline()
                lineType = "RoomHardConstraints"
            if "InstitutionalWeightings" in line:
                line = f.readline()
                lineType = "InstitutionalWeightings"

            if lineType == "Rooms":
                arr = line.split(",")
                r1 = Room(capacity=arr[0], penalty=arr[1])
                roomRows.append(r1)

    session.add_all(roomRows)
    session.commit()


def readFile(
    file,
    examRows,
    periodRows,
    roomRows,
    studentRows,
    constraints,
    softconstraints,
    Period,
    session,
    Exam,
    Student,
):
    examRows = []
    periodRows = []
    studentRows = []
    students = []
    examcount = 0
    lineType = ""
    with open(file) as f:
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
                lineType = "PeriodHardConstraints"
                line = f.readline()
            if "RoomHardConstraints" in line:
                line = f.readline()
                lineType = "RoomHardConstraints"
            if "InstitutionalWeightings" in line:
                line = f.readline()
                lineType = "InstitutionalWeightings"

            if lineType == "Periods":
                arr = line.split(",")
                dateTime = arr[0] + arr[1]
                p1 = Period(
                    time=datetime.strptime(dateTime, "%d:%m:%Y %H:%M:%S"),
                    duration=arr[2],
                    penalty=arr[3],
                )
                periodRows.append(p1)

            if lineType == "PeriodHardConstraints":
                arr = line.split(",")
                print("period", arr)
                c1 = Constraint(
                    "period",
                    name=arr[1].strip(),
                    periods=[int(arr[0].strip()) + 1, int(arr[2].strip()) + 1],
                )
                constraints.append(c1)

            if lineType == "RoomHardConstraints":
                arr = line.split(",")
                print("room", arr)
                if len(arr) > 1:
                    c1 = Constraint(
                        "room", name=arr[1].strip(), periods=[int(arr[0].strip()) + 1]
                    )
                    constraints.append(c1)
                else:
                    c1 = Constraint("room", name=arr[0].strip(), periods=None)
                    constraints.append(c1)
            if lineType == "InstitutionalWeightings":
                arr = [x.strip() for x in line.split(",")]
                print(arr)
                sc1 = SoftConstraint(name=arr[0], params=[int(i) for i in arr[1:]])
                softconstraints.append(sc1)

            if lineType == "Exams":
                arr = line.split(",")
                examRows.append(Exam(duration=int(arr[0])))
                examRows[examcount].rooms.append(
                    roomRows[random.randint(0, len(roomRows) - 1)]
                )

                for no in arr[1:]:
                    no = no.strip()
                    no = int(no)
                    if no not in students:
                        students.append(int(no))
                        tempStudent = Student(number=int(no))
                        studentRows.append(tempStudent)
                    if no in students:
                        studentRows[students.index(no)].exams.append(
                            examRows[examcount]
                        )
                #                     examRows[examcount].students.append(studentRows[students.index(no)])
                examcount += 1

    session.add_all(examRows)
    session.add_all(periodRows)
    session.add_all(studentRows)
    session.add_all(roomRows)
    session.commit()


def generateStatisHeurisitcs(connection):
    sql_query = db.text(
        "create or replace view staticHeuristics as  select a.exam_id, b.student_id, b.exam_count, a.student_count from ( select exam_id, count(student_id) as student_count from exam_student group by exam_id) as a, ( select student_id , count(exam_id) as exam_count from exam_student group by student_id) as b order by b.exam_count desc"
    )
    connection.execute(sql_query)


def periodHeuristics(allocated_periods, period_heuristic, connection):
    periods = ",".join([str(elem) for elem in allocated_periods])
    if period_heuristic == 1:
        sql_query = db.text("select id from period order by penalty limit 1")
        period = connection.execute(sql_query).fetchone()[0]
        allocated_periods.append(period)
    if period_heuristic == 2:
        sql_query = db.text("select id from period order by time asc limit 1")
        period = connection.execute(sql_query).fetchone()[0]
        allocated_periods.append(period)
    if period_heuristic == 3:
        sql_query = db.text("select id from period order by duration asc limit 1")
        period = connection.execute(sql_query).fetchone()[0]
        allocated_periods.append(period)
    if period_heuristic == 4:
        sql_query = db.text("select id from period order by random() asc limit 1")
        period = connection.execute(sql_query).fetchone()[0]
        allocated_periods.append(period)
    return period


def examHeuristics(
    allocated_exams,
    allocated_periods,
    exam_heuristic,
    period_heuristic,
    examRows,
    connection,
    session,
    periodRows,
):
    allocated = ",".join([str(elem) for elem in allocated_exams])
    periodId = periodHeuristics(allocated_periods, period_heuristic, connection)
    if exam_heuristic == 1:
        # schedule exam with most clashes first
        sql_query = db.text(
            "select exam_id from staticHeuristics  where exam_id not in ("
            + allocated
            + ") order by exam_count desc limit 1"
        )
        exam = connection.execute(sql_query).fetchone()
        if exam is None:
            return None
        exam = exam[0]
        examRows[exam - 1].periods.append(periodRows[periodId - 1])
        session.add(examRows[exam - 1])
        session.commit()
        allocated_exams.append(exam)
    if exam_heuristic == 2:
        # schedule exam with most students first
        sql_query = db.text(
            "select exam_id from staticheuristics where exam_id not in ("
            + allocated
            + ")  order by student_count desc limit 1"
        )
        exam = connection.execute(sql_query).fetchone()
        if exam is None:
            return None
        exam = exam[0]
        examRows[exam - 1].periods.append(periodRows[periodId - 1])
        session.add(examRows[exam - 1])
        session.commit()
        allocated_exams.append(exam)
    return exam


def heuristics(examRows, connection, session, periodRows):
    allocated_exams = [0]
    allocated_periods = [0]
    exam_heuristic = random.randint(1, 2)
    period_heuristic = random.randint(1, 4)
    while len(allocated_exams) - 1 < len(examRows):

        examHeuristics(
            allocated_exams,
            allocated_periods,
            exam_heuristic,
            period_heuristic,
            examRows,
            connection,
            session,
            periodRows,
        )

    return exam_heuristic, period_heuristic


def clearPeriodTable(examRows, session):
    for exam in examRows:
        exam.periods.clear()
    session.commit()


def EvaluateSolution(sql_view, connection, constraints):
    dates = []
    violationCount = 0
    for constraint in constraints:
        # 2, EXAM_COINCIDENCE, 3
        # exam 2 and 3 should be in the same period:
        if constraint.name == "EXAM_COINCIDENCE":
            sql_query = db.text(
                "SELECT COUNT(DISTINCT period_id) FROM "
                + sql_view
                + " WHERE exam_id=:idOne OR exam_id =:idTwo"
            )
            result = connection.execute(
                sql_query, idOne=constraint.periods[0], idTwo=constraint.periods[1]
            )
            for r in result:
                #                 print(r[0])
                if r[0] > 1:
                    violationCount += 1

        # 1, EXCLUSION, 5
        # exam 1 and 5 should not be in the same period:
        if constraint.name == "EXCLUSION":
            sql_query = db.text(
                "SELECT COUNT(DISTINCT period_id) FROM "
                + sql_view
                + " WHERE exam_id=:idOne OR exam_id =:idTwo"
            )
            result = connection.execute(
                sql_query, idOne=constraint.periods[0], idTwo=constraint.periods[1]
            )
            for r in result:
                #                 print(r[0])
                if r[0] < 2:
                    violationCount += 1

        # 0, AFTER, 9
        # 0 should be timetabled after 9
        if constraint.name == "AFTER":
            sql_query = db.text(
                "SELECT exam_id, datetime FROM (SELECT exam_id, time as datetime FROM "
                + sql_view
                + " INNER JOIN period ON "
                + sql_view
                + ".period_id = period.id) AS T WHERE exam_id =:idOne OR exam_id =:idTwo ORDER BY exam_id"
            )
            result = connection.execute(
                sql_query, idOne=constraint.periods[0], idTwo=constraint.periods[1]
            )
            for r in result:
                dates.append(r["datetime"])

            if dates[0] < dates[1]:
                violationCount += 1
            result_as_list = result.fetchall()
        # 9, ROOM_EXCLUSIVE
        # exam 9 should be the only exam scheduled in a room
        if constraint.name.strip() == "ROOM_EXCLUSIVE":
            sql_query = db.text(
                "SELECT COUNT(DISTINCT exam_id) as exam_count FROM "
                + sql_view
                + " WHERE room_id = (SELECT room_id FROM "
                + sql_view
                + " WHERE exam_id =1 limit 1) and period_id = (SELECT period_id FROM "
                + sql_view
                + " WHERE exam_id =:examId limit 1)"
            )
            result = connection.execute(sql_query, examId=constraint.periods[0])
            for r in result:
                if r["exam_count"] > 1:
                    violationCount += 1

    return violationCount


def createSolution(sql_view, connection, examRows, session, periodRows):

    heuristics(examRows, connection, session, periodRows)

    query_string = (
        "CREATE OR REPLACE VIEW "
        + sql_view
        + " AS SELECT exam_period.exam_id, period_id, exam_room.room_id FROM exam_room INNER JOIN exam_period ON exam_room.exam_id = exam_period.exam_id"
    )
    view_query = db.text(query_string)
    connection.execute(view_query)


def generateSolution(examRows, connection, session, periodRows):
    clearPeriodTable(examRows, session)
    exam, period = heuristics(examRows, connection, session, periodRows)
    createSolution("tempSolution2", connection, examRows, session, periodRows)
    return exam, period


def getSolutionScore(sql_view, softconstraints, connection, constraints):

    currentScore = EvaluateSolution(sql_view, connection, constraints)

    # def getCurrentScore(sql_view, softconstraints, connection):
    currentSoftConstraintScore = getCurrentScore(sql_view, softconstraints, connection)
    return currentScore + currentSoftConstraintScore


def GreedyHillClimbing(
    iterations,
    softconstraints,
    connection,
    sample,
    constraints,
    examRows,
    session,
    periodRows,
):
    currentScore = getSolutionScore(
        "tempSolution", softconstraints, connection, constraints
    )
    iteration = 0
    scores = []
    examHeuristic = 0
    periodHeuristic = 0
    while iteration < iterations:
        random.seed(random.randint(3, 9))
        print("amount of violations so far", currentScore)
        print("iteartion:", iteration)
        #     if currentScore == 0:
        #         break

        examHeuristic, periodHeuristic = generateSolution(
            examRows, connection, session, periodRows
        )

        score = getSolutionScore(
            "tempSolution2", softconstraints, connection, constraints
        )
        scores.append(score)
        print("neighbour score:", score)
        if score < currentScore:
            drop_view = db.text("DROP VIEW tempSolution")
            connection.execute(drop_view)
            alter_view = db.text("ALTER VIEW tempSolution2 RENAME TO tempSolution")
            connection.execute(alter_view)
            currentScore = score
        #     clear_output(wait=True)
        iteration += 1

    scores_arr = np.asarray(scores)
    print("result for :", sample)
    print("Objective scores:", scores)
    print("mean:", np.mean(scores_arr))
    print("std:", np.std(scores_arr))
    print("min:", np.min(scores_arr))
    print(
        "best exam heuristic:", examHeuristic, "best period heuristic:", periodHeuristic
    )


def getCurrentScore(sql_view, softconstraints, connection):
    runningScore = 0
    for cons in softconstraints:
        if cons.name == "TWOINAROW":
            sql_query = db.text(
                "select Count(student_id) as studentCount from ( select prev_exam, time, elapsed_time, exam_id from ( select time, elapsed_time, exam_id, lag(exam_id) over ( order by exam_id) prev_exam from ( select exam_id, time, time - lag(time) over ( order by time) elapsed_time from ( select exam_id, time from "
                + sql_view
                + " inner join period on "
                + sql_view
                + ".period_id = period.id) T order by time asc) T ) T where elapsed_time between '60 MINUTES' and '90 MINUTES') as exams inner join exam_student on exams.exam_id = exam_student.exam_id and exam_student.exam_id = exams.prev_exam"
            )
            studentCount = connection.execute(sql_query).fetchone()[0]
            runningScore += studentCount * cons.params[0]
        if cons.name == "TWOINADAY":
            sql_query = db.text(
                "select Count(student_id) as studentCount from ( select prev_exam, time, elapsed_time, exam_id from ( select time, elapsed_time, exam_id, lag(exam_id) over ( order by exam_id) prev_exam from ( select exam_id, time, time - lag(time) over ( order by time) elapsed_time from ( select exam_id, time from "
                + sql_view
                + " inner join period on "
                + sql_view
                + ".period_id = period.id) T order by time asc) T ) T where elapsed_time between '1 DAYS' and '2 DAYS') as exams inner join exam_student on exams.exam_id = exam_student.exam_id and exam_student.exam_id = exams.prev_exam"
            )
            studentCount = connection.execute(sql_query).first()[0]
            runningScore += studentCount * cons.params[0]
        if cons.name == "NOMIXEDDURATIONS":
            sql_query = db.text(
                "select sum(durations) as totalMixed from (SELECT period_id, count(distinct duration) as durations FROM ( select period_id, exam_id, duration, room_id from ( select "
                + sql_view
                + ".exam_id, "
                + sql_view
                + ".room_id, period_id from "
                + sql_view
                + " inner join exam_room on "
                + sql_view
                + ".exam_id = exam_room.exam_id order by period_id) as examrooms inner join exam on examrooms.exam_id = exam.id) T GROUP BY period_id HAVING COUNT(DISTINCT duration) > 1) T"
            )
            mixedCount = connection.execute(sql_query).fetchone()[0]
            runningScore += mixedCount * cons.params[0]

    return runningScore


def main():
    print("hello world")
    # --------------SAMPLE DATASETS----------------------------------
    test = "test.exam"
    sample_one_early = "./itc2007_dataset/exam_comp_set4.exam"  # done
    sample_two_early = "./itc2007_dataset/exam_comp_set1.exam"

    sample_one_late = "./itc2007_dataset/exam_comp_set6.exam"  # done
    sample_two_late = "./itc2007_dataset/exam_comp_set8.exam"  # done

    sample_one_hidden = "./itc2007_dataset/exam_comp_set9.exam"  # done
    sample_two_hidden = "./itc2007_dataset/exam_comp_set12.exam"  # done

    sample = sample_two_late

    # --------------DATATBASE CONNECTION----------------------------------
    engine = db.create_engine("postgresql://postgres:password@localhost:5432/postgres")
    connection = engine.connect()
    meta = db.MetaData(connection)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()

    print("hey")

    # --------------READ SAMPLE INTO DATABASE----------------------------------
    roomRows = []
    examRows = []
    periodRows = []
    studentRows = []
    constraints = []
    softconstraints = []

    Period, Room, Student, Exam = createModels(Base, engine)

    readRoomsFromFile(sample, roomRows, session, Room)

    readFile(
        sample,
        examRows,
        periodRows,
        roomRows,
        studentRows,
        constraints,
        softconstraints,
        Period,
        session,
        Exam,
        Student,
    )

    # --------------GENERATE STATIC HEURISTICS----------------------------------
    generateStatisHeurisitcs(connection)

    # --------------CREATE INITIAL SOLUTION----------------------------------

    createSolution("tempSolution", connection, examRows, session, periodRows)

    # --------------RUN GREEDY HILLCLIMBING FOR INTERATIONS----------------------------------

    GreedyHillClimbing(
        10,
        softconstraints,
        connection,
        sample,
        constraints,
        examRows,
        session,
        periodRows,
    )


if __name__ == "__main__":
    main()

