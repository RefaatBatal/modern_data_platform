WITH daily AS (
    SELECT
        city,
        DATE(weather_timestamp) as weather_date,
        AVG(temperature) as avg_temperature,
        MAX(temperature) as max_temperature,
        MIN(temperature) as min_temperature,
        AVG(windspeed) as avg_windspeed,
        COUNT(*) as record_count
    FROM {{ ref('stg_weather') }}
    GROUP BY city, DATE(weather_timestamp)
)

SELECT * FROM daily