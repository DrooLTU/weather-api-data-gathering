CREATE VIEW max_min_stddev_temp_last_seven_days AS
SELECT
    c.country,
    c.city,
    MAX(w.temperature) AS max_temperature_last_seven_days,
    MIN(w.temperature) AS min_temperature_last_seven_days,
    STDDEV(w.temperature) AS stddev_temperature_last_seven_days
FROM
    weather_api.weather_data w
JOIN
    weather_api.cities c ON w.city_id = c.id
WHERE
    FROM_UNIXTIME(w.datetime) >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY
    c.country, c.city;
