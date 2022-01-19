from canvasapi import Canvas
from datetime import date
import logging, os, platform, subprocess
from getAnswer import get_ans_int,get_ans_array, get_ans_str

def clear():
#Clears the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    return ''
def init():
    #Connects to Canvas account and gets user id
    #Checks if user info saved
    if os.path.exists('Canvas_login_init.txt')==0 or os.path.getsize('Canvas_login_init.txt')==0:
    #If not saved get and save user info
        API_URL=get_ans_str("Canvas API URL: ")
        API_KEY=get_ans_str("Canvas API STR: ")
        with open('Canvas_login_init.txt','w') as info:
            info.writelines([f'{API_URL}\n',f'{API_KEY}'])
    #If saved get user info from file
    else:
        with open('Canvas_login_init.txt','r') as info:
            Lines=info.readlines()
            for count,line in enumerate(Lines):
                if count==0:
                    API_URL=line.strip()
                elif count==1:
                    API_KEY=line.strip()
    #Connect to Canvas
    canvas=Canvas(API_URL,API_KEY)
    user=canvas.get_current_user()
    course_list=get_active_courses(user,canvas)
    main(user,canvas,course_list)
def main(user,canvas,course_list):
    #Gives user options
    print("Options\n---------------------------\n1. Get Members of Class\n2. Get Assignments\n3. Get User Logins\n4. Get Grades\n5. Quit the Program\n")
    choice=get_ans_int('Enter your choice: ',[1,5])
    if choice==1:
        clear()
        user_type=get_ans_array("Type of User(s)",['student','teacher','ta','designer'])
        get_users(course_list,user_type,canvas)
    elif choice==2:
        clear()
        get_assignments(course_list)
    elif choice==3:
        clear()
        get_usernames(user)
    elif choice==4:
        clear()
        get_grade(canvas,user)
    elif choice==5:
        raise SystemExit
    main(user,canvas,course_list)
    return None
def get_active_courses(user,canvas):
    #Gets courses student is actively enrolled in
    course_list=[]
    courses=user.get_courses(enrollment_state='active')
    for course in courses:
            course_list.append(canvas.get_course(course))
    return course_list
def get_all_courses(user,canvas):
    #Gets every course student has been enrolled in
    #course list
    course_list=[]
    courses=user.get_courses()
    for count,course in enumerate(courses):
        if hasattr(course,'course_code'):
            course_list.append(canvas.get_course(course))
        else:
            logging.info(f'Course {count+1} does not have a course code')
    return course_list
def get_usernames(user):
    #Prints usernames user has used
    logins=user.get_user_logins()
    for login in logins:
        print(login)
    return None
def get_users(course_list,level,canvas):
    #Gets the members of a class by type of member
    #Removes classes that don't allow user to access members
    clear()
    no_access=[]
    for course in course_list:
        users = course.get_users(enrollment_type=level,include=['email'])
        try:
            users[0]
        except Exception as e:
            print(f'Course {course} doesn\'t allow user to access members of the class')
            no_access.append(course)
            logging.info(e)
    for course in no_access:
        if course in course_list:
            course_list.remove(course)
    #Get courses user wants to know students from
    clear()
    print("Courses:")
    for count,course in enumerate(course_list):
        print(f'{count+1}: {course}' )
    courses=get_ans_array('Courses interested in',list(range(1,len(course_list)+1)))
    #parameters:enrollment_type[],include[],user_ids[],entrollment_state[]
    #users = course.get_users(enrollment_type=level,include=['email'])
    #Print users
    clear()
    for course in courses:
        course=course_list[int(course)-1]
        users=course.get_users(enrollment_type=level)
        print(f'{course}\n---------------------------')
        for user in users:
            print(user)
        print('')
    return None
def get_assignments(course_list):
    #Gets the assignemnts in x courses for x days
    #User selects courses
    print("Courses:")
    for count,course in enumerate(course_list):
        print(f'{count+1}: {course}' )
    courses=get_ans_array('Courses interested in',list(range(1,len(course_list)+1)))
    #Get amount of days user wants to know assignemtns for
    day=date.today()
    print(day)
    limit=get_ans_int('How many days do you want to see assignments for?\n')+1
    #Prints assignments
    for course in courses:
        hasWork=True
        course=course_list[int(course)-1]
        try:
            course.get_assignments()
        except:
            print("No assignments in this class")
            hasWork=False
        if hasWork==True:
            for hw in course.get_assignments():
                dueDate=str(hw.due_at)
                if dueDate != "None":
                    dueDate="{}-{}-{}".format(dueDate[0:4],dueDate[5:7],dueDate[8:10])
                    dueDate=date.fromisoformat(dueDate)
                    timedelta=dueDate-day
                    timedelta=timedelta.days-1
                    if -1<timedelta<limit:
                        print(course.name)
                        print(hw.name)
                        print("Due in {} days".format(timedelta))
    return None
def get_grade(canvas,user):
    #Gets user's grade in every course
    #Gets the calsses user is currently enrolled in 
    enrollments=user.get_enrollments()
    #Prints grades or no current grade if none found
    for course in enrollments:
        try:
            print(f'{canvas.get_course(course.course_id).name}: {course.current_grade}')
        except:
            print("No current grade")
    return None
init()