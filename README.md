# fmpchat_dialogflow
fmpchat_dialogflow
1) 환경변수 추가하기
export export GOOGLE_APPLICATION_CREDENTIALS="/home/yoeri/ydir/fmpchat-udbn-6fb390582ddb.json"

2) python fmpchat.py 실행

* fmpchat.py 설명
chatTest() 함수에서 input 함에 넣은 질문에 대한 답을 받기 위해
detect_intent_texts() 를 부름.
이때, 인자값은 (프로젝트 이름, 세션ID, 사용자가 질문한 input, 유니코드)임.
detect_intent_texts('fmpchat-udbn', '123456789', unicode_content, 'ko-kr')
여기서 unicode_content에 질문만 바꿔서 물어본다고 생각하면 됨.

오빠는 여기서 detect_intent_texts만 사용하면 됨!!!!!!!!!!!!

detect_intent_texts 의 return 값은
오라클 에러 났어 - Request
오류난 에러코드가 무엇인가요? - Response (return)

입니다!!

다른 거는 몰라도 쓰는데 문제 되지 않눈다~~!!
