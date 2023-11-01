import sys
import pytest
sys.path.append("..")
from database.db import connect_to_database, execute_query, insert_user_into_db,fetch_hashed_password,getValidationCode,alterValidationState,isAccountVerified

def test():
    assert True==insert_user_into_db(2, 2, 2, 2, 2)
    assert "$2b$12$xqOaRzZ3oOT.NRXaLeaqreml0Td8EbmvHJrBWSVMJw80SP4klDMEy"==fetch_hashed_password('1538773813@qq.com')
    assert isAccountVerified('1538773813@qq.com')[0]==1
    assert isAccountVerified('tstorm1538@gmail.com')[0]==0
    assert getValidationCode('1538773813@qq.com')[0]=='S391Mz'
    print("Pass")

if __name__ == '__main__':
    test()
    

        
        

