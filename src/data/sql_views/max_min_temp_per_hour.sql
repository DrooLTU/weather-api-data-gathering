CREATE VIEW max_min_temp_per_hour AS
SELECT
    HOUR(FROM_UNIXTIME(w.datetime)) AS hour,
    MAX(w.temperature) AS max_temperature,
    MIN(w.temperature) AS min_temperature,
    (SELECT c.city FROM weather_api.cities c WHERE c.id = (SELECT w1.city_id FROM weather_api.weather_data w1 WHERE w1.temperature = MAX(w.temperature) LIMIT 1)) AS max_temp_city_name,
    (SELECT c.city FROM weather_api.cities c WHERE c.id = (SELECT w2.city_id FROM weather_api.weather_data w2 WHERE w2.temperature = MIN(w.temperature) LIMIT 1)) AS min_temp_city_name
FROM
    weather_api.weather_data w
GROUP BY
    hour;
