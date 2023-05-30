from django.shortcuts import render
from .form import *
import os

# Create your views here.
def main (req):
    form = QustionForm(req.POST,req.FILES)
    all_coursec = Stack.objects.all()

    if req.method == "POST":
        file = req.FILES.get("quiz")

        course_name = req.POST.get("course_name")
        course_num = req.POST.get("course_num")
        print(course_name,course_num)
        valid = valid_file(file,course_name,course_num)
        if valid == False:
            return render(req, "Solutions/main.html", {"form": form, "stack": all_coursec, "not_valid": 1})

        else:
            return render(req, "Solutions/main.html", {"form": form, "stack": all_coursec, "form2": 1})





    return render(req,"Solutions/main.html",{"form":form,"stack":all_coursec})


def valid_file(file,course_name,course_num):
    #check ext:
    fileName, fileExtension = os.path.splitext(file.name)
    if fileExtension != ".txt":
        return False

    else:
        read = read_file(file)
        stack = Stack.objects.filter(course_name=course_name,stack_num = course_num)
        stack_len = stack.values("len").get()["len"]
        if len(read) == stack_len:
            valid = rows_to_q_a(read,course_name,course_num)
            print(valid)
            if valid:
             return True
            else:
                return False


def sloved (req):
    file = req.FILES.get("unsloved")
    ext = fileName, fileExtension = os.path.splitext(file.name)
    try:
        course_name = req.POST.get("course_name2")
        course_num = req.POST.get("course_num2")

    except:
        raise Exception("Not good")

    if fileExtension == ".txt":

        file_c = read_unsloved(file)
        dict = real_slove(file_c,course_name,course_num)


    return render(req,"Solutions/answer.html",{"answer_dict":dict})



def real_slove(rows,course_name,course_num):
    row_num = 0
    q_a_dict = {}
    stack = Stack.objects.get(course_name=course_name,stack_num=course_num)
    for q in rows:
        row_num += 1
        for j in range (len(q)):
            if q[j] == "תוכן השאלה":
                check = j+1
                bool = False
                pos_ans = Question.objects.filter (stack = stack,q__contains = q[check])
                if len(pos_ans) == 0:
                    q_a_dict["שאלה:"+str(row_num)] = "No Answer yet"

                elif len(pos_ans) == 1:
                    value = pos_ans.values('a').get()
                    q_a_dict["שאלה:" + str(row_num)] = "$$"+value["a"]+"$$"

                else:
                    if row_num == 1:
                        print(pos_ans)
                    check += 1
                    if row_num == 1:
                        print(q[check][::-1])
                    while check < len(q):
                        pos_ans = Question.objects.filter(stack=stack, q__contains=q[check])
                        if row_num == 1:
                            print(pos_ans)
                        if len(pos_ans) == 0:
                            q_a_dict["שאלה:" + str(row_num)] = "No Answer yet"
                            bool = True
                            break

                        elif len(pos_ans) == 1:
                            value = pos_ans.values('a').get()

                            q_a_dict["שאלה:" + str(row_num)] = "$$" + value["a"] + "$$"

                            bool = True
                            break

                        else:
                            check += 1

                    if bool == False:
                        if len([pos_ans]) > 1:
                                x= (pos_ans[:1].get())
                                q_a_dict["שאלה:" + str(row_num)] = x
                                break


    return q_a_dict

def read_file (file):
    all = []
    que = []
    for row in file.readlines():
        row = row.decode("utf-8")
        row = row.strip()
        if row.isspace():
            continue
        if  "יש לבחור תשובה אחת:" in row:
            continue
        else:
            row = row.strip()
            if row.startswith("שאלה") and len(row) > 7:
                que.append(row)

            elif row.startswith("שאלה") != True :
                if row != "." and row != "" and row != ",":
                    que.append(row)

            else:
                if que != []:
                    all.append(que)

                que = [row]

    all.append(que)

    return all

def read_unsloved (file):
    all = []
    q = []
    for row in file.readlines():
        row = row.decode("utf-8")
        row = row.strip()
        if len(q) == 0:
            q.append(row)

        elif row.startswith("שאלה") and q!= [] and len(row) <=7:
            all.append(q)
            q = [row]

        else:
            if row != "." and row != "" and row != ",":
                q.append(row)

    all.append(q)
    return all

def rows_to_q_a (rows_lst,course_name,course_num):
    x =0
    for q in rows_lst:
        x+= 1
        for j in range(len(q)):

            if q[j] == "תוכן השאלה":
                find_finish = False
                bool = False
                tochen = j+1
                check = j + 1
                string_to_check = q[check]
                try_que = Question.objects.filter(q__contains=string_to_check)
                if len(try_que) == 0:
                    bool = True
                    start = check

                else:
                    check +=1
                try:
                    while q[check] != "תשובה נכונה אפשרית:" and q[check] !=  "התשובה הנכונה:" and q[check] != "התשובות הנכונות הן:":
                        string_to_check = q[check]
                        if  len(Question.objects.filter(q__contains=string_to_check)) == 0:
                            bool = True
                            start = check
                            break

                        else:
                            check+=1

                except:
                    bool = False



           # get answer
            if q[j].startswith("תשובה נכונה אפשרית:")  or q[j].startswith("התשובה הנכונה:") or  q[j].startswith("התשובות הנכונות הן:"):

                find_finish = True
                finish = j+1
                if j == len(q) - 1:
                    a = q[j].split(":")[1]

                else:
                    a = "".join(q[j + 1::])





        if find_finish == False:
            return False

        if bool and find_finish:
            que = "".join(q[tochen:finish+1])
            x+=1


            stack = Stack.objects.get(course_name= course_name,stack_num=course_num)
            new_que = Question(stack =stack,q=que,a=a)
            new_que.save()




    return True























