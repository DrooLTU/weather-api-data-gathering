CREATE VIEW max_min_stddev_temp_current_week AS
SELECT
    c.country,
    c.city,
    MAX(w.temperature) AS max_temperature_current_week,
    MIN(w.temperature) AS min_temperature_current_week,
    STDDEV(w.temperature) AS stddev_temperature_current_week
FROM
    weather_api.weather_data w
JOIN
    weather_api.cities c ON w.city_id = c.id
WHERE
    WEEK(FROM_UNIXTIME(w.datetime)) = WEEK(CURDATE())
GROUP BY
    c.country, c.city;
