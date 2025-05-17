import pandas as pd


def predict_(single_input, model_dict):
    model = model_dict['model']
    imputer = model_dict['imputer']
    scaler = model_dict['scaler']
    encoder = model_dict['encoder']
    numeric_cols = model_dict['numeric_cols']
    categorical_cols = model_dict['categorical_cols']
    encoded_cols = model_dict['encoded_cols']

    input_df = pd.DataFrame([single_input])
    input_df[numeric_cols] = imputer.transform(input_df[numeric_cols])
    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])
    input_df[encoded_cols] = encoder.transform(input_df[categorical_cols])
    X_input = input_df[numeric_cols + encoded_cols]

    pred = model.predict(X_input)[0]
    prob = model.predict_proba(X_input)[0][list(model.classes_).index(pred)]
    return pred, prob
