import streamlit as st
from utils.model_loader import load_model, load_stats
from utils.prediction import predict_
from utils.form_inputs import get_user_input
from view.background import set_background_color, show_gif

st.set_page_config(page_title="Прогноз дощу в Австралії", page_icon="\U0001F327\ufe0f")
show_gif("assets//sun-and-cloud.gif", width=300, height=200)
st.title("Прогноз дощу на завтра")
model_dict = load_model()
feature_limits = load_stats()

model = model_dict['model']
encoder = model_dict['encoder']
categorical_cols = model_dict['categorical_cols']


def get_categories_for(col_name: str) -> list[str]:
    return encoder.categories_[categorical_cols.index(col_name)].tolist()


available_locations = get_categories_for("Location")
gust_directions = get_categories_for("WindGustDir")
wind_dir_9am_options = get_categories_for("WindDir9am")
wind_dir_3pm_options = get_categories_for("WindDir3pm")
rain_today_options = get_categories_for("RainToday")

user_input = get_user_input(
    available_locations,
    gust_directions,
    wind_dir_9am_options,
    wind_dir_3pm_options,
    rain_today_options,
    feature_limits
)

if user_input:
    input_dict = user_input.to_dict()
    prediction, probability = predict_(input_dict, model_dict)

    if prediction == "Yes":
        set_background_color("#cde2f2")
        show_gif("assets/rain.gif")
    else:
        set_background_color("#fff8dc")
        show_gif("assets/sun.gif")

    st.subheader("Результат прогнозу")
    st.markdown(f"**Чи буде дощ завтра?** — **{prediction}**")
    st.markdown(f"**Ймовірність:** {probability:.2%}")
