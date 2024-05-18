
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# from peft import PeftModel

import pandas as pd

def load_manual_csv(file_path="appstore_review\simsimireviewsAnswer.csv"):
    """
    답변 매뉴얼을 CSV 형식으로 로드하고 인덱스를 생성.

    Args:
        file_path (str): 답변 매뉴얼 파일 경로. (inputs, response 컬럼 필요)

    Returns:
        dict: 인덱스를 키로 하고 response를 값으로 갖는 딕셔너리.
        str: 답변 매뉴얼을 텍스트로 반환.
    """
    # CSV 파일 읽기
    df = pd.read_csv(file_path)

    # 인덱스 번호를 생성
    df = df.reset_index()

    # 답변 매뉴얼을 딕셔너리로 변환 (index: response)
    manual_dict = dict(zip(df["index"].astype(str), df["response"]))

    # 답변 매뉴얼을 문자열로 변환 (프롬프트에 사용)
    manual_text = "\n".join([f"{row['index']}: {row['inputs']}" for _, row in df.iterrows()])

    return manual_dict, manual_text


# base_model = AutoModelForCausalLM.from_pretrained("beomi/Llama-3-Open-Ko-8B")
# model = PeftModel.from_pretrained(base_model, "LeeDuho/llama3_simsimi")

# # 텍스트 생성 파이프라인 초기화
# generator = pipeline("text-generation", model=model, tokenizer=model.tokenizer)



# def generate_responses(review_body):
#     """
#     LLaMA3 모델을 사용해 주어진 리뷰 내용에 대한 응답을 생성.

#     Args:
#         review_body (str): 리뷰 본문 텍스트.

#     Returns:
#         list: 생성된 응답 목록 (3개의 응답)
#     """
#     try:
#         # 답변 매뉴얼 로드
#         manual_dict, manual_text = load_manual_csv(manual_path)

#         prompt = (
#             f"회사의 답변 매뉴얼을 보고서 문장과 가장 의미가 비슷한 문장의 번호를 3개 알려줘. "
#             f"다른 문자는 작성하지 말고 가장 의미가 비슷한 문장 3개의 번호만 작성해줘. "
#             f"{review_body} 다음은 답변 매뉴얼이야. {manual_text}"
#         )
        
#         # LLaMA 모델 호출
#         response = generator(prompt, max_length=50, num_return_sequences=1)[0]["generated_text"]

#         # 생성된 텍스트에서 숫자만 추출
#         numbers = [int(num) for num in response.split(",") if num.strip().isdigit()]

#         # 번호로 답변 찾기
#         answers = [manual_dict[str(num)] for num in numbers if str(num) in manual_dict]

#         return answers

#     except Exception as e:
#         # 오류가 발생할 경우 기본 응답 반환
#         return [
#             # f"Error generating response: {str(e)}",
#             "Error generating response:",
#             "We are glad you shared your feedback. Our team will look into it.",
#             "Please provide more details so we can assist you better."
#         ]



# MODEL_NAME = "meta-llama/Llama-3.2-1B"

# HF_TOKEN 
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME,token=HF_TOKEN)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME,token=HF_TOKEN)
# generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


def generate_responses(review_body):

    return [
        # f"Error generating response: {str(e)}",
        "Error generating response:",
        "We are glad you shared your feedback. Our team will look into it.",
        "Please provide more details so we can assist you better."
    ]
