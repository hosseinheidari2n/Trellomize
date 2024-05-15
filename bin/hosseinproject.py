

class Project:
    def __init__(self):
        self.Id = str(uuid.uuid4()) # Generate a unique identifier
        self.Title = ""
        self.Members = []
        self.Tasks = []
        self.Leader = ""


class Priority(Enum):
    Low = 1
    Medium = 2
    High = 3

class Status(Enum):
    Backlog = 1
    InProgress = 2
    Completed = 3

class Task:
    def __init__(self):
        self.Id = str(uuid.uuid4()) # Generate a unique identifier
        self.Title = ""
        self.Description = ""
        self.StartDate = datetime.datetime.now()
        self.EndDate = datetime.datetime.now() + datetime.timedelta(hours=24)
        self.Assignees = []
        self.Priority = Priority.Low # Default value for priority
        self.Status = Status.Backlog # Default value for status
        self.History = []
        self.Comments = []

if __name__ == "__main__":
    FirstCommandList()
