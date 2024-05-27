from project import *
import json
ClassFieldNames = {
    'Project': {
        'title': 'Name',
        'date': 'Date',
        'id': 'CreatorID',
        'l_u': 'Members',
        'l_t': 'Tasks'
    },
    'Task': {
        'title': 'Name',
        'id': 'ID',
        'date': 'Date',
        'desc': 'Desc',
        'tpr': 'TaskPriority',
        'state' : 'State',
        'l_up': 'Updates',
        'duedate': 'DueDate',
        'member_config': 'Member_Perms'
    },
    'Update': {
        'title': 'Title',
        'date': 'Date',
        'txt': 'Content',
        'u_writer': 'CreatorID',
        'l_notes': 'Notes',
        'l_comments': 'Comments'
    },
    'Comment': {
        'title': 'Title',
        'date': 'Date',
        'u_writer': 'CreatorID',
        'txt': 'Content'
    },
    'User': {
        'username': 'Username',
        'id': 'UserID',
        'rank': 'Rank'
    }
}

def deserialize_dict_user(u1):
    #stub
    return u1

def deserialize_user_list(l1):
    l_result = []
    for d_u in l1:
        l_result.append(deserialize_dict_user(d_u))
    return l_result

def deserialize_dict_comment(c1):
    try:
        keywords = ClassFieldNames['Comment']
        title = c1[keywords['title']]
        date =  c1[keywords['date']]
        txt = c1[keywords['txt']]
        u_writer = deserialize_dict_user(c1[keywords['u_writer']])
    except:
        raise ValueError(f'comment deserialization failed: \n    {c1}')
    return Comment(title, date, u_writer.ID, txt)

def deserialize_comment_list(l1):
    l_result = []
    for d_c in l1:
        l_result.append(deserialize_dict_comment(d_c))
    return l_result

def deserialize_dict_update(up1):
    try:
        keywords = ClassFieldNames['Update']
        title = up1[keywords['title']]
        date =  up1[keywords['date']]
        txt = up1[keywords['txt']]
        u_writer = deserialize_dict_user(up1[keywords['u_writer']])
        l_notes = up1[keywords['l_notes']]
        l_comments = deserialize_comment_list(up1[keywords['l_comments']])
    except ZeroDivisionError:
        raise ValueError(f'update deserialization failed: \n    {up1}')
    return Update(title, date, txt, u_writer.ID, l_notes, l_comments)

def deserialize_update_list(l1):
    l_result = []
    for d_u in l1:
        l_result.append(deserialize_dict_update(d_u))
    return l_result

def deserialize_dict_task(t1):
    try:
        keywords = ClassFieldNames['Task']
        title = t1[keywords['title']]
        date =  t1[keywords['date']]
        id = t1[keywords['id']]
        desc = t1[keywords['desc']]
        tpr = t1[keywords['tpr']]
        l_up = deserialize_update_list(t1[keywords['l_up']])
        duedate = t1[keywords['duedate']]
        state = t1[keywords['state']]
        member_config = t1[keywords['member_config']]
    except:
        raise ValueError(f'Task deserialization failed: \n    {t1}')
    return Task(title, date, id, desc, duedate, member_config, tpr, l_up, state)

def deserialize_task_list(l1):
    l_result = []
    for d_t in l1:
        l_result.append(deserialize_dict_task(d_t))
    return l_result

def deserialize_dict_project(p1):
    try:
        keywords = ClassFieldNames['Project']
        title = p1[keywords['title']]
        date =  p1[keywords['date']]
        creator_id = p1[keywords['id']]
        l_u = deserialize_user_list(p1[keywords['l_u']])
        l_t = deserialize_task_list(p1[keywords['l_t']])
    except ZeroDivisionError:
        raise ValueError(f'project deserialization failed: \n    {p1}')
    return Project(title, date, creator_id, l_u, l_t)

#dynamic testing
def main():
    with open('test1.json', 'r') as file:
        a = deserialize_dict_project(json.load(file))
    print(json.dumps(a, default = lambda obj: obj.__dict__))

if __name__ == 'main':
    main()