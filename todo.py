from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, default="Nothing to do!")
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

list_num = 0
num = 1
weekdays = {"0": "Monday", "1": "Tuesday", "2": "Wednesday",
            "3": "Thursday", "4": "Friday", "5": "Saturday", "6": "Sunday"}


def add_task():
    global list_num
    list_num += 1
    print("Enter task:")
    new_task = input()
    print("Enter deadline (YYYY-MM-DD):")
    new_deadline = input()
    new_row = Table(task=new_task, deadline=datetime.strptime(new_deadline, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    return "The task has been added!\n"


def today_tasks():
    global num
    print(f"Today {datetime.today().day} {datetime.today().strftime('%b')}:")
    if list_num == 0:
        return "Nothing to do!\n"
    else:
        today_rows = session.query(Table).filter(Table.deadline == datetime.today().date()).all()
        for item in today_rows:
            print(f"{num}. {item.task}")
            num += 1
        num = 1
        return "\n"


def week_tasks():
    global num
    week_rows = session.query(Table).all()
    day_of_week = 0
    while day_of_week < 7:
        today = datetime.today().date() + timedelta(days=day_of_week)
        weekday = str(today.weekday())
        day = today.day
        month = today.strftime('%b')
        print(f"{weekdays[weekday]} {day} {month}:")
        for row in week_rows:
            if row.deadline == today:
                print(f"{num}. {row.task}")
                num += 1
        num = 1
        if not session.query(Table).filter(Table.deadline == today).all():
            print("Nothing to do!")
        print()
        day_of_week += 1


def all_tasks():
    global num
    all_rows = session.query(Table).order_by(Table.deadline)
    for row in all_rows:
        print(f"{num}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        num += 1
    num = 1
    return "\n"


def missed_tasks():
    global num
    print("Missed tasks:")
    missed = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    if not missed:
        print("Nothing is missed!")
    else:
        print(missed)
        for row in missed:
            print(f"{num}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
            num += 1
        num = 1
    return "\n"


def delete_task():
    global num
    print("Chose the number of the task you want to delete:")
    all_rows = session.query(Table).order_by(Table.deadline)
    for row in all_rows:
        print(f"{num}. {row.task}. {row.deadline.day} {row.deadline.strftime('%b')}")
        num += 1
    num = 1
    delete_row = int(input())
    session.delete(all_rows[delete_row - 1])
    session.commit()
    print("The task has been deleted!")
    return "\n"


while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    choice = int(input())
    if choice == 0:
        print("\nBye!")
        break
    elif choice == 1:
        print(today_tasks())
    elif choice == 2:
        week_tasks()
    elif choice == 3:
        print(all_tasks())
    elif choice == 4:
        print(missed_tasks())
    elif choice == 5:
        print(add_task())
    elif choice == 6:
        print(delete_task())
