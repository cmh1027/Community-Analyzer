# Community_analyzer

## 실행 순서
1. utility/constant.py에서 관련 상수들 수정
2. 각 사이트 크롤러 실행
3. tokenizer.py 실행
4. doc2vec.py 실행
5. data_preprocessor.py 실행
6-1. model.py 실행 (--mode arg : train(default)/test] [--words starting words(Only Evaluation)] [--website website index])
6-2. graph.py : Doc2Vec 그래프 시각화