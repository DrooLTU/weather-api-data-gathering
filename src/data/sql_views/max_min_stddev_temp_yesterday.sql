CREATE VIEW max_min_stddev_temp_yesterday AS
SELECT
    c.country,
    c.city,
    MAX(w.temperature) AS max_temperature_yesterday,
    MIN(w.temperature) AS min_temperature_yesterday,
    STDDEV(w.temperature) AS stddev_temperature_yesterday
FROM
    weather_api.weather_data w
JOIN
    weather_api.cities c ON w.city_id = c.id
WHERE
    DATE(FROM_UNIXTIME(w.datetime)) = CURDATE() - INTERVAL 1 DAY
GROUP BY
    c.country, c.city;
