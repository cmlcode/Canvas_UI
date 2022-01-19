def get_ans_str(question,txt_array=None):
    if txt_array is not None:
        txt_array=[str(x) for x in txt_array]
        ans=input(question)
        while ans not in txt_array:
            print(f'Please respond with an answer in {txt_array}')
            ans=input(question)
    else:
        ans=input(question)
    return ans
def get_ans_flt(question,limits=[None,None],error='Please respond with a valid number'):
    ans=''
    while True:
        ans=input(question)
        try:
            ans=float(ans)
        except ValueError as er:
            print(er)
            continue
        if limits is None:
            return ans
        else:
            if not (limits[0]<=ans<=limits[1]):
                print(f"Please enter a value between {limits[0]} and {limits[1]}")
            else:
                return ans
def get_ans_int(question,limits=[None,None],error='Please respond with a valid integer'):
    ans=''
    while True:
        ans=input(question)
        try:
            ans=int(ans)
        except ValueError as er:
            print(er)
            continue
        if limits is (None) or ([None,None]):
            return ans
        else:
            if not (limits[0]<=ans<=limits[1]):
                print(f"Please enter a inter between {limits[0]} and {limits[1]}")
            else:
                return ans
def get_ans_array(question,txt_array,response_limit=-1):
    print(f'{question} out of {txt_array}')
    print("Hit the enter button to finish submitting responses")
    ans_array=[]
    txt_array.append('')
    while True:
        if len(ans_array)==response_limit:
            print("Max answers received")
            return ans_array
        print(f'Answers: {ans_array}')
        ans=get_ans_str('Enter value: ',txt_array)
        if (ans==''):
            print('')
            return ans_array
        ans_array.append(ans)