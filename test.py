# list = ['철수', '영희', '민희']

# def printList(list) : 
#     for index,name in enumerate(list):
#         print('list의 '+str(index+1)+'번째 이름 : ' + name)

# print('list의 길이 = ' + str(len(list)));
# printList(list);


dict_arr = [];
dict_prac = {'name': 'Alice', 'age': 25, 'city': 'Seoul'};

dict_arr.append(dict_prac);

def adddict(name,age,city):
    dict_ele = {'name' : name, 'age' : age, 'city' : city};
    dict_arr.append(dict_ele);

adddict('이재훈',31,'서울');

def printDict(dict_ele) :
    for  key, value in dict_ele.items():
        if key != "age":
            print(f"{key} : {value}")
        else:
            print('나이는 26세 이상인가? ' + str(value >= 26))
       
    
def printArr(dict_arr) :
    print('dict_arr 의 총 길이 : ' + str(len(dict_arr)));
    for index, ele in enumerate(dict_arr):
        print('dict_arr 의' + str(index+1)+'번쨰 요소');
        printDict(ele);
        
printArr(dict_arr);