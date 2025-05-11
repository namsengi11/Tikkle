import pandas as pd
import numpy as np
import pickle
import json
import joblib

# 모델 불러오기

model = joblib.load("models/predict_accident.pkl")
micro_accident_model = joblib.load("models/micro_accident_model.pkl")
le_dict = joblib.load("models/label_encoders.pkl")
feature_cols = ['중업종','대업종','발생형태','규모','성별','연령','근무기간',
                '작업종류','보호구착용','유사사고경험','안전감독자']

def predict_full_risk_assessment(input_json_str: str) -> dict:
    input_json = json.loads(input_json_str)
    result = {}

    # 사고 근로자 정보
    result["basic_information"] = {
        "date": input_json.get("날짜"),
        "name": input_json.get("이름"),
        "factory": input_json.get("발생공장"),
        "image": input_json.get("사진"),
        "description": input_json.get("설명")
    }

    # 산업 재해 발생 가능성 
    rule_score = 0
    if input_json.get("Q10_6_1") == 1:
        rule_score += 1
    if input_json.get("Q3_1_2", 0) >= 30:
        rule_score += 2
    if input_json.get("Q15_8", 0) >= 8:
        rule_score += 1
    if input_json.get("SQ3_1") == 3:
        rule_score += 2
    elif input_json.get("SQ3_1") == 2:
        rule_score += 1
    if input_json.get("Q24_1") == 1:
        rule_score += 1

    risk_level = (
        "High" if rule_score >= 6 else "Medium" if rule_score >= 3 else "Low"
    )
    score_pred = 1 if rule_score >= 6 else 0

    used_features = ["Q10_6_1", "Q3_1_2", "Q15_8", "SQ3_1", "Q24_1"]
    input_data = {k: input_json.get(k, -1) for k in used_features}
    input_df = pd.DataFrame([input_data])

    proba = model.predict_proba(input_df)[0][1]
    ml_pred = 1 if proba >= 0.4 else 0
    hybrid_pred = 1 if score_pred == 1 or ml_pred == 1 else 0

    result["accident_possibility"] = {
        "risk_score": rule_score,
        "risk_level": risk_level,
        "predicted_probability": round(proba, 4),
    }

    # 미세 산재 발생 시 근로자의 피해 계산 로직
    try:
        rec = {c: input_json[c] for c in feature_cols + ['위험정도']}
        df_in = pd.DataFrame([rec])

        for col in feature_cols:
            if col in le_dict:
                val = df_in[col].values[0]
                if val in le_dict[col].classes_:
                    df_in[col] = le_dict[col].transform(df_in[col])
                else:
                    df_in[col] = -1  # unknown 처리

        X_new = df_in[feature_cols + ['위험정도']]
        proba_new = micro_accident_model.predict_proba(X_new)[0]

        if "재해정도" in le_dict:
            classes = le_dict["재해정도"].inverse_transform(np.arange(len(proba_new)))
        else:
            classes = micro_accident_model.classes_

        prob_dict = {cls: float(p) for cls, p in zip(classes, proba_new)}
        most_likely = classes[np.argmax(proba_new)]

        result["micro_accident_severity"] = {
            "probabilities": prob_dict,
            "most_likely_time": most_likely
        }
    except Exception as e:
        result["mirco_accident_severity"] = {
            "error": str(e)
        }
        
    return result

if __name__ == "__main__":
    test_json = json.dumps({
        "날짜":"2025-05-11",
        "이름":"홍길동",
        "발생공장": "A제조공장",
        "사진":"example.jpg",
        "설명": "A제조공장에서 홍길동씨 사고 발생",
        "중업종": "기계기구제조업",
        "대업종": "제조업",
        "발생형태": "감전",
        "규모": "20~29인",
        "성별": "남",
        "연령": "50세~54세",
        "근무기간": "6개월미만",
        "작업종류": "전기작업",
        "보호구착용": "n",
        "유사사고경험": "n",
        "안전감독자": "n",
        "위험정도": 5,
        "Q10_6_1": 1,
        "Q3_1_2": 31,
        "Q15_8": 8,
        "SQ3_1": 3,
        "Q24_1": 1
    })

    print(json.dumps(predict_full_risk_assessment(test_json), indent=2, ensure_ascii=False))