CREATE VIEW times_rained_last_week AS
SELECT COUNT(*)
FROM weather_api.weather_data
WHERE DATE(FROM_UNIXTIME(datetime)) >= DATE(NOW() - INTERVAL 7 DAY)
  AND DATE(FROM_UNIXTIME(datetime)) <= DATE(NOW())
  AND weather_description LIKE '%rain%';