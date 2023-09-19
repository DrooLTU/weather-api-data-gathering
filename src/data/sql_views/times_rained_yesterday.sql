CREATE VIEW times_rained_yesterday AS
SELECT COUNT(*) as times_rained
FROM weather_api.weather_data
WHERE DATE(FROM_UNIXTIME(datetime)) = DATE(NOW() - INTERVAL 1 DAY)
  AND weather_description LIKE '%rain%';