WITH source AS (
    SELECT * FROM {{ source('raw','raw_weather') }}
),

cleaned AS (
    SELECT
        city,
        latitude,
        longitude,
        temperature,
        windspeed,
        winddirection,
        weathercode,
        weather_timestamp,
        loaded_at
    FROM source
    WHERE city IS NOT NULL
)

SELECT * FROM cleaned