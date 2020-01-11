from os import getcwd, listdir
from os.path import join
from random import choice, uniform
from copy import deepcopy

# GLOBALS
course = None
lessons = None
rate_of_change_question = 2.0

def main():
    while True:
        order = input("Command: ")
        if order == "exit":
            save_lessons()
            quit()
        elif order == "courses":
            courses_list()
        elif order[:4] == "set ":
            set_course(order[4:])
        elif order == "course":
            print_current_course()
        elif order == "lessons":
            lessons_list()
        elif order == "study":
            study()
        elif order == "help":
            print_help()
        else:
            print("Invalid command, use 'help' to see a list of possible commands")

def print_help():
    print("'exit': closes the program")
    print("'courses': displays a list of possible courses")
    print("'set <course name>': make <course name> the default course")
    print("'course': display the current course")
    print("'lessons': display a list of possible lessons and their relative frequencies")
    print("'study': begin the study process")
    print("'help': print a list of available commands")

def study():
    global course
    global lessons
    global rate_of_change
    if course is None:
        print("You have not chosen a course to study.")
        how_to_choose_course()
        return
    lessons = get_lessons(course)
    while True:
        order = input("Press Enter to continue, anything else to stop lesson: ")
        if order != "":
            save_lessons()
            return
        lesson = choose_lesson(lessons)
        questions, question = get_question(course, lesson)
        print("Asking about " + str(question['question']))
        input("Ready for answer?")
        print("The correct answer is: ")
        print_answer(question["answer"])
        correct = input("Correct? (y/n)")
        for i in range(len(questions)):
            if questions[i]['id'] == question['id']:
                if correct == "y":
                    questions[i]['chance'] /= rate_of_change_question
                    lessons[lesson] = get_average_chance_of_questions(questions)
                elif correct == "n":
                    questions[i]['chance'] *= rate_of_change_question
                    lessons[lesson] = get_average_chance_of_questions(questions)
                else:
                    print("Unable to interpret feedback, not modifying frequencies.")
                break
        save_chances(questions, lesson)

def get_average_chance_of_questions(questions):
    total = 0
    count = len(questions)
    for question in questions:
        total += question["chance"]
    return total / count

def print_answer(answer_list):
    for answer in answer_list:
        print(answer)

def get_question(course, lesson):
    questions = get_questions(course, lesson)
    questions = make_question_dict_list(questions)
    questions = add_chances(questions, lesson)
    return questions, choice(questions)

def add_chances(questions, lesson):
    chances = get_chances_from_file(lesson)
    new_questions = []
    for question in questions:
        if question['id'] in chances.keys():
            chance = chances[question['id']]
        else:
            chance = 1.0
        new_questions.append({'id': question['id'], 'question': question['question'], 'answer': question['answer'], 'chance': chance})
    return new_questions

def save_chances(questions, lesson):
    global course
    base_path = getcwd()
    folder_path = join(base_path, course)
    lesson_meta = get_lesson_meta_name(lesson)
    file_name = join(folder_path, lesson_meta)
    file = open(file_name, "w")
    for question in questions:
        file.write(str(question['id']) + ":" + str(question['chance']) + "\n")
    file.close()

def get_chances_from_file(lesson):
    global course
    base_path = getcwd()
    folder_path = join(base_path, course)
    lesson_meta = get_lesson_meta_name(lesson)
    file_name = join(folder_path, lesson_meta)
    try:
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        lines = []
    chances = {}
    for line in lines:
        chances[int(line.split(":")[0])] = float(line.split(":")[1])
    return chances

def get_lesson_meta_name(lesson):
    parts = lesson.split(".")
    return parts[0] + "meta." + parts[1]

def make_question_dict_list(questions):
    return_list = [{}]
    for question in questions:
        if question == "":
            return_list.append({})
        elif len(question) < 3:
            if "answer" not in return_list[-1].keys():
                return_list[-1]["answer"] = []
            return_list[-1]["answer"].append(question)
        elif question[2] == ":" and question[:2].isdigit():
            return_list[-1]["id"] = int(question[:2])
            return_list[-1]["question"] = question.split(": ")[1]
        elif question[1] == ":" and question[:1].isdigit():
            return_list[-1]["id"] = int(question[:1])
            return_list[-1]["question"] = question.split(": ")[1]
        else:
            if "answer" not in return_list[-1].keys():
                return_list[-1]["answer"] = []
            return_list[-1]["answer"].append(question)
    while {} in return_list:
        return_list.remove({})
    return return_list

def get_questions(course, lesson):
    base_path = getcwd()
    folder_path = join(base_path, course)
    file = join(folder_path, lesson)
    file = open(file, "r")
    data = file.read()
    file.close()
    return data.split("\n")

def choose_lesson(lessons):
    total = sum(lessons.values())
    choice = uniform(0.0, total)
    for lesson, frequency in lessons.items():
        if choice < frequency:
            return lesson
        choice -= frequency

def lessons_list():
    global course
    global lessons
    if course is None:
        print("Lessons can not be displayed because you have not chosen a course.")
        how_to_choose_course()
        return
    lessons = get_lessons(course)
    print_lessons_list(lessons)

def get_lessons(course_name):
    base_path = getcwd()
    folder_path = join(base_path, course_name)
    lessons = listdir(folder_path)
    file_exists = "meta.txt" in lessons
    lessons = [l for l in lessons if l[0] != "."]
    lessons = [l for l in lessons if l.split(".")[0][-4:] != "meta"]
    lessons = get_lesson_chances(folder_path, lessons, file_exists)
    return lessons

def get_lesson_chances(folder, lesson_list, file_exists):
    old_dict = {}
    if file_exists:
        file = open(join(folder, "meta.txt"), "r")
        for line in file.readlines():
            split_line = line.split(":")
            old_dict[split_line[0]] = float(split_line[1])
    for lesson in lesson_list:
        if lesson not in old_dict.keys():
            old_dict[lesson] = 1.0
    return old_dict

def print_current_course():
    global course
    if course is None:
        print("No course selected.")
        how_to_choose_course()
    else:
        print("Current course is: " + course)

def save_lessons():
    global course
    global lessons
    if not course or not lessons:
        return
    base_path = getcwd()
    folder_path = join(base_path, course)
    file_path = join(folder_path, "meta.txt")
    file = open(file_path, "w")
    for lesson, frequency in lessons.items():
        file.write(lesson + ":" + str(frequency) + "\n")
    file.close()

def set_course(course_name):
    global course
    if course is not None:
        save_lessons()
    course = course_name

def courses_list():
    courses = get_courses_list()
    print_courses_list(courses)

def get_courses_list():
    path = getcwd()
    everything = listdir(path)
    everything.remove("main.py")
    everything = [course for course in everything if course[0] != "."]
    return everything

def print_courses_list(courses):
    for course in courses:
        print(course)

def print_lessons_list(lessons):
    for lesson, frequency in lessons.items():
        print(lesson.strip(".txt") + ": " + str(frequency))

def how_to_choose_course():
    print("Use 'set <course name' to select a course.")

if __name__ == '__main__':
    main()
