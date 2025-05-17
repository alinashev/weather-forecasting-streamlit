import streamlit as st

from models.fearures import FIELD_LABELS
from models.input_data import WeatherInput
from models.limits import HARD_LIMITS
from view.background import set_background_color, show_gif


def _number_input(label, feature_name, feature_limits, default=0.0, format_str="%.1f", step=1.0):
    return st.number_input(
        label,
        value=feature_limits.get(feature_name, {}).get("mean", default),
        format=format_str,
        step=step,
        key=feature_name
    )


def _selectbox_input(label, options):
    return st.selectbox(label, options=options)


def _validate_numeric_inputs(values: dict, feature_limits: dict) -> bool:
    for feature_name, value in values.items():
        if feature_name in HARD_LIMITS:
            min_val = HARD_LIMITS[feature_name]["min"]
            max_val = HARD_LIMITS[feature_name]["max"]
        elif feature_name in feature_limits:
            min_val = feature_limits[feature_name]["min"]
            max_val = feature_limits[feature_name]["max"]
        else:
            continue

        if not (min_val <= value <= max_val):
            label = FIELD_LABELS.get(feature_name, feature_name)
            st.error(
                f"Значення поля **{label}** {value} виходить за межі допустимого діапазону: [{min_val}, {max_val}]."
            )
            return False
    return True


def get_user_input(
        available_locations: list[str],
        gust_directions: list[str],
        wind_dir_9am_options: list[str],
        wind_dir_3pm_options: list[str],
        rain_today_options: list[str],
        feature_limits: dict
) -> WeatherInput | None:
    st.markdown("### Введіть погодні дані для прогнозу")

    with st.form("weather_form"):
        with st.expander("Загальна інформація", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Дата")
            with col2:
                location = _selectbox_input("Локація", available_locations)

            rain_today = _selectbox_input("Чи був дощ сьогодні?", rain_today_options)

        with st.expander("Температурні показники"):
            col1, col2 = st.columns(2)
            with col1:
                min_temp = _number_input(FIELD_LABELS["MinTemp"], "MinTemp", feature_limits, 15.0)
                temp_9am = _number_input(FIELD_LABELS["Temp9am"], "Temp9am", feature_limits, 18.0)
            with col2:
                max_temp = _number_input(FIELD_LABELS["MaxTemp"], "MaxTemp", feature_limits, 25.0)
                temp_3pm = _number_input(FIELD_LABELS["Temp3pm"], "Temp3pm", feature_limits, 24.0)

        with st.expander("Вологість, хмарність та сонце"):
            col1, col2 = st.columns(2)
            with col1:
                humidity_9am = _number_input(FIELD_LABELS["Humidity9am"], "Humidity9am", feature_limits, 70.0, "%.0f")
                cloud_9am = _number_input(FIELD_LABELS["Cloud9am"], "Cloud9am", feature_limits, 4.0, "%.0f")
            with col2:
                humidity_3pm = _number_input(FIELD_LABELS["Humidity3pm"], "Humidity3pm", feature_limits, 50.0, "%.0f")
                cloud_3pm = _number_input(FIELD_LABELS["Cloud3pm"], "Cloud3pm", feature_limits, 4.0, "%.0f")

            sunshine = _number_input(FIELD_LABELS["Sunshine"], "Sunshine", feature_limits, 7.0)

        with st.expander("Тиск"):
            col1, col2 = st.columns(2)
            with col1:
                pressure_9am = _number_input(FIELD_LABELS["Pressure9am"], "Pressure9am", feature_limits, 1010.0)
            with col2:
                pressure_3pm = _number_input(FIELD_LABELS["Pressure3pm"], "Pressure3pm", feature_limits, 1005.0)

        with st.expander("Вітер"):
            col1, col2 = st.columns(2)
            with col1:
                wind_gust_dir = _selectbox_input("Напрямок пориву вітру", gust_directions)
                wind_dir_9am = _selectbox_input("Напрямок вітру о 9 ранку", wind_dir_9am_options)
                wind_speed_9am = _number_input(FIELD_LABELS["WindSpeed9am"], "WindSpeed9am", feature_limits, 10.0)
            with col2:
                wind_gust_speed = _number_input(FIELD_LABELS["WindGustSpeed"], "WindGustSpeed", feature_limits, 35.0)
                wind_dir_3pm = _selectbox_input("Напрямок вітру о 3 дня", wind_dir_3pm_options)
                wind_speed_3pm = _number_input(FIELD_LABELS["WindSpeed3pm"], "WindSpeed3pm", feature_limits, 20.0)

        with st.expander("Опади та випаровування"):
            col1, col2 = st.columns(2)
            with col1:
                rainfall = _number_input(FIELD_LABELS["Rainfall"], "Rainfall", feature_limits, 0.0)
            with col2:
                evaporation = _number_input(FIELD_LABELS["Evaporation"], "Evaporation", feature_limits, 4.0)

        submitted = st.form_submit_button("Прогнозувати")

    if submitted:
        values_to_validate = {
            "MinTemp": min_temp,
            "MaxTemp": max_temp,
            "Temp9am": temp_9am,
            "Temp3pm": temp_3pm,
            "Humidity9am": humidity_9am,
            "Humidity3pm": humidity_3pm,
            "Cloud9am": cloud_9am,
            "Cloud3pm": cloud_3pm,
            "Sunshine": sunshine,
            "Pressure9am": pressure_9am,
            "Pressure3pm": pressure_3pm,
            "Rainfall": rainfall,
            "Evaporation": evaporation,
            "WindGustSpeed": wind_gust_speed,
            "WindSpeed9am": wind_speed_9am,
            "WindSpeed3pm": wind_speed_3pm
        }

        if not _validate_numeric_inputs(values_to_validate, feature_limits):
            set_background_color("#ffe6e6")
            show_gif("assets/cat.gif")
            return None

        return WeatherInput(
            Date=str(date),
            Location=location,
            MinTemp=min_temp,
            MaxTemp=max_temp,
            Rainfall=rainfall,
            Evaporation=evaporation,
            Sunshine=sunshine,
            WindGustDir=wind_gust_dir,
            WindGustSpeed=wind_gust_speed,
            WindDir9am=wind_dir_9am,
            WindDir3pm=wind_dir_3pm,
            WindSpeed9am=wind_speed_9am,
            WindSpeed3pm=wind_speed_3pm,
            Humidity9am=humidity_9am,
            Humidity3pm=humidity_3pm,
            Pressure9am=pressure_9am,
            Pressure3pm=pressure_3pm,
            Cloud9am=cloud_9am,
            Cloud3pm=cloud_3pm,
            Temp9am=temp_9am,
            Temp3pm=temp_3pm,
            RainToday=rain_today
        )

    return None
