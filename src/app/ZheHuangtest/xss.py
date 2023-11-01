
import re
def test():
    with open('./inputdata.txt','r',encoding='utf-8') as Inputdata:
        with open('./testcase.txt','r',encoding='utf-8') as Testcase:
            Inputdatalines=Inputdata.readlines()
            Testcaselines=Testcase.readlines()
            for index in range(len(Inputdatalines)):
                assert xssdefender(Inputdatalines[index])==Testcaselines[index], f'In {index}th line, error occurs.'
                print(f"test{index} pass")
            print("--------------All test Pass")

def xssdefender(inputdata):
    text=re.sub(pattern='&',repl="&amp;",string=inputdata)
    text=re.sub(pattern='<',repl="&lt;",string=text)
    text=re.sub(pattern='>',repl="&gt;",string=text)
    text=re.sub(pattern='\/',repl="&#x2F;",string=text)
    text=re.sub(pattern='"',repl="&quot;",string=text)
    text=re.sub(pattern='\'',repl="&#x27;",string=text)
    return text

test()
